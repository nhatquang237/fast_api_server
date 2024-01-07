from fastapi import HTTPException

from data_connection import DatabaseConnection
from utility import update_document, get_ids_from_documents, hash_password

def close_connection():
    DatabaseConnection.delete_instance()

async def delete_spend_data(req):
    connection = DatabaseConnection()
    client = connection.client
    try:
        # Convert the list of IDs to ObjectId instances
        ids = req.ids
        object_ids = get_ids_from_documents(ids)

        database = client['test']
        collection = database['spendData']

        # Delete documents with matching ObjectIds
        result = collection.delete_many({"_id": {"$in": object_ids}})

        return {"message": f"Database value updated successfully. Deleted {result.deleted_count} documents."}
    except Exception as error:
        print(f'Error updating database: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')

async def update_database(req):
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['test']
        collection = database['spendData']

        updated_data = req.items
        for spend in updated_data:
            update_document(collection, spend)

        return {"message": "Database value updated successfully"}
    except Exception as error:
        print(f'Error updating database: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')

async def get_from_database():
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['test']
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

async def add_to_database(new_data):
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['test']
        spendDataCollection = database['spendData']

        # Required format for insert_many function: List[Dict] while as data get from UI is List[CreateSpend]
        new_data = [dict(data) for data in new_data]
        result = spendDataCollection.insert_many(new_data)

        return result.inserted_ids
    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def check_email_existence(email):
    connection = DatabaseConnection()
    client = connection.client
    database = client['test']
    collection = database['users']

    # Check if email was used
    is_exist = collection.count_documents(email.model_dump())
    return {"exists": bool(is_exist)}

async def add_user_to_database(new_user):
    connection = DatabaseConnection()
    client = connection.client
    database = client['test']
    collection = database['users']

    # Get dictionary of fields in data
    new_user = new_user.model_dump()

    # Check if email was used
    is_exist = collection.count_documents({"username": new_user["username"]})

    if is_exist:
        return {"status_code": 400, "detail": None}

    # Hash password value before saving to database
    new_user['password'] = str(hash_password(new_user['password']))

    # Add new user to database
    result = collection.insert_one(new_user)

    return {"status_code": 200, "detail": result.inserted_id}


async def get_user_from_database(data):
    connection = DatabaseConnection()
    client = connection.client
    try:
        database = client['test']
        collection = database['users']

        result = collection.find_one({"username": data.username, "password": str(hash_password(data.password))})

        return result
    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

