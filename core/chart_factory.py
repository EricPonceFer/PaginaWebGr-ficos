import plotly.express as px


def create_chart(chart_type, x, y):
    """
    Crea una gráfica usando listas ya procesadas
    x -> eje X
    y -> eje Y
    """

    if chart_type == "Línea":
        return px.line(x=x, y=y, markers=True)

    elif chart_type == "Barra":
        return px.bar(x=x, y=y)

    elif chart_type == "Dispersión":
        return px.scatter(x=x, y=y)

    else:
        raise ValueError("Tipo de gráfica no soportado")