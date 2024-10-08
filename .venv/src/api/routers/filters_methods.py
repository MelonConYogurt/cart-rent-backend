from fastapi import APIRouter
from ...database.connect import *
from fastapi import Depends,  HTTPException, status
from ..auth.authentication import get_current_active_user
from ..models.filters_models import *
from typing import Annotated, List


filter_methods = APIRouter(
    prefix="/filters",
    tags=["Information for filters"]
)

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


@filter_methods.get("/brands", response_model=List[Brand], dependencies=[Depends(get_current_active_user)])
def get_brands():
    try:
        db = Connect()
        brands = db.get_all_brands()
        return brands
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@filter_methods.get("/colors", response_model=List[Color], dependencies=[Depends(get_current_active_user)])
def get_colors():
    try:
        db = Connect()
        brands = db.get_all_colors()
        return brands
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


