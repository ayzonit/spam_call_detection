from fastapi import APIRouter, UploadFile, Form, HTTPException
from App.services import preprocessing, feature_extraction, inference
from App.models.model_loader import load_models
from App.utils import save_embedding, load_embedding

router = APIRouter()
speaker_model, spoof_model = load_models()


@router.post("/enroll")
async def enroll_user(user_id: str = Form(...), file: UploadFile = None):
    if not file:
        raise HTTPException(status_code=400, detail="No voice file provided")
    
    try:
        audio, sr = preprocessing.load_audio(file.file)
        feats = feature_extraction.extract_features(audio, sr)
        embedding = inference.extract_embedding(feats, speaker_model)
        save_embedding(user_id, embedding)
        return {"message": f"User '{user_id}' enrolled successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enrollment failed: {str(e)}")


@router.post("/verify")
async def verify_user(user_id: str = Form(...), file: UploadFile = None):
    if not file:
        raise HTTPException(status_code=400, detail="No voice file provided")
    
    try:
        audio, sr = preprocessing.load_audio(file.file)
        feats = feature_extraction.extract_features(audio, sr)
        stored_emb = load_embedding(user_id)
        
        if stored_emb is None:
            raise HTTPException(status_code=404, detail=f"User '{user_id}' not enrolled")
        
        result = inference.verify_with_embedding(feats, stored_emb, speaker_model, spoof_model)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")