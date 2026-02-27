from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
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
from sqlalchemy import select
from utils.settings import config
from abc import ABC, abstractmethod




password_hash = PasswordHash.recommended()


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
        access_token = await self.get_access_token(code)

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to fetch access token")

        user_info = await self.get_user_info(access_token)

        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")

        user = await self.get_or_create_user(user_info)
        return user

# GOOGLE PROVIDER

class GoogleOAuthProvider(BaseOAuthProvider):

    async def get_access_token(self, code: str) -> str:
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
            return response.json().get("access_token")

    async def get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            return response.json()

    async def get_or_create_user(self, user_info: dict) -> User:
        email = user_info.get("email")

        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                username=user_info.get("name"),
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

        return user

# GITHUB PROVIDER

class GithubOAuthProvider(BaseOAuthProvider):

    async def get_access_token(self, code: str) -> str:
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
            return response.json().get("access_token")

    async def get_user_info(self, access_token: str) -> dict:
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

            primary_email = next(
                (e["email"] for e in emails if e.get("primary")),
                None
            )

            user_info["email"] = primary_email
            return user_info

    async def get_or_create_user(self, user_info: dict) -> User:

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

        return user


# NORMAL AUTH ROUTES

@auth_router.get("/")
async def current_user(
    user: Annotated[dict, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}


@auth_router.post("/create")
async def create_user(
    userrequest: CreateUserRequest,
    db: AsyncSession = Depends(get_async_session)
):
    user = User(
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
        updated_by_id=0
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@auth_router.post("/token", response_model=Token)
async def login_for_accesstoken(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )

    token = create_user_token(user.username, user.id, timedelta(minutes=15))

    return {"access_token": token, "token_type": "bearer"}

# GOOGLE ROUTES

@auth_router.get("/google/login")
async def google_login():
    return (
        f"{GOOGLE_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={config.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={config.GOOGLE_REDIRECT_URI}"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )


@auth_router.get("/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_async_session)):

    provider = GoogleOAuthProvider(db)
    user = await provider.authenticate(code)

    jwt_token = create_user_token(user.username, user.id, timedelta(minutes=15))

    return RedirectResponse(
                url=f"{config.FRONTEND_URL}/auth/google/callback?token={jwt_token}"
            )

# GITHUB ROUTES


@auth_router.get("/github/login")
async def github_login():
    return (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={config.GITHUB_CLIENT_ID}"
        f"&redirect_uri={config.GITHUB_REDIRECT_URI}"
        f"&scope=user:email"
    )


@auth_router.get("/github/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_async_session)):

    provider = GithubOAuthProvider(db)
    user = await provider.authenticate(code)

    jwt_token = create_user_token(user.username, user.id, timedelta(minutes=15))
    return RedirectResponse(
                url=f"{config.FRONTEND_URL}/auth/github/callback?token={jwt_token}"
            )