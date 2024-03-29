
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from data_connect import add_to_database, delete_spend_data, get_from_database, update_database, get_spend_sort_by_payer
from models.spend import AddSpendList, DeleteSpendList, UpdateSpendList
from utility import decode_jwt_token, get_oid_str, rate_limiter, validate_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create local dictionary for caching get request
cache_dict = {}

endpoint_path = "/spends/"

# GET route to get data from the database
@router.get(endpoint_path)
@rate_limiter(limit_rate=2, time_frame=10)
@validate_token
async def get_data(request: Request, payer: str | None = None, token: str = Depends(oauth2_scheme)):

    if payer:
        if not payer in cache_dict:
            data = await get_spend_sort_by_payer(payer)
            cache_dict[payer] = data

        return cache_dict[payer]

    if not 'saved_data' in cache_dict:
        data = await get_from_database()
        cache_dict['saved_data'] = data

    return cache_dict['saved_data']


# PUT route to handle the to update the database
@router.put(endpoint_path, response_model=UpdateSpendList)
@validate_token
async def update_data(request_data: UpdateSpendList=Depends(), token: str = Depends(oauth2_scheme)):

    try:
        await update_database(request_data)
        # Clear the cache
        cache_dict.clear()
        return JSONResponse(content="Database updated successfully")
    except Exception as e:
        print(f'Error updating database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


# POST route for adding a document
@router.post(endpoint_path, response_model=AddSpendList)
@validate_token
async def add_data(request_data: AddSpendList=Depends(), token: str = Depends(oauth2_scheme)):

    try:
        # Add data validation function before connecting to the database
        result = await add_to_database(request_data.items)
        insert_ids = ",".join((get_oid_str(document) for document in result))
        # Clear the cache
        cache_dict.clear()
        return JSONResponse(content=insert_ids)
    except Exception as e:
        print(f'Error adding data to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


@router.patch(endpoint_path, response_model=DeleteSpendList)
@validate_token
async def delete_data(request_data: DeleteSpendList, token: str = Depends(oauth2_scheme)):
    try:
        result = await delete_spend_data(request_data)
        # Clear the cache
        cache_dict.clear()
        return JSONResponse(content=f'{result["message"]}')
    except Exception as e:
        print(f'Error deleting document database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')


# NOTE:
# Add some route with path parameters to retreive sorted data from database
# Apply advance query action with mongodb into this project
