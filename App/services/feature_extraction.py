import librosa
import numpy as np
from App.config import N_MFCC
from App.core.logger import logger

def extract_features(audio, sr):
    try:
        # MFCC
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)

        # Chroma
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        # Spectral contrast
        spec_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
        spec_mean = np.mean(spec_contrast, axis=1)

        features = np.concatenate([mfcc_mean, mfcc_std, chroma_mean, spec_mean])
        logger.info(f"Extracted features of shape {features.shape}")
        return features
    except Exception as e:
        logger.error(f"Feature extraction failed: {e}")
        raise