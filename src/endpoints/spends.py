
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from data_connect import add_to_database, delete_spend_data, get_from_database, update_database, get_spend_sort_by_payer
from models.spend import AddSpendList, DeleteSpendList, UpdateSpendList
from utility import decode_jwt_token, get_oid_str

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create local dictionary for caching get request
cache_dict = {"saved_data": None}

endpoint_path = "/spends"

# GET route to get data from the database
@router.get(endpoint_path)
async def get_data(token: str = Depends(oauth2_scheme)):
    # Decode and verify the JWT token, exception will be raised in case token is not valid
    decode_jwt_token(token)

    if not cache_dict['saved_data']:
        data = await get_from_database()
        cache_dict['saved_data'] = data

    return cache_dict['saved_data']


@router.get(endpoint_path + '/{payer}')
async def get_data(payer: str, token: str = Depends(oauth2_scheme)):
    # Decode and verify the JWT token, exception will be raised in case token is not valid
    decode_jwt_token(token)

    data = await get_spend_sort_by_payer(payer)
    return data


# PUT route to handle the to update the database
@router.put(endpoint_path, response_model=UpdateSpendList)
async def update_data(request_data: UpdateSpendList=Depends(), token: str = Depends(oauth2_scheme)):
    decode_jwt_token(token)
    try:
        await update_database(request_data)
        # Clear the cache
        cache_dict['saved_data'] = None
        return JSONResponse(content="Database updated successfully")
    except Exception as e:
        print(f'Error updating database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


# POST route for adding a document
@router.post(endpoint_path, response_model=AddSpendList)
async def add_data(request_data: AddSpendList=Depends(), token: str = Depends(oauth2_scheme)):
    decode_jwt_token(token)
    try:
        # Add data validation function before connecting to the database
        result = await add_to_database(request_data.items)
        insert_ids = ",".join((get_oid_str(document) for document in result))
        # Clear the cache
        cache_dict['saved_data'] = None
        return JSONResponse(content=insert_ids)
    except Exception as e:
        print(f'Error adding data to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.patch(endpoint_path, response_model=DeleteSpendList)
async def delete_data(request_data: DeleteSpendList, token: str = Depends(oauth2_scheme)):
    decode_jwt_token(token)
    try:
        result = await delete_spend_data(request_data)
        # Clear the cache
        cache_dict['saved_data'] = None
        return JSONResponse(content=f'{result["message"]}')
    except Exception as e:
        print(f'Error deleting document database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')



# NOTE:
# Add some route with path parameters to retreive sorted data from database
# Apply advance query action with mongodb into this project
