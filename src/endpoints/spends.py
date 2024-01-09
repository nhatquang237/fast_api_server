
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from data_connect import add_to_database, delete_spend_data, get_from_database, update_database
from models import AddSpendList, DeleteSpendList, UpdateSpendList
from utility import decode_jwt_token, get_oid_str

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# GET route to get data from the database
@router.get('/data')
async def get_data(token: str = Depends(oauth2_scheme)):
    # Decode and verify the JWT token, exception will be raised in case token is not valid
    decode_jwt_token(token)
    
    data = await get_from_database()
    return data


# PUT route to handle the to update the database
@router.put('/update', response_model=UpdateSpendList)
async def update_data(request_data: UpdateSpendList=Depends(), token: str = Depends(oauth2_scheme)):
    decode_jwt_token(token)
    try:
        await update_database(request_data)
        return JSONResponse(content="Database updated successfully")
    except Exception as e:
        print(f'Error updating database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


# POST route for adding a document
@router.post('/add', response_model=AddSpendList)
async def add_data(request_data: AddSpendList=Depends(), token: str = Depends(oauth2_scheme)):
    decode_jwt_token(token)
    try:
        # Add data validation function before connecting to the database
        result = await add_to_database(request_data.items)
        insert_ids = ",".join((get_oid_str(document) for document in result))
        return JSONResponse(content=insert_ids)
    except Exception as e:
        print(f'Error adding data to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.delete('/delete', response_model=DeleteSpendList)
async def delete_data(request_data: DeleteSpendList, token: str = Depends(oauth2_scheme)):
    decode_jwt_token(token)
    try:
        result = await delete_spend_data(request_data)
        return JSONResponse(content=f'{result["message"]}')
    except Exception as e:
        print(f'Error deleting document database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')
