import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_file(file):
    """
    Carga archivos CSV, TXT, DATA, XLS, XLSX
    y devuelve un DataFrame.
    """
    try:
        file_name = file.name
        extension = os.path.splitext(file_name)[1].lower()
        if extension in [".csv"]:
            df = pd.read_csv(file)
        elif extension in [".txt", ".data"]:
            df = pd.read_csv(file, sep=None, engine="python")
        elif extension in [".xls", ".xlsx"]:
            df = pd.read_excel(file)
        else:
            raise ValueError("Formato de archivo no soportado")
        if df.empty:
            raise ValueError("El archivo está vacío")
        return df
    except Exception as e:
        raise ValueError(f"Error al leer el archivo: {e}")

def calcular_planta(df):
    total_row = pd.DataFrame({
        "Código": ["PLANTA"],
        "Horas_trabajadas": [df["Horas_trabajadas"].sum()]
    })

    return pd.concat([df, total_row], ignore_index=True)


def procesar_por_operador(df, anio, mes, dia):

    try:
        columnas_requeridas = [
            "Código",
            "Año",
            "Mes",
            "Día",
            "Horas_trabajadas"
        ]

        for col in columnas_requeridas:
            if col not in df.columns:
                raise ValueError(f"La columna '{col}' no existe en el DataFrame")

        df_temp = df.copy()

        # Código como string
        df_temp["Código"] = (
            df_temp["Código"]
            .astype(str)
            .str.strip()
        )

        # 🔹 Convertir horas a número (si vienen tipo HH:MM)
        df_temp['Horas_trabajadas'] = pd.to_timedelta(
            df_temp['Horas_trabajadas'] + ':00'
        )

        df_temp['Horas_trabajadas'] = (
            df_temp['Horas_trabajadas'].dt.total_seconds() / 3600
        )

        # 🔹 HORAS DEL DÍA SELECCIONADO
        horas_dia = (
            df_temp[
                (df_temp["Año"] == anio) &
                (df_temp["Mes"] == mes) &
                (df_temp["Día"] == dia)
            ]
            .groupby("Código")["Horas_trabajadas"]
            .sum()
            .reset_index()
        )


        # 🔹 HORAS DEL MES SELECCIONADO
        horas_mes = (
            df_temp[
                (df_temp["Año"] == anio) &
                (df_temp["Mes"] == mes)
            ]
            .groupby("Código")["Horas_trabajadas"]
            .sum()
            .reset_index()
        )

        # 🔹 HORAS DEL AÑO SELECCIONADO
        horas_anio = (
            df_temp[
                (df_temp["Año"] == anio)
            ]
            .groupby("Código")["Horas_trabajadas"]
            .sum()
            .reset_index()
        )
        horas_dia = calcular_planta(horas_dia)
        horas_mes = calcular_planta(horas_mes)
        horas_anio = calcular_planta(horas_anio)
        return horas_dia, horas_mes, horas_anio

    except Exception as e:
        raise ValueError(f"Error al procesar horas por operador: {e}")