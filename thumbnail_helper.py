import os
import io
import tempfile
from PIL import Image
import cv2

SUPPORTED_IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
SUPPORTED_VIDEO_EXTS = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}

def get_file_thumbnail(filepath, size=(40, 40)):
    """Genera miniatura para un archivo en el disco local."""
    if not os.path.exists(filepath):
        return None

    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext in SUPPORTED_IMAGE_EXTS:
            with Image.open(filepath) as img:
                img = img.convert("RGBA")
                img.thumbnail(size)
                return img.copy()

        elif ext in SUPPORTED_VIDEO_EXTS:
            cap = cv2.VideoCapture(filepath)
            success, frame = cap.read()
            cap.release()

            if success:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img.thumbnail(size)
                return img
    except Exception as e:
        print(f"Error miniatura local ({filepath}): {e}")

    return None

def get_cloud_file_thumbnail(s3_client, bucket_name, object_name, size=(40, 40)):
    """Descarga los primeros bytes de un archivo de R2 para generar miniatura en memoria."""
    ext = os.path.splitext(object_name)[1].lower()

    try:
       
        if ext in SUPPORTED_IMAGE_EXTS:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_name, Range="bytes=0-524288")
            image_bytes = response['Body'].read()
            
            with Image.open(io.BytesIO(image_bytes)) as img:
                img = img.convert("RGBA")
                img.thumbnail(size)
                return img.copy()

       
        elif ext in SUPPORTED_VIDEO_EXTS:
            response = s3_client.get_object(Bucket=bucket_name, Key=object_name, Range="bytes=0-2097152")
            video_bytes = response['Body'].read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(video_bytes)
                tmp_path = tmp_file.name

            cap = cv2.VideoCapture(tmp_path)
            success, frame = cap.read()
            cap.release()

            if os.path.exists(tmp_path):
                os.remove(tmp_path)

            if success:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img.thumbnail(size)
                return img

    except Exception:
     
        pass

    return None