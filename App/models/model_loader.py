import torch
import os
from App.models.architectures import SpeakerEmbeddingModel, SpoofDetectionModel
from App.config import SPEAKER_MODEL_PATH, SPOOF_MODEL_PATH
from App.core.logger import logger

def load_models():
    try:
        speaker_model = SpeakerEmbeddingModel(input_dim=59, embedding_dim=128)
        spoof_model = SpoofDetectionModel(input_dim=59)
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(SPEAKER_MODEL_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(SPOOF_MODEL_PATH), exist_ok=True)
        
        if os.path.exists(SPEAKER_MODEL_PATH):
            try:
                speaker_model.load_state_dict(torch.load(SPEAKER_MODEL_PATH, map_location='cpu'))
                logger.info(f"Loaded speaker model from {SPEAKER_MODEL_PATH}")
            except Exception as e:
                logger.warning(f"Failed to load speaker model: {e}. Using untrained model.")
        else:
            logger.warning(f"Speaker model not found at {SPEAKER_MODEL_PATH}. Using untrained model.")
            
        if os.path.exists(SPOOF_MODEL_PATH):
            try:
                spoof_model.load_state_dict(torch.load(SPOOF_MODEL_PATH, map_location='cpu'))
                logger.info(f"Loaded spoof model from {SPOOF_MODEL_PATH}")
            except Exception as e:
                logger.warning(f"Failed to load spoof model: {e}. Using untrained model.")
        else:
            logger.warning(f"Spoof model not found at {SPOOF_MODEL_PATH}. Using untrained model.")
        
        speaker_model.eval()
        spoof_model.eval()
        
        logger.info("Models loaded successfully (untrained models will be used for demo)")
        return speaker_model, spoof_model
        
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise