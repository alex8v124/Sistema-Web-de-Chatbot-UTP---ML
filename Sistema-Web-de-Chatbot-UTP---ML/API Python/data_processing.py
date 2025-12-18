# data_processing.py
import pandas as pd # NECESARIO: Porque usa pd.read_excel y pd.isna
import re           # NECESARIO: Porque usa re.sub
import os           # NECESARIO: Para construir la ruta del archivo Excel

# Cargar el dataset (adapta la ruta del archivo)
# ¡ADAPTA ESTA RUTA! Asegúrate de que 'Consultas-SAE-20250724.xlsx' esté en la misma carpeta que data_processing.py y main.py
excel_file_path = os.path.join(os.path.dirname(__file__), 'Consultas-SAE-20250724.xlsx')

df = None # Inicializar df para manejar el caso de error de carga

try:
    df = pd.read_excel(excel_file_path)
    print(f"Archivo '{excel_file_path}' cargado exitosamente en data_processing.py.")
except FileNotFoundError:
    print(f"Error: El archivo '{excel_file_path}' no fue encontrado en data_processing.py.")
    print("Asegúrate de que el archivo Excel esté en la ruta especificada.")
    # Considera cargar un DataFrame de ejemplo o manejar este error.
    data_example_large = {
        'ID_Consulta': range(1, 21),
        'Tipo_Consulta': ['Académica', 'Financiera', 'Académica', 'Tecnológica', 'Bienestar',
                          'Académica', 'Financiera', 'Académica', 'Bienestar', 'Tecnológica',
                          'Financiera', 'Académica', 'Académica', 'Tecnológica', 'Bienestar',
                          'Académica', 'Financiera', 'Académica', 'Bienestar', 'Tecnológica'],
        'Consulta': ['¿Cuándo son las matrículas?', 'Necesito pagar la cuota.', 'Quiero convalidar un curso.', 'Mi aula virtual no carga.', 'Apoyo psicológico.',
                      'Fechas de reincorporación.', 'Costo de matrícula.', 'Certificado de estudios.', 'Clubes deportivos.', 'Problemas con el correo.',
                      'Beca de estudios.', 'Reglamento académico.', 'Cambio de carrera.', 'Acceso a la plataforma.', 'Asesoría vocacional.',
                      'Horario de clases.', 'Pagar multa.', 'Inscripción a examen.', 'Servicio médico.', 'Error en sistema.'],
        'Respuesta_SAE': ['Del 15 al 30 de agosto.', 'En el portal de pagos.', 'En Secretaría Académica.', 'Contacta Soporte TI.', 'Agenda cita en Bienestar.',
                          'Del 1 al 10 de agosto.', 'Depende de la carrera.', 'Requiere pagos al día.', 'En área de Deportes.', 'Contacta Soporte TI.',
                          'Oficina de Bienestar.', 'Secretaría Académica.', 'Secretaría Académica.', 'Soporte TI.', 'Bienestar Universitario.',
                          'Consulta en el portal.', 'En Tesorería.', 'En Secretaría Académica.', 'Contacta Bienestar Universitario.', 'Contacta Soporte TI.'],
        'Departamento_SAE': ['Secretaría Académica', 'Tesorería', 'Secretaría Académica', 'Soporte TI', 'Bienestar Universitario',
                             'Secretaría Académica', 'Tesorería', 'Secretaría Académica', 'Bienestar Universitario', 'Soporte TI',
                             'Bienestar Universitario', 'Secretaría Académica', 'Secretaría Académica', 'Soporte TI', 'Bienestar Universitario',
                             'Secretaría Académica', 'Tesorería', 'Secretaría Académica', 'Bienestar Universitario', 'Soporte TI'],
        'Satisfaccion_Cliente': [4, 5, 3, 2, 4, 4, 5, 5, 4, 3, 5, 4, 3, 2, 5, 4, 5, 4, 5, 3],
        'Tiempo_Respuesta_Minutos': [45, 10, 60, 75, 90, 60, 25, 50, 20, 80, 15, 30, 70, 95, 40, 35, 12, 55, 22, 85]
    }
    df = pd.DataFrame(data_example_large)
    print("Usando DataFrame de ejemplo en data_processing.py.")

# Función de preprocesamiento de texto
def preprocess_text(text):
    if pd.isna(text): # Manejar valores NaN
        return ""
    text = str(text).lower() # Convertir a minúsculas y asegurar que sea string
    text = re.sub(r'[^\w\s]', '', text) # Eliminar puntuación
    return text

if df is not None:
    df['Consulta_Processed'] = df['Consulta'].apply(preprocess_text)
    df['Respuesta_Processed'] = df['Respuesta_SAE'].apply(preprocess_text)
    print("Datos preprocesados en data_processing.py.")