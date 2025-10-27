
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import os
import os
from google import genai
from pathlib import Path
from PIL import Image
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Message
from google import genai
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

import pytesseract
import fitz 

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

def dashboard_view(request):
    return render(request, 'base/index.html')

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


# def registerPage(request):
#     form = MyUserCreationForm()

#     if request.method == 'POST':
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'An error occurred during registration')

#     return render(request, 'base/login_register.html', {'form': form})

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # Loop through all field errors and show them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


# def room(request, pk):
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all()
#     participants = room.participants.all()
#     hashtag_filter = request.GET.get('hashtag')

#     if request.method == 'POST':
#         message = Message.objects.create(
#             user=request.user,
#             room=room,
#             body=request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect('room', pk=room.id)

#     context = {'room': room, 'room_messages': room_messages,
#                'participants': participants}
#     return render(request, 'base/room.html', context)

# def room(request, pk):
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all()
#     participants = room.participants.all()
#     hashtag_filter = request.GET.get('hashtag')

#     if hashtag_filter:
#         room_messages = room.message_set.filter(hashtags__icontains=hashtag_filter)
#     else:
#         room_messages = room.message_set.all()

#     participants = room.participants.all()

#     if request.method == 'POST':
#         message = Message.objects.create(
#             user=request.user,
#             room=room,
#             body=request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect('room', pk=room.id)

#     # extract all hashtags in the room (unique)
#     all_tags = set()
#     for msg in room.message_set.all():
#         all_tags.update(msg.hashtag_list())

#     context = {
#         'room': room,
#         'room_messages': room_messages,
#         'participants': participants,
#         'hashtags': sorted(all_tags),
#     }
#     return render(request, 'base/room.html', context)
@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    # hashtag_filter = request.GET.get('hashtag', '')
    hashtag_filter1 = request.GET.get('hashtag', '').strip()
    hashtag_filter = hashtag_filter1.lstrip('#')
    # if not hashtag_filter.startswith('#') and hashtag_filter != '':
    #     hashtag_filter = '#' + hashtag_filter


    if hashtag_filter:
        # room_messages = room_messages.filter(hashtags__icontains=hashtag_filter)
        room_messages = room_messages.filter(hashtags__regex=rf'\b{hashtag_filter}\b')

    # Collect all distinct hashtags in the room
    all_hashtags = []
    for msg in room.message_set.all():
        all_hashtags.extend(msg.hashtags.split())
    distinct_hashtags = sorted(set(all_hashtags))

    # if request.method == 'POST':
    #     message = Message.objects.create(
    #         user=request.user,
    #         room=room,
    #         body=request.POST.get('body')                      # working one
    #     )
    #     room.participants.add(request.user)
    #     return redirect('room', pk=room.id)
    # body = None
    # image = None
    # pdf = None
    
    if request.method == 'POST':
        body = request.POST.get('body')
        image = request.FILES.get('image')
        pdf = request.FILES.get('pdf')

        if body or image or pdf:  # prevent empty messages
            message=Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                image=image,
                pdf=pdf
            )
            room.participants.add(request.user)
            
        return redirect('room', pk=room.id)


    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'hashtags': distinct_hashtags,
        'hashtag_filter': hashtag_filter
    }
    return render(request, 'base/room.html', context)




def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

@login_required(login_url='login')
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

@login_required(login_url='login')
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})



# Setup Gemini API client

os.environ["API_KEY"] = "AIzaSyDuCmFicMCoCmg2DUuT5eUZhIEPz_2f03c"

client = genai.Client(api_key=os.environ["API_KEY"])

# def generate_flashcard(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
#     input_text = message.body

#     # prompt = (
#     #     f"Read the following text and generate 3 flashcards in Q&A format. "
#     #     f"Each card should include a question and an answer covering key ideas.\n\n"
#     #     f"Text:\n{input_text}\n\n"
#     #     f"Flashcards:\n"
#     #     f"1. Q: ...\n   A: ...\n"
#     # )
#     prompt = (
#     f"Read the following text and generate 3 short, summary-style flashcards. "
#     f"Each flashcard should be concise so it's easy to read and understand quickly. "
#     f"Format each flashcard as a question and answer (Q&A), and add '###' at the end of each flashcard as a separator.\n\n"
#     f"Text:\n{input_text}\n\n"
#     f"Flashcards:\n"
#     f"1. Q: ...\n   A: ... ###\n"
# )


#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     generated_text = response.text if hasattr(response, "text") else "No flashcards generated."

