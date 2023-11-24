import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

from data_connect import get_from_database, update_database, add_to_database, delete_spend_data
from models import AddSpendList, UpdateSpendList, DeleteSpendList

app = FastAPI()
port = 3001

# CORS (Cross-Origin Resource Sharing) configuration
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=port)
