"""
S3-compatible storage wrapper untuk S3 Compatible Storage dengan boto3.
"""

from __future__ import annotations

import logging
import io
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app_backend.conf.settings import settings

logger = logging.getLogger(__name__)


def get_s3_client():
    """Mengembalikan S3 client yang dikonfigurasi untuk endpoint S3-compatible."""
    endpoint = settings.s3_endpoint or None
    region = settings.s3_region or None
    access_key = settings.s3_access_key_id or None
    secret = settings.s3_secret_access_key or None

    config = Config(signature_version="s3v4", region_name=region)

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        config=config,
    )
    return client


def upload_fileobj(client, fileobj: io.IOBase, bucket: str, key: str, content_type: Optional[str] = None):
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    try:
        client.upload_fileobj(fileobj, bucket, key, ExtraArgs=extra_args or None)
        return True
    except (BotoCoreError, ClientError) as exc:
        logger.exception("upload_fileobj failed: %s", exc)
        return False


def list_buckets(client):
    try:
        return client.list_buckets()
    except (BotoCoreError, ClientError) as exc:
        logger.exception("list_buckets failed: %s", exc)
        return None


def head_bucket(client, bucket: str):
    try:
        return client.head_bucket(Bucket=bucket)
    except ClientError as exc:
        logger.exception("head_bucket failed: %s", exc)
        raise
