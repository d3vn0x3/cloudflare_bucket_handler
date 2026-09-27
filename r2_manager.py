import os
from pathlib import Path
from dotenv import load_dotenv
import boto3


env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

class R2Manager:
    def __init__(self):
        self.account_id = os.getenv("R2_ACCOUNT_ID")
        self.access_key_id = os.getenv("R2_ACCESS_KEY_ID")
        self.secret_access_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.bucket_public = os.getenv("R2_BUCKET_PUBLIC")
        self.bucket_private = os.getenv("R2_BUCKET_PRIVATE")
        
        domains_raw = os.getenv("PUBLIC_DOMAINS", "")
        self.public_domains = [d.strip() for d in domains_raw.split(",") if d.strip()]

    
        if not self.account_id:
            raise ValueError(f"No se ha podido leer R2_ACCOUNT_ID. Buscado en: {env_path}")

        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"

        self.s3_client = boto3.client(
            service_name="s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name="auto"
        )

    def upload_file(self, local_path, bucket_name, object_name):
        self.s3_client.upload_file(local_path, bucket_name, object_name)

    def download_file(self, bucket_name, object_name, local_path):
        self.s3_client.download_file(bucket_name, object_name, local_path)

    def delete_file(self, bucket_name, object_name):
        self.s3_client.delete_object(Bucket=bucket_name, Key=object_name)

    def list_cloud_files(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if "Contents" in response:
                return [item["Key"] for item in response["Contents"]]
            return []
        except Exception as e:
            print(f"Error listing files in {bucket_name}: {e}")
            return []

    def move_between_buckets(self, source_bucket, target_bucket, object_name):
        copy_source = {'Bucket': source_bucket, 'Key': object_name}
        self.s3_client.copy_object(CopySource=copy_source, Bucket=target_bucket, Key=object_name)
        self.s3_client.delete_object(Bucket=source_bucket, Key=object_name)

    def generate_public_url(self, domain, object_name):
        domain = domain.replace("https://", "").replace("http://", "").strip("/")
        return f"https://{domain}/{object_name}"

    def generate_presigned_url(self, object_name, expiration=3600):
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_private, 'Key': object_name},
            ExpiresIn=expiration
        )