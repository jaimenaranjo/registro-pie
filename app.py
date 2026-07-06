import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import datetime
from config import LIBROS_REGISTRO, LISTA_CURSOS

# Configuración de API
SCOPES = ['https://www.googleapis.com/auth/documents']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)

def registrar(curso, estudiante, actividad):
    doc_id = LIBROS_REGISTRO.get(curso)
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Formato profesional para el Libro de Registro
    texto = f"\n--- REGISTRO PIE: {fecha} ---\nEstudiante: {estudiante}\nActividad: {actividad}\n"
    
    requests = [{'insertText': {'text': texto, 'endOfSegmentLocation': {'segmentId': ''}}}]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

# --- INTERFAZ INTELIGENTE ---
st.title("🗂️ Registro PIE Móvil")

# Selector de curso
curso = st.selectbox("Selecciona el Curso", LISTA_CURSOS)

# Campo de Estudiante (puedes escribir o seleccionar de tu lista real)
estudiante = st.text_input("Nombre del Estudiante")

# Cuadrícula de acciones rápidas (Esto es lo que pediste)
st.write("Acciones:")
col1, col2 = st.columns(2)
with col1:
    asistencia = st.checkbox("Asistencia")
with col2:
    evaluacion = st.checkbox("Evaluación")

# Descripción dinámica
desc_base = "Asistencia confirmada. " if asistencia else ""
desc_base += "Se realizó evaluación formal. " if evaluacion else ""
actividad = st.text_area("Descripción detallada", value=desc_base)

if st.button("✅ Guardar Registro"):
    if estudiante and actividad:
        registrar(curso, estudiante, actividad)
        st.success(f"Guardado en {curso}")
    else:
        st.error("Por favor completa estudiante y actividad.")
