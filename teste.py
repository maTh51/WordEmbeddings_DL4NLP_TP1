import pandas as pd
import numpy as np

def load_vectors(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        # Lê a primeira linha (tamanho do vocabulário e dimensão do embedding)
        vocab_size, layer1_size = map(int, f.readline().strip().split())
        
        # Cria um dicionário para armazenar os embeddings
        embeddings = {}

        for line in f:
            # Divide cada linha em palavra e seus valores
            values = line.strip().split()
            word = values[0]
            vector = np.array(list(map(float, values[1:])))
            embeddings[word] = vector

    return embeddings

# Carregando o arquivo
file_path = "vectors.txt"  # Substitua pelo caminho do seu arquivo
embeddings = load_vectors(file_path)

# Exemplo de uso
print(f"Vetor da palavra 'were': {embeddings['were']}")
print(f"Dimensão do vetor: {len(embeddings['were'])}")
