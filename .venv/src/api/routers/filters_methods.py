from fastapi import APIRouter
from ...database.connect import *
from fastapi import Depends,  HTTPException, status
from ..auth.authentication import get_current_active_user
from ..models.filters_models import *
from typing import List


filter_methods = APIRouter(
    prefix="/filters",
    tags=["Information for filters"]
)

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

