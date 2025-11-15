from supabase import create_client
import os

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")



supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# def upload_file(file, path):
#     """
#     file: Django InMemoryUploadedFile or File object
#     path: path in bucket, e.g., 'message_images/img1.png'
#     """
#     file_data = file.read()
#     supabase.storage.from_(SUPABASE_BUCKET).upload(path, file_data)
#     public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)
#     return public_url


def upload_file(file, path):
    """
    file: Django InMemoryUploadedFile or File object
    path: path in bucket, e.g., 'message_files/doc1.pdf'
    """

    file_data = file.read()
    mime_type = file.content_type  # <= Detect MIME correctly

    # Upload with correct content-type
    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        file_data,
        {
            "contentType": mime_type
        }
    )

    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)
    return public_url
