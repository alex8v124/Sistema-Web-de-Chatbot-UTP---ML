# rag_system.py
from sklearn.feature_extraction.text import TfidfVectorizer # NECESARIO
from sklearn.metrics.pairwise import cosine_similarity # NECESARIO

from data_processing import df, preprocess_text # NECESARIO: importa el df y la función de preprocesamiento

rag_vectorizer = None
response_vectors = None

if df is not None and 'Respuesta_Processed' in df.columns:
    rag_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=None)
    response_vectors = rag_vectorizer.fit_transform(df['Respuesta_Processed'])
    print("Vectorizador RAG y vectores de respuesta creados (o listos para cargar) en rag_system.py.")
else:
    print("No se pudo configurar RAG en rag_system.py debido a un error de carga de datos o columna faltante.")

def retrieve_info(query, top_n=3):
    if rag_vectorizer is None or response_vectors is None:
         return [{"Respuesta_Relevante": "Error: Sistema de recuperación no configurado.", "Similitud": 0.0}]

    processed_query = preprocess_text(query) # Usa la función de preprocesamiento importada
    query_vector = rag_vectorizer.transform([processed_query])

    similarities = cosine_similarity(query_vector, response_vectors).flatten()

    top_indices = similarities.argsort()[-min(top_n, len(df)):][::-1]

    retrieved_data = []
    for i in top_indices:
        retrieved_data.append({
            'Respuesta_Relevante': df.loc[i, 'Respuesta_SAE'],
            'Similitud': float(similarities[i])
        })
    return retrieved_data