import streamlit as st
from core.data_loader import load_file, procesar_por_operador
from core.validator import validate_columns
from core.chart_factory import create_chart
from datetime import datetime

def configure_page():
    """Configura la página."""
    st.set_page_config(page_title="GRAFICAS", layout="wide")
    st.markdown(
    """
    <h1 style='text-align: center; font-size: 40px; color: #fffff;'>
        📊 Monitor de Rendimiento Operativo: Asistencia vs. Producción
    </h1>
    """, 
    unsafe_allow_html=True
)


def render_uploader():
    """Renderiza el componente para subir archivos."""
    return st.file_uploader("Sube un archivo CSV", type=["csv", "txt", "data","xls", "xlsx"])


def render_preview(df):
    """Muestra vista previa del DataFrame dentro de un desplegable."""
    # El parámetro expanded=False hace que aparezca cerrado por defecto
    with st.expander("VISTA PREVIA DATOS", expanded=False):
        st.dataframe(df, use_container_width=True)


def render_chart_controls(df):

    with st.container(border=True):
        st.markdown("<h3 style='color: #00000;'>⚙️ Configuración</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)

        with col1:
            # Usamos ** para negritas en el label
            fecha_seleccionada = st.date_input(
                "**📅 Selecciona la fecha**", 
                value=datetime.today()
            )

        with col2:
            chart_type = st.selectbox(
                "**📈 Tipo de gráfica**",
                ["Barra", "Línea", "Dispersión"]
            )
            
        with col3:
            tipo_archivo = st.selectbox(
                "**📁 Tipo de archivo**",
                ["Asistencia", "Producción"]
            )
    # 🔹 Extraer año, mes y día
    anio = fecha_seleccionada.year
    mes = fecha_seleccionada.month
    dia = fecha_seleccionada.day

    # 🔹 Pasar esos valores a tu función
    data_dia, data_mes, data_anio = procesar_por_operador(df,anio,mes,dia)

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
        horas_objetivo = 8

    elif modo == "Mes":
        df = data_mes.copy()
        horas_objetivo = 160 

    else:
        df = data_anio.copy()
        horas_objetivo = 1920 

    if df.empty:
        st.warning("No hay datos para mostrar")
        return

    if not seleccion:
        st.warning("Selecciona al menos un operador")
        return

    df = df[df["Código"].isin(seleccion)]


    # 🔹 Crear gráfico
    fig = create_chart(chart_type, df,horas_objetivo)
    with col2:
        st.plotly_chart(fig, use_container_width=True,theme=None)


def main():
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