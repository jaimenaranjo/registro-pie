import streamlit as st
import smtplib
from email.message import EmailMessage

st.title("📝 Registro PIE - Envío por Mail")

# Datos básicos
cursos = ["1ro A", "2do B", "3ro C", "4to D"]
estudiantes = ["Esteban JIMENEZ", "Matías LOPEZ", "Vicente Parada", "Hannibal DROGUETTE"]

curso = st.selectbox("Selecciona Curso", cursos)
estudiante = st.selectbox("Estudiante", estudiantes)
lugar = st.radio("Lugar", ["A.R.", "A.C."], horizontal=True)
actividad = st.text_area("Actividad realizada")

if st.button("🚀 Enviar Registro"):
    # Configuración del correo
    msg = EmailMessage()
    msg['Subject'] = f"[REGISTRO-PIE] | {curso} | {estudiante}"
    msg.set_content(f"Curso: {curso}\nEstudiante: {estudiante}\nLugar: {lugar}\nActividad: {actividad}")
    
    # --- TUS DATOS CONFIGURADOS ---
    msg['From'] = "bablopravo@gmail.com" 
    msg['To'] = "pablo.rojas@ebss.cl"
    
    try:
        # Conexión al servidor de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Reemplaza 'TU_CODIGO_DE_16_LETRAS' por tu contraseña de aplicación real
            smtp.login("bablopravo@gmail.com", "ecrilpyxayeoosny")
            smtp.send_message(msg)
        st.success("¡Registro enviado al correo institucional!")
    except Exception as e:
        st.error(f"Error al enviar: {e}")
