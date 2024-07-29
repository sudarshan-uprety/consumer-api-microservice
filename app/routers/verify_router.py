# from fastapi import status, Depends, APIRouter, Path
# from sqlalchemy.orm import Session
# from fastapi.responses import JSONResponse
#
# from utils.database import get_db
# from app.api import api
#
#
# router = APIRouter(
#     prefix="/accounts",
#     tags=['verify_accounts'],
# )
#
#
# @router.get('/verify/user/{token}', status_code=status.HTTP_200_OK)
# async def verify_email(token: str = Path(..., description="Verification token"), db: Session = Depends(get_db))\
#         -> JSONResponse:
#     await api.verify_user_email_api(token=token, db=db)
#     return JSONResponse(status_code=200, content={"message": "Email Verified"})
