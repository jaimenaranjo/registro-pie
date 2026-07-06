import streamlit as st
import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from config import LIBROS_REGISTRO
from horario_data import HORARIO # Importamos el horario desde el nuevo archivo

# Configuración API
SCOPES = ['https://www.googleapis.com/auth/documents']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
service = build('docs', 'v1', credentials=creds)

def registrar_en_doc(curso, estudiante, actividad):
    doc_id = LIBROS_REGISTRO.get(curso)
    fecha = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    texto = f"\n--- REGISTRO PIE | {fecha} ---\nEstudiante: {estudiante}\nActividad: {actividad}\n"
    
    body = {'requests': [{'insertText': {'text': texto, 'endOfSegmentLocation': {'segmentId': ''}}}]}
    service.documents().batchUpdate(documentId=doc_id, body=body).execute()

# Interfaz Principal
st.title("🗂️ Centro de Control PIE")
dia = st.selectbox("Día", list(HORARIO.keys()))
hora = st.selectbox("Hora", list(HORARIO[dia].keys()))

datos = HORARIO[dia][hora]
st.info(f"Estudiante: {datos['estudiante']} | Curso: {datos['curso']}")

# Acciones Rápidas
col1, col2 = st.columns(2)
asist = col1.checkbox("Asistencia")
eval = col2.checkbox("Evaluación")

# Descripción automática
desc = f"Atención {datos['curso']}. "
if asist: desc += "Asistencia presente. "
if eval: desc += "Realizó evaluación. "
actividad = st.text_area("Descripción final", value=desc)

if st.button("✅ Registrar en Libro"):
    registrar_en_doc(datos['curso'], datos['estudiante'], actividad)
    st.success(f"Registro guardado en libro de {datos['curso']}")
