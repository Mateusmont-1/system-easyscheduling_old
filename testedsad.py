from datetime import datetime, timedelta

def get_week_dates(date_str):
    # Converte a string de data para um objeto datetime
    date = datetime.strptime(date_str, '%d/%m/%Y')
    
    # Encontra o dia da semana (0 é segunda e 6 é domingo)
    start_of_week = date - timedelta(days=date.weekday())
    
    # Cria uma lista com as datas da semana
    week_dates = [(start_of_week + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
    
    return week_dates

# Exemplo de uso:
date_str = '16/06/2024'
week_dates = get_week_dates(date_str)
print(week_dates)