from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

tradecount = Blueprint('tradecount', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

@tradecount.route('/tradecount', methods=['GET'])

def calculate_tradecount(data):

    username = data.get('username')
    raw_date = data.get('dateAndTimeOpening')
    identifier = data.get('identifier')  # Je suppose que chaque trade a un ID unique pour le récupérer.

    if not raw_date:
        return jsonify({"error": "Date not provided"}), 400

    try:
        date_of_trade = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
    except ValueError as e:
        

    collection_close = db[f"{username}_close"]
    collection_open = db[f"{username}_open"]

    # Suppression du trade de la collection 'open'
    trade_to_close = collection_open.find_one_and_delete({"_id": identifier})

   
    # Récupération du dernier trade_number dans la collection 'close'
    last_closed_trade = collection_close.find_one(sort=[("trade_number", -1)])
    if last_closed_trade:
        new_trade_number = last_closed_trade["trade_number"] + 1
    else:
        new_trade_number = 1

   
    return  new_trade_number
