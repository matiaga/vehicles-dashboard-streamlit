import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Leer los datos del archivo CSV
car_data = pd.read_csv("vehicles_us.csv")

# Configuración de la página
st.set_page_config(
    page_title="Dashboard: Ventas de vehículos", page_icon="🚗", layout="wide"
)

# Crear encabezado
st.header("🚗 Dashboard: Ventas de vehículos")

# crear una casilla de verificación
build_histogram = st.checkbox("Construir un histograma")

# Lógica a ejecutar cuando se hace clic en el botón
if build_histogram:
    # Escribir un mensaje en la aplicación
    st.write(
        "Creación de un histograma para el conjunto de datos de anuncios de venta de coches"
    )

    # Crear un histograma utilizando plotly.graph_objects
    # Se crea una figura vacía y luego se añade un rastro de histograma
    fig = go.Figure(data=[go.Histogram(x=car_data["odometer"])])

    # Opcional: Puedes añadir un título al gráfico si lo deseas
    fig.update_layout(title_text="Distribución del Odómetro")

    # Mostrar el gráfico Plotly interactivo en la aplicación Streamlit
    # 'use_container_width=True' ajusta el ancho del gráfico al contenedor
    st.plotly_chart(fig, use_container_width=True)

"""
## Dataset
"""

car_data
