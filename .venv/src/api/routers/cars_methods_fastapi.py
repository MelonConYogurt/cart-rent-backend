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
    db = Connect()
    try:
        car_dalete = db.delete_car_by_id( id= id.id)
        return car_dalete    
    except  Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@manage_functions.post("/change/state/", response_model=ResponseDeleteMethod)
def change_car_state_by_id(data: ChangeState ):
    db = Connect()
    try:
        car_info = db.change_car_state( id= data.id, available=data.available )
        return car_info    
    except  Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    