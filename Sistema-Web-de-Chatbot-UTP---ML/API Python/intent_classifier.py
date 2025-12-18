# intent_classifier.py
from sklearn.feature_extraction.text import TfidfVectorizer # NECESARIO
from sklearn.naive_bayes import MultinomialNB # NECESARIO
from sklearn.svm import LinearSVC # Si decides usar SVM
from sklearn.model_selection import train_test_split # NECESARIO

from data_processing import df, preprocess_text # NECESARIO: importa el df y la función de preprocesamiento

intent_classifier = None
tfidf_vectorizer = None

if df is not None:
    X = df['Consulta_Processed']
    y = df['Tipo_Consulta']

    if y.nunique() > 1 and min(y.value_counts()) >= 2:
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    else:
        print("Advertencia (intent_classifier.py): No hay suficientes muestras por clase para estratificar. Dividiendo sin estratificación.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

    intent_classifier = MultinomialNB()
    intent_classifier.fit(X_train_tfidf, y_train)

    print("Clasificador de intenciones entrenado (o listo para cargar) en intent_classifier.py.")
else:
    print("No se pudo entrenar el clasificador en intent_classifier.py debido a un error de carga de datos.")

def classify_intent(query):
    if intent_classifier is None or tfidf_vectorizer is None:
        return "Error: Modelo de clasificación no cargado o entrenado."
    processed_query = preprocess_text(query) # Usa la función de preprocesamiento importada
    query_tfidf = tfidf_vectorizer.transform([processed_query])
    prediction = intent_classifier.predict(query_tfidf)[0]
    return prediction