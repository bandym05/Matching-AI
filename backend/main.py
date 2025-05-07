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

@app.post("/extract-text")
async def extract_text(id_image: UploadFile = File(...)):
    try:
        img_bytes = await id_image.read()
        np_img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            return {"success": False, "message": "Could not decode image"}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)

        print("Extracted text:")
        print(text)

        extracted = {
            "name": None,
            "id_number": None,
            "dob": None,
            "nationality": None,
            "raw_text": text.strip()
        }

        # Simple regex patterns
        import re
        name_match = re.search(r"Name[:\-]?\s*([A-Za-z\s]+)", text, re.IGNORECASE)
        id_match = re.search(r"ID(?: Number)?:?\s*(\d{6,})", text, re.IGNORECASE)
        dob_match = re.search(r"(?:DOB|Date of Birth)[:\-]?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text)
        nationality_match = re.search(r"Nationality[:\-]?\s*([A-Za-z]+)", text, re.IGNORECASE)

        if name_match:
            extracted["name"] = name_match.group(1).strip()
        if id_match:
            extracted["id_number"] = id_match.group(1).strip()
        if dob_match:
            extracted["dob"] = dob_match.group(1).strip()
        if nationality_match:
            extracted["nationality"] = nationality_match.group(1).strip()

        return {"success": True, "data": extracted}

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return {"success": False, "message": f"Error: {str(e)}"}

