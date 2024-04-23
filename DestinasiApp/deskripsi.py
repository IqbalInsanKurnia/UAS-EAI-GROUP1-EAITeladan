from flask import Flask, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from flask import request
from werkzeug.utils import secure_filename
import base64


app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uts_eaiteladan_destinasi'
mysql = MySQL(app)

# Function to generate timestamp
def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to generate image to binary
def image_to_binary(file_path):
    with open(file_path, "rb") as image_file:
        binary_data = base64.b64encode(image_file.read())
    return binary_data.decode('utf-8')

@app.route('/destinasi', methods=['GET'])
def get_all_destinasi():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM destinasi")
    columns = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Convert BLOB image data to base64 encoded string
        row_data = list(row)
        row_data[columns.index('foto_tujuan')] = base64.b64encode(row_data[columns.index('foto_tujuan')]).decode('utf-8')
        data.append(dict(zip(columns, row_data)))
    cursor.close()
    timestamp = generate_timestamp()
    return jsonify({'timestamp': timestamp, 'data': data})

@app.route('/destinasi/<kota_tujuan>', methods=['GET'])
def get_tujuan_destinasi(kota_tujuan):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM destinasi WHERE kota_tujuan = %s", (kota_tujuan,))
    columns = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        row_data = list(row)
        row_data[columns.index('foto_tujuan')] = base64.b64encode(row_data[columns.index('foto_tujuan')]).decode('utf-8')
        data.append(dict(zip(columns, row_data)))
    cursor.close()
    timestamp = generate_timestamp()
    if data:
        return jsonify({'timestamp': timestamp, 'data': data, 'status code': 200}), 200
    else:
        return jsonify({'timestamp': timestamp, 'message': 'Destinasi tidak ditemukan', 'status' : 404}), 404

@app.route('/destinasi/create', methods=['POST'])
def add_destinasi():
    if request.method == 'POST':
        # Mengambil data dari permintaan POST
        id_perjalanan = request.form['id_perjalanan']
        tanggal_keberangkatan = request.form['tanggal_keberangkatan']
        kota_asal = request.form['kota_asal']
        kota_tujuan = request.form['kota_tujuan']
        
        # Menyimpan data gambar dari permintaan
        foto_tujuan = request.files['foto_tujuan'].read()
        
        # Menyimpan data ke dalam database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO destinasi (id_perjalanan, tanggal_keberangkatan, kota_asal, kota_tujuan, foto_tujuan) VALUES (%s, %s, %s, %s, %s)", (id_perjalanan, tanggal_keberangkatan, kota_asal, kota_tujuan, foto_tujuan))
        mysql.connection.commit()
        cursor.close()
        
        # Menyusun respons
        timestamp = generate_timestamp()
        response = jsonify({'timestamp': timestamp, 'message': 'Data destinasi berhasil ditambahkan'})
        response.status_code = 201  # Created
        return response
    else:
        return jsonify({'message': 'Method not allowed'}), 405  # Method Not Allowed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)