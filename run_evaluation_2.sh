#!/bin/bash

START_TIME=$(date +%s)

# Parâmetros a serem variáveis
CBOW_VALUES=(0 1)
SIZE_VALUES=(25 50 75 100)
WINDOW_VALUES=(1 2 3 4 5)
ITER_VALUES=(1 3 5 7 10)

# Arquivo de saída para os resultados
RESULTS_CSV="model_results_2_conta_certa.csv"
TIME_LOG="execution_time.txt"

# Verifica se o arquivo de resultados já existe
if [ ! -f "$RESULTS_CSV" ]; then
  echo "cbow,size,window,iter,mean_distance,time" >"$RESULTS_CSV"
fi

# Baixa o dataset se necessário
if [ ! -e text8 ]; then
  wget http://mattmahoney.net/dc/text8.zip -O text8.gz
  gzip -d text8.gz -f
fi

# Itera sobre todas as combinações de parâmetros
for CBOW in "${CBOW_VALUES[@]}"; do
  for SIZE in "${SIZE_VALUES[@]}"; do
    for WINDOW in "${WINDOW_VALUES[@]}"; do
      for ITER in "${ITER_VALUES[@]}"; do

        # Define o nome do arquivo de saída para o modelo
        MODEL_FILE="vectors.txt"

        # Treina o modelo
        echo "Treinando modelo: cbow=$CBOW, size=$SIZE, window=$WINDOW, iter=$ITER"
        ./word2vec -train text8 -output "$MODEL_FILE" -cbow "$CBOW" -size "$SIZE" -window "$WINDOW" -threads 16 -binary 0 -iter "$ITER"

        # Chama o script Python para avaliar o modelo e salvar o resultado
        echo "Avaliando modelo..."
        MEAN_DISTANCE=$(python3 compute_mean_dist.py "$MODEL_FILE" questions-words.txt)

        # Salva os resultados no CSV
        echo "$CBOW,$SIZE,$WINDOW,$ITER,$MEAN_DISTANCE" >>"$RESULTS_CSV"
        echo "Resultado salvo no CSV: $MEAN_DISTANCE"

        # Remove o arquivo do modelo para liberar espaço
        rm -f "$MODEL_FILE"

      done
    done
  done
done

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
echo "Tempo total de execução: $TOTAL_TIME segundos" > "$TIME_LOG"
