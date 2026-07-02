import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Vehículos Usados", page_icon="🚗", layout="wide"
)


@st.cache_data
def load_data():
    """Lee el archivo CSV y devuelve un DataFrame."""
    df = pd.read_csv("vehicles_us.csv")
    return df


# Leer los datos del archivo CSV
car_data = load_data()

# Título principal
st.title("🚗 Dashboard de Vehículos Usados en EE. UU.")
st.markdown("""
    En esta aplicación vamos a explorar anuncios de venta de vehículos usados.
    Vamos a analizar tendencias de precio, kilometraje, condición y año del modelo.
    """)

# Vista rápida de datos
st.header("📌 Vista general del dataset")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de vehículos", len(car_data), border=True)

with col2:
    st.metric("Precio promedio", f"${car_data['price'].mean():,.0f}", border=True)

with col3:
    st.metric(
        "Kilometraje promedio", f"{car_data['odometer'].mean():,.0f} mi", border=True
    )

with col4:
    st.metric("Precio Máximo", f"${car_data['price'].max():,.0f}", border=True)


# "Creación de un histograma para el conjunto de datos de anuncios de venta de coches"

# Sección de visualizaciones
st.header("📊 Visualizaciones interactivas")

# Histograma de precios
fig_hist_price = px.histogram(
    car_data, x="price", nbins=50, title="Distribución de precios"
)
# Histograma de kilometraje
fig_hist_odometer = px.histogram(
    car_data, x="odometer", nbins=50, title="Distribución del kilometraje"
)

# Crear una casilla de verificación
build_hist = st.checkbox("Construir Histogramas de Precios y Kilometraje")

if build_hist:
    # Columnas para mostrar los histogramas
    col1, col2 = st.columns(2)

    with col1:
        # 'use_container_width=True' ajusta el ancho del gráfico al contenedor
        st.plotly_chart(fig_hist_price, use_container_width=True)
        st.write("Distribución de precios de los vehículos.")

    with col2:
        st.plotly_chart(fig_hist_odometer, use_container_width=True)
        st.write("Distribución del kilometraje de los vehículos.")


"""
## Dataset
"""
st.dataframe(car_data.head())
