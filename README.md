# 🧠 Matching-AI: ID Card vs Selfie Face Matching API

This project provides an API for verifying a person’s identity by comparing a face from an ID card photo with a live selfie or headshot. It uses state-of-the-art deep learning for facial recognition and returns a **confidence score** that indicates how closely the two faces match.

---

## 🚀 Features

- 🔍 **Face Detection**: Automatically detects faces in uploaded images (ID and selfie).
- 🧬 **Face Embedding**: Extracts high-dimensional embeddings using ArcFace (via InsightFace).
- 📐 **Face Matching**: Computes cosine similarity between ID and selfie face embeddings.
- 📊 **Confidence Score**: Returns a similarity score to indicate identity match.
- 🌐 **REST API**: Built with FastAPI for easy integration with mobile or web apps.
- 🧪 **Streamlit Frontend**: Included for testing the model via a simple UI.

---

## 🧱 Tech Stack

| Component         | Tool                                |
|------------------|-------------------------------------|
| API Backend       | FastAPI (Python)                    |
| Face Recognition  | InsightFace + ArcFace               |
| Similarity Metric | Cosine similarity                   |
| Frontend (Test)   | Streamlit                           |
| Deployment        | Docker + Uvicorn (Optional Nginx)   |
| Hosting           | Render, Railway, Fly.io, or VPS     |

## 🔁 How It Works

### 1. **Image Upload**
A user submits two images via a web or mobile interface:
- **ID Image**: A photo of an ID card or document that includes a face.
- **Selfie Image**: A live-captured photo or headshot of the person.

These images are sent to the backend API through a POST request.

---

### 2. **Face Detection and Alignment**
The backend uses the **InsightFace** library to:
- Detect and crop the most prominent face in each image.
- Align the faces properly to normalize for pose and orientation.

---

### 3. **Face Embedding Generation**
Each aligned face is passed through a pre-trained **ArcFace** model (via InsightFace), which converts the face into a high-dimensional **embedding vector** — a numerical representation of facial features.

---

### 4. **Similarity Calculation**
The two embedding vectors (one from the ID photo and one from the selfie) are compared using **cosine similarity**, which measures how close the two vectors are in the embedding space.

- A score close to `1.0` indicates a strong match (same person).
- A score near `0.0` indicates no match (different people).

---

### 5. **Result Output**
The system returns a JSON response with:
- `similarity_score`: A float value between 0 and 1.
- `match`: A boolean (`true` if the similarity score exceeds a preset threshold, e.g. 0.6).

Example:
```json
{
  "similarity_score": 0.84,
  "match": true
}