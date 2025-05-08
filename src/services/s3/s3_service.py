import boto3
import io
from botocore.exceptions import NoCredentialsError

s3 = boto3.client('s3')


def upload_image_from_memory(bucket_name, image, object_key, expires_in=3600):
    """
    Upload a PIL image directly to S3 from memory and return a pre-signed URL.

    :param bucket_name: Name of the S3 bucket
    :param image: A PIL image object
    :param object_key: Key under which to store the image in the bucket
    :param expires_in: Expiration time for pre-signed URL (in seconds)
    :return: Pre-signed URL
    """
    buffer = io.BytesIO(image)

    try:
        s3.upload_fileobj(
            buffer,
            bucket_name,
            object_key,
            ExtraArgs={"ContentType": "image/jpeg"}
        )
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expires_in
        )
        return url

    except NoCredentialsError:
        print("AWS credentials not found.")
        return None
    except Exception as e:
        print(f" Error uploading image: {e}")
        return None

def get_pre_signed_image_url(bucket_name, object_key, expires_in=3600):
    """
    Generates a pre-signed URL for an existing S3 image.

    :param bucket_name: Name of the S3 bucket
    :param object_key: Key of the image in the bucket (e.g., 'images/photo.jpg')
    :param expires_in: Expiration time in seconds (default: 3600)
    :return: Pre-signed URL string
    """
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expires_in
        )
        return url
    except Exception as e:
        print(f"❌ Error generating pre-signed URL: {e}")
        return None

if __name__ == '__main__':
    print(get_pre_signed_image_url("emptorix-images", "X0tjDa1MBdQ8pH31DE3-b_2184fff4af614bebac3b43f61c02f7b3.jpg"))