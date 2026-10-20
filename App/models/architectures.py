import torch
import torch.nn as nn
import torch.nn.functional as F

class SpeakerEmbeddingModel(nn.Module):
    def __init__(self, input_dim=59, embedding_dim=128):
        super(SpeakerEmbeddingModel, self).__init__()
        
        self.fc1 = nn.Linear(input_dim, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.dropout1 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(256, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc3 = nn.Linear(256, 128)
        self.bn3 = nn.BatchNorm1d(128)
        self.dropout3 = nn.Dropout(0.2)
        
        self.fc_embedding = nn.Linear(128, embedding_dim)
        
    def forward(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(0)
            
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)
        
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)
        
        x = F.relu(self.bn3(self.fc3(x)))
        x = self.dropout3(x)
        
        embedding = self.fc_embedding(x)
        embedding = F.normalize(embedding, p=2, dim=1)
        
        return embedding


class SpoofDetectionModel(nn.Module):
    def __init__(self, input_dim=59):
        super(SpoofDetectionModel, self).__init__()
        
        self.fc1 = nn.Linear(input_dim, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.dropout1 = nn.Dropout(0.4)
        
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.dropout2 = nn.Dropout(0.3)
        
        self.fc3 = nn.Linear(128, 64)
        self.bn3 = nn.BatchNorm1d(64)
        self.dropout3 = nn.Dropout(0.2)
        
        self.fc_out = nn.Linear(64, 1)
        
    def forward(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(0)
            
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)
        
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)
        
        x = F.relu(self.bn3(self.fc3(x)))
        x = self.dropout3(x)
        
        logits = self.fc_out(x)
        
        return logits