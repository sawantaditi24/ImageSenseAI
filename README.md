# Imagesense AI

A generative AI powered web application to organize, search, and categorize images using OCR, LLMs, and semantic search.

---

## Problem Statement

In today’s digital world, students, professionals and job seekers often take countless screenshots of valuable content from platforms like LinkedIn job postings, career advice, learning resources, and networking tips. Over time, these screenshots pile up in device galleries, becoming disorganized, hard to search, and nearly impossible to categorize or retrieve when needed.

**The problem:**
- Important information (like job posts, learning resources, or job search strategies) gets lost in a sea of uncategorized images.
- Manual organization is tedious and time-consuming.
- Searching for a specific screenshot by topic or semantic is nearly impossible without text recognition and semantic understanding.

**This application solves the problem by:**
- Automatically extracting text from screenshots using OCR.
- Using LLMs to categorize each screenshot (e.g., Job Post, Learning Resource, Job Search Strategy).
- Enabling fast, semantic search so users can find relevant screenshots by meaning, not just keywords.
- Providing a modern, chat-style interface for intuitive searching and organization.

**In short:**
This app transforms a chaotic collection of screenshots into a smart, searchable, and organized knowledge base—empowering users to quickly find and leverage the career content that matters most.

---

## Features
- **Upload LinkedIn screenshots** via a modern React frontend
- **Store images in AWS S3** (original + thumbnail)
- **Extract text from images** using Tesseract OCR
- **Categorize screenshots** with OpenAI GPT-3.5/4
- **Semantic search** using Hugging Face sentence-transformers and FAISS
- **Store metadata** (text, category, S3 key, etc.) in PostgreSQL
- **Chatbot-style search UI** for natural language queries

---

## Architecture
<img width="1536" height="1024" alt="ChatGPT Image Jul 23, 2025, 05_02_24 PM" src="https://github.com/user-attachments/assets/642d82f1-1380-4f6a-941e-e8134f063a5c" />



---

## Image Sense App demo
- **Demo**
You can check the live demo here: https://imagesenseai-1.onrender.com/

- **Landing Page** 
<img width="1708" height="864" alt="Screenshot 2025-07-23 at 4 36 52 PM" src="https://github.com/user-attachments/assets/caabe015-6dae-4615-851e-103f65f7d1e5" />

- **Chat Bar** 
<img width="1026" height="252" alt="search bar" src="https://github.com/user-attachments/assets/694ef253-b717-4be4-8978-063c4bd98a0f" />
<img width="1705" height="679" alt="Screenshot 2025-07-23 at 3 54 35 PM" src="https://github.com/user-attachments/assets/f47b13fd-f589-4ce4-8dfe-2e6b4d7cd826" />
<img width="992" height="624" alt="Screenshot 2025-07-23 at 4 06 47 PM" src="https://github.com/user-attachments/assets/444ec7fd-abc7-4949-950b-56a328085e9f" />

---

## Tech Stack
- **Frontend:** React (TypeScript), Tailwind/CSS
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Storage:** AWS S3
- **OCR:** Tesseract (pytesseract)
- **LLM:** OpenAI GPT-3.5/4
- **Embeddings:** Hugging Face (MiniLM)
- **Semantic Search:** FAISS

---

## Quick Start

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/ai-screenshot-organizer.git
cd ai-screenshot-organizer
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- Set up your `.env` or `app/core/config.py` with AWS, DB, and OpenAI credentials.
- Start the backend:
```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm start
```
- App runs at [http://localhost:3000](http://localhost:3000)

---

## Configuration
- **AWS S3:** Set credentials and bucket in backend config
- **PostgreSQL:** Set DB URL in backend config
- **OpenAI API Key:** Set in backend config
- **Tesseract:** Must be installed on your system

---

## Usage
1. **Upload**: Drag & drop or select screenshots in the web UI
2. **Automatic Processing**: Backend extracts text, categorizes, stores in S3/DB, and indexes for search
3. **Semantic Search**: Use the chat-style search bar to find screenshots by meaning, not just keywords
4. **View Results**: See category and thumbnail, click to view full image

---

## Important Files & Structure
- `backend/app/api/routes/upload.py` — Upload, OCR, categorize, S3, FAISS
- `backend/app/api/routes/search.py` — Semantic search endpoint
- `backend/app/services/s3_service.py` — S3 upload/thumbnail logic
- `backend/app/utils/ocr.py` — OCR logic
- `backend/app/utils/categorize.py` — LLM categorization
- `backend/app/utils/embeddings.py` — Embedding generation
- `backend/app/utils/faiss_index.py` — FAISS index
- `frontend/src/components/ChatSearch.tsx` — Chat search UI
- `frontend/src/components/ScreenshotResult.tsx` — Search result card
- `frontend/src/components/ChatSearch.css` — UI styles

---

## Troubleshooting
- **500 Internal Server Error on upload:** Check image file integrity, backend logs, and S3/DB credentials
- **Images not displaying:** Ensure S3 bucket/object is public or use pre-signed URLs
- **No search results:** Make sure FAISS index is populated (re-upload after backend restart)
- **CORS issues:** Check backend CORS settings

---

## License
MIT

---

## Credits
- [OpenAI](https://openai.com/)
- [Hugging Face](https://huggingface.co/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [React](https://react.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

> Built with ❤️ by Aditi
