# imports.py
import pandas as pd # Se usa para manejar DataFrames, aunque aquí solo por consistencia si fuera necesario
import re # Se usa para expresiones regulares, puede ser usado en preprocesamiento
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer # Solo si se usan aquí directamente, sino en intent_classifier/rag_system
from sklearn.naive_bayes import MultinomialNB # Solo si se usan aquí directamente
from sklearn.svm import LinearSVC # Solo si se usan aquí directamente
from sklearn.metrics.pairwise import cosine_similarity # Solo si se usan aquí directamente
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import openpyxl # Solo si se usa aquí para cargar algo, sino en data_processing

# Descargar léxicos/modelos (ejecutar una vez)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
     nltk.download('vader_lexicon')

try:
    nlp = spacy.load("es_core_news_sm")
    print("Modelo 'es_core_news_sm' de spaCy cargado.")
except Exception as e:
    print(f"Error al cargar el modelo 'es_core_news_sm' de spaCy: {e}")
    print("Por favor, ejecuta 'python -m spacy download es_core_news_sm' en tu entorno si es necesario.")
    nlp = None # Asegurarse de que nlp sea None si falla la carga

try:
    analyzer = SentimentIntensityAnalyzer()
    print("VADER SentimentIntensityAnalyzer inicializado.")
except Exception as e:
    print(f"Error al inicializar VADER: {e}")
    analyzer = None

print("Importaciones y cargas iniciales de 'imports.py' completadas.")