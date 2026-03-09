import random
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status,Request
from fastapi.responses import RedirectResponse
from notifications.dispatcher import emit_event
from db.db import get_async_session
from db.models.user import User
from db.schemas.user import CreateUserRequest, Token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from typing import Annotated
from datetime import timedelta
from repositories.auth import authenticate_user, create_user_token, get_current_user
import httpx
from utils.settings import config
from abc import ABC, abstractmethod
from sqlalchemy import select
from notifications.channels.email_channel import EmailChannel
from db.models.notifications import NotificationPreference
from notifications.dispatcher import emit_event
from logging_system.log_helper import new_span, end_span, log_info, log_warning, log_exception




password_hash = PasswordHash.recommended()
background_tasks = BackgroundTasks()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_URL = "https://api.github.com/user"
GITHUB_EMAIL_URL = "https://api.github.com/user/emails"

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# ABSTRACT OAUTH CLASS

class BaseOAuthProvider(ABC):

    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def get_access_token(self, code: str) -> str:
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> dict:
        pass

    @abstractmethod
    async def get_or_create_user(self, user_info: dict) -> User:
        pass

    async def authenticate(self, code: str) -> User:
        new_span("oauth_authenticate")
        try:
            new_span("fetch_access_token")
            access_token = await self.get_access_token(code)
            end_span()

            if not access_token:
                log_warning(None, "Failed to fetch access token")
                raise HTTPException(status_code=400, detail="Failed to fetch access token")

            new_span("fetch_user_info")
            user_info = await self.get_user_info(access_token)
            end_span()

            if not user_info:
                log_warning(None, "Failed to fetch user info")
                raise HTTPException(status_code=400, detail="Failed to fetch user info")
            
            new_span("get_or_create_user")
            user = await self.get_or_create_user(user_info)
            end_span()

            log_info(None, f"OAuth authentication succeeded for {user.email}")
            return user
        
        except Exception as e:
            log_exception(None, f"Error in OAuth authentication: {str(e)}")
            raise
        finally:
            end_span()

# GOOGLE PROVIDER

class GoogleOAuthProvider(BaseOAuthProvider):

    async def get_access_token(self, code: str) -> str:
        new_span("google_get_access_token")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    GOOGLE_TOKEN_URL,
                    data={
                        "code": code,
                        "client_id": config.GOOGLE_CLIENT_ID,
                        "client_secret": config.GOOGLE_CLIENT_SECRET,
                        "redirect_uri": config.GOOGLE_REDIRECT_URI,
                        "grant_type": "authorization_code",
                    },
                )
                token = response.json().get("access_token")
                log_info(None, "Google access token fetched")
                return token
        except Exception as e:
            log_exception(None, f"Google get_access_token failed: {str(e)}")
            raise
        finally:
            end_span()

    async def get_user_info(self, access_token: str) -> dict:
        new_span("google_get_user_info")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    GOOGLE_USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                log_info(None, "Google user info fetched")
                return response.json()
        except Exception as e:
            log_exception(None, f"Google get_user_info failed: {str(e)}")
            raise
        finally:
            end_span()

    async def get_or_create_user(self, user_info: dict) -> User:
        new_span("google_get_or_create_user")
        try:
            email = user_info.get("email")

            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()

            name = user_info.get("name").replace(" ", "")
            user_name = name + str(random.randint(100, 999))

            if not user:
                user = User(
                    username=user_name,
                    email=email,
                    password=password_hash.hash("google_login"),
                    firstname=user_info.get("given_name"),
                    lastname=user_info.get("family_name") or "",
                    phone="",
                    department_id=1,
                    designation="Google User",
                    reporting_to_id=0,
                    suspended=False,
                    deleted=False,
                    is_client=False,
                    created_by_id=0,
                    updated_by_id=0
                )

                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)

                log_info(None, f"Google user created: {email}")
            else:
                log_info(None, f"Google user exists: {email}")

            return user

        except Exception as e:
            log_exception(None, f"Google get_or_create_user failed: {str(e)}")
            raise
        finally:
            end_span()
