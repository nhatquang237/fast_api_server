import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from data_connect import *
from models import AddSpendList, UpdateSpendList, DeleteSpendList, User, Email
from config import PORT, ORIGINS
from utility import create_jwt_token, decode_jwt_token

app = FastAPI()

# OAuth2PasswordBearer is a class for the OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    token_data = {"sub": form_data.username}
    return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}


@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # Decode and verify the JWT token
    token_data = decode_jwt_token(token)
    return {"message": "You are authenticated", "token_data": token_data}


# GET route to get data from the database
@app.get('/data')
async def get_data():
    data = await get_from_database()
    return data


# PUT route to handle the to update the database
@app.put('/update', response_model=UpdateSpendList)
async def update_data(request_data: UpdateSpendList=Depends()):
    try:
        await update_database(request_data)
        return JSONResponse(content="Database updated successfully")
    except Exception as e:
        print(f'Error updating database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


# POST route for adding a document
@app.post('/add', response_model=AddSpendList)
async def add_data(request_data: AddSpendList=Depends()):
    try:
        # Add data validation function before connecting to the database
        result = await add_to_database(request_data.items)
        return JSONResponse(content=f"Added new data successfully: {result}")
    except Exception as e:
        print(f'Error adding data to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@app.delete('/delete', response_model=DeleteSpendList)
async def delete_data(request_data: DeleteSpendList):
    try:
        result = await delete_spend_data(request_data)
        return JSONResponse(content=f'{result["message"]}')
    except Exception as e:
        print(f'Error deleting document database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@app.post("/register")
async def register(user: User):
    try:
        # Add data validation function before connecting to the database
        result = await add_user_to_database(user)
        return JSONResponse(content=f"{result['detail']}", status_code=result['status_code'])

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@app.post("/check")
async def email_check(email: Email):
    try:
        result = await check_email_existence(email)
        return JSONResponse(content=result['exists'])

    except Exception as e:
        print(f'Error adding user to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@app.post("/login")
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


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=PORT)

"""
Write test components for APIs above
"""