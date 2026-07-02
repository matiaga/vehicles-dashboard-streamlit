import pandas as pd
import plotly.express as px
import streamlit as st


# Función para aplicar estilo a los gráficos
def apply_chart_style(fig):
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,
        title_font=dict(size=18),
        font=dict(size=12),
        margin=dict(l=10, r=20, t=60, b=10),
    )

    fig.update_xaxes(title_font=dict(size=14))
    fig.update_yaxes(title_font=dict(size=14))

    return fig


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
    st.metric(" 🚘 Total de vehículos", len(car_data), border=True)

with col2:
    st.metric("💲 Precio promedio", f"${car_data['price'].mean():,.0f}", border=True)

with col3:
    st.metric(
        "🕕 Kilometraje promedio", f"{car_data['odometer'].mean():,.0f} mi", border=True
    )

with col4:
    st.metric("🏷 Precio Máximo", f"${car_data['price'].max():,.0f}", border=True)


# Sección de visualizaciones
st.header("📊 Visualizaciones interactivas")

# Creación de los gráficos del dashboard
# Histograma de precios
fig_hist_price = px.histogram(
    car_data,
    x="price",
    nbins=50,
    title="Distribución de precios",
    labels={"price": "Precio (USD)"},
)
fig_hist_price.update_yaxes(title_text="")
fig_hist_price = apply_chart_style(fig_hist_price)

# Histograma de kilometraje
fig_hist_odometer = px.histogram(
    car_data,
    x="odometer",
    nbins=50,
    title="Distribución del kilometraje",
    labels={"odometer": "Kilometraje (millas)"},
)
fig_hist_odometer.update_yaxes(title_text="")
fig_hist_odometer = apply_chart_style(fig_hist_odometer)

# Scatter Precio vs Kilometraje
fig_scatter_1 = px.scatter(
    car_data,
    x="odometer",
    y="price",
    title="Precio vs. kilometraje",
    opacity=0.5,
    labels={"odometer": "Kilometraje (millas)", "price": "Precio (USD)"},
)
fig_scatter_1 = apply_chart_style(fig_scatter_1)

# Gráfico de relación Precio y Año del Modelo
avg_price_by_year = (
    car_data.groupby("model_year")["price"]
    .mean()
    .reset_index()
    .sort_values("model_year")
)

fig_line_model = px.line(
    avg_price_by_year,
    x="model_year",
    y="price",
    title="Precio Promedio por Año del Modelo",
    labels={"model_year": "Año del Modelo)", "price": "Precio (USD)"},
)
fig_line_model = apply_chart_style(fig_line_model)

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


col1, col2 = st.columns(2)

with col1:
    # Gráfico de dispersión
    build_scatter = st.checkbox("Mostrar relación entre precio y su kilometraje")

    if build_scatter:
        st.plotly_chart(fig_scatter_1, use_container_width=True)
        st.write(
            "En este gráfico de dispersión podemos ver la relación entre el precio del vehículo y su kilometraje."
        )

with col2:
    # Gráfico por año
    build_year_chart = st.checkbox("Mostrar precio promedio por año del modelo")

    if build_year_chart:
        st.plotly_chart(fig_line_model, use_container_width=True)
        st.write(
            "En el gráfico que antecede observamos como varía el precio del vehículo según el año de fabricación."
        )

"""
## Dataset
"""
st.dataframe(car_data.head())
