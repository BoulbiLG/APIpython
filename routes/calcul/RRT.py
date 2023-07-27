from flask import Blueprint
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

RRT = Blueprint('RRT', __name__)
@RRT.route('/rrt', methods=['GET'])

def calculate_rrt(data):
  
    take_profit = data['takeProfit']
    price_opening = data['priceOpening']
    stop_loss = data['stopLoss']
    rrt = (take_profit - price_opening) / (price_opening - stop_loss)

    return rrt  # Renvoie la valeur de la clé "RR"