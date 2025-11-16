# from supabase import create_client
# import os

# SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
# SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")



# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# def upload_file(file, path):
#     """
#     file: Django InMemoryUploadedFile or File object
#     path: path in bucket, e.g., 'message_images/img1.png'
#     """
#     file_data = file.read()
#     supabase.storage.from_(SUPABASE_BUCKET).upload(path, file_data)
#     public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)
#     return public_url


# import mimetypes

# def upload_file(file, path):
#     """
#     file: InMemoryUploadedFile (from request.FILES)
#     path: storage path (string)
#     """

#     # Read raw binary
#     file_data = file.read()

#     # Detect MIME type
#     content_type = file.content_type if hasattr(file, "content_type") else mimetypes.guess_type(path)[0]

#     supabase.storage.from_(SUPABASE_BUCKET).upload(
#         path=path,
#         file=file_data,
#         options={"content-type": content_type}  # <-- important
#     )

#     return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)

# import mimetypes
# from django.core.files.uploadedfile import InMemoryUploadedFile

# def upload_file(file, path):
#     """
#     file: Can be InMemoryUploadedFile, FieldFile, or any file-like object
#     path: storage path (string)
#     """

#     # Read file data
#     if hasattr(file, 'read'):
#         # Reset cursor to beginning if needed
#         if hasattr(file, 'seek') and hasattr(file, 'tell'):
#             if file.tell() > 0:
#                 file.seek(0)
#         file_data = file.read()
#     elif hasattr(file, 'path'):
#         # FieldFile with path attribute
#         with open(file.path, 'rb') as f:
#             file_data = f.read()
#     else:
#         raise ValueError("Unsupported file type")

#     # Determine content type
#     content_type = None
    
#     # First try: check if file has content_type attribute
#     if hasattr(file, 'content_type') and file.content_type:
#         content_type = file.content_type
    
#     # Second try: guess from filename
#     if not content_type and hasattr(file, 'name'):
#         content_type = mimetypes.guess_type(file.name)[0]
    
#     # Third try: guess from path
#     if not content_type:
#         content_type = mimetypes.guess_type(path)[0]
    
#     # Final fallback
#     if not content_type:
#         content_type = 'application/octet-stream'

#     # Upload to Supabase
#     supabase.storage.from_(SUPABASE_BUCKET).upload(
#         path=path,
#         file=file_data,
#         options={"content-type": content_type}
#     )

#     return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)

from supabase import create_client
import os

import re
import unicodedata

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")  # Default to 'media' bucket

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(file, path):
    """
    Upload file to Supabase storage with correct MIME type
    """
    try:
        # Read file data
        if hasattr(file, 'read'):
            # Reset cursor to beginning if needed
            if hasattr(file, 'seek') and hasattr(file, 'tell'):
                if file.tell() > 0:
                    file.seek(0)
            file_data = file.read()
        elif hasattr(file, 'path'):
            # FieldFile with path attribute
            with open(file.path, 'rb') as f:
                file_data = f.read()
        else:
            raise ValueError("Unsupported file type")

        # Determine content type based on file extension and name
        file_name = file.name if hasattr(file, 'name') else path
        
        # Special handling for PDF files
        if file_name.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        else:
            # Use file's content_type if available
            if hasattr(file, 'content_type') and file.content_type:
                content_type = file.content_type
            else:
                # Fallback to mimetypes guessing
                import mimetypes
                content_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

        # Upload to Supabase
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=path,
            file=file_data,
            file_options={"content-type": content_type}
        )

        # Get public URL
        return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)

    except Exception as e:
        print(f"Error uploading file to Supabase: {e}")
        raise



def sanitize_filename(filename):
    # Convert unicode → ASCII
    filename = unicodedata.normalize("NFKD", filename).encode("ascii", "ignore").decode()

    # Replace invalid characters
    filename = re.sub(r'[^A-Za-z0-9._-]', '_', filename)

    return filename
