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


import mimetypes

def upload_file(file, path):
    """
    file: InMemoryUploadedFile (from request.FILES)
    path: storage path (string)
    """

    # Read raw binary
    file_data = file.read()

    # Detect MIME type
    content_type = file.content_type if hasattr(file, "content_type") else mimetypes.guess_type(path)[0]

    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=path,
        file=file_data,
        options={"content-type": content_type}  # <-- important
    )

    return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)

