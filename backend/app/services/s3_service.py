import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from PIL import Image
import io
import uuid
from datetime import datetime
from typing import Dict, Optional, Tuple
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_S3_BUCKET
        self.base_url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com"
    
    def upload_screenshot(self, image_file: bytes, user_id: str, filename: str) -> Dict[str, str]:
        """
        Upload and optimize screenshot to S3
        """
        try:
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            
            # Optimize image
            optimized_image = self._optimize_image(image_file)
            thumbnail = self._create_thumbnail(optimized_image)
            
            # Define S3 keys
            original_key = f"users/{user_id}/original/{file_id}.webp"
            thumbnail_key = f"users/{user_id}/thumbnails/{file_id}.webp"
            
            # Upload original image
            self.s3_client.upload_fileobj(
                optimized_image,
                self.bucket_name,
                original_key,
                ExtraArgs={
                    'ContentType': 'image/webp',
                    'Metadata': {
                        'original-filename': filename,
                        'upload-date': datetime.now().isoformat(),
                        'user-id': user_id
                    }
                }
            )
            
            # Upload thumbnail
            self.s3_client.upload_fileobj(
                thumbnail,
                self.bucket_name,
                thumbnail_key,
                ExtraArgs={
                    'ContentType': 'image/webp',
                    'Metadata': {
                        'original-filename': filename,
                        'upload-date': datetime.now().isoformat(),
                        'user-id': user_id
                    }
                }
            )
            
            return {
                'file_id': file_id,
                'original_url': f"{self.base_url}/{original_key}",
                'thumbnail_url': f"{self.base_url}/{thumbnail_key}",
                'original_filename': filename,
                'upload_date': datetime.now().isoformat()
            }
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise Exception("AWS credentials not configured")
        except ClientError as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise Exception(f"Upload failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            raise Exception(f"Upload failed: {str(e)}")
    
    def _optimize_image(self, image_data: bytes) -> io.BytesIO:
        """
        Optimize image for storage
        """
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if too large
            max_size = settings.MAX_IMAGE_SIZE
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save as WebP with optimization
            buffer = io.BytesIO()
            img.save(
                buffer, 
                format='WebP', 
                quality=settings.IMAGE_QUALITY, 
                optimize=True
            )
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            logger.error(f"Image optimization failed: {str(e)}")
            raise Exception(f"Image optimization failed: {str(e)}")
    
    def _create_thumbnail(self, image_buffer: io.BytesIO) -> io.BytesIO:
        """
        Create thumbnail for gallery view
        """
        try:
            img = Image.open(image_buffer)
            img.thumbnail(settings.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(
                buffer, 
                format='WebP', 
                quality=80, 
                optimize=True
            )
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            logger.error(f"Thumbnail creation failed: {str(e)}")
            raise Exception(f"Thumbnail creation failed: {str(e)}")
    
    def delete_screenshot(self, user_id: str, file_id: str) -> bool:
        """
        Delete screenshot and thumbnail from S3
        """
        try:
            original_key = f"users/{user_id}/original/{file_id}.webp"
            thumbnail_key = f"users/{user_id}/thumbnails/{file_id}.webp"
            
            # Delete original
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=original_key
            )
            
            # Delete thumbnail
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=thumbnail_key
            )
            
            logger.info(f"Successfully deleted file {file_id} for user {user_id}")
            return True
            
        except ClientError as e:
            logger.error(f"S3 delete failed: {str(e)}")
            raise Exception(f"Delete failed: {str(e)}")
    
    def get_storage_usage(self, user_id: Optional[str] = None) -> Dict[str, any]:
        """
        Get storage usage statistics
        """
        try:
            if user_id:
                prefix = f"users/{user_id}/"
            else:
                prefix = "users/"
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            total_size = 0
            total_files = 0
            
            for obj in response.get('Contents', []):
                total_size += obj['Size']
                total_files += 1
            
            return {
                'total_size_bytes': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'total_size_gb': total_size / (1024 * 1024 * 1024),
                'total_files': total_files,
                'free_tier_limit_gb': 5.0,
                'usage_percentage': (total_size / (5 * 1024 * 1024 * 1024)) * 100
            }
            
        except ClientError as e:
            logger.error(f"Failed to get storage usage: {str(e)}")
            raise Exception(f"Failed to get storage usage: {str(e)}")
    
    def cleanup_old_files(self, days_old: int = 30) -> int:
        """
        Clean up files older than specified days
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days_old)
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix="users/"
            )
            
            deleted_count = 0
            
            for obj in response.get('Contents', []):
                if obj['LastModified'] < cutoff_date:
                    self.s3_client.delete_object(
                        Bucket=self.bucket_name,
                        Key=obj['Key']
                    )
                    deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old files")
            return deleted_count
            
        except ClientError as e:
            logger.error(f"Cleanup failed: {str(e)}")
            raise Exception(f"Cleanup failed: {str(e)}") 