from datetime import datetime
from operator import itemgetter

records = [
    {
        "source": "48-996355555",
        "destination": "48-666666666",
        "end": 1564610974,
        "start": 1564610674,
    },
    {
        "source": "41-885633788",
        "destination": "41-886383097",
        "end": 1564506121,
        "start": 1564504821,
    },
    {
        "source": "48-996383697",
        "destination": "41-886383097",
        "end": 1564630198,
        "start": 1564629838,
    },
    {
        "source": "48-999999999",
        "destination": "41-885633788",
        "end": 1564697158,
        "start": 1564696258,
    },
    {
        "source": "41-833333333",
        "destination": "41-885633788",
        "end": 1564707276,
        "start": 1564704317,
    },
    {
        "source": "41-886383097",
        "destination": "48-996384099",
        "end": 1564505621,
        "start": 1564504821,
    },
    {
        "source": "48-999999999",
        "destination": "48-996383697",
        "end": 1564505721,
        "start": 1564504821,
    },
    {
        "source": "41-885633788",
        "destination": "48-996384099",
        "end": 1564505721,
        "start": 1564504821,
    },
    {
        "source": "48-996355555",
        "destination": "48-996383697",
        "end": 1564505821,
        "start": 1564504821,
    },
    {
        "source": "48-999999999",
        "destination": "41-886383097",
        "end": 1564610750,
        "start": 1564610150,
    },
    {
        "source": "48-996383697",
        "destination": "41-885633788",
        "end": 1564505021,
        "start": 1564504821,
    },
    {
        "source": "48-996383697",
        "destination": "41-885633788",
        "end": 1564627800,
        "start": 1564626000,
    },
]


def classify_by_phone_number(records):
    dict_result = {}
    final_result = []

    for call in records:
        # funções Timestamp >>> minutos do dia(inicial/final)
        start = start_min(records, records.index(call))
        end = end_min(records, records.index(call))

        # função minutos do dia(inicial, final) >>> taxa total
        total_to_pay = tariff(start, end)

        # verifica se o 'source' não está no novo dicionário {dict_result},
        # e se assim for adiciona o 'source' e a taxa total correspondente;
        # caso 'source' já esteja no dicionário, soma os valores da taxa total
        if call["source"] not in dict_result:
            dict_result[call["source"]] = total_to_pay
        else:
            dict_result[call["source"]] += total_to_pay

    # organiza os valores de taxa total no dict_result em ordem decrescente
    dict_result = sorted(dict_result.items(), key=itemgetter(1), reverse=True)

    # adiciona os resultados de cada 'source' na nova lista [final_result]
    for customer in dict_result:
        final_result.append(
            {"source": customer[0], "total": round(customer[1], 2)}
            )
    return final_result


# converte o valor Timestamp 'start' de cada ligação em formato datetime
# e depois em minutos do dia
def start_min(records, i):
    start_time = datetime.fromtimestamp(records[i]["start"])
    minutes = start_time.hour * 60 + start_time.minute + start_time.second / 60
    return minutes


# converte o valor Timestamp 'end' de cada ligação em formato datetime
# e depois em minutos do dia
def end_min(records, i):
    end_time = datetime.fromtimestamp(records[i]["end"])
    minutes = end_time.hour * 60 + end_time.minute + end_time.second / 60
    return minutes


# através dos parâmetros inicial e final dos minutos do dia,
# sendo que 360 (minutos) == 6am e 1320 (minutos) == 22pm,
# retorna o valor da total da taxa de acordo com o README
def tariff(start, end):
    PERMANENT_TAX = 0.36
    if end < 360 or start > 1320:
        min_tax = 0
    elif start < 360 and end < 1320:
        min_tax = int(end - 360) * 0.09
    elif start < 360 and end > 1320:
        min_tax = 960 * 0.09
    elif start > 360 and end <= 1320:
        min_tax = int(end - start) * 0.09
    elif start > 360 and end > 1320:
        min_tax = int(1320 - start) * 0.09
    total_tax = PERMANENT_TAX + min_tax

    return total_tax


print(classify_by_phone_number(records))
