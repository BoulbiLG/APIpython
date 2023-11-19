from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

SLRCount = Blueprint('SLRCount', __name__)

def count_slr(username, date_of_trade):
    collection_close = db[f"{username}_close"]
    count_slr = collection_close.count_documents({"dateAndTimeOpening": {"$regex": f"^{date_of_trade}"}, "SLR": True})
    return count_slr

@SLRCount.route('/SLRCount', methods=['GET'])
def calculate_SLRCount():

    data = request.json  # Assuming the data is sent as JSON
    username = data.get('username')
    raw_date = data.get('dateAndTimeOpening')
    status = data.get('closurePosition')  # "open" ou "close"

    if not raw_date:
        return jsonify({"error": "Date not provided"}), 400

    try:
        date_of_trade = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%Y-%m-%d')
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if status == "Open":
        new_slr_number = count_slr(username, date_of_trade)
    elif status == "Close":
        # You might want to implement a similar logic for counting closed stop losses if needed
        pass
    else:
        return jsonify({"error": f"Invalid status value: {status}"}), 400

    return jsonify({"new_slr_number": new_slr_number})

# Register the SLRCount Blueprint
app.register_blueprint(SLRCount)

if __name__ == '__main__':
    app.run(debug=True)
