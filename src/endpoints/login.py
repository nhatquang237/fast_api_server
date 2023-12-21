from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from data_connect import *
from models import Token, NewUser, Username
from utility import create_jwt_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(user: NewUser):
    try:
        # Add data validation function before connecting to the database
        result = await add_user_to_database(user)
        return JSONResponse(content=f"{result['detail']}", status_code=result['status_code'])

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.post("/check")
async def username_check(username: Username):
    try:
        result = await check_email_existence(username)
        return JSONResponse(content=result['exists'])

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        result = await get_user_from_database(form_data)
        token = ""
        # Create token and send back to front-end
        if result:
            result.pop("_id", None)
            token = create_jwt_token(result)

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')

    return {
        "access_token": token,
        "token_type": "bearer",
    }
