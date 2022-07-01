# Salva diversos valores a cada minuto em um banco de dados
# https://www.investing.com/equities/brazil

import requests, re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time, csv, datetime, pytz
import sqlite3

# url_base="https://www.investing.com/equities/brazil"

call_sell = 0
call_buy = 0

k = 1
t = 0  # t =1 salva os valores minimo e maximos sempre. t = 0 avalia pelo fornecido pelo site
rate = 0.4  # valor em % ex: 0.8 = 0.8%

stock_name = []
stock_last = []
stock_high = []
stock_low = []
stock_volume = []

stock_high_max = []
stock_low_max = []
sell_list = []
buy_list = []
all_list = []
all_list_aux = []


def print_values_high(name, last, high, safe, low):
    low = float(low)
    last = float(last)
    h_l = ((last / low) - 1) * 100
    # print(f"Sell {name}. Last {last}. High {high} e Safe Signal {safe}.")
    sell_list.append(
        f"Sell {name}. Last {last}. High {high}. Safe Signal {safe}. Day Low {low}. Last/Low +{round(h_l, 2)}. ")


def print_values_low(name, last, low, safe, high):
    high = float(high)
    low = float(low)
    last = float(last)
    h_l = ((high / last) - 1) * 100
    # print(f"Buy {name}. Last {last}. Low {low} e Safe Signal {safe}.")
    buy_list.append(
        f"Buy {name}. Last {last}. Low {low}. Safe Signal {safe}. Day High {high}. High/Last -{round(h_l, 2)}. ")


def print_values_all(name, last, low, safe, high):
    high = float(high)
    low = float(low)
    h_l = ((high / low) - 1) * 100
    # print(f"Buy {name}. Last {last}. Low {low} e Safe Signal {safe}.")
    all_list.append(f" {name}. Last {last}. Low {low}. High {high}. -{round(h_l, 2)}. ")
    all_list_aux.append(f" {name},{last},{low},{high} ")


def time_now():
    date_sp = datetime.datetime.utcnow()  # data UTC
    date_sp1 = date_sp.replace(tzinfo=pytz.UTC)  # replace data
    date_sao_paulo1 = date_sp1.astimezone(pytz.timezone("America/Sao_Paulo"))  # Fuso horário
    hour_start = date_sao_paulo1.strftime("%H:%M")  # Hora
    seconds_now = date_sao_paulo1.strftime("%S")  # Hora
    date_sao_paulo2 = date_sao_paulo1.strftime("%d/%m/%Y")
    return (hour_start, date_sao_paulo2, seconds_now)


