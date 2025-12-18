# ner_system.py

# Ya no importamos 'nlp' directamente desde imports aquí.
# La función detect_entities lo recibirá como argumento.

def detect_entities(query, nlp_model): # <--- AHORA RECIBE nlp_model como argumento
    # DEBUGGING: Print the object to see its ID
    print(f"DEBUG (detect_entities function): nlp object received in function: {nlp_model}")
    if nlp_model is None: # Usamos nlp_model en lugar de nlp
        return {"error": "Modelo de spaCy no cargado en 'imports.py' o no pasado correctamente."}
    try:
        doc = nlp_model(query) # <--- Usamos nlp_model
    except Exception as e:
        print(f"ERROR (ner_system): Falló nlp_model(query) con: {e}")
        return {"error": f"Error procesando con spaCy: {e}"}

    entities = {}
    for ent in doc.ents:
        # Refina qué tipos de entidades te interesan y cómo nombrarlas
        if ent.label_ == 'DATE':
            if 'fecha' not in entities: entities['fecha'] = []
            entities['fecha'].append(ent.text)
        elif ent.label_ == 'ORG':
            if 'organizacion' not in entities: entities['organizacion'] = []
            entities['organizacion'].append(ent.text)
        elif ent.label_ == 'MISC': # MISC a menudo captura nombres propios o términos específicos
             if 'elemento_clave' not in entities: entities['elemento_clave'] = []
             entities['elemento_clave'].append(ent.text)
    return entities