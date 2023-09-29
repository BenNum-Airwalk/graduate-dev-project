from flask import Blueprint, jsonify, request
from datetime import datetime
import db


items = Blueprint("items", __name__)
inventory = Blueprint("inventory", __name__)



@items.route("/", methods=['POST'])
def post_items():
    request_data = request.get_json()
    request_data["createdDate"] = datetime.now()
    db.mongo.db.schema.insert_one(request_data)
    print (request_data)
    del request_data['_id']
    return jsonify(request_data)



@inventory.route("/", methods=['GET'])
def get_inventory():
    # Return the list of items
    # Return the item name and total quantity
    pipeline = [
    {"$unwind": "$items"},
    {"$group": {"_id": "$items", "inventory": {"$sum": "$inventory"}}},
    {"$project": {"_id": 0, "items": "$_id", "inventory": "$inventory"}},
    ]
    return jsonify(list(db.mongo.db.collection.aggregate(pipeline)))

    # return jsonify(list(db.mongo.db.schema.find({}, {"_id": False})))

