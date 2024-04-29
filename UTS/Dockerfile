# Stage 1: Menginstal dependensi untuk aplikasi Node.js
FROM node:latest as node_build

# Menyalin file package.json dan package-lock.json
COPY package*.json /app/

# Pindah ke direktori kerja /app
WORKDIR /app

# Menginstal dependensi Node.js
RUN npm install --no-cache

# Menyalin kode aplikasi Node.js
COPY . .

# Stage 2: Menginstal dependensi untuk aplikasi Python
FROM python:latest as python_build

# Menyalin file requirements.txt
COPY requirements.txt /app/

# Pindah ke direktori kerja /app
WORKDIR /app

# Menginstal dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin kode aplikasi Python
COPY . .

# Stage 3: Menggabungkan kedua tahap sebelumnya
FROM node:latest

# Menyalin dependensi Node.js dari tahap pertama
COPY --from=node_build /app/node_modules /app/node_modules

# Menyalin dependensi Python dari tahap kedua
COPY --from=python_build /app /app

# Pindah ke direktori kerja /app
WORKDIR /app

# Mengekspos beberapa port
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
EXPOSE 5009

# Menjalankan aplikasi
CMD ["node", "app.js"]
