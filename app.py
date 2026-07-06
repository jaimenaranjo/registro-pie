import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import datetime
# Importamos tus configuraciones desde el archivo config.py que creamos antes
from config import LIBROS_REGISTRO, LISTA_CURSOS

st.title("📝 Registro PIE - Escritura Directa")

# 1. Configuración de la API de Google Docs
SCOPES = ['https://www.googleapis.com/auth/documents']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)

def registrar_en_doc(curso, estudiante, lugar, actividad):
    doc_id = LIBROS_REGISTRO.get(curso)
    
    # Formato del texto a insertar
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    texto = f"\n--- REGISTRO: {fecha} ---\nEstudiante: {estudiante}\nLugar: {lugar}\nActividad: {actividad}\n"
    
    # Llamada a la API
    requests = [{'insertText': {'text': texto, 'endOfSegmentLocation': {'segmentId': ''}}}]
    service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

# 2. Interfaz de Usuario
curso = st.selectbox("Selecciona Curso", LISTA_CURSOS)
# Aquí podrías cargar tu lista real de estudiantes luego
estudiante = st.text_input("Nombre del Estudiante") 
lugar = st.radio("Lugar", ["A.R.", "A.C."], horizontal=True)
actividad = st.text_area("Actividad realizada")

if st.button("🚀 Guardar en Libro de Registro"):
    if not estudiante or not actividad:
        st.warning("Completa los campos")
    else:
        try:
            registrar_en_doc(curso, estudiante, lugar, actividad)
            st.success(f"¡Registro insertado correctamente en el libro de {curso}!")
        except Exception as e:
            st.error(f"Error al conectar con el documento: {e}")
