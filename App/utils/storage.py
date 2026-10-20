import os
import numpy as np
from App.core.logger import logger
from App.config import EMBEDDINGS_DIR

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

def save_embedding(user_id, embedding):
    try:
        file_path = os.path.join(EMBEDDINGS_DIR, f"{user_id}.npy")
        np.save(file_path, embedding)
        logger.info(f"Saved embedding for user '{user_id}' at {file_path}")
    except Exception as e:
        logger.error(f"Failed to save embedding for '{user_id}': {e}")
        raise


def load_embedding(user_id):
    try:
        file_path = os.path.join(EMBEDDINGS_DIR, f"{user_id}.npy")
        if not os.path.exists(file_path):
            logger.warning(f"No embedding found for user '{user_id}'")
            return None
        embedding = np.load(file_path)
        logger.info(f"Loaded embedding for user '{user_id}'")
        return embedding
    except Exception as e:
        logger.error(f"Failed to load embedding for '{user_id}': {e}")
        raise