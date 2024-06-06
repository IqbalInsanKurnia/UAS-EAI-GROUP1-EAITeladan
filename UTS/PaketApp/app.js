const express = require('express');
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
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

// Endpoint untuk menambahkan data baru paket liburan dengan ID manual
app.post('/add', async (req, res) => {
  try {
    const { paket_id, stock } = req.body;

    // Validasi ID dan stok
    if (!paket_id || typeof paket_id !== 'string' || paket_id.trim() === '') {
      return res.status(400).json({ error: 'ID paket liburan harus disertakan dan tidak boleh kosong.' });
    }
    if (typeof stock !== 'number' || stock < 0) {
      return res.status(400).json({ error: 'Stok harus berupa angka positif.' });
    }

    // Menambahkan data baru ke koleksi Firestore dengan ID manual
    await paketRef.doc(paket_id).set(req.body);

    res.status(200).json({ success: true, paket_id });
  } catch (error) {
    res.status(500).json({ error: error.toString() });
  }
});

// Endpoint untuk mengambil daftar semua paket liburan
app.get('/get', async (req, res) => {
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
    const { stock } = req.body;

    // Validasi stok
    if (stock !== undefined && (typeof stock !== 'number' || stock < 0)) {
      return res.status(400).json({ error: 'Stok harus berupa angka positif.' });
    }

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

// Endpoint untuk memilih paket liburan dan mengurangi stok
app.post('/pilih/:paket_id', async (req, res) => {
  try {
    const paket_id = req.params.paket_id;
    const { jumlah } = req.body;

    // Validasi jumlah yang dipilih
    if (typeof jumlah !== 'number' || jumlah <= 0) {
      return res.status(400).json({ error: 'Jumlah yang dipilih tidak valid.' });
    }

    // Dapatkan data paket liburan dari database
    const paketDoc = await paketRef.doc(paket_id).get();
    if (!paketDoc.exists) {
      return res.status(404).json({ error: 'Paket liburan tidak ditemukan.' });
    }

    // Periksa apakah stok cukup untuk jumlah yang dipilih
    const paketData = paketDoc.data();
    if (!paketData.stock || paketData.stock < jumlah) {
      return res.status(400).json({ error: 'Stok tidak mencukupi.' });
    }

    // Kurangi stok di database
    const updatedStock = paketData.stock - jumlah;
    await paketRef.doc(paket_id).update({ stock: updatedStock });

    // Kirim respons sukses
    res.status(200).json({ message: 'Paket berhasil dipilih.', new_stock: updatedStock });
  } catch (error) {
    // Tangani kesalahan
    res.status(500).json({ error: error.toString() });
  }
});


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(5002, () => {
  console.log('Server is running on port 5002');
});

// Skrip untuk memperbarui semua dokumen dan menambahkan atribut stok dengan nilai default 20
async function updateAllDocuments() {
  const snapshot = await paketRef.get();
  const batch = db.batch();

  snapshot.forEach(doc => {
    const docRef = paketRef.doc(doc.id);
    batch.update(docRef, { stock: 20 }); // Menambahkan stok default 20
  });

  await batch.commit();
  console.log('Semua dokumen berhasil diperbarui.');
}

// Jalankan skrip pembaruan
updateAllDocuments().catch(console.error);
