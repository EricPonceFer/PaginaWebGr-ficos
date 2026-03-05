import plotly.graph_objects as go
import pandas as pd

def create_chart(chart_type, df, horas_objetivo):
    """
    Crea una gráfica con control de errores para asegurar la integridad de los datos.
    """
    try:
        # 1. Validaciones iniciales de datos
        if not isinstance(df, pd.DataFrame):
            raise TypeError("El objeto proporcionado no es un DataFrame de Pandas.")
            
        if df.empty:
            raise ValueError("El DataFrame está vacío.")

        if df.shape[1] < 2:
            raise ValueError("El DataFrame debe tener al menos 2 columnas (Operador y Horas).")

        # 2. Extracción y procesamiento de datos
        # Usamos try-except interno si sospechamos que el formato de las celdas puede fallar
        try:
            operadores = df.iloc[:-1, 0].to_list()
            hora_trabajadas = df.iloc[:-1, 1].to_list()
            planta = df.iloc[-1, 0]
            planta_horas_trabajadas = df.iloc[-1, 1]
            promedio = df.iloc[:-1, 1].mean()
        except Exception as e:
            raise RuntimeError(f"Error al procesar las filas del DataFrame: {e}")

        fig = go.Figure()

        # 3. Selección de tipo de gráfico
        # Nota: Aseguramos que los argumentos coincidan con tus funciones definidas
        if chart_type == "Línea":
            fig = crear_grafico_lineas(fig, operadores, hora_trabajadas, planta, planta_horas_trabajadas)
        elif chart_type == "Barra":
            fig = crear_grafico_barras(fig, operadores, hora_trabajadas, planta, planta_horas_trabajadas)
        elif chart_type == "Dispersión":
            fig = crear_grafico_dispersion(fig, operadores, hora_trabajadas, planta, planta_horas_trabajadas)
        else:
            raise ValueError(f"Tipo de gráfico '{chart_type}' no reconocido. Usa: Línea, Barra o Dispersión.")

        # 4. Capas adicionales (Líneas de referencia)
        # Promedio
        fig.add_trace(
            go.Scatter(
                x=operadores,
                y=[promedio] * len(operadores),
                mode="lines",
                name="Promedio Horas",
                line=dict(width=2, color="red", dash="dash")
            )
        )

        # Objetivo
        fig.add_trace(
            go.Scatter(
                x=operadores,
                y=[horas_objetivo] * len(operadores),
                mode="lines",
                name="Horas Objetivo",
                line=dict(width=2, color="black")
            )
        )

        fig.update_layout(
            template="simple_white",
            title="Horas trabajadas por Operador",
            xaxis=dict(
                        title=dict(
                            text="Código del Operador",
                            font=dict(color="black", size=18)  # <--- Color del título X
                        ), 
                        type="category",
                        tickangle=45,
                        
                    ),
            yaxis=dict(title=dict(text="Total de Horas", font=dict(color="black", size=18)),
                    zeroline=True,
                    zerolinecolor='black'),
            showlegend=True
        )

        return fig

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        return None
    except TypeError as te:
        print(f"Error de tipo de dato: {te}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

# --- Tus funciones auxiliares (sin cambios mayores, solo consistencia de nombres) ---

def crear_grafico_barras(fig, x, y, planta, planta_horas_trabajadas):
    fig.add_trace(go.Bar(x=x, y=y, name="Horas Trabajadas", marker_color='steelblue'))
    fig.add_trace(go.Bar(x=[planta], y=[planta_horas_trabajadas], name="PLANTA", marker_color='orange'))
    return fig

def crear_grafico_lineas(fig, x, y, planta, planta_horas_trabajadas):
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="Horas Trabajadas",  marker_color='steelblue'))
    fig.add_trace(go.Scatter(x=[planta], y=[planta_horas_trabajadas], mode="lines+markers", name="PLANTA", marker_color='orange', marker_size=12))
    return fig

def crear_grafico_dispersion(fig, x, y, planta, planta_horas_trabajadas):
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="Horas Trabajadas", marker=dict(size=10, color='steelblue')))
    fig.add_trace(go.Scatter(x=[planta], y=[planta_horas_trabajadas], mode="markers", name="PLANTA", marker_color='orange', marker_size=12))
    return fig