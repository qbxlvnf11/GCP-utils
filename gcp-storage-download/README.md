### 🔍 GCS (Google-Cloud-Storage) Secure Report Download System
* This project provides a secure way to download files from Google Cloud Storage (GCS) by generating temporary, authenticated links, ensuring your storage remains private while allowing authorized access.
    * Secure Downloads (Signed URLs): Instead of making your GCS bucket public, the system generates V4 Signed URLs that are valid for only 10 minutes.
    * Korean Filename Optimization (NFC Normalization): It uses unicodedata to perform NFC Normalization, preventing filename mismatch errors caused by different encoding methods between macOS (NFD) and Windows/Linux (NFC).
    * User-Defined Input: The frontend allows users to manually enter filenames to retrieve and download specific reports dynamically.
    * Environment-Based Configuration: Key settings and security paths are managed via .env files using python-dotenv, keeping sensitive credentials out of the source code.

### - Environment Configuration
* The script relies on a .env file located in the project root. Create a file named .env and include the following variables:
  
```ini
# The unique ID of your Google Cloud Project
GCP_PROJECT_ID=clear-tooling-...

# The name of the GCS Bucket where report files are stored
GCP_BUCKET_NAME=storage_name

# Local path to your Service Account JSON key file
GOOGLE_APPLICATION_CREDENTIALS=./clear-tooling-....json

# The base directory path inside the bucket (e.g., folder structure)
BASE_PATH=storage_name/Report

# The port number where the FastAPI server will run
DEPLOY_SERVER_PORT=8000
```

### - How to Run

```
pip install fastapi uvicorn google-cloud-storage python-dotenv jinja2
uvicorn main:app --reload
```

---

## Author

#### - [LinkedIn](https://www.linkedin.com/in/taeyong-kong-016bb2154)

#### - [Blog URL](https://blog.naver.com/qbxlvnf11)

#### - Email: qbxlvnf11@google.com, qbxlvnf11@naver.com


