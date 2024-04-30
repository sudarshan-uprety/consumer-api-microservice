from fastapi import status, HTTPException, Depends, APIRouter, BackgroundTasks, Path
from sqlalchemy.orm import Session

from app.database.database import get_db
from app import schemas, api


router = APIRouter(
    prefix="/accounts",
    tags=['verify_accounts'],
)


@router.get('/verify/user/{token}', status_code=status.HTTP_200_OK)
async def verify_email(token: str = Path(..., description="Verification token"), db: Session = Depends(get_db)):
    try:
        verify = await api.verify_user_email_api(token=token, db=db)
        return {"message": "Email verified."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
