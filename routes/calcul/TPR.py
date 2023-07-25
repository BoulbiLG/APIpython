from flask import Blueprint, jsonify, request
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')

tpr = Blueprint('tpr', __name__)

def calculate_tpr(entry):
    # Your TPR calculation logic here based on the 'entry' data
    # For example:
    type_of_transaction = entry.get('typeOfTransaction')
    price_closure = entry.get('priceClosure')
    take_profit = entry.get('takeProfit')
    
    if type_of_transaction == "buy" and price_closure >= take_profit:
        entry['TPR'] = True
    elif type_of_transaction == "sell" and price_closure <= take_profit:
        entry['TPR'] = True
    else:
        entry['TPR'] = False

    return entry

@tpr.route('/tpr', methods=['GET'])
def update_tpr():
    client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = client['test']
    collection = db['test2_open']

    #data = list(collection.find())
    data = request.json

    for entry in data:
        # Calculate the TPR value for each entry
        entry = calculate_tpr(entry)

        # Update the TPR value in the database
        collection.update_one({'_id': entry['_id']}, {'$set': {'TPR': entry['TPR']}})

    client.close()

    return jsonify({'message': 'TPR updated successfully'})

