#!/usr/bin/env python3
import os
import click
import json
import boto3
import requests
from botocore.exceptions import NoCredentialsError, ClientError

CONFIG_PATH = os.path.expanduser("~/.xitecli/config.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def is_minio_alive(endpoint):
    try:
        health_url = endpoint.rstrip("/") + "/minio/health/live"
        r = requests.get(health_url, timeout=2)
        return r.status_code == 200
    except:
        return False

def get_s3_client(config, use_r2=False):
    if use_r2:
        r2 = config.get("r2", {})
        if not all(k in r2 for k in ("endpoint", "access_key", "secret_key")):
            raise ValueError("R2 fallback requested, but R2 credentials are missing.")
        return boto3.client(
            "s3",
            endpoint_url=r2["endpoint"],
            aws_access_key_id=r2["access_key"],
            aws_secret_access_key=r2["secret_key"],
            region_name=r2.get("region", "auto")
        )
    else:
        minio = config.get("minio", {})
        return boto3.client(
            "s3",
            endpoint_url=minio["endpoint"],
            aws_access_key_id=minio["access_key"],
            aws_secret_access_key=minio["secret_key"],
            region_name=minio.get("region", "us-east-1")
        )

def get_client(no_fallback=False):
    config = load_config()
    minio_endpoint = config.get("minio", {}).get("endpoint")
    alive = is_minio_alive(minio_endpoint)
    use_r2 = not alive and not no_fallback
    client = get_s3_client(config, use_r2=use_r2)
    return client, "r2" if use_r2 else "minio"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--bucket', required=True)
@click.option('--file', required=True, type=click.Path(exists=True))
@click.option('--no-fallback', is_flag=True, default=False, help="Disable R2 fallback")
def upload(bucket, file, no_fallback):
    client, used = get_client(no_fallback)
    try:
        client.upload_file(file, bucket, os.path.basename(file))
        click.echo(f"[{used.upper()}] Uploaded {file} to {bucket}")
    except (NoCredentialsError, ClientError) as e:
        click.echo(f"Upload failed: {e}")

@cli.command()
@click.option('--bucket', required=True)
@click.option('--key', required=True)
@click.option('--out', required=True, type=click.Path())
@click.option('--no-fallback', is_flag=True, default=False, help="Disable R2 fallback")
def download(bucket, key, out, no_fallback):
    client, used = get_client(no_fallback)
    try:
        client.download_file(bucket, key, out)
        click.echo(f"[{used.upper()}] Downloaded {key} to {out}")
    except Exception as e:
        click.echo(f"Download failed: {e}")

@cli.command()
@click.option('--bucket', required=True)
@click.option('--no-fallback', is_flag=True, default=False, help="Disable R2 fallback")
def list(bucket, no_fallback):
    client, used = get_client(no_fallback)
    try:
        objects = client.list_objects_v2(Bucket=bucket)
        click.echo(f"[{used.upper()}] Objects in {bucket}:")
        for obj in objects.get("Contents", []):
            click.echo(f" - {obj['Key']}")
    except Exception as e:
        click.echo(f"List failed: {e}")

@cli.command()
def configure():
    minio_endpoint = click.prompt("MinIO Endpoint (e.g. http://127.0.0.1:9000)")
    access_key = click.prompt("MinIO Access Key")
    secret_key = click.prompt("MinIO Secret Key")
    region = click.prompt("Default Region", default="us-east-1")
    config = {
        "minio": {
            "endpoint": minio_endpoint,
            "access_key": access_key,
            "secret_key": secret_key,
            "region": region
        },
        "r2": {}  # optional
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    click.echo("Configuration saved to ~/.xitecli/config.json")

if __name__ == "__main__":
    cli()
