from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/paket/<paket_id>')
def get_paket_info(paket_id):
    # Retrieve paket information
    paket_response = requests.get(f'http://127.0.0.1:5002/get/{paket_id}')
    paket_info = paket_response.json()['paket_liburan']

    # Retrieve hotel information
    hotel_response = requests.get(f'http://127.0.0.1:5001/hotel/{paket_id}')
    hotel_info = hotel_response.json()
    # Retrieve user info
    user_response = requests.get(f'http://127.0.0.1:5003/user/{paket_id}')
    user_info = user_response.json()

    # Render the template with paket and hotel information
    return render_template('paket.html', paket=paket_info, hotel_info=hotel_info, user_info=user_info)

@app.route('/')
def index():
    # Fetch paket liburan data from the API
    response = requests.get('http://127.0.0.1:5002/get')
    paket_liburan = response.json()['paket_liburan']
    
    # Render the template with paket liburan data
    return render_template('index.html', paket_liburan=paket_liburan)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
