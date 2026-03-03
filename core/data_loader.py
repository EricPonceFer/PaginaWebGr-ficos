import pandas as pd
import streamlit as st

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

import pandas as pd

def procesar_por_operador(
    df,
    columna_operador,
    columna_anio,
    columna_mes,
    columna_dia,
    fecha_inicio,
    fecha_fin
):
    """
    Construye fecha desde año/mes/día,
    filtra por rango y devuelve:
    x_axis -> códigos de operador (como string ID)
    y_axis -> días trabajados
    """

    try:
        # Validar columnas
        columnas_requeridas = [
            columna_operador,
            columna_anio,
            columna_mes,
            columna_dia
        ]

        for col in columnas_requeridas:
            if col not in df.columns:
                raise ValueError(f"La columna '{col}' no existe en el DataFrame")

        # Trabajar sobre copia
        df_temp = df.copy()

        # 🔹 Forzar código como STRING tipo ID
        df_temp[columna_operador] = (
            df_temp[columna_operador]
            .astype(str)
            .str.strip()
        )

        # 🔹 Crear fecha combinada
        df_temp["fecha_temp"] = pd.to_datetime(
            dict(
                year=df_temp[columna_anio],
                month=df_temp[columna_mes],
                day=df_temp[columna_dia]
            ),
            errors="coerce"
        )

        # Validar rango de fechas
        fecha_inicio = pd.to_datetime(fecha_inicio)
        fecha_fin = pd.to_datetime(fecha_fin)

        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha inicio no puede ser mayor que fecha fin")

        # 🔹 Filtrar por rango
        df_filtrado = df_temp.loc[
            (df_temp["fecha_temp"] >= fecha_inicio) &
            (df_temp["fecha_temp"] <= fecha_fin)
        ].dropna(subset=["fecha_temp", columna_operador])

        if df_filtrado.empty:
            return [], []

        # 🔹 Contar días únicos trabajados
        df_filtrado["fecha_temp"] = df_filtrado["fecha_temp"].dt.date

        resultado = (
            df_filtrado
            .groupby(columna_operador)["fecha_temp"]
            .nunique()
            .reset_index()
        )

        # Ordenar de mayor a menor
        resultado = resultado.sort_values(by="fecha_temp", ascending=False)

        # 🔹 Convertir operador explícitamente a string (seguridad extra)
        resultado[columna_operador] = resultado[columna_operador].astype(str)

        x_axis = resultado[columna_operador].tolist()
        y_axis = resultado["fecha_temp"].tolist()

        return x_axis, y_axis

    except Exception as e:
        raise ValueError(f"Error al procesar datos por operador: {e}")