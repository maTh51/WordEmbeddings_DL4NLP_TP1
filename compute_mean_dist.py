import numpy as np
import sys
from tqdm import tqdm

def load_vectors(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        vocab_size, layer1_size = map(int, f.readline().strip().split())
        embeddings = {}
        for line in f:
            values = line.strip().split()
            word = values[0]
            vector = np.array(list(map(float, values[1:])))
            embeddings[word] = vector
    return embeddings

def cosine_distance(vec1, vec2):
    return 1 - (np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def evaluate_analogy(model_path, analogy_file):
    embeddings = load_vectors(model_path)
    with open(analogy_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    distances = []
    for line in tqdm(lines, desc="Processing analogies"):
        if line.startswith(":") or len(line.strip()) == 0:
            continue

        word1, word2, word3, expected_word = line.strip().split()
        if any(word not in embeddings for word in [word1, word2, word3, expected_word]):
            continue

        vec1 = embeddings[word1]
        vec2 = embeddings[word2]
        vec3 = embeddings[word3]
        expected_vec = embeddings[expected_word]

        result_vec = vec2 - vec1 + vec3
        distance = cosine_distance(result_vec, expected_vec)
        distances.append(distance)

    mean_distance = np.mean(distances)
    return mean_distance

if __name__ == "__main__":
    model_path = sys.argv[1]
    analogy_file = sys.argv[2]
    mean_distance = evaluate_analogy(model_path, analogy_file)
    print(mean_distance)  # Retorna apenas a média
