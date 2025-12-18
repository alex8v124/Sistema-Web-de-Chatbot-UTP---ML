# sentiment_analysis.py
import pandas as pd
# from nltk.sentiment.vader import SentimentIntensityAnalyzer # Ya no se importa aquí, se usa el de imports
from textblob import TextBlob

from imports import analyzer # Importamos el analyzer ya inicializado

# Función para analizar sentimiento con VADER
def analyze_sentiment_vader(text):
    if analyzer is None or pd.isna(text):
        print("DEBUG (VADER): Analyzer is None or text is NaN. Returning Neutral.") # Debug
        return 'Neutral'
    try:
        vs = analyzer.polarity_scores(text)
        if vs['compound'] >= 0.05:
            return 'Positivo'
        elif vs['compound'] <= -0.05:
            return 'Negativo'
        else:
            return 'Neutral'
    except Exception as e:
        print(f"ERROR (VADER): Falló analyze_sentiment_vader para '{text}' con: {e}")
        return "Error de procesamiento VADER" # Retorna un string en caso de error

# Función para analizar sentimiento con TextBlob (en español)
def analyze_sentiment_textblob(text):
    if pd.isna(text):
        print("DEBUG (TextBlob): Text is NaN. Returning Neutral.") # Debug
        return 'Neutral'
    try:
        blob = TextBlob(text)
        if blob.polarity > 0.1:
            return 'Positivo'
        elif blob.polarity < -0.1:
            return 'Negativo'
        else:
            return 'Neutral'
    except Exception as e:
        print(f"ERROR (TextBlob): Falló analyze_sentiment_textblob para '{text}' con: {e}")
        return "Error de procesamiento TextBlob" # Retorna un string en caso de error