# GITHUB PROVIDER

class GithubOAuthProvider(BaseOAuthProvider):

    async def get_access_token(self, code: str) -> str:
        new_span("github_get_access_token")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    GITHUB_TOKEN_URL,
                    headers={"Accept": "application/json"},
                    data={
                        "client_id": config.GITHUB_CLIENT_ID,
                        "client_secret": config.GITHUB_CLIENT_SECRET,
                        "code": code,
                        "redirect_uri": config.GITHUB_REDIRECT_URI,
                    },
                )
                token = response.json().get("access_token")
                log_info(None, "GitHub access token fetched")
                return token
        except Exception as e:
            log_exception(None, f"GitHub get_access_token failed: {str(e)}")
            raise
        finally:
            end_span()

    async def get_user_info(self, access_token: str) -> dict:
        new_span("github_get_user_info")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                user_response = await client.get(
                    GITHUB_USERINFO_URL,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                email_response = await client.get(
                    GITHUB_EMAIL_URL,
                    headers={"Authorization": f"Bearer {access_token}"}
                )

                user_info = user_response.json()
                emails = email_response.json()
                primary_email = next((e["email"] for e in emails if e.get("primary")), None)
                user_info["email"] = primary_email
                log_info(None, "GitHub user info fetched")
                return user_info
        except Exception as e:
            log_exception(None, f"GitHub get_user_info failed: {str(e)}")
            raise
        finally:
            end_span()

    async def get_or_create_user(self, user_info: dict) -> User:
        new_span("github_get_or_create_user")
        try:
            email = user_info.get("email")

            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()

            if not user:
                user = User(
                    username=user_info.get("name"),
                    email=email,
                    password=password_hash.hash("github_login"),
                    firstname=user_info.get("name"),
                    lastname="",
                    phone="",
                    department_id=1,
                    designation="GitHub User",
                    reporting_to_id=0,
                    suspended=False,
                    deleted=False,
                    is_client=False,
                    created_by_id=0,
                    updated_by_id=0
                )

                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)

                log_info(None, f"GitHub user created: {email}")
            else:
                log_info(None, f"GitHub user exists: {email}")

            return user

        except Exception as e:
            log_exception(None, f"GitHub get_or_create_user failed: {str(e)}")
            raise
        finally:
            end_span()
# NORMAL AUTH ROUTES

@auth_router.get("/")
async def current_user_route(
    request: Request,
    user: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request,"current_user_route", )
    try:
        if user is None:
            log_warning(request, "Authentication failed: no user")
            raise HTTPException(status_code=401, detail="Authentication Failed")
        log_info(request, f"User fetched: {user.get('email')}")
        return {"User": user}
    finally:
        end_span(request)

@auth_router.post("/create")
async def create_user_route(
    request: Request,
    userrequest: CreateUserRequest,
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request, "create_user_route")
    try:
        create_user_model = User(
            username=userrequest.username,
            password=password_hash.hash(userrequest.password),
            firstname=userrequest.firstname,
            lastname=userrequest.lastname,
            email=userrequest.email,
            phone=userrequest.phone,
            department_id=userrequest.department_id,
            designation=userrequest.designation,
            reporting_to_id=userrequest.reporting_to,
            suspended=userrequest.suspended,
            deleted=userrequest.deleted,
            is_client=userrequest.is_client,
            created_by_id=0,
            updated_by_id=0,
            is_verified=False
        )

        db.add(create_user_model)
        await db.commit()
        await db.refresh(create_user_model)

        # send verification email in background
        new_span(request, "send_verification_email")
        try:
            verification_link = f"http://localhost:8000/auth/verify/{create_user_model.id}"

            email = EmailChannel()

            background_tasks.add_task(
                email.send,
                user_id=create_user_model.id,
                message=f"Welcome {create_user_model.firstname}! Please verify here: {verification_link}",
                title="VERIFICATION"
            )

            log_info(request, f"Verification email sent to {create_user_model.email}")

        finally:
            end_span(request)

        return create_user_model

    except Exception as e:
        log_exception(request, f"User creation failed: {str(e)}")
        raise

    finally:
        end_span(request)

