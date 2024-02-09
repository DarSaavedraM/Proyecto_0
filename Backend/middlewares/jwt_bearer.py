from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Se esperaba un esquema de autorización Bearer")
            payload = validate_token(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Credenciales no proporcionadas")