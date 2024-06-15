from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import webbrowser
from flask import make_response
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.DEBUG)
def open_browser_tab():
    url = "http://localhost:5000"
    webbrowser.open_new_tab(url)

def start_server():
    print("Starting python flask server...")
    util.load_saved_artifacts()
    app.run(debug=True, host='0.0.0.0', port=5000)



@app.route('/', methods=['GET'])
def get_form_info():
    response = jsonify(util.get_form_info())
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/favicon.ico')
def favicon():
    return make_response('', 200)


@app.route('/predict_apartment_price', methods=['POST'])
def predict_apartment_price():
    data = request.get_json()

    logging.debug("Received data: %s", data)

    apartment_type = data.get('apartment_type')
    metro_station = data.get('metro_station')
    minutes_to_metro = int(data.get('minutes_to_metro', 0))
    region = data.get('region')
    number_of_rooms = int(data.get('number_of_rooms', 0))
    area = float(data.get('area', 0))
    living_area = float(data.get('living_area', 0))
    kitchen_area = float(data.get('kitchen_area', 0))
    floor = int(data.get('floor', 0))
    number_of_floors = int(data.get('number_of_floors', 0))
    renovation_type = data.get('renovation_type')


    observation = [
        apartment_type,
        metro_station,
        minutes_to_metro,
        region,
        number_of_rooms,
        area,
        living_area,
        kitchen_area,
        floor,
        number_of_floors,
        renovation_type
    ]

    response = jsonify({
        'estimated_price': util.get_estimated_price(*observation)
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    start_server()
