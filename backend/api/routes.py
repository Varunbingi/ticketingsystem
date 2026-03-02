from fastapi import APIRouter
from api.v1.auth import auth_router
from api.v1.user import user_router
from api.v1.clients.client import client_router
from api.v1.clients.contract import contract_router
from api.v1.permissions.permission_category import pc_router
from api.v1.permissions.permission import permission_router
from api.v1.permissions.user_permission import up_router
from api.v1.roles.role import role_router
from api.v1.roles.user_roles import user_role_router
from api.v1.ticket import ticket_router
from api.v1.notification_routes import notification_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(client_router)
api_router.include_router(contract_router)
api_router.include_router(pc_router)
api_router.include_router(permission_router)
api_router.include_router(up_router)
api_router.include_router(role_router)
api_router.include_router(user_role_router)
api_router.include_router(ticket_router)
api_router.include_router(notification_router)
