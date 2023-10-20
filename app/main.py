import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

from data_connect import connectToDatabase, updateDatabase, addToDatabase
from models import SpendList

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
    data = await connectToDatabase()
    return data

# PUT route to handle the to update the database
@app.put('/update', response_model=SpendList)
async def update_data(request_data: SpendList=Depends()):
    try:
        await updateDatabase(request_data)
        return JSONResponse(content="Database updated successfully")
    except Exception as e:
        print(f'Error updating database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')

# POST route for adding a document
@app.post('/add', response_model=SpendList)
async def add_data(request_data: SpendList=Depends()):
    try:
        # Add data validation function before connecting to the database
        result = await addToDatabase(request_data.items)
        return JSONResponse(content=f"Added new data successfully: {result}")
    except Exception as e:
        print(f'Error adding data to the database: {e}')
        raise HTTPException(status_code=500, detail='Internal server error')

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=port)
