from fillpdf import fillpdfs

# Función para rellenar el PDF existente con datos de ejemplo usando fillpdf
def fill_pdf_with_fillpdf(input_pdf, output_pdf):
    # Leer los campos del formulario del PDF
    fields = fillpdfs.get_form_fields(input_pdf)
    
    # Mostrar los campos disponibles para depurar
    print("Campos detectados en el PDF:")
    for field_name in fields:
        print(f"{field_name}: {fields[field_name]}")

    # Datos de ejemplo que vamos a rellenar
    example_data = {
        'Nombre': 'Juan Pérez',
        'Fecha': '10/09/2024',
        'cargo_persona': 'Estudiante',
        'afiliacion': 'Universidad Unillanos',
        'Correo': 'juan.perez@example.com',
        'Primer_nombre': 'Juan'
    }

    # Rellenar los campos con los datos de ejemplo
    fillpdfs.write_fillable_pdf(input_pdf, output_pdf, example_data)

    # Opción de aplanar el PDF (hacer que los campos ya no sean editables)
    fillpdfs.flatten_pdf(output_pdf, output_pdf)  # Corregido: pasamos el archivo PDF de salida dos veces

    print(f"PDF rellenado y generado correctamente: {output_pdf}")

# Llamar a la función para rellenar el PDF
fill_pdf_with_fillpdf("Template01.pdf", "Filled_Template01.pdf")