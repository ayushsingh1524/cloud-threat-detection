import json
import boto3
import gzip
from io import BytesIO

class CloudTrailIngester:
    def __init__(self, s3_bucket: str):
        self.s3_client = boto3.client('s3')
        self.bucket = s3_bucket

    def fetch_logs(self, prefix: str) -> list[dict]:
        """Fetch and decompress CloudTrail logs from S3."""
        logs = []
        paginator = self.s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket, Prefix=prefix)

        for page in pages:
            if 'Contents' not in page:
                continue
            for obj in page['Contents']:
                key = obj['Key']
                if not key.endswith('.json.gz'):
                    continue
                
                response = self.s3_client.get_object(Bucket=self.bucket, Key=key)
                content = response['Body'].read()
                
                with gzip.GzipFile(fileobj=BytesIO(content)) as gz:
                    data = json.loads(gz.read().decode('utf-8'))
                    if 'Records' in data:
                        logs.extend(data['Records'])
        return logs