def get_page_investing():
    get_page = ''
    url = "https://www.investing.com/equities/brazil"
    req = Request(url, headers={'User-Agent': 'Mozilla/76.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    get_page = BeautifulSoup(webpage, 'html.parser')
    get_page = get_page.find("tbody")
    return (get_page)


def get_page_investing_indices():
    get_page = ''
    url = "https://www.investing.com/indices/major-indices"
    req = Request(url, headers={'User-Agent': 'Mozilla/73.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    get_page = BeautifulSoup(webpage, 'html.parser')
    get_page = get_page.find("tbody")
    ibov_now = get_page.find(class_="pid-17920-last").get_text()
    dw_now = get_page.find(class_="pid-169-last").get_text()
    sep500_now = get_page.find(class_="pid-166-last").get_text()
    nasdaq_now = get_page.find(class_="pid-14958-last").get_text()
    small_cap2k_now = get_page.find(class_="pid-170-last").get_text()
    sep500vix_now = get_page.find(class_="pid-44336-last").get_text()
    ft_se100_now = get_page.find(class_="pid-27-last").get_text()
    euro_stoxx50_now = get_page.find(class_="pid-175-last").get_text()

    return (ibov_now, dw_now, sep500_now, nasdaq_now, small_cap2k_now, sep500vix_now, ft_se100_now, euro_stoxx50_now)


def get_page_investing_commodity():
    get_page = ''
    url = "https://www.investing.com/commodities/real-time-futures"
    req = Request(url, headers={'User-Agent': 'Mozilla/75.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    get_page = BeautifulSoup(webpage, 'html.parser')
    get_page = get_page.find("tbody")
    gold = get_page.find(class_="pid-8830-last").get_text()
    silver = get_page.find(class_="pid-8836-last").get_text()
    copper = get_page.find(class_="pid-8831-last").get_text()
    platinum = get_page.find(class_="pid-8910-last").get_text()
    palladium = get_page.find(class_="pid-8883-last").get_text()
    crude_oil = get_page.find(class_="pid-8849-last").get_text()
    brent_oil = get_page.find(class_="pid-8833-last").get_text()
    natural_gas = get_page.find(class_="pid-8862-last").get_text()
    heating_oil = get_page.find(class_="pid-8988-last").get_text()
    gasoline = get_page.find(class_="pid-954867-last").get_text()
    return (gold, silver, copper, platinum, palladium, crude_oil, brent_oil, natural_gas, heating_oil, gasoline)


def get_page_investing_forex():
    get_page = ''
    url = "https://www.investing.com/currencies/single-currency-crosses"
    req = Request(url, headers={'User-Agent': 'Mozilla/71.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    get_page = BeautifulSoup(webpage, 'html.parser')
    get_page = get_page.find("tbody")
    eurusd = get_page.find(class_="pid-1-bid").get_text()
    gbpusd = get_page.find(class_="pid-2-bid").get_text()
    usdjpy = get_page.find(class_="pid-3-bid").get_text()
    usdchf = get_page.find(class_="pid-4-bid").get_text()
    audusd = get_page.find(class_="pid-5-bid").get_text()
    usdcad = get_page.find(class_="pid-7-bid").get_text()
    usdbrl = get_page.find(class_="pid-2103-bid").get_text()

    return (eurusd, gbpusd, usdjpy, usdchf, audusd, usdcad, usdbrl)


def convert_to_number(analysis_volume):
    aux1 = analysis_volume
    aux2 = aux1.replace('G', '000000000')
    aux3 = aux2.replace('M', '000000')
    aux4 = aux3.replace('K', '000')
    aux5 = str(aux4.replace('.', ''))
    aux5 = str(aux5)
    return (aux5)


def get_names_stocks(page, stocks):
    stocks_names = []
    for i in stocks:
        page_names = page.find(id="pair_" + i)
        page_names_1 = page_names.find_all(class_="bold left noWrap elp plusIconTd")[0].get_text()
        stocks_names.append(page_names_1)
    return (stocks_names)


def create_db(table_name):
    conn = sqlite3.connect("prices.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `%s` (date TEXT, hour INTEGER, price REAL)" % (
        table_name))  # Inserir o nome da tabela de forma variavel
    # cur.execute("CREATE TABLE IF NOT EXISTS tabela1 (date TEXT, hour INTEGER, name TEXT, price REAL)" % (table_name))
    conn.commit()
    # print("Table created successfully");
    conn.close


def create_db_stocks(table_name):
    conn = sqlite3.connect("prices.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `%s` (date TEXT, hour INTEGER, price REAL, volume REAL)" % (
        table_name))  # Inserir o nome da tabela de forma variavel
    conn.commit()
    # print("Table created successfully");
    conn.close


def insert_data(date, hour, name, price):
    conn = sqlite3.connect("prices.db")
    cur = conn.cursor()
    # cur.execute("INSERT INTO `%s` VALUES(?,?,?)",(date,hour,name,price) %(table_name))
    # cur.execute("INSERT INTO tabela1 (?,?,?)" ,(date,hour,name,price))
    cur.execute("INSERT INTO `%s` VALUES(?,?,?)" % (name), (date, hour, price))
    conn.commit()
    conn.close


def insert_data_full(date, hour, name, price, volume):
    conn = sqlite3.connect("prices.db")
    cur = conn.cursor()
    # cur.execute("INSERT INTO `%s` VALUES(?,?,?)",(date,hour,name,price) %(table_name))
    # cur.execute("INSERT INTO tabela1 (?,?,?)" ,(date,hour,name,price))
    cur.execute("INSERT INTO `%s` VALUES(?,?,?,?)" % (name), (date, hour, price, volume))
    conn.commit()
    conn.close


def read_data(name):
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM `%s`;""" % (name))

    for linha in cursor.fetchall():
        print(linha)
    conn.close()


stocks = ['18599', '1025085', '1008677', '18626', '18628', '996550', '50509', '18621', '1127941', '18606', '18616',
          '18604', '1155784', '18620', '18617', '18633', '18642', '18696', '18639', '40433', '18651', '18645',
          '50513',
          '18657', '18663', '18666', '18667', '18669', '18670', '977700', '18790', '18672', '18682', '18691',
          '18689',
          '18692', '1073236', '18698', '18701', '1030995', '18706', '18708', '18709', '102072', '18770', '18717',
          '18724', '18729', '18736', '18608', '18738', '18740', '18742', '1073664', '1056489', '18749', '18750',
          '18764',
          '40436', '18593', '18776', '18775', '18653', '18786', '1055002', '18804', '18818', '18797', '18801',
          '18807',
          '18812', '18814', '986421', '18820', '18673']

indices = ['IBOVESPA', 'DOWJONES', 'SEP500', 'NASDAQ', 'SMALLCAP2k', 'SEP500_VIX', 'FT_SE100', 'EURO_STOXX50']

commodities = ['GOLD', 'SILVER', 'COPPER', 'PLATINUM', 'PALLADIUM', 'CRUDE_OIL WTI', 'BRENT_OIL', 'NATURAL_GAS',
               'HEATING_OIL', 'GASOLINE RBOB']

forex = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'USDBRL']

# stock=['18599','1025085','1008677','18626','18628','996550','50509','18621','1127941','18616','18604','1155784','18620','18617','18633','18642','18696','18639','40433','18651','18645','50513','18657','18663','18666','18667','18669','18670','977700','18790','18672','18682','18691','18689','18692','1073236','18698','18701','1030995','18706','18709','102072','18770','18717','18724','18736','18608','18738','18740','18742','1073664','1056489','18749','18764','40436','18593','18776','18775','18653','18786','1055002','18804','18818','18797','18801','18807','18812','18820','18673']

(page) = get_page_investing()

(stocks_names) = get_names_stocks(page, stocks)

for table_name in stocks_names:
    create_db_stocks(table_name)

for table_indices in indices:
    create_db(table_indices)

for table_commodities in commodities:
    create_db(table_commodities)

for table_forex in forex:
    create_db(table_forex)

while True:

    (hour_now, date_now, seconds_now) = time_now()

    get_page = get_page_investing()

    for i in stocks:
        # print(i)

        page_part1 = get_page.find(id="pair_" + i)
        # print(page_part1)

        page_part1_1 = page_part1.find_all(class_="bold left noWrap elp plusIconTd")[0].get_text()
        stock_name.append(page_part1_1)
        # print(stock_name)
        page_part1_2 = page_part1.find_all(class_="pid-" + i + "-last")[0].get_text()
        stock_last.append(page_part1_2)
        # print(stock_last)
        page_part1_3 = page_part1.find_all(class_="pid-" + i + "-high")[0].get_text()
        stock_high_max.append(page_part1_3)
        round1 = round(((1 - (rate / 100)) * float(page_part1_3)), 2)
        stock_high.append(str(round1))
        # print(stock_high)
        page_part1_4 = page_part1.find_all(class_="pid-" + i + "-low")[0].get_text()
        stock_low_max.append(page_part1_4)
        round1 = round(((1 + (rate / 100)) * float(page_part1_4)), 2)
        stock_low.append(str(round1))
        # print(stock_low)
        page_part1_5 = page_part1.find_all(class_="pid-" + i + "-turnover")[0].get_text()
        (stock_volume_unit) = convert_to_number(page_part1_5)
        stock_volume.append(str(stock_volume_unit))

        if t == 1:
            if k == 1:
                stock_high_max.append(page_part1_2)
                stock_low_max.append(page_part1_2)

    (ibov_now, dw_now, sep500_now, nasdaq_now, small_cap2k_now, sep500vix_now, ft_se100_now,
     euro_stoxx50_now) = get_page_investing_indices()
    (hour_now, date_now, seconds_now) = time_now()

    insert_data(date_now, hour_now, indices[0], ibov_now)
    insert_data(date_now, hour_now, indices[1], dw_now)
    insert_data(date_now, hour_now, indices[2], sep500_now)
    insert_data(date_now, hour_now, indices[3], nasdaq_now)
    insert_data(date_now, hour_now, indices[4], small_cap2k_now)
    insert_data(date_now, hour_now, indices[5], sep500vix_now)
    insert_data(date_now, hour_now, indices[6], ft_se100_now)
    insert_data(date_now, hour_now, indices[7], euro_stoxx50_now)

    (gold, silver, copper, platinum, palladium, crude_oil, brent_oil, natural_gas, heating_oil,
     gasoline) = get_page_investing_commodity()

    insert_data(date_now, hour_now, commodities[0], gold)
    insert_data(date_now, hour_now, commodities[1], silver)
    insert_data(date_now, hour_now, commodities[2], copper)
    insert_data(date_now, hour_now, commodities[3], platinum)
    insert_data(date_now, hour_now, commodities[4], palladium)
    insert_data(date_now, hour_now, commodities[5], crude_oil)
    insert_data(date_now, hour_now, commodities[6], brent_oil)
    insert_data(date_now, hour_now, commodities[7], natural_gas)
    insert_data(date_now, hour_now, commodities[8], heating_oil)
    insert_data(date_now, hour_now, commodities[9], gasoline)

    (eurusd, gbpusd, usdjpy, usdchf, audusd, usdcad, usdbrl) = get_page_investing_forex()

    insert_data(date_now, hour_now, forex[0], eurusd)
    insert_data(date_now, hour_now, forex[1], gbpusd)
    insert_data(date_now, hour_now, forex[2], usdjpy)
    insert_data(date_now, hour_now, forex[3], usdchf)
    insert_data(date_now, hour_now, forex[4], audusd)
    insert_data(date_now, hour_now, forex[5], usdcad)
    insert_data(date_now, hour_now, forex[6], usdbrl)

    for i, item in enumerate(stocks, 0):
        # print(f"======={stock_name[i]}=======")
        # print(f"{stock_name[i]}")
        (hour_now, date_now, seconds_now) = time_now()
        insert_data_full(date_now, hour_now, stock_name[i], stock_last[i], stock_volume[i])
    # print(stock_high_max[i])
    # print(stock_low_max[i])

    print(k)
    k += 1
    get_page = " "
    stock_last = []
    stock_volume_now = []
    time.sleep(60)

for table_name in stocks_names:
    read_data(table_name)

    # time.sleep(60)