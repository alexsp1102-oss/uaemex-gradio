
import os
import gradio as gr
import mysql.connector
import pandas as pd


# ==========================================================
# CONFIGURACION DE LA BASE DE DATOS
# ==========================================================

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "escuela")
}


# ==========================================================
# INFORMACION INSTITUCIONAL DE LA UAEMEX
# ==========================================================

contenido = """
# UAEMex

## Información General

**Nombre:** Universidad Autónoma del Estado de México

**Teléfono:** (722) 1614089

**Correo:** contacto@uaemex.mx

**Sitio Web:** [www.uaemex.mx](https://www.uaemex.mx)

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


# ==========================================================
# FUNCION PARA CONSULTAR LOS ALUMNOS
# ==========================================================

def consultar_alumnos():
    conexion = None

    columnas = [
        "id",
        "nombre",
        "edad",
        "carrera",
        "correo"
    ]

    try:
        # Establecer conexion con MySQL/MariaDB
        conexion = mysql.connector.connect(**DB_CONFIG)

        # Consulta SQL
        consulta = """
            SELECT id, nombre, edad, carrera, correo
            FROM alumnos
            ORDER BY id ASC
        """

        cursor = conexion.cursor()
        cursor.execute(consulta)

        # Recuperar registros
        registros = cursor.fetchall()

        # Crear DataFrame con los resultados
        df = pd.DataFrame(registros, columns=columnas)

        cursor.close()

        if df.empty:
            return df, "La conexion fue exitosa, pero no hay alumnos registrados."

        return df, (
            "Consulta exitosa. Se encontraron "
            f"{len(df)} alumnos en la base de datos."
        )

    except mysql.connector.Error as error:
        df_vacio = pd.DataFrame(columns=columnas)

        return df_vacio, (
            "Error de conexion o consulta a la base de datos: "
            f"{error}"
        )

    except Exception as error:
        df_vacio = pd.DataFrame(columns=columnas)

        return df_vacio, f"Error inesperado: {error}"

    finally:
        if conexion is not None and conexion.is_connected():
            conexion.close()


# ==========================================================
# INTERFAZ PRINCIPAL DE GRADIO
# ==========================================================

with gr.Blocks(
    title="UAEMex - Informacion Institucional y Base de Datos",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown("""
    # Universidad Autónoma del Estado de México

    ### Información institucional y consulta de alumnos

    Esta aplicación integra información institucional y una consulta
    de registros almacenados en una base de datos MySQL/MariaDB.
    """)

    with gr.Tabs():

        # --------------------------------------------------
        # PESTAÑA 1: INFORMACION INSTITUCIONAL
        # --------------------------------------------------

        with gr.Tab("Información institucional"):

            gr.Markdown(contenido)

        # --------------------------------------------------
        # PESTAÑA 2: CONSULTA DE ALUMNOS
        # --------------------------------------------------

        with gr.Tab("Consulta de alumnos"):

            gr.Markdown("""
            ## Conexión a base de datos con Python

            **Base de datos:** `escuela`

            **Tabla:** `alumnos`

            **Lenguaje:** Python

            **Gestor de base de datos:** MySQL/MariaDB mediante XAMPP

            **Interfaz:** Gradio

            ### Objetivo

            Consultar los registros de la tabla alumnos y mostrarlos
            en una tabla interactiva dentro de la aplicación web.

            ### Funcionamiento

            1. Python establece una conexión con la base de datos.
            2. Se ejecuta una consulta SQL mediante SELECT.
            3. Se recuperan los registros de la tabla alumnos.
            4. Pandas organiza los resultados en una tabla.
            5. Gradio muestra los resultados en pantalla.
            6. La conexión se cierra al finalizar la consulta.
            """)

            boton_consultar = gr.Button(
                "Consultar alumnos",
                variant="primary"
            )

            tabla_alumnos = gr.Dataframe(
                headers=[
                    "id",
                    "nombre",
                    "edad",
                    "carrera",
                    "correo"
                ],
                label="Resultados de la consulta",
                interactive=False,
                wrap=True
            )

            mensaje = gr.Textbox(
                label="Estado de la consulta",
                interactive=False
            )

            boton_consultar.click(
                fn=consultar_alumnos,
                inputs=[],
                outputs=[
                    tabla_alumnos,
                    mensaje
                ]
            )

            gr.Markdown("""
            ---

            ### Tecnologías utilizadas

            - Python
            - Gradio
            - MySQL/MariaDB
            - mysql-connector-python
            - Pandas
            """)


# ==========================================================
# INICIAR LA APLICACION
# ==========================================================

if __name__ == "__main__":

    puerto = int(os.environ.get("PORT", "7860"))

    demo.launch(
        server_name="0.0.0.0",
        server_port=puerto
    )
    
