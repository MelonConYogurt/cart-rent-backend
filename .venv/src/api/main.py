from typing import Annotated
from fastapi.responses import RedirectResponse
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm

#load models for api security
from .models.security import *

# Strawberry router
from strawberry.fastapi import GraphQLRouter
from .routers.cars_methods_graphql import schema
from .routers.cars_methods_fastapi import manage_functions

# auth
from .auth.authentication import *

#
from .routers.filters_methods import *

# Crear el router de GraphQL
graphql_app = GraphQLRouter(schema)
app = FastAPI()

app.include_router(graphql_app, prefix="/graphql", tags=["Graphql Functions"])
app.include_router(filter_methods)
app.include_router(manage_functions)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False, tags=["Other Functions"])
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/token", tags=["Authorization Functions"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(users_in_db_api, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
