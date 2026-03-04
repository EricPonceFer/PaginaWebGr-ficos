import streamlit as st
from core.data_loader import load_file, procesar_por_operador
from core.validator import validate_columns
from core.chart_factory import create_chart
import plotly.graph_objects as go
import locale
from datetime import datetime
from plotly.subplots import make_subplots

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

    col1, col2 = st.columns(2)

    with col1:
        fecha_seleccionada = st.date_input(
            "Selecciona la fecha",
            value=datetime.today()
        )

    with col2:
        chart_type = st.selectbox(
            "Tipo de gráfica",
            ["Línea", "Barra", "Dispersión"]
        )

    # 🔹 Extraer año, mes y día
    anio = fecha_seleccionada.year
    mes = fecha_seleccionada.month
    dia = fecha_seleccionada.day

    # 🔹 Pasar esos valores a tu función
    data_dia, data_mes, data_anio = procesar_por_operador(
        df,
        anio,
        mes,
        dia
    )

    return data_dia, data_mes, data_anio, chart_type

def render_chart(data_dia, data_mes, data_anio,chart_type):
    # 🔹 Selector múltiple de operadores
    operadores = data_anio["Código"].unique().tolist()

    seleccion = st.multiselect(
        "Selecciona operador(es)",
        options=operadores,
        default=operadores
    )
    # 🔹 Selector de vista
    col1, col2 = st.columns([1, 10]) 
    with col1:
        st.markdown("""
        <style>
        .vertical-center {
            display: flex;
            flex-direction: column;
            justify-content: center;  /* centra vertical */
            height: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="vertical-center">', unsafe_allow_html=True)

        modo = st.radio(
            "Selecciona vista:",
            ["Día", "Mes", "Año"],
            horizontal=False
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # 🔹 Selección dinámica del DataFrame
    if modo == "Día":
        df = data_dia.copy()
        horas_objetivo = 8  # puedes cambiarlo

    elif modo == "Mes":
        df = data_mes.copy()
        horas_objetivo = 160  # ejemplo: 22 días laborales

    else:
        df = data_anio.copy()
        horas_objetivo = 1920  # ejemplo anual

    if df.empty:
        st.warning("No hay datos para mostrar")
        return

    if not seleccion:
        st.warning("Selecciona al menos un operador")
        return

    df = df[df["Código"].isin(seleccion)]


    # 🔹 Crear gráfico
    fig = create_chart(chart_type   , df,horas_objetivo)
    with col2:
        st.plotly_chart(fig, use_container_width=True)


def main():
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain')
    except:
        pass
    configure_page()

    uploaded_file = render_uploader()

    if uploaded_file:
        try:
            df = load_file(uploaded_file)

            render_preview(df)
 
            data_dia, data_mes, data_anio, chart_type  = render_chart_controls(df)

            render_chart(data_dia,data_mes,data_anio, chart_type )

        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()