import streamlit as st
from fillpdf import fillpdfs
from io import BytesIO
import base64
from babel.dates import format_date
from datetime import datetime

# Función para rellenar el PDF con los datos del usuario y almacenarlo en caché para su descarga
@st.cache_data
def generate_filled_pdf(name, institution, position, email, date):
    # Formatear la fecha como "19 de Septiembre de 2024"
    formatted_date = format_date(date, format="d 'de' MMMM 'de' y", locale='es_ES')

    # Datos de ejemplo con el primer nombre seguido de una coma
    example_data = {
        'Nombre': name,  # Nombre completo del usuario
        'Fecha': formatted_date,  # Fecha formateada
        'cargo_persona': position,
        'afiliacion': institution,
        'Correo': email,
        'Primer_nombre': name.split()[0] + ","  # Primer nombre con una coma al final
    }

    # Generar el PDF en memoria (BytesIO)
    pdf_buffer = BytesIO()
    
    # Escribir los datos en el PDF en memoria
    fillpdfs.write_fillable_pdf("Template01.pdf", pdf_buffer, example_data)

    # Rebobinar el buffer después de escribir
    pdf_buffer.seek(0)

    # Aplanar el PDF en memoria para evitar que los campos sean editables
    fillpdfs.flatten_pdf(pdf_buffer, pdf_buffer)

    # Rebobinar el buffer después de aplanar
    pdf_buffer.seek(0)
    
    # Retornar el buffer en memoria del PDF
    return pdf_buffer

# Función para mostrar la descarga con un botón estilizado
def show_pdf_download_button(pdf_bytes, filename):
    # Como pdf_bytes ya es de tipo 'bytes', no necesitamos usar getvalue()
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    href = f'''
    <a href="data:application/octet-stream;base64,{b64_pdf}" download="{filename}">
        <button style="
            display: inline-block;
            padding: 10px 20px;
            font-size: 18px;
            font-family: 'Poppins', sans-serif;
            color: white;
            background-color: #4CAF50;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        " onmouseover="this.style.backgroundColor='#45a049';" onmouseout="this.style.backgroundColor='#4CAF50';">
        📄 Descargar carta de invitación
        </button>
    </a>
    '''
    st.markdown(href, unsafe_allow_html=True)

# App de Streamlit
# Agregar imagen de encabezado centrada
st.markdown('<div class="center-image">', unsafe_allow_html=True)
st.image("image.png", width=700)
st.markdown('</div>', unsafe_allow_html=True)

st.title("📩 Invitación METAROBOTS 2024")

# Establecer las fechas límite para el input
min_date = datetime.now().date()  # Fecha actual
max_date = datetime(2024, 10, 25).date()  # 25 de octubre de 2024

# Formulario para ingresar los datos
with st.form("form"):
    name = st.text_input("🔤 Digita tu nombre completo:")
    institution = st.text_input("🏫 ¿De qué institución perteneces? (Ej: Unillanos):")
    position = st.text_input("🎓 ¿Qué cargo tienes en dicha institución? (Ej: Estudiante):")
    email = st.text_input("✉️ Digita tu correo electrónico:")
    date = st.date_input("📅 Selecciona la fecha de emisión:", min_value=min_date, max_value=max_date)
    
    submitted = st.form_submit_button("📄 Generar Carta")

# Validación de datos
if submitted:
    if not name or not institution or not position or not email:
        st.error("❌ Por favor completa todos los campos antes de continuar.")
    elif "@" not in email:
        st.error("❌ Correo electrónico inválido. Por favor ingresa un correo válido.")
    else:
        st.info("📄 Generando PDF...")

        # Generar el PDF con la función correcta (generate_filled_pdf)
        modified_pdf = generate_filled_pdf(name, institution, position, email, date)

        # Barra de progreso
        with st.spinner("⏳ Generando PDF..."):
            st.progress(100)

        # Botón de descarga estilizado
        show_pdf_download_button(modified_pdf.getvalue(), "Carta_Invitacion.pdf")