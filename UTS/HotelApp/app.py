from flask import Flask, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import request
import base64

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'mysql-d48e9f6-bal-start.l.aivencloud.com'
app.config['MYSQL_PORT'] = 14160
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_HyawaTvSffYugyllPGf'
app.config['MYSQL_DB'] = 'hotel'
mysql = MySQL(app)

# Function to generate timestamp
def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# @app.route('/hotel', methods=['GET'])
# def get_all_destinasi():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT * FROM hotel")
#     columns = [i[0] for i in cursor.description]
#     data = []
#     for row in cursor.fetchall():
#         # Convert BLOB image data to base64 encoded string
#         row_data = list(row)
#         row_data[columns.index('foto_hotel')] = base64.b64encode(row_data[columns.index('foto_hotel')]).decode('utf-8')
#         data.append(dict(zip(columns, row_data)))
#     cursor.close()
#     timestamp = generate_timestamp()
#     return jsonify({'timestamp': timestamp, 'data': data})

@app.route('/hotel', methods=['GET'])
def get_all_hotel():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hotel")
    columns = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
    cursor.close()
    timestamp = generate_timestamp()
    return jsonify({'timestamp': timestamp, 'data': data})

@app.route('/hotel/<paket_id>', methods=['GET'])
def get_hotel_by_paket_id(paket_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hotel.hotel WHERE paket_id = %s", (paket_id,))
    columns = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
    cursor.close()
    timestamp = generate_timestamp()
    return jsonify({'timestamp': timestamp, 'data': data})

@app.route('/hotel/create', methods=['POST'])
def add_hotel():
    if request.method == 'POST':
        # Mengambil data dari permintaan POST
        id_hotel = request.form['id_hotel']
        nama_hotel = request.form['nama_hotel']
        lokasi_hotel = request.form['lokasi_hotel']
        harga_sewa = request.form['harga_sewa']
        paket_id = request.form['paket_id']
        
        # Menyimpan data ke dalam database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO hotel (id_hotel, nama_hotel, lokasi_hotel, harga_sewa, paket_id) VALUES (%s, %s, %s, %s)", (id_hotel, nama_hotel, harga_sewa, paket_id))
        mysql.connection.commit()
        cursor.close()
        
        # Menyusun respons
        timestamp = generate_timestamp()
        response = jsonify({'timestamp': timestamp, 'message': 'Data hotel berhasil ditambahkan'})
        response.status_code = 201  # Created
        return response
    else:
        return jsonify({'message': 'Method not allowed'}), 405  # Method Not Allowed


@app.route('/hotel/update/<id_hotel>', methods=['PUT'])
def update_hotel(id_hotel):
    if request.method == 'PUT':
        # Mengambil data dari permintaan POST
        nama_hotel = request.form['nama_hotel']
        lokasi_hotel = request.form['lokasi_hotel']
        harga_sewa = request.form['harga_sewa']
        paket_id = request.form['paket']
        
        # Menyimpan data ke dalam database
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE hotel SET nama_hotel = %s, lokasi_hotel = %s, harga_sewa = %s, paket_id = %s WHERE id_hotel = %s", (nama_hotel, lokasi_hotel, harga_sewa, paket_id, id_hotel))
        mysql.connection.commit()
        cursor.close()
        
        # Menyusun respons
        timestamp = generate_timestamp()
        response = jsonify({'timestamp': timestamp, 'message': 'Data hotel berhasil diupdate'})
        response.status_code = 201  # Created
        return response
    else:
        return jsonify({'message': 'Method not allowed'}), 405  # Method Not Allowed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)