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
    msg['From'] = "TU_CORREO_PERSONAL@gmail.com" # Tu cuenta de origen
    msg['To'] = "TU_MAIL_INSTITUCIONAL@ebss.cl"  # Tu cuenta de destino
    
    try:
        # Conexión al servidor de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # IMPORTANTE: Aquí va tu contraseña de aplicación (NO tu clave normal)
            smtp.login("TU_CORREO_PERSONAL@gmail.com", "TU_CONTRASEÑA_DE_APLICACION")
            smtp.send_message(msg)
        st.success("¡Registro enviado al correo institucional!")
    except Exception as e:
        st.error(f"Error: {e}")