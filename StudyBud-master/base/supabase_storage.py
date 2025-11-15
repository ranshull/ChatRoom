from supabase import create_client
import os

# SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
# SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")

SUPABASE_URL = 'https://zjsarscptztnuqgtesjp.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpqc2Fyc2NwdHp0bnVxZ3Rlc2pwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzEwOTcxMywiZXhwIjoyMDc4Njg1NzEzfQ.UJUXWw4xm1FGo_yBB5jpgVb4qaISBLHyb_W-23RfAdg'
SUPABASE_BUCKET = 'media'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(file, path):
    """
    file: Django InMemoryUploadedFile or File object
    path: path in bucket, e.g., 'message_images/img1.png'
    """
    file_data = file.read()
    supabase.storage.from_(SUPABASE_BUCKET).upload(path, file_data)
    public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path)
    return public_url
