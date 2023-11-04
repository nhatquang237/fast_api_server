from fastapi import HTTPException

from data_connection import DatabaseConnection
from utility import update_document

def close_connection():
    DatabaseConnection.delete_instance()

async def updateDatabase(req):
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['spendData']
        collection = database['spendData']

        updated_data = req.items
        for spend in updated_data:
            update_document(collection, spend)

        return {"message": "Database value updated successfully"}
    except Exception as error:
        print(f'Error updating database: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')

async def getFromDatabase():
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['spendData']
        spendDataCollection = database['spendData']
        shareholderDataCollection = database['shareholderData']

        spendData = list(spendDataCollection.find({}))
        shareholderData = list(shareholderDataCollection.find({}))

        for spend in spendData:
            spend["_id"] = str(spend["_id"])
        shareholderData[0]["_id"] = str(shareholderData[0]["_id"])

        return {'shareholderData': shareholderData[0], 'spendData': spendData}
    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        return {'shareholderData': [], 'spendData': []}
    finally:
        close_connection()

async def addToDatabase(new_data):
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['spendData']
        spendDataCollection = database['spendData']

        # Required format for insert_many function: List[Dict] while as data get from UI is List[CreateSpend]
        new_data = [dict(data) for data in new_data]
        result = spendDataCollection.insert_many(new_data)

        return result.inserted_ids
    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")
