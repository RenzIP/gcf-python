# Python Cloud Function - MongoDB Integration

Proyek ini adalah contoh implementasi Google Cloud Function menggunakan Python yang terintegrasi dengan MongoDB. Cloud Function ini menyediakan endpoint untuk health check dan query data dari database MongoDB.

## Fitur

- **Health Check**: Endpoint `/` atau `/ping` untuk memverifikasi fungsi berjalan
- **MongoDB Query**: Endpoint `/users` untuk mengambil data user dari MongoDB
- **Error Handling**: Penanganan error yang baik untuk koneksi database

## Struktur Proyek

```
gcf-python/
├── main.py           # Kode utama Cloud Function
├── requirements.txt  # Dependencies Python
└── README.md        # Dokumentasi ini
```

## Prerequisites

Sebelum deploy, pastikan Anda memiliki:

1. **Google Cloud SDK** terinstall
2. **Google Cloud Project** yang aktif
3. **MongoDB Database** (Atlas atau self-hosted)
4. **Billing** yang aktif di GCP
5. **GitHub Repository** (untuk automated deployment)

## Setup dan Deployment

### 1. Setup GitHub Secrets (untuk Automated Deployment)

Jika menggunakan GitHub Actions, setup secrets berikut di repository GitHub:

1. **GOOGLE_CREDENTIALS**:

   - Buat service account di Google Cloud Console
   - Download JSON key
   - Paste seluruh JSON sebagai secret

2. **MONGOSTRING**:
   - MongoDB connection string Anda
   - Format: `mongodb+srv://user:pass@cluster.mongodb.net/database`

### 2. Install Google Cloud SDK

```bash
# Download dan install dari: https://cloud.google.com/sdk/docs/install
# Atau gunakan package manager sesuai OS Anda
```

### 3. Login ke Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 4. Enable Required APIs

```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 5. Set Environment Variables

Set MongoDB connection string sebagai environment variable:

```bash
gcloud functions deploy coba \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars MONGOSTRING="your_mongodb_connection_string"
```

### 6. Deploy Cloud Function

#### Manual Deployment

```bash
gcloud functions deploy coba \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point coba \
  --source . \
  --region asia-southeast1
```

#### Automated Deployment (GitHub Actions)

Proyek ini sudah dikonfigurasi dengan GitHub Actions untuk deployment otomatis. Pastikan Anda telah mengatur secrets berikut di repository GitHub:

1. **GOOGLE_CREDENTIALS**: Service account key JSON dari Google Cloud
2. **MONGOSTRING**: MongoDB connection string

Workflow akan otomatis deploy saat push ke branch `main` dengan konfigurasi:

- Function name: `cobain`
- Runtime: Python 3.13 (Gen 2)
- Region: asia-southeast2
- Timeout: 540s

## Environment Variables

| Variable      | Description               | Example                                                |
| ------------- | ------------------------- | ------------------------------------------------------ |
| `MONGOSTRING` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/database` |

## API Endpoints

### Health Check

```
GET /
GET /ping
```

**Response:**

```json
{
  "status": "ok",
  "message": "Cloud Function aktif!"
}
```

### Get Users

```
GET /users
```

**Response:**

```json
{
  "status": "success",
  "users": [
    {
      "name": "John Doe",
      "email": "john@example.com"
    }
  ]
}
```

**Error Response:**

```json
{
  "status": "error",
  "message": "Error message here"
}
```

## Testing

### Local Testing

Untuk testing lokal, Anda bisa menggunakan Flask development server:

```bash
pip install -r requirements.txt
export MONGOSTRING="your_mongodb_connection_string"
python -m flask run
```

### Testing Deployed Function

```bash
# Get function URL (sesuaikan dengan nama function dan region)
gcloud functions describe cobain --region=asia-southeast2 --format="value(httpsTrigger.url)"

# Test endpoints
curl https://YOUR_FUNCTION_URL/
curl https://YOUR_FUNCTION_URL/ping
curl https://YOUR_FUNCTION_URL/users
```

### Monitoring GitHub Actions Deployment

1. **Check Workflow Status**: Lihat tab "Actions" di GitHub repository
2. **View Logs**: Klik pada workflow run untuk melihat detail logs
3. **Debug Deployment**: Workflow sudah include debug steps untuk troubleshooting

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**

   - Pastikan `MONGOSTRING` environment variable sudah benar
   - Periksa network access di MongoDB Atlas
   - Pastikan IP address diizinkan

2. **Deployment Error**

   - Periksa billing account aktif
   - Pastikan semua required APIs sudah enabled
   - Periksa log deployment: `gcloud functions logs read coba`

3. **Runtime Error**
   - Periksa log function: `gcloud functions logs read coba --limit=50`
   - Pastikan semua dependencies ada di `requirements.txt`

### Logs dan Monitoring

```bash
# View function logs
gcloud functions logs read coba --limit=50

# View real-time logs
gcloud functions logs tail coba
```

## Security Considerations

1. **Authentication**: Fungsi ini menggunakan `--allow-unauthenticated`. Untuk production, pertimbangkan menggunakan authentication.
2. **MongoDB Security**: Gunakan connection string dengan credentials yang aman
3. **Environment Variables**: Jangan hardcode sensitive data dalam kode

## Cost Optimization

- Cloud Functions dibayar per invocation dan execution time
- Pertimbangkan menggunakan connection pooling untuk MongoDB
- Monitor usage melalui Google Cloud Console

## Support

Untuk bantuan lebih lanjut:

- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [MongoDB Python Driver Documentation](https://pymongo.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## License

Lihat file [LICENSE](LICENSE) untuk informasi lisensi.
