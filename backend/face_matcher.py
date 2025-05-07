import numpy as np
import cv2
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

# Initialize InsightFace model
face_app = FaceAnalysis(name='buffalo_l')
face_app.prepare(ctx_id=0, det_size=(640, 640))

def get_embedding(image_bytes: bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    faces = face_app.get(img)
    if not faces:
        return None
    return faces[0].embedding

def match_faces(id_bytes: bytes, selfie_bytes: bytes):
    emb_id = get_embedding(id_bytes)
    emb_selfie = get_embedding(selfie_bytes)
    if emb_id is None or emb_selfie is None:
        return None, "Could not detect face in one or both images."
    
    score = cosine_similarity([emb_id], [emb_selfie])[0][0]
    return round(float(score), 4), None