#  # Process flashcards into a list of dicts: [{'Q': '...', 'A': '...'}, ...]
#     flashcards = []
#     for card_text in generated_text.split('\n\n'):
#         card_text = card_text.strip()
#         if not card_text:
#             continue
#         q, a = '', ''
#         for line in card_text.splitlines():
#             if line.startswith('Q:'):
#                 q = line[3:].strip()
#             elif line.startswith('A:'):
#                 a = line[3:].strip()
#         if q and a:
#             flashcards.append({'Q': q, 'A': a})

#     return render(request, "base/flashcards.html", {
#         "message": message,
#         "flashcards": flashcards
#     })

#=----------------------------------------------------------------------
# views.py

# Set your Gemini API key
# os.environ["API_KEY"] = "YOUR_GEMINI_API_KEY"
# client = genai.Client(api_key=os.environ["API_KEY"])

# Optional: Extract text from PDFs using PyMuPDF
def extract_text_from_pdf(pdf_path):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Optional: Extract text from image
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print("OCR failed:", e)
        return ""

# Generate flashcards using Gemini API
def generate_flashcards_from_text(input_text, num_cards=10, explain=True):
    # explanation = "Explain each answer clearly and concisely." if explain else ""
    prompt = (
    f"Read the following text carefully and generate **student-friendly flashcards**. "
    f"Requirements:\n"
    f"1. Each flashcard must cover **only one main idea**.\n"
    f"2. Keep flashcards **short and easy to remember** (1–2 sentences max).\n"
    f"3. Use **concise statements or bullets**; do NOT use Q&A format.\n"
    f"4. Each flashcard should be **self-contained**—it should make sense on its own.\n"
    f"5. Cover **all key points** from the text; create as many flashcards as necessary.\n"
    f"6. After each flashcard, include '###' as a separator.\n"
    f"7. Do not include any extra instructions or filler text.\n\n"
    f"Text:\n{input_text}\n\n"
    f"Flashcards:\n"
)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# Django view
def generate_flashcard(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    input_text = ""

    # 1. Text input
    if message.body:
        input_text += message.body + "\n\n"

    # 2. PDF input
    if message.pdf:
        pdf_path = message.pdf.path
        if Path(pdf_path).exists():
            input_text += extract_text_from_pdf(pdf_path) + "\n\n"

    # 3. Image input
    if message.image:
        image_path = message.image.path
        if Path(image_path).exists():
            input_text += extract_text_from_image(image_path) + "\n\n"

    flashcards = ""
    if input_text.strip():  # Only generate if there's any text
        flashcard_text = generate_flashcards_from_text(input_text, num_cards=10)
        flashcards = [f.strip() for f in flashcard_text.split("###") if f.strip()]


    context = {
        "message": message,
        "flashcards": flashcards,
    }
    return render(request, "base/flashcards.html", context)


# def extract_text_from_image(image_field):
#     """Extract text from an uploaded image using pytesseract"""
#     if not image_field:
#         return ""
#     try:
#         img = Image.open(image_field)
#         text = pytesseract.image_to_string(img)
#         return text.strip()
#     except Exception as e:
#         print("Image OCR error:", e)
#         return ""

# def extract_text_from_pdf(pdf_field):
#     """Extract text from a PDF (supports text PDFs and scanned PDFs)"""
#     if not pdf_field:
#         return ""
#     try:
#         pdf_path = pdf_field.path
#         doc = fitz.open(pdf_path)
#         full_text = ""

#         for page in doc:
#             page_text = page.get_text().strip()
#             if page_text:  # Normal text PDF
#                 full_text += page_text + "\n"
#             else:  # Scanned PDF → OCR
#                 pix = page.get_pixmap()
#                 img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#                 ocr_text = pytesseract.image_to_string(img)
#                 full_text += ocr_text + "\n"

#         return full_text.strip()
#     except Exception as e:
#         print("PDF extraction error:", e)
#         return ""


# @login_required(login_url='login')
# def generate_flashcard(request, message_id):
#     message = get_object_or_404(Message, id=message_id)

#     # 1️⃣ Collect all text sources
#     texts = []

#     if message.body and message.body.strip():
#         texts.append(message.body.strip())

#     if message.image:
#         img_text = extract_text_from_image(message.image)
#         if img_text:
#             texts.append(img_text)

#     if message.pdf:
#         pdf_text = extract_text_from_pdf(message.pdf)
#         if pdf_text:
#             texts.append(pdf_text)

#     input_text = "\n".join(texts)

#     # 2️⃣ Handle empty content
#     if not input_text.strip():
#         flashcards = ["No readable text found in this message."]
#     else:
#         # 3️⃣ Build prompt for Gemini
#         prompt = (
#             f"Read the following text and generate flashcards in a student-friendly study style. "
#             f"Requirements:\n"
#             f"1. Each flashcard should cover **one main idea** only.\n"
#             f"2. Flashcards must be **short, 1–2 sentences max**.\n"
#             f"3. Do **NOT** use Q&A format. Just concise statements or bullets.\n"
#             f"4. Each flashcard should be **self-contained**.\n"
#             f"5. Include **all key points** from the text; create as many flashcards as needed.\n"
#             f"6. After each flashcard, add '###' as a separator.\n\n"
#             f"Text:\n{input_text}\n\n"
#             f"Flashcards:\n"
#         )

#         # 4️⃣ Call Gemini API
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#         flashcard_text = getattr(response, "text", "No flashcards generated.")
#         flashcards = [f.strip() for f in flashcard_text.split("###") if f.strip()]

#     # 5️⃣ Send to template
#     context = {
#         "message": message,
#         "flashcards": flashcards,
#     }
#     return render(request, "base/flashcards.html", context)
# -----------------------------------------------------------
# def extract_text_from_image(image_field):
#     """Extract text from an uploaded image"""
#     if not image_field:
#         return ""
#     try:
#         img = Image.open(image_field)
#         return pytesseract.image_to_string(img)
#     except Exception as e:
#         print("Image OCR error:", e)
#         return ""


# def extract_text_from_pdf(pdf_field):
#     """Extract text from an uploaded PDF"""
#     if not pdf_field:
#         return ""
#     try:
#         pdf_path = pdf_field.path  # path to the uploaded file
#         doc = fitz.open(pdf_path)
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         return text
#     except Exception as e:
#         print("PDF extraction error:", e)
#         return ""


# def generate_flashcard(request, message_id):
#     message = get_object_or_404(Message, id=message_id)

#     # 1️⃣ Gather all text sources
#     input_text = message.body or ""
    
#     # Add OCR text if image exists
#     if message.image:
#         input_text += "\n" + extract_text_from_image(message.image)

#     # Add PDF text if PDF exists
#     if message.pdf:
#         input_text += "\n" + extract_text_from_pdf(message.pdf)

#     if not input_text.strip():
#         flashcards = ["No text available in this message."]
#     else:
#         # 2️⃣ Build Gemini prompt
#         prompt = (
#             f"Read the following text and generate flashcards in a student-friendly study style. "
#             f"Requirements:\n"
#             f"1. Each flashcard should cover **one main idea** only.\n"
#             f"2. Flashcards must be **short, 1–2 sentences max**.\n"
#             f"3. Do **NOT** use Q&A format. Just concise statements or bullets.\n"
#             f"4. Each flashcard should be **self-contained**.\n"
#             f"5. Include **all key points** from the text; create as many flashcards as needed.\n"
#             f"6. After each flashcard, add '###' as a separator.\n\n"
#             f"Text:\n{input_text}\n\n"
#             f"Flashcards:\n"
#         )

#         # 3️⃣ Call Gemini API
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#         # 4️⃣ Extract and split flashcards
#         flashcard_text = getattr(response, "text", "No flashcards generated.")
#         flashcards = [f.strip() for f in flashcard_text.split("###") if f.strip()]

#     # 5️⃣ Send to template
#     context = {
#         "message": message,
#         "flashcards": flashcards,
#     }
#     return render(request, "base/flashcards.html", context)

#-------------------------------------------------------------------------------------
# def generate_flashcard(request, message_id):
#     message = get_object_or_404(Message, id=message_id)

#     # Start with text from message body
#     input_text = message.body or ""

#     # --- Extract text from PDF if present ---
#     if message.pdf:
#         pdf_path = message.pdf.path
#         try:
#             # Convert PDF pages to images
#             pages = convert_from_path(pdf_path)
#             for page in pages:
#                 input_text += "\n" + pytesseract.image_to_string(page)
#         except Exception as e:
#             input_text += f"\n[Error reading PDF: {str(e)}]"

#     # --- Extract text from image if present ---
#     if message.image:
#         image_path = message.image.path
#         try:
#             img = Image.open(image_path)
#             input_text += "\n" + pytesseract.image_to_string(img)
#         except Exception as e:
#             input_text += f"\n[Error reading image: {str(e)}]"

#     # --- Build prompt for flashcard generation ---
#     prompt = (
#         f"Read the following text and generate flashcards in a student-friendly study style. "
#         f"Requirements:\n"
#         f"1. Each flashcard should cover **one main idea** only.\n"
#         f"2. Flashcards must be **short, 1–2 sentences max**, so they are easy to read and remember.\n"
#         f"3. Do **NOT** use Q&A format. Just concise statements or bullets.\n"
#         f"4. Each flashcard should be **self-contained**—it should make sense on its own.\n"
#         f"5. Include **all key points** from the text; create as many flashcards as needed.\n"
#         f"6. After each flashcard, add '###' as a separator.\n\n"
#         f"Text:\n{input_text}\n\n"
#         f"Flashcards:\n"
#     )

#     # --- Call Gemini API ---
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     # Extract generated text
#     flashcard_text = getattr(response, "text", "No flashcards generated.")

#     # Split flashcards by '###' separator
#     flashcards = [f.strip() for f in flashcard_text.split("###") if f.strip()]

#     # Send to template using context
#     context = {
#         'message': message,
#         'flashcards': flashcards
#     }

#     return render(request, 'base/flashcards.html', context)


#old
# def generate_flashcard(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
#     input_text = message.body

#     # Your prompt for short, summary-style flashcards with separator
#     prompt = (
#         f"Read the following text and generate flashcards in a student-friendly study style. "
#         f"Requirements:\n"
#         f"1. Each flashcard should cover **one main idea** only.\n"
#         f"2. Flashcards must be **short, 1–2 sentences max**, so they are easy to read and remember.\n"
#         f"3. Do **NOT** use Q&A format. Just concise statements or bullets.\n"
#         f"4. Each flashcard should be **self-contained**—it should make sense on its own.\n"
#         f"5. Include **all key points** from the text; create as many flashcards as needed.\n"
#         f"6. After each flashcard, add '###' as a separator.\n\n"
#         f"Text:\n{input_text}\n\n"
#         f"Flashcards:\n"
#     )


#     # prompt = (
#     #     f"Read the following text and generate short, summary-style flashcards for all important points. "
#     #     f"Each flashcard should be concise, highlighting a single main idea so that anyone can quickly understand the content. "
#     #     f"Do NOT limit the number of flashcards—create as many as needed to cover all key points. "
#     #     f"Do NOT use Q&A format, just short clear statements. "
#     #     f"Add '###' at the end of each flashcard as a separator.\n\n"
#     #     f"Text:\n{input_text}\n\n"
#     #     f"Flashcards:\n"
#     # )


#     # Call to Gemini API
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=prompt
#     )

#     # Extract generated text
#     flashcard_text = response.text if hasattr(response, "text") else "No flashcards generated."
#   # or check your API response structure

#     # Split flashcards by '###' separator
#     flashcards = [f.strip() for f in flashcard_text.split("###") if f.strip()]

#     # Send to template using context
#     context = {
#         'message': message,
#         'flashcards': flashcards
#     }

#     return render(request, 'base/flashcards.html', context)


# old 
# in views.py


# @login_required(login_url='login')
# @require_POST
# def add_hashtag(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
#     if request.user != message.user:
#         return HttpResponse('You are not allowed to tag this message.')

#     new_tag = request.POST.get('hashtag', '').strip()
#     if not new_tag.startswith('#'):
#         new_tag = f'#{new_tag}'

#     # Append to existing hashtags
#     existing_tags = message.hashtag_list()
#     if new_tag not in existing_tags:
#         existing_tags.append(new_tag)
#         message.hashtags = " ".join(existing_tags)
#         message.save()

#     return redirect('room', pk=message.room.id)

@login_required(login_url='login')
@require_POST
def add_hashtag(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.user:
        return HttpResponse('You are not allowed to tag this message.')

    # Get user input and clean it
    new_tag = request.POST.get('hashtag', '').strip()

    # ✅ Remove # if user typed it by mistake
    if new_tag.startswith('#'):
        new_tag = new_tag[1:]

    # Append to existing hashtags
    existing_tags = message.hashtag_list()
    if new_tag and new_tag not in existing_tags:
        existing_tags.append(new_tag)
        message.hashtags = " ".join(existing_tags)
        message.save()

    return redirect('room', pk=message.room.id)



# @login_required(login_url='login')
# def edit_message_hashtags(request, pk):
#     message = get_object_or_404(Message, id=pk)

#     # Only the message owner can edit
#     if request.user != message.user:
#         return HttpResponse("You are not allowed to edit this message!")

#     if request.method == "POST":
#         new_hashtags = request.POST.get("hashtags", "")
#         message.hashtags = new_hashtags
#         message.save()
#         return redirect('room', pk=message.room.id)

#     return render(request, "base\edit_hashtags.html", {"message": message})
@login_required(login_url='login')
def edit_message_hashtags(request, pk):
    message = get_object_or_404(Message, id=pk)

    # Only the message owner can edit
    if request.user != message.user:
        return HttpResponse("You are not allowed to edit this message!")

    if request.method == "POST":
        new_hashtags = request.POST.get("hashtags", "")
        message.hashtags = new_hashtags
        message.save()
        return redirect('room', pk=message.room.id)

    return render(request, "base/edit_hashtags.html", {"message": message})




