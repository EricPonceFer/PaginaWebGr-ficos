
def validate_columns(df, x, y):
    if x not in df.columns:
        raise ValueError("Columna X inválida")

    if y not in df.columns:
        raise ValueError("Columna Y inválida")

    if df[x].isnull().all():
        raise ValueError("La columna X está vacía")

    if df[y].isnull().all():
        raise ValueError("La columna Y está vacía")