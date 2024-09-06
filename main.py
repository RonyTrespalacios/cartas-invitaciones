import streamlit as st
from fpdf import FPDF
import base64

# Función para generar el PDF
def generar_pdf(nombre, correo, cedula):
    pdf = FPDF()
    pdf.add_page()

    # Título de la carta
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Carta de Invitación", ln=True, align="C")

    # Espacio
    pdf.ln(10)

    # Cuerpo de la carta
    pdf.set_font("Arial", size=12)
    texto = (f"Estimado/a {nombre},\n\n"
             f"Nos complace invitarle al Torneo de Robótica que se llevará a cabo el 25 de octubre.\n"
             f"Sus datos de registro son los siguientes:\n\n"
             f"Nombre: {nombre}\n"
             f"Correo: {correo}\n"
             f"Cédula: {cedula}\n\n"
             "Esperamos contar con su valiosa participación en este evento, "
             "que reunirá a entusiastas y profesionales de la robótica.\n\n"
             "Saludos cordiales,\n"
             "Comité Organizador del Torneo de Robótica")
    
    pdf.multi_cell(0, 10, txt=texto)

    return pdf

# Función para convertir el PDF a un enlace descargable
def convertir_pdf_a_descargable(pdf):
    pdf.output("invitacion.pdf")
    with open("invitacion.pdf", "rb") as f:
        pdf_data = f.read()
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="invitacion_torneo_robotica.pdf">Descargar carta de invitación</a>'
    return pdf_link

# Interfaz de Streamlit
st.title("Generador de Carta de Invitación al Torneo de Robótica")

# Entradas del formulario
nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo electrónico")
cedula = st.text_input("Cédula")

# Botón para generar el PDF
if st.button("Generar carta de invitación"):
    if nombre and correo and cedula:
        # Generar el PDF con los datos ingresados
        pdf = generar_pdf(nombre, correo, cedula)
        
        # Mostrar enlace para descargar el PDF
        link_descarga = convertir_pdf_a_descargable(pdf)
        st.markdown(link_descarga, unsafe_allow_html=True)
    else:
        st.error("Por favor, complete todos los campos.")
