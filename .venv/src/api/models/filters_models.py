from pydantic import BaseModel

class Brand(BaseModel):
    name: str
    
class Color(BaseModel):
    name: str

    