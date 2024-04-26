const express = require('express');
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
const { v4: uuidv4 } = require('uuid');
const path = require('path');

const app = express();

// Inisialisasi Firebase Admin
const serviceAccount = require('./key.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});
const db = admin.firestore();
const paketRef = db.collection('paket_liburan');

// Middleware untuk memproses body JSON
app.use(bodyParser.json());

// Endpoint untuk menambahkan data baru paket liburan
app.post('/add', (req, res) => {
  try {
    const paket_id = uuidv4();
    req.body.paket_id = paket_id;
    paketRef.doc(paket_id).set(req.body);
    res.status(200).json({ success: true, paket_id });
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
});

// Endpoint untuk mengambil daftar semua paket liburan
app.get('/list', async (req, res) => {
  try {
    const snapshot = await paketRef.get();
    const all_paket = [];
    snapshot.forEach(doc => {
      all_paket.push(doc.data());
    });
    res.status(200).json({ paket_liburan: all_paket });
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
});

// Endpoint untuk mengambil data paket liburan berdasarkan ID
app.get('/get/:paket_id', async (req, res) => {
  try {
    const paket_id = req.params.paket_id;
    const paket = await paketRef.doc(paket_id).get();
    if (paket.exists) {
      res.status(200).json({ paket_liburan: paket.data() });
    } else {
      res.status(404).json({ message: 'Paket liburan tidak ditemukan.' });
    }
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
});

// Endpoint untuk mengupdate data paket liburan
app.put('/update/:paket_id', async (req, res) => {
  try {
    const paket_id = req.params.paket_id;
    await paketRef.doc(paket_id).update(req.body);
    res.status(200).json({ message: `Paket liburan dengan ID ${paket_id} berhasil diupdate.` });
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
});

// Endpoint untuk menghapus data paket liburan
app.delete('/delete/:paket_id', async (req, res) => {
  try {
    const paket_id = req.params.paket_id;
    await paketRef.doc(paket_id).delete();
    res.status(200).json({ message: `Paket liburan dengan ID ${paket_id} berhasil dihapus.` });
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
    // atau gunakan res.render() jika menggunakan mesin template
  });

app.listen(5002, () => {
  console.log('Server is running on port 5002');
});
