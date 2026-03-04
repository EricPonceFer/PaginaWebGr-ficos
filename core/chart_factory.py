import plotly.graph_objects as go

def create_chart(chart_type, df, horas_objetivo):
    """
    Crea una gráfica usando:
    Primera columna -> X
    Segunda columna -> Y
    """
    fig = go.Figure()

    if df.shape[1] < 2:
        raise ValueError("El DataFrame debe tener al menos 2 columnas")

    operadores = df.iloc[:-1, 0].to_list()
    hora_trabajadas = df.iloc[:-1, 1].to_list()
    planta = df.iloc[-1, 0]
    planta_horas_trabajadas = df.iloc[-1, 1]
    promedio = df.iloc[:-1, 1].mean()

    if chart_type == "Línea":
        fig = crear_grafico_lineas(fig,operadores,hora_trabajadas, planta, planta_horas_trabajadas)

    elif chart_type == "Barra":
        fig =  crear_grafico_barras(fig,operadores,hora_trabajadas, planta, planta_horas_trabajadas)

    elif chart_type == "Dispersión":
        fig = crear_grafico_dispersion(fig,operadores,hora_trabajadas, planta, planta_horas_trabajadas)


    fig.add_trace(
        go.Scatter(
            x=operadores,
            y=[promedio] * len(operadores),  # ← aquí está la clave
            mode="lines+markers",
            name="Promedio Horas Trabajadas",
            line=dict(width=2, color="red")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=operadores,
            y=[horas_objetivo] * len(operadores),  # ← aquí está la clave
            mode="lines+markers",
            name="Horas Objetivo",
            line=dict(width=2, color="black")
        )
    )

    fig.update_layout(
        title="Horas trabajadas por Operador",
        xaxis=dict(type="category"),
        showlegend=True
    )
    return fig
    
def crear_grafico_barras(fig,x,y, planta, planta_horas_trabajadas):
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            name="Horas Trabajadas",
        )
    )
    fig.add_trace(
        go.Bar(
            x=planta,
            y=planta_horas_trabajadas,
            name="PLANTA",
            marker_color='orange'
        )
    )
    return fig

def crear_grafico_lineas(fig,x,y, promedio,horas_objetivo):
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            name="Horas Trabajadas",
        )
    )
    return fig

def crear_grafico_dispersion(fig, x, y, promedio, horas_objetivo):

    # 🔵 Puntos (dispersión real)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",  # ← clave para dispersión
            name="Horas Trabajadas",
            marker=dict(
                size=10
            )
        )
    )

    return fig