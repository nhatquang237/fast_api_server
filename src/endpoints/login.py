
from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from data_connect import *
from models import User, Email
from utility import create_jwt_token

router = APIRouter()

@router.post("/register")
async def register(user: User):
    try:
        # Add data validation function before connecting to the database
        result = await add_user_to_database(user)
        return JSONResponse(content=f"{result['detail']}", status_code=result['status_code'])

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.post("/check")
async def email_check(email: Email):
    try:
        result = await check_email_existence(email)
        return JSONResponse(content=result['exists'])

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.post("/login")
async def login(user: User):
    try:
        result = await get_user_from_database(user)
        token = None
        # Create token and send back to front-end
        if result:
            result.pop("_id", None)
            token = create_jwt_token(result)

        return JSONResponse(content={"token": token})

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    token_data = {"sub": form_data.username}
    return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}
