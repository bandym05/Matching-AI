from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from face_matcher import match_faces

app = FastAPI()

# Allow frontend (Streamlit) access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compare")
async def compare_faces(id_image: UploadFile = File(...), selfie_image: UploadFile = File(...)):
    id_bytes = await id_image.read()
    selfie_bytes = await selfie_image.read()
    
    score, error = match_faces(id_bytes, selfie_bytes)
    if error:
        return {"success": False, "message": error}
    
    return {
        "success": True,
        "confidence": score,
        "match": score > 0.6  # You can adjust threshold
    }
