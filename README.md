# **Connexta – AI-Powered University Collaboration & Chat Platform**

Connexta is a Django-based real-time academic collaboration platform designed to bring structured digital communication to universities. It replaces unorganized WhatsApp/Telegram groups with subject-wise rooms, centralized announcements, file sharing, and AI-powered learning assistance. The system integrates the Google Gemini API to provide doubt-solving, OCR document understanding, and automatic flashcard generation.

This project was built as a final-year submission and includes complete documentation, deployment instructions, and environment variable configuration.

---

# 📘 **Table of Contents**
- [Features](#-features)
- [System Architecture](#️-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Local Development Setup](#-local-development-setup)
- [Render Deployment Guide](#-render-deployment-guide)
- [Environment Variables](#-environment-variables-descriptions-only)
- [Security Measures](#-security-measures)
- [License](#-license)
- [Final-Year Submission Notes](#-final-year-submission-notes)

---

# 🚀 **Features**

### 🧩 **Communication & Collaboration**
- Subject-wise rooms, study groups, private spaces  
- Real-time chat with edit/delete  
- Message search, filters, hashtags (`#topic`)  
- Activity logs, room-wise analytics  

### 📂 **File Sharing & Storage**
- Upload PDFs, images, notes  
- Preview & download documents  
- Supabase Storage integration  
- File validation & size/type checks  

### 🤖 **AI-Powered Academic Tools**  
Powered by **Google Gemini API**

- AI doubt solving inside chatrooms  
- Smart conversation suggestions  
- PDF/OCR content extraction  
- Auto-flashcard generation  
- Flashcard study tool built-in  

### 📢 **Announcements & Events**
- Centralized announcement dashboard  
- Event details with date filters  
- School/department-level filtering  

### 🔐 **Authentication & User Roles**
- Student, Faculty, Staff roles  
- Password reset + validations  
- Avatar/profile system  
- Access control for rooms, events  

### ⚡ **Performance & UI**
- Lazy loading + optimized ORM  
- Responsive design (mobile-first)  
- AJAX partial updates  
- Basic PWA (app-like behavior)  

---

# 🏗️ **System Architecture**

### **Frontend**
- Django Templates  
- HTML, CSS, JavaScript  
- AJAX-based updates  

### **Backend**
- Django (Python)  
- Google Gemini API for AI features  
- Supabase PostgreSQL Database  
- Supabase Storage Buckets  

### **Hosting**
- Render Web Service (Backend)  
- Supabase (DB + Storage)  

---

# 💻 **Tech Stack**

- **Backend:** Django, Python  
- **Database:** PostgreSQL (Supabase)  
- **Storage:** Supabase Buckets  
- **AI Model:** Google Gemini API  
- **Frontend:** HTML, CSS, JS, AJAX  
- **Deployment:** Render + Gunicorn  

---

# 📁 **Project Structure**

Your project is inside the folder **`StudyBud-master/`**  
(Your Render settings also use this as the root directory.)

```
ChatRoom/
│── StudyBud-master/
│   ├── base/
│   ├── static/
│   ├── studybud/
│   ├── templates/
│   ├── theme/
│   ├── db.sqlite3
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│
└── (other repo files)
```

---

# 🔧 **Local Development Setup**

### **1️⃣ Clone your repository**

```
git clone https://github.com/ranshull/ChatRoom
cd ChatRoom/StudyBud-master
```

### **2️⃣ Create a virtual environment**

```
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### **3️⃣ Install dependencies**

```
pip install -r requirements.txt
```

### **4️⃣ Create a `.env` file in `StudyBud-master/`**

```
API_KEY=
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_URL=
DB_POOL_MODE=
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_BUCKET=
```

> ⚠️ Do **NOT** commit `.env` to GitHub.

### **5️⃣ Apply migrations**

```
python manage.py migrate
```

### **6️⃣ Start development server**

```
python manage.py runserver
```

---

# 🚀 **Render Deployment Guide**

This section matches the deployment configuration described for Render.

### **1️⃣ Create a New Web Service on Render**

- Select Public GitHub Repo:  
  `https://github.com/ranshull/ChatRoom`
- Root Directory:  
  `StudyBud-master`

### **2️⃣ Build Command**

```
pip install -r requirements.txt && python manage.py collectstatic --no-input
```

This will:

- Install all dependencies  
- Collect all static files  

### **3️⃣ Start Command**

```
python manage.py runserver 0.0.0.0:8000
```

### **4️⃣ Add Environment Variables**

In Render → Environment:

```
API_KEY=
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_URL=
DB_POOL_MODE=
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_BUCKET=
```

### **5️⃣ Database Setup**

Using Supabase PostgreSQL in `settings.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv("DB_HOST"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'PORT': os.getenv("DB_PORT"),
    }
}
```

Use `DB_URL` only if required by external tools or pooling libraries.

### **6️⃣ Static Files Configuration**

```
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### **7️⃣ Media Storage**

All user-uploaded media is handled through:

- Supabase Storage  
- Secure public URLs  
- Bucket name: `media` (or value from `SUPABASE_BUCKET`)  

### **8️⃣ Deployment**

Once environment variables are set:

- Save configuration  
- Let Render build and deploy  
- Access your live Connexta instance via the Render URL  

---

# 🔐 **Environment Variables (Descriptions Only)**

| Variable         | Description                                                            |
|-----------------|------------------------------------------------------------------------|
| `API_KEY`       | Gemini API key used for AI features (doubt solving, OCR, flashcards). |
| `DB_HOST`       | Supabase PostgreSQL database host.                                     |
| `DB_NAME`       | Database name.                                                         |
| `DB_USER`       | PostgreSQL username.                                                   |
| `DB_PASSWORD`   | Database password.                                                     |
| `DB_PORT`       | Database port .                                          |
| `DB_URL`        | Full PostgreSQL connection URL (optional).                             |
| `DB_POOL_MODE`  | Connection pooling mode .                             |
| `SUPABASE_URL`  | Base URL of Supabase project.                                          |
| `SUPABASE_KEY`  | Supabase API/service key.                                              |
| `SUPABASE_BUCKET` | Storage bucket name (e.g., `media`).                                |

> ⚠️ Never commit environment variable values.

---

# 🛡️ **Security Measures**

- CSRF protection enabled  
- XSS sanitization via Django templating and validation  
- Django ORM usage to prevent SQL Injection  
- File upload validation (type, size, and path sanitization)  
- Supabase public/signed URLs for media access  
- Strong password rules and auth validations  
- Basic rate limiting on AI-related endpoints (recommended in views/middleware)  

---

# 📜 **License**

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it with proper attribution.

