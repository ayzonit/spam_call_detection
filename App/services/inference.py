import torch
import numpy as np
from App.config import THRESHOLD_SPEAKER, THRESHOLD_SPOOF
from App.core.logger import logger

def extract_embedding(features, speaker_model):
    try:
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            emb = speaker_model(x).squeeze().numpy()
        logger.info(f"Generated embedding of shape {emb.shape}")
        return emb
    except Exception as e:
        logger.error(f"Failed to extract embedding: {e}")
        raise


def verify_with_embedding(features, stored_emb, speaker_model, spoof_model):
    try:
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            current_emb = speaker_model(x).squeeze().numpy()
            spoof_logits = spoof_model(x).squeeze()
            spoof_prob = torch.sigmoid(spoof_logits).item()

        cos_sim = np.dot(current_emb, stored_emb) / (
            np.linalg.norm(current_emb) * np.linalg.norm(stored_emb)
        )

        if cos_sim >= THRESHOLD_SPEAKER and spoof_prob <= THRESHOLD_SPOOF:
            decision = "ALLOW"
        elif spoof_prob > THRESHOLD_SPOOF:
            decision = "DENY (Spoof Detected)"
        else:
            decision = "DENY (Low Confidence)"

        result = {
            "decision": decision,
            "cosine_similarity": round(float(cos_sim), 3),
            "spoof_probability": round(float(spoof_prob), 3)
        }

        logger.info(f"Verification result: {result}")
        return result

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return {"error": str(e)}