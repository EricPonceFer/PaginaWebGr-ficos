import streamlit as st
from core.data_loader import load_file, procesar_por_operador
from core.validator import validate_columns
from core.chart_factory import create_chart


def configure_page():
    """Configura la página."""
    st.set_page_config(page_title="GRAFICAS", layout="wide")
    st.title("📊 Diseñador de Gráficas Dinámicas")


def render_uploader():
    """Renderiza el componente para subir archivos."""
    return st.file_uploader("Sube un archivo CSV", type=["csv", "txt", "data","xls", "xlsx"])


def render_preview(df):
    """Muestra vista previa del DataFrame."""
    st.subheader("Vista previa")
    st.dataframe(df)


def render_chart_controls(df):
    x_axis, y_axis = procesar_por_operador(
        df,
        columna_operador="Código",
        columna_anio="Año",
        columna_mes="Mes",
        columna_dia="Día",
        fecha_inicio="2023-01-01",
        fecha_fin="2026-12-31"
    )
    chart_type = st.selectbox(
        "Tipo de gráfica",
        ["Línea", "Barra", "Dispersión"]
    )

    return x_axis, y_axis, chart_type

import streamlit as st

def render_chart(chart_type, x_axis, y_axis):
    """Genera, filtra y muestra la gráfica."""

    # 🔹 Obtener valores únicos ordenados
    opciones = sorted(set(x_axis))

    # 🔹 Selector múltiple
    seleccion = st.multiselect(
        "Selecciona operador(es)",
        options=opciones,
        default=opciones  # por defecto todos
    )

    if not seleccion:
        st.warning("Selecciona al menos un operador")
        return

    # 🔹 Filtrar datos según selección
    datos_filtrados = [
        (x, y) for x, y in zip(x_axis, y_axis)
        if x in seleccion
    ]

    x_filtrado, y_filtrado = zip(*datos_filtrados)

    # Crear figura
    fig = create_chart(chart_type, list(x_filtrado), list(y_filtrado))

    fig.update_layout(
        xaxis_type="category",
        xaxis_title="Operador",
        yaxis_title="Días Trabajados"
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    configure_page()

    uploaded_file = render_uploader()

    if uploaded_file:
        try:
            df = load_file(uploaded_file)

            render_preview(df)

            x_axis, y_axis, chart_type = render_chart_controls(df)

            # 🔥 Renderizar siempre (sin botón)
            render_chart(chart_type, x_axis, y_axis)

        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()