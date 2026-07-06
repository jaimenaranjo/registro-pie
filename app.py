import streamlit as st
import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from config import LIBROS_REGISTRO

# 1. SETUP: Conexión a Google Docs
SCOPES = ['https://www.googleapis.com/auth/documents']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)

# 2. DATA: El Horario que extrajimos de tus fotos (El mapa de tu día)
HORARIO = {
    "Lunes": {
        "08:00": {"curso": "7B", "estudiante": "Edgar SANCHEZ"},
        "08:45": {"curso": "7B", "estudiante": "Esteban JIMENEZ / Hannibal DROGUETT"},
        "09:45": {"curso": "PKB", "estudiante": "Matías Edme"},
    },
    # ... aquí completarías los demás días según tu horario ...
}

# 3. LÓGICA: Escritura automática en Google Doc
def escribir_en_doc(curso, estudiante, actividad):
    doc_id = LIBROS_REGISTRO.get(curso)
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    texto = f"\n[REGISTRO PIE - {fecha}]\nEstudiante: {estudiante}\nActividad: {actividad}\n"
    
    body = {'requests': [{'insertText': {'text': texto, 'endOfSegmentLocation': {'segmentId': ''}}}]}
    service.documents().batchUpdate(documentId=doc_id, body=body).execute()

# 4. INTERFAZ: El Calendario Interactivo
st.title("📅 Calendario Inteligente PIE")

dia = st.selectbox("Día", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
hora = st.selectbox("Hora", ["08:00", "08:45", "09:45", "10:30", "12:15"])

# Lógica del Calendario: Busca automáticamente en el horario
if dia in HORARIO and hora in HORARIO[dia]:
    datos = HORARIO[dia][hora]
    st.info(f"Curso: {datos['curso']} | Estudiante: {datos['estudiante']}")
    
    # Cuadrícula de Acciones (Disparador de Descripción)
    col1, col2 = st.columns(2)
    asist = col1.checkbox("Asistencia")
    eval = col2.checkbox("Evaluación")
    
    # Descripción automática
    desc_auto = f"Atención {datos['curso']}. "
    if asist: desc_auto += "Asistencia presente. "
    if eval: desc_auto += "Realizó evaluación. "
    
    actividad = st.text_area("Descripción final", value=desc_auto)
    
    if st.button("Guardar en Libro de Registro"):
        escribir_en_doc(datos['curso'], datos['estudiante'], actividad)
        st.success("¡Registro enviado con éxito!")
else:
    st.warning("No hay registros programados en este horario.")
