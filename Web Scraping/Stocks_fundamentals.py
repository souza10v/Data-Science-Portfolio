#!pip install xlsxwriter

import requests
from bs4 import BeautifulSoup
import csv
import xlsxwriter

k=0
column_cont=0

csv_save=[]
csv_save2=[]

stocks_list=['petr4', 'itub4', 'itsa4','itub3' ]

info=['VALOR ATUAL','MIN. 52 SEMANAS','MÁX 52 SEMANAS','DIVIDEND YELD','VALORIZAÇÃO 12M','TIPO','TAG ALONG','LIQUIDEZ MÉDIA DIÁRIA','PARTICIÇÃO IBOV','MERCADO DE OPÇÕES','P/L','EV/EBITDA','P/VP','EV/EBIT','P/EBITDA','P/EBIT','VPA','P/ATIVO','LPA','P/SR','P/CAP. GIRO','P/ATIVO CIRC.LIQ.','DIVIDA LIQ/PL','DIVIDA LIQ/EBITDA','DIVIDA LÍQ/EBIT','PL/ATIVOS','PASSIVOS/ATIVOS','LIQ. CORRENTE','MARGEM BRUTA','MARGEM EBITDA','MARGEM EBIT','MARGEM LIQUIDA','ROE','ROA','ROIC','GIRO ATIVOS','CAGR RECEITAS 5 ANOS','CAGR LUCROS 5 ANOS', 'ANO PASSADO','ANO ATUAL','COMPARAÇÃO','PROVISIONADO','COMPARAÇÃO + PROVISIONADO','PATRIMÔNIO LÍQUIDO','ATIVOS','ATIVO CIRCULANTE','DÍVIDA BRUTA','DISPONIBILIDADE','DÍVIDA LÍQUIDA','VALOR DE MERCADO','VALOR DE FIRMA','Nº TOTAL DE PAPEIS','SEGMENTO DE LISTAGEM','FREE FLOAT','SETOR DE ATUAÇÃO','SUBSETOR DE ATUAÇÃO','SEGMENTO DE ATUAÇÃO']

url_base="https://statusinvest.com.br/acoes/"

def replace(aux):
    aux = str(aux)
    aux = aux.replace("[", "")
    aux = aux.replace("]", "")
    aux = aux.replace("'", "")
    aux = aux.replace(".", "")
    return(aux)

