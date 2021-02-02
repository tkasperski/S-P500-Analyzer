import streamlit         as sl
import pandas            as pd
import base64
import matplotlib.pyplot as plt
import seaborn           as sns
import numpy             as np
import yfinance          as yf

sl.title('Aplikacja S&P500')

sl.set_option('deprecation.showPyplotGlobalUse', False)
sl.sidebar.header('Dane')

# Pobieranie danych ze strony
@sl.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sortowanie wg konkretnej kolumny
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = sl.sidebar.multiselect('Sektor', sorted_sector_unique, sorted_sector_unique)

df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

sl.header('Wyświetla firmy z wybranego sektora')
sl.write('Dane: ' + str(df_selected_sector.shape[0]) + ' wierszy i  ' + str(df_selected_sector.shape[1]) + ' kolumn.')
sl.dataframe(df_selected_sector)

# https://pypi.org/project/yfinance/
# Dane do wykresow
data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "max",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Cena zamkniecia
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='red', alpha=0.3)
  plt.plot(df.Date, df.Close, color='crimson', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Data', fontweight='bold')
  plt.ylabel('Cena zamknięcia', fontweight='bold')
  return sl.pyplot()

# Suwak ilości firm
num_company = sl.sidebar.slider('Ilość firm', 1, 5)

# Przycisk wykresow 
if sl.button('Pokaż wykresy akcji'):
    sl.header('Ceny zamknięcia akcji')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
