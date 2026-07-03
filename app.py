import pandas as pd
import plotly.express as px
import streamlit as st
import preprocessing as pre

# from preprocessing import preprocess_data, prepare_display_data


# Función para aplicar estilo a los gráficos
def apply_chart_style(fig):
    fig.update_layout(
        template="plotly_white",
        title_x=0.3,  # Centra el título
        title_font=dict(size=18),
        font=dict(size=12),
        margin=dict(l=10, r=20, t=60, b=10),
    )

    fig.update_xaxes(title_font=dict(size=14))
    fig.update_yaxes(title_font=dict(size=14))

    return fig


# Función para crear boxplot
def generate_box_plot(df, percentil99=False):
    """Crea el box plot basado en el df enviado y si muestra o no los datos del percentil 99."""
    fig = px.box(
        df,
        x="price",
        y="condition",
        orientation="h",
        # points=False,
        title="Diagráma de Cajas: Precio según condición del vehículo",
        labels={"condition": "Condición", "price": "Precio (USD)"},
    )

    # Limita visualización al percentil 99
    if percentil99:
        price_limit = df["price"].quantile(0.99)
        fig.update_xaxes(range=[0, price_limit])

    return fig


# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Vehículos Usados", page_icon="🚗", layout="wide"
)


# @st.cache_data
def load_data():
    """Lee el archivo CSV y devuelve un DataFrame."""
    df = pd.read_csv("vehicles_us.csv")
    # Prepocesamiento de los datos
    df = pre.preprocess_data(df)
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
    st.metric(
        " 🚘 Total de vehículos",
        len(car_data),
        border=True,
        delta_arrow="up",
        delta_color="green",
    )

with col2:
    st.metric(
        "💲 Precio promedio",
        f"${car_data['price'].mean():,.0f}",
        border=True,
    )

with col3:
    st.metric(
        "🕕 Kilometraje promedio", f"{car_data['odometer'].mean():,.0f} mi", border=True
    )

with col4:
    st.metric("🎫 Precio Máximo", f"${car_data['price'].max():,.0f}", border=True)


# Sección de visualizaciones
st.subheader("📊 Visualizaciones interactivas")

# Creación de los gráficos del dashboard
# Histograma de precios
fig_hist_price = px.histogram(
    car_data,
    x="price",
    nbins=100,
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
    labels={"model_year": "Año del Modelo", "price": "Precio (USD)"},
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
        st.write(
            "La distribución de precios permite observar que la mayoría de los vehículos "
            "se concentra en rangos de precio bajos y medios, mientras que existen algunos "
            "vehículos con precios considerablemente más altos (outliers)."
        )

    with col2:
        st.plotly_chart(fig_hist_odometer, use_container_width=True)
        st.write(
            "La distribución del kilometraje permite identificar la concentración "
            "de vehículos según su nivel de uso, aquellos con kilometraje bajo, medio o alto. "
            "También permite observar posibles valores extremos, que podrían corresponder "
            "a vehículos con uso intensivo o registros poco comunes."
        )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    # Gráfico de dispersión
    build_scatter = st.checkbox("Mostrar relación entre precio y su kilometraje")

    if build_scatter:
        st.plotly_chart(fig_scatter_1, use_container_width=True)
        st.markdown(
            """Este gráfico de dispersión permite identificar si los vehículos con mayor 
            kilometraje tienden a tener precios más bajos, lo cual sería esperable en el 
            mercado de vehículos usados.
            """
        )

with col2:
    # Gráfico por año
    build_year_chart = st.checkbox("Mostrar precio promedio por año del modelo")

    if build_year_chart:
        st.plotly_chart(fig_line_model, use_container_width=True)
        st.write(
            "Los modelos más recientes tienden a registrar precios promedio más elevados, "
            "reflejando el efecto de la depreciación. Las variaciones observadas entre algunos "
            "años sugieren la influencia de otras variables como el modelo, el kilometraje, "
            "la condición y el tipo de vehículo."
        )

st.markdown("---")

# Gráfico Precio según condición del vehículo
check_percentil99 = st.checkbox("Limita el Diagráma de cajas al percentil 99")

# Crear Diagrama de cajas segun condición del vehículo
fig_plot_cond = generate_box_plot(car_data, check_percentil99)
fig_plot_cond = apply_chart_style(fig_plot_cond)
st.plotly_chart(fig_plot_cond, use_container_width=True)
st.markdown(
    """El boxplot muestra que los vehículos en mejor condición tienden a presentar precios 
    más altos. Sin embargo,la alta dispersión observada evidencia que otros factores también
    tienen un impacto importante en el valor del vehículo."""
)

st.markdown("---")

st.subheader("📄 Conjunto de datos (Dataset)")

# Prepara el data set para mostrarse
display_data = pre.prepare_display_data(car_data)

rows_to_show = st.slider(
    "Número de registros a mostrar", min_value=5, max_value=100, value=10, step=5
)

st.dataframe(
    display_data.head(rows_to_show),
    use_container_width=True,
    hide_index=True,
    column_config=pre.CONFIG_DATAFRAME,
)


st.header("👓 Conclusiones")
st.markdown(
    """Del análisis exploratorio se identificó que las variables **precio**, **kilometraje**, **condición** y **año del modelo** 
    proporcionan la información más relevante para comprender el mercado de vehículos usados. Por este motivo, 
    estas variables fueron seleccionadas para construir el dashboard interactivo en Streamlit."""
)
