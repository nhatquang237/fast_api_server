from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient
# Replace <YOUR_MONGODB_URI> with your MongoDB URI
uri = "mongodb://localhost:27017"

async def updateDatabase(req):
    print("Something to print " * 2)
    client = MongoClient(uri)
    try:
        # Connect to the MongoDB database
        client.server_info()  # Check if the server is available
        database = client['spendData']
        collection = database['spendData']

        updated_data = req.items
        for spend in updated_data:
            update_document(collection, spend)

        return {"message": "Database value updated successfully"}
    except Exception as error:
        print(f'Error updating database: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')
    finally:
        client.close()

async def connectToDatabase():
    client = MongoClient(uri)
    try:
        # Connect to the MongoDB database
        client.server_info()  # Check if the server is available

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
        client.close()

async def addToDatabase(new_data):
    client = MongoClient(uri)
    try:
        # Connect to the MongoDB database
        client.server_info()  # Check if the server is available
        database = client['spendData']
        spendDataCollection = database['spendData']

        # Required format for insert_many function: List[Dict] while as data get from UI is List[CreateSpend]
        new_data = [dict(data) for data in new_data]
        result = spendDataCollection.insert_many(new_data)

        return result.inserted_ids
    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        client.close()

def update_document(collection, spend):
    collection.update_one(
        {"_id": ObjectId(spend.id)},
        {"$set": {
            "name": spend.name,
            "value": spend.value,
            "payer": spend.payer,
            "shareholder": spend.shareholder
        }}
    )

def get_oid_str(object_id: ObjectId):
    return str(object_id)