for stocks in stocks_list:
   print(stocks)
   k=0
   csv_save.append(stocks)
   url_stocks=str(url_base+stocks)
   page = requests.get(url_stocks)

   get_page = BeautifulSoup(page.text, 'html.parser')
   page_part1=get_page.find(class_='top-info has-special d-flex justify-between flex-wrap')
   page_part2=get_page.find(class_='top-info top-info-1 top-info-sm-2 top-info-md-3 top-info-xl-n sm d-flex justify-between')
   page_part3=get_page.find(class_='d-flex flex-wrap')
   page_part4=get_page.find(class_='top-info width-auto sm d-flex justify-between bg-main-gd-h white-text')
   page_part5=get_page.find(class_='top-info info-3 sm d-flex justify-between mb-5')
   page_part6=get_page.find(class_='top-info top-info-1 top-info-sm-2 top-info-md-n sm d-flex justify-between ')

   page_part1_1=page_part1.find_all("strong")
   page_part1_2=page_part2.find_all("strong")
   page_part1_3=page_part3.find_all("strong")
   page_part1_4=page_part4.find_all("strong")
   page_part1_5=page_part5.find_all("strong")
   page_part1_6=page_part6.find_all("strong")

   for read_values in page_part1_1:
    if len(read_values) == 0:
         break
    else:
      value=(read_values.contents[0])
      k+=1
      if k == 1:
         #print(f"Valor atual: {value}.")
         csv_save.append(value)
      if k == 2:
         #print(f"Min 52 semanas: {value}.")
         csv_save.append(value)
      if k == 3:
         #print(f"Máx 52 semanas: {value}.")
         csv_save.append(value)
      if k == 4:
         #print(f"Dividend Yeld: {value}.")
         csv_save.append(value)
      if k == 5:
         #print(f"Varlorização 12M: {value}.")
         csv_save.append(value)
         k=0;
         break

   for read_values in page_part1_2:
    if len(read_values) == 0:
         break
    else:
      value=(read_values.contents[0])
      k+=1
      value = value.replace(".", "")
      if k == 1:
         #print(f"Tipo: {value}.")
         csv_save.append(value)
      if k == 2:
         #print(f"Tag Along: {value}.")
         csv_save.append(value)
      if k == 3:
         #print(f"Liquidez Média Diária: {value}.")
         csv_save.append(value)
      if k == 6:
         #print(f"Participação Ibovespa: {value}.")
         csv_save.append(value)
      if k == 8:
         #print(f"Mercado de opções: {value}.")
         csv_save.append(value)
         k=0;
         break

   for read_values in page_part1_3:
    if len(read_values) == 0:
         break
    else:
      value=(read_values.contents[0])
      k+=1
      if k == 2:
         #print(f"P/L: {value}.")
         csv_save.append(value)
      if k == 3:
         #print(f"EV/EBITIDA: {value}.")
         csv_save.append(value)
      if k == 4:
         #print(f"P/VP: {value}.")
         csv_save.append(value)
      if k == 5:
         #print(f"EV/EBIT: {value}.")
         csv_save.append(value)
      if k == 6:
         #print(f"P/EBITDA: {value}.")
         csv_save.append(value)
      if k == 7:
         #print(f"P/EBITDA: {value}.")
         csv_save.append(value)
      if k == 8:
         #print(f"VPA: {value}.")
         csv_save.append(value)
      if k == 9:
         #print(f"P/ATIVO: {value}.")
         csv_save.append(value)
      if k == 10:
         #print(f"LPA: {value}.")
         csv_save.append(value)
      if k == 11:
         #print(f"P/SR: {value}.")
         csv_save.append(value)
      if k == 12:
         #print(f"P/Cap. Giro: {value}.")
         csv_save.append(value)
      if k == 13:
         #print(f"P/Ativo Circ Liq.: {value}.")
         csv_save.append(value)

      if k == 15:
         #print(f"Dívida Líq/PL: {value}.")
         csv_save.append(value)
      if k == 16:
         #print(f"Dívida Líq/EBITDA: {value}.")
         csv_save.append(value)
      if k == 17:
         #print(f"Dívida Líq/EBIT: {value}.")
         csv_save.append(value)
      if k == 18:
         #print(f"PL/Ativos: {value}.")
         csv_save.append(value)
      if k == 19:
         #print(f"Passivos/Ativos: {value}.")
         csv_save.append(value)
      if k == 20:
         #print(f"Liquidez Corrent: {value}.")
         csv_save.append(value)

      if k == 22:
         #print(f"M. Bruta: {value}.")
         csv_save.append(value)
      if k == 23:
         #print(f"M. Ebitda: {value}.")
         csv_save.append(value)
      if k == 24:
         #print(f" M. Ebit: {value}.")
         csv_save.append(value)
      if k == 25:
         #print(f" M. Liquida: {value}.")
         csv_save.append(value)

      if k == 27:
         #print(f"ROE: {value}.")
         csv_save.append(value)
      if k == 28:
         #print(f"ROA: {value}.")
         csv_save.append(value)
      if k == 29:
         #print(f"ROIC: {value}.")
         csv_save.append(value)
      if k == 30:
         #print(f"Giro Ativos: {value}.")
         csv_save.append(value)

      if k == 32:
         #print(f"Cagr Receitas 5 anos: {value}.")
         csv_save.append(value)
      if k == 33:
         #print(f"Cagr Lucros 5 anos: {value}.")
         csv_save.append(value)
         k=0;
         break

   for read_values in page_part1_4:
    if len(read_values) == 0:
         break
    else:
      value=(read_values.contents[0])
      k+=1
      if k == 1:
         #print(f"Ano Passado: {value}.")
         csv_save.append(value)
      if k == 2:
         #print(f"Ano Atual: {value}.")
         csv_save.append(value)
      if k == 3:
         #print(f"Comparação: {value}.")
         csv_save.append(value)
      if k == 4:
         #print(f"Provisionado: {value}.")
         csv_save.append(value)
      if k == 5:
         #print(f"Comparação + Provisionado: {value}.")
         csv_save.append(value)
         k=0;
         break

   for read_values in page_part1_5:
    if len(read_values) == 0:
         break
    else:
      value=(read_values.contents[0])
      value=(read_values.contents)
      (value)=replace(value)
      k+=1
      if k == 1:
         #print(f"Patrimônio Líquido: {value}.")
         csv_save.append(value)
      if k == 2:
         #print(f"Ativos: {value}.")
         csv_save.append(value)
      if k == 3:
         #print(f"Ativo Circulante: {value}.")
         csv_save.append(value)
      if k == 4:
         #print(f"Dívida Bruta: {value}.")
         csv_save.append(value)
      if k == 5:
         #print(f"Disponibilidade: {value}.")
         csv_save.append(value)
      if k == 6:
         #print(f"Dívida Líquida: {value}.")
         csv_save.append(value)
      if k == 7:
         #print(f"Valor de Mercado: {value}.")
         csv_save.append(value)
      if k == 8:
         #print(f"Valor de Firma: {value}.")
         csv_save.append(value)
      if k == 9:
         #print(f"Nº Total de Papeis: {value}.")
         csv_save.append(value)
      if k == 10:
         #print(f"Segmento de Listagem: {value}.")
         csv_save.append(value)
      if k == 11:
         #print(f"Free Float: {value}.")
         csv_save.append(value)
         k=0;
         break

   for read_values in page_part1_6:
      value=(read_values.contents[0])
      k+=1
      if k == 1:
         #print(f"Setor de Atuação: {value}.")
         csv_save.append(value)
      if k == 2:
         #(f"Subsetor de atuação: {value}.")
         csv_save.append(value)
      if k == 3:
         #print(f"Segmento de atuação: {value}.")
         csv_save.append(value)
         k=0;
         break
   #print(csv_save)
   csv_save2.append(csv_save)
   csv_save=[]


with xlsxwriter.Workbook('status_invest.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num1, data in enumerate(stocks_list):
          worksheet.write(0,row_num1+1,data)

    for row_num2, info in enumerate(info):
          worksheet.write(row_num2+1,0,info)

    for row_data, data in enumerate(csv_save2):
        for row_data_aux, data_aux in enumerate(data):
          worksheet.write(row_data_aux,row_data+1,data_aux)
          #print(f'{row_data_aux}, {row_data+1}, {data_aux}')