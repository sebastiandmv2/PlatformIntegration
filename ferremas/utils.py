import bcchapi
import pandas as pd
from datetime import datetime, timedelta

def obtener_valor_dolar(user, password):
    # Obtener la fecha de hoy y restar 7 días
    today_date = datetime.now()
    seven_days_ago_date = today_date - timedelta(days=7)

    # Formatear las fechas como strings en el formato deseado
    today_date_str, seven_days_ago_date_str = today_date.strftime("%Y-%m-%d"), seven_days_ago_date.strftime("%Y-%m-%d")

    # Inicializar la instancia de la API BCCH
    siete = bcchapi.Siete(user, password)

    # Obtener el cuadro de valores del dólar observado
    observable_dollar = siete.cuadro(
        series=['F073.TCO.PRE.Z.D'],
        nombres=['dolar_day'],
        desde=seven_days_ago_date_str,
        hasta=today_date_str,
    )

    # Ordenar el DataFrame por el índice de manera descendente
    observable_dollar_sorted = observable_dollar.sort_index(ascending=False)

    # Buscar el primer valor válido de 'dolar_day' hacia abajo en la lista ordenada de fechas
    latest_valid_dollar = next((date for date in observable_dollar_sorted.index if not pd.isna(observable_dollar_sorted.loc[date, 'dolar_day'])), None)

    # Retornar el valor del dólar más reciente válido si existe, sino retornar None
    if latest_valid_dollar is not None:
        return observable_dollar_sorted.loc[latest_valid_dollar, 'dolar_day']
    else:
        return None
