import boto3
import os
from botocore.config import Config

def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
        config=Config(signature_version="s3v4"),
        region_name="auto"
    )

def upload_pdf(file_bytes: bytes, filename: str) -> str:
    client = get_r2_client()
    bucket = os.getenv("R2_BUCKET_NAME")
    client.put_object(
        Bucket=bucket,
        Key=filename,
        Body=file_bytes,
        ContentType="application/pdf"
    )
    return filename

def get_pdf_url(filename: str) -> str:
    client = get_r2_client()
    bucket = os.getenv("R2_BUCKET_NAME")
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": filename},
        ExpiresIn=3600
    )
    return url