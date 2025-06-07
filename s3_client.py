import boto3
from botocore.client import Config

def get_s3_client(config, use_r2=False):
    if use_r2:
        creds = config.get("r2", {})
        if not creds or not creds.get("endpoint"):
            raise ValueError("R2 fallback requested, but R2 credentials are missing.")
    else:
        creds = config["minio"]

    return boto3.client(
        's3',
        endpoint_url=creds["endpoint"],
        aws_access_key_id=creds["access_key"],
        aws_secret_access_key=creds["secret_key"],
        region_name=creds.get("region", "us-east-1"),
        config=Config(signature_version='s3v4')
    )

def upload_file(s3, bucket, file_path):
    import os
    file_name = os.path.basename(file_path)
    s3.upload_file(file_path, bucket, file_name)
    print(f"✅ Uploaded {file_name} to bucket `{bucket}`")

def download_file(s3, bucket, key, out_path):
    s3.download_file(bucket, key, out_path)
    print(f"✅ Downloaded {key} to {out_path}")

def list_objects(s3, bucket):
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp.get("Contents", []):
        print(f"{obj['Key']} - {obj['Size']} bytes")
