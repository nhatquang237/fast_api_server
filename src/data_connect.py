from fastapi import HTTPException

from data_connection import DatabaseConnection
from utility import update_document, get_ids_from_documents, hash_password

def close_connection():
    DatabaseConnection.delete_instance()

async def delete_spend_data(req):
    db = DatabaseConnection()
    try:
        # Convert the list of IDs to ObjectId instances
        ids = req.ids
        object_ids = get_ids_from_documents(ids)

        spend_collection = db.spend_collection

        # Delete documents with matching ObjectIds
        result = spend_collection.delete_many({"_id": {"$in": object_ids}})

        return {"message": f"Database value updated successfully. Deleted {result.deleted_count} documents."}

    except Exception as error:
        print(f'Error updating database: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')

async def update_database(req):
    db = DatabaseConnection()
    try:
        spends = db.spend_collection

        updated_spend = req.items
        for spend in updated_spend:
            update_document(spends, spend)

        return {"message": "Database value updated successfully"}

    except Exception as error:
        print(f'Error updating database: {error}')
        raise HTTPException(status_code=500, detail='Internal server error')

async def get_spend_sort_by_payer(payer: str):
    db = DatabaseConnection()
    try:
        spend_collection = db.spend_collection
        shareholder_collection = db.shareholder_collection

        ## For inspecting execution steps of database query
        # result = spend_collection.find({"payer": payer}).explain()["executionStats"]

        result = spend_collection.find({"payer": payer})
        spends = list(result)
        shareholders = list(shareholder_collection.find({}))

        # Get id string from ObjectId to get serialize data to sent in json format
        for spend in spends:
            spend["_id"] = str(spend["_id"])
        shareholders[0]["_id"] = str(shareholders[0]["_id"])

        return {'shareholderData': shareholders[0], 'spendData': spends}

    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        return {'shareholderData': [], 'spendData': []}

    finally:
        close_connection()

async def get_from_database():
    db = DatabaseConnection()
    try:
        spend_collection = db.spend_collection
        shareholder_collection = db.shareholder_collection

        spends = list(spend_collection.find({}).sort("_id"))
        shareholders = list(shareholder_collection.find({}))

        for spend in spends:
            # Get id string from ObjectId to get serialize data to sent in json format
            spend["_id"] = str(spend["_id"])
        shareholders[0]["_id"] = str(shareholders[0]["_id"])

        return {'shareholderData': shareholders[0], 'spendData': spends}

    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        return {'shareholderData': [], 'spendData': []}

    finally:
        close_connection()

async def add_to_database(new_data):
    db = DatabaseConnection()
    try:
        spend_collection = db.spend_collection

        # Required format for insert_many function: List[Dict] while as data get from UI is List[CreateSpend]
        new_data = [dict(data) for data in new_data]
        result = spend_collection.insert_many(new_data)

        return result.inserted_ids

    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def check_email_existence(email):
    db = DatabaseConnection()

    user_collection = db.user_collection

    # Check if email was used
    is_exist = user_collection.count_documents(email.model_dump())
    return {"exists": bool(is_exist)}

async def add_user_to_database(new_user):
    db = DatabaseConnection()
    user_collection = db.user_collection

    # Get dictionary of fields in data
    new_user = new_user.model_dump()

    # Check if email was used
    is_exist = user_collection.count_documents({"username": new_user["username"]})

    if is_exist:
        return {"status_code": 400, "detail": None}

    # Hash password value before saving to database
    new_user['password'] = str(hash_password(new_user['password']))

    # Add new user to database
    result = user_collection.insert_one(new_user)

    return {"status_code": 200, "detail": result.inserted_id}


async def get_user_from_database(data):
    db = DatabaseConnection()
    try:
        user_collection = db.user_collection

        result = user_collection.find_one(
            {"username": data.username, "password": str(hash_password(data.password))}
        )

        return result

    except Exception as error:
        print(f"Error connecting to MongoDB: {error}")
        raise HTTPException(status_code=500, detail="Internal server error")
