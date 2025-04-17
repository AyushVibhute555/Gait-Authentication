import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_dataset(csv_path='features.csv'):
    df = pd.read_csv(csv_path, header=None)
    labels = df.iloc[:, 0]
    features = df.iloc[:, 1:]
    return labels, features

def match_user(features, dataset_labels, dataset_features, threshold=0.85):
    sims = cosine_similarity([features], dataset_features)[0]
    best_idx = np.argmax(sims)
    best_score = sims[best_idx]
    if best_score >= threshold:
        return dataset_labels[best_idx], best_score
    else:
        return "Unknown", best_score
