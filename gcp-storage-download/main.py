import os
import unicodedata
from datetime import timedelta
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from google.cloud import storage
from google.oauth2 import service_account

app = FastAPI()
templates = Jinja2Templates(directory="templates")

## Variables
from dotenv import load_dotenv
load_dotenv()

KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BASE_PATH = os.getenv("BASE_PATH")

def get_gcs_client():
    """서비스 계정 키를 사용하여 GCS 클라이언트를 생성"""
    try:
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
        return storage.Client(credentials=credentials, project=PROJECT_ID)
    except Exception as e:
        logger.error(f"GCS 클라이언트 생성 실패: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get_report_download_url")
async def get_report_download_url(file_name: str):

    ## 한글 자소 분리 방지를 위한 정규화
    normalized_file_name = unicodedata.normalize('NFC', file_name)
    blob_path = f"{BASE_PATH}/{normalized_file_name}"

    try:
        storage_client = get_gcs_client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(blob_path)

        if not blob.exists():
            return JSONResponse(status_code=404, content={"message": "파일이 없습니다."})

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=10),
            method="GET",
        )
        return {"download_url": url}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("DEPLOY_SERVER_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)