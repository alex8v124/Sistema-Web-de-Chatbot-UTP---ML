# main.py - Lógica de la API con FastAPI

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

# --- IMPORTAR LÓGICA DE OTROS MÓDULOS (.py) ---
# Importaciones de tus módulos locales
from imports import nlp, analyzer # nlp y analyzer son cargados/inicializados en imports.py
from data_processing import df, preprocess_text # df y preprocess_text vienen de data_processing.py
from intent_classifier import classify_intent # classify_intent viene de intent_classifier.py
from rag_system import retrieve_info # retrieve_info viene de rag_system.py
from ner_system import detect_entities # detect_entities viene de ner_system.py
from sentiment_analysis import analyze_sentiment_vader, analyze_sentiment_textblob

# --- Inicializar FastAPI ---
app = FastAPI()

# --- Definir modelos de datos para las solicitudes/respuestas ---
class QueryRequest(BaseModel):
    query: str

class IntentResponse(BaseModel):
    intent: str

class RAGResponse(BaseModel):
    results: list

class NERResponse(BaseModel):
    entities: dict

class SentimentResponse(BaseModel):
    vader_sentiment: str
    textblob_sentiment: str

# --- Endpoints de la API ---

@app.get("/")
async def read_root():
    return {"message": "API de Análisis de Consultas UTP"}

@app.post("/classify-intent", response_model=IntentResponse)
async def classify(request: QueryRequest):
    # Ya no necesitas los 'in globals()' si sabes que los módulos están bien importados
    # Pero no hace daño dejarlos si quieres robustez extra en tiempo de ejecución.
    # En un setup robusto, estos errores se capturarían al importar.
    if callable(classify_intent):
        intent = classify_intent(request.query)
        return {"intent": intent}
    else:
        return {"intent": "Error: Función de clasificación no encontrada."}

@app.post("/retrieve-info", response_model=RAGResponse)
async def rag(request: QueryRequest):
    if callable(retrieve_info):
        relevant_info = retrieve_info(request.query)
        return {"results": relevant_info}
    else:
        return {"results": [{"Respuesta_Relevante": "Error: Función de RAG no encontrada.", "Similitud": 0.0}]}

@app.post("/detect-entities", response_model=NERResponse)
async def ner(request: QueryRequest):
    # Asegurarse de que la función detect_entities esté definida
    if callable(detect_entities):
        # AQUÍ ES DONDE PASAMOS EL OBJETO NLP GLOBAL
        entities = detect_entities(request.query, nlp) # <--- MODIFICACIÓN CLAVE
        return {"entities": entities}
    else:
        return {"entities": {"error": "Función de detección de entidades no encontrada."}}

@app.post("/analyze-sentiment", response_model=SentimentResponse)
async def sentiment(request: QueryRequest):
    # Inicializa con valores predeterminados para que siempre devuelva algo
    vader_sentiment_result = "N/A"
    textblob_sentiment_result = "N/A"

    try:
        if callable(analyze_sentiment_vader):
            vader_sentiment_result = analyze_sentiment_vader(request.query)
        else:
            print("WARNING: analyze_sentiment_vader not callable.")
            vader_sentiment_result = "Función VADER no encontrada."

        if callable(analyze_sentiment_textblob):
            textblob_sentiment_result = analyze_sentiment_textblob(request.query)
        else:
            print("WARNING: analyze_sentiment_textblob not callable.")
            textblob_sentiment_result = "Función TextBlob no encontrada."

    except Exception as e:
        # Captura cualquier error inesperado en este nivel antes de que se convierta en 500
        print(f"CRITICAL ERROR in /analyze-sentiment endpoint: {e}")
        # Retornar un 500 si esto es un error grave que quieres propagar
        # O manejarlo de forma más elegante si quieres que la API siempre responda 200
        # raise HTTPException(status_code=500, detail=f"Error en el análisis de sentimiento: {e}")
        vader_sentiment_result = f"Error general: {e}"
        textblob_sentiment_result = f"Error general: {e}"

    return {"vader_sentiment": vader_sentiment_result, "textblob_sentiment": textblob_sentiment_result}

# --- Cómo ejecutar la API ---
# Nota: Este bloque solo se ejecuta si corres main.py directamente (python main.py),
# no cuando Uvicorn lo carga (uvicorn main:app --reload).
# Sin embargo, la lógica de importación y carga de modelos sí se ejecuta cuando Uvicorn lo carga.
try:
    import nest_asyncio
    nest_asyncio.apply()
    print("Iniciando servidor Uvicorn...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
except Exception as e:
    print(f"No se pudo iniciar el servidor Uvicorn desde el notebook: {e}")
    # print("Considera guardar este código en un archivo main.py y ejecutarlo desde la terminal.")

print("API de FastAPI definida. Para ejecutarla, guarda este código en 'main.py' y usa 'uvicorn main:app --reload' en la terminal.")