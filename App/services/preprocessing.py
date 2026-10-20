import librosa
import numpy as np
from App.config import SAMPLE_RATE, TOP_DB_TRIM
from App.core.logger import logger

def load_audio(file, target_sr=SAMPLE_RATE):
    try:
        audio, sr = librosa.load(file, sr=target_sr)
        logger.info(f"Loaded audio (sr={sr})")
        audio = remove_silence(audio)
        audio = normalize_audio(audio)
        return audio, target_sr
    except Exception as e:
        logger.error(f"Failed to load audio: {e}")
        raise

def remove_silence(audio, top_db=TOP_DB_TRIM):
    trimmed_audio, _ = librosa.effects.trim(audio, top_db=top_db)
    logger.info(f"Trimmed silence: {len(audio)} -> {len(trimmed_audio)} samples")
    return trimmed_audio

def normalize_audio(audio):
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))
    return audio