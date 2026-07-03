import pandas as pd
import streamlit as st

CONFIG_DATAFRAME = {
    "Modelo": st.column_config.TextColumn("Modelo", help="Modelo del vehículo"),
    "Año del modelo": st.column_config.NumberColumn("Año del modelo", format="%d"),
    "Precio": st.column_config.NumberColumn(
        "Precio", help="Precio publicado del vehículo en dólares", format="$%d"
    ),
    "Kilometraje": st.column_config.NumberColumn(
        "Kilometraje", help="Kilometraje registrado del vehículo", format="%d mi"
    ),
    "Condición": st.column_config.TextColumn(
        "Condición", help="Estado general del vehículo"
    ),
    "Combustible": st.column_config.TextColumn("Combustible"),
    "Transmisión": st.column_config.TextColumn("Transmisión"),
    "Tipo": st.column_config.TextColumn("Tipo"),
    "Color": st.column_config.TextColumn("Color"),
    "4x4": st.column_config.CheckboxColumn(
        "4x4", help="Indica si el vehículo tiene tracción 4x4"
    ),
    "Fecha de publicación": st.column_config.DateColumn(
        "Fecha de publicación", format="YYYY-MM-DD"
    ),
    "Días publicado": st.column_config.NumberColumn("Días publicado", format="%d días"),
}


def preprocess_data(df):
    """Función va a realizar la limpieza y preparación de los datos."""
    # Cambios de tipos de datos
    df["date_posted"] = pd.to_datetime(df["date_posted"])
    df["model_year"] = df["model_year"].astype("Int64")
    df["cylinders"] = df["cylinders"].astype("Int64")
    df["is_4wd"] = df["is_4wd"].astype("Int64").fillna(0)

    # Imputar los valores nullos con la mediana agrupando por modelo
    df["model_year"] = df.groupby("model")["model_year"].transform(
        lambda x: x.fillna(x.median().round())
    )

    # Imputar con la moda agrupando por modelo
    df["cylinders"] = df.groupby("model")["cylinders"].transform(
        lambda x: x.fillna(x.mode().iloc[0])
    )

    # Imputar con la mediana y por año de modelo y eliminamos los registros con valores nulos restantes
    df["odometer"] = df.groupby("model_year")["odometer"].transform(
        lambda x: x.fillna(x.median())
    )
    df.dropna(subset=["odometer"], inplace=True)

    # Asignamos el color Unknown para los valores nulos
    df["paint_color"] = df["paint_color"].fillna("Unknown")

    # Traducir categorías principales para mejorar lectura
    condition_map = {
        "new": "Nuevo",
        "like new": "Como nuevo",
        "excellent": "Excelente",
        "good": "Bueno",
        "fair": "Regular",
        "salvage": "Recuperado",
    }

    fuel_map = {
        "gas": "Gasolina",
        "diesel": "Diésel",
        "electric": "Eléctrico",
        "hybrid": "Híbrido",
        "other": "Otro",
    }

    transmission_map = {"automatic": "Automática", "manual": "Manual", "other": "Otra"}

    df["condition"] = df["condition"].map(condition_map).fillna(df["condition"])
    df["fuel"] = df["fuel"].map(fuel_map).fillna(df["fuel"])
    df["transmission"] = (
        df["transmission"].map(transmission_map).fillna(df["transmission"])
    )

    return df


def prepare_display_data(df):
    display_df = df.copy()

    # Convertir fecha a formato fecha
    display_df["date_posted"] = pd.to_datetime(
        display_df["date_posted"], errors="coerce"
    ).dt.date

    # Convertir columna 4WD a booleano
    display_df["is_4wd"] = display_df["is_4wd"].fillna(0).astype(int).astype(bool)

    # Seleccionar columnas útiles para mostrar en dashboard
    selected_columns = [
        "model",
        "model_year",
        "price",
        "odometer",
        "condition",
        "fuel",
        "transmission",
        "type",
        "paint_color",
        "is_4wd",
        "date_posted",
        "days_listed",
    ]

    display_df = display_df[selected_columns]

    # Renombrar columnas para presentación
    display_df = display_df.rename(
        columns={
            "model": "Modelo",
            "model_year": "Año del modelo",
            "price": "Precio",
            "odometer": "Kilometraje",
            "condition": "Condición",
            "fuel": "Combustible",
            "transmission": "Transmisión",
            "type": "Tipo",
            "paint_color": "Color",
            "is_4wd": "4x4",
            "date_posted": "Fecha de publicación",
            "days_listed": "Días publicado",
        }
    )

    return display_df
