from fastapi import APIRouter, HTTPException
from starlette import status
from ..models.cars_models import DeleteMethod, ResponseDeleteMethod
from ...database.connect import *

manage_functions = APIRouter(
    prefix="/manage",
    tags=["Manage Functions (Admins only)"]
)

@manage_functions.post("/delete/", response_model=ResponseDeleteMethod)
def delete_car_by_id(id: DeleteMethod ):
    try:
        db = Connect()
        car_dalete = db.delete_car_by_id( id= id.id)
        return car_dalete    
    except  Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()
    