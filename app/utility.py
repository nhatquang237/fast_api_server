from bson import ObjectId

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
