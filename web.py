import os
import gradio as gr

contenido = """
# UAEMex

## Información General

**Nombre:** Universidad Autónoma del Estado de México

**Teléfono:** (722) 1614089 

**Correo:** contacto@uaemex.mx

**Sitio Web:** www.uaemex.mx

---

## Carreras Disponibles

- Ingeniería en Sistemas Computacionales
- Ingeniería Industrial
- Contaduría Pública
- Administración de Empresas
- Informática Administrativa

---

## Datos Institucionales

**Fundación:** 2005

**Modalidad:** Escolarizada y Mixta

**Turnos:** Matutino y Vespertino

**Número de Alumnos:** 11500

---

## Misión

Formar profesionistas competentes con valores y compromiso social.

## Visión

Ser una institución líder en educación superior reconocida por su calidad académica.
"""

with gr.Blocks(title="Información Institucional") as demo:
    gr.Markdown(contenido)

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=puerto
    )