from bson import ObjectId
from typing import List
from models import UpdateSpendList

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

def get_ids_from_documents(ids: List[str]) -> List[ObjectId]:
    """Get id of all documents

    Args:
        documents (UpdateSpendList): List of target document

    Returns:
        List[ObjectId]: list of ObjectId
    """

    return [ObjectId(id) for id in ids]