@auth_router.post("/verify/{user_id}")
async def verify_user_route(
    request: Request,
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request, "verify_user_route")
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            log_warning(request, f"User not found for verification: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            log_info(request, f"User already verified: {user.email}")
            return {"message": "User is already verified."}

        # mark user as verified
        user.is_verified = True

        # create notification preferences
        prefs = NotificationPreference(
            user_id=user_id,
            email_enabled=True,
            inapp_enabled=True
        )
        db.add(prefs)

        await db.commit()

        # emit welcome event
        new_span(request, "emit_welcome_event")
        try:
            await emit_event(
                event_name="WELCOME",
                strategy="DIRECT",
                payload={
                    "user_id": user_id,
                    "message": f"Welcome {user.firstname}! Your account is ready."
                }
            )

            log_info(request, f"WELCOME event emitted for {user.email}")

        finally:
            end_span(request)

        return {"message": f"User {user.username} has been verified."}

    except Exception as e:
        log_exception(request, f"Verification failed: {str(e)}")
        raise

    finally:
        end_span(request)

        
@auth_router.post("/token", response_model=Token)
async def login_for_accesstoken_route(request:Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request,"login_for_accesstoken_route")
    try:
        user = await authenticate_user(form_data.username, form_data.password, db)
        if not user:
            log_warning(request, f"Login failed for username: {form_data.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

        token = create_user_token(user.username, user.id, timedelta(minutes=15))
        log_info(request, f"Login successful: {user.email}")
        return {"access_token": token, "token_type": "bearer"}
    finally:
        end_span(request)


# GOOGLE ROUTES

@auth_router.get("/google/login")
async def google_login_route():
    return (
        f"{GOOGLE_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={config.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={config.GOOGLE_REDIRECT_URI}"
        f"&scope=openid email profile"
        f"&access_type=offline"
        f"&prompt=select_account"
    )



@auth_router.get("/google/callback")
async def google_callback_route(
    request: Request,
    code: str,
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request, "google_callback_route")
    try:
        provider = GoogleOAuthProvider(db)

        # authenticate user with google
        user = await provider.authenticate(code)

        # mark user verified
        user.is_verified = True
        await db.commit()

        # create jwt token
        jwt_token = create_user_token(user.username, user.id, timedelta(minutes=15))

        log_info(request, f"Google OAuth login success: {user.email}")

        return RedirectResponse(
            url=f"{config.FRONTEND_URL}/auth/google/callback?token={jwt_token}"
        )

    except Exception as e:
        log_exception(request, f"Google OAuth callback failed: {str(e)}")
        raise

    finally:
        end_span(request)


@auth_router.get("/github/login")
async def github_login_route():
    return (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={config.GITHUB_CLIENT_ID}"
        f"&redirect_uri={config.GITHUB_REDIRECT_URI}"
        f"&scope=user:email"
        f"&prompt=select_account"
    )
    
@auth_router.get("/github/callback")
async def github_callback_route(
    request: Request,
    code: str,
    db: AsyncSession = Depends(get_async_session)
):
    new_span(request, "github_callback_route")
    try:
        provider = GithubOAuthProvider(db)

        # authenticate user via github
        user = await provider.authenticate(code)

        # mark user verified
        user.is_verified = True
        await db.commit()

        # create jwt token
        jwt_token = create_user_token(user.username, user.id, timedelta(minutes=15))

        log_info(request, f"GitHub OAuth login success: {user.email}")

        return RedirectResponse(
            url=f"{config.FRONTEND_URL}/auth/github/callback?token={jwt_token}"
        )

    except Exception as e:
        log_exception(request, f"GitHub OAuth callback failed: {str(e)}")
        raise

    finally:
        end_span(request)
