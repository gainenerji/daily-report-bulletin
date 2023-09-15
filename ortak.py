import requests
import pandas as pd

""" Şeffaflık Platformuna istek atmak için kullanılan fonksiyon.
    sub_url parametresi ile istenen veriyi çeker, json formatında döner.
"""
def make_request(sub_url):
    headers = {
    'x-ibm-client-id': "",
    'accept': "application/json"
    }
    main_url = "https://seffaflik.epias.com.tr/transparency/service/"
    corresponding_url = main_url + sub_url
    resp = requests.get(corresponding_url,headers=headers)
    resp.raise_for_status()
    json = resp.json()
    return json

# Girilen tabloya saat sütunu ekler
def saat_sutunu_ekle(df):
    columns = df.columns.tolist()
    columns.insert(1, 'Saat')
    df = df.reindex(columns=columns)
    for i in range(len(df["Tarih"])):
        df.loc[i,"Saat"] = df.loc[i,"Tarih"].hour
    df.reset_index(drop=True, inplace=True)
    
    return df

# Girilen tablonun günlük bazda toplamını döndürür
def daily_sum(df):
    # Tarih sütununu datetime formatına dönüştürme
    df["Tarih"] = pd.to_datetime(df["Tarih"])
    
    # Tarih sütununu indeks olarak ayarlama
    df.set_index("Tarih", inplace=True)
    
    # Saatlik bazda toplam değerleri günlük bazda toplama
    df = df.resample('D').sum(numeric_only=True)
    
    # Tarih sütununu eski formatta ayrı bir sütun olarak ekler
    df['Tarih'] = df.index
    
    # Sıralama ve sütun düzenini düzenleme
    sutunlar = list(df.columns)
    sutunlar.remove('Tarih')
    df = df[['Tarih'] + sutunlar]
    df.reset_index(drop=True, inplace=True)
    
    # Günlük bazda yeni bir df döndürme
    return df

# Girilen tablonun günlük bazda ortalamasını döndürür
def daily_mean(df):
    # Tarih sütununu datetime formatına dönüştürme
    df["Tarih"] = pd.to_datetime(df["Tarih"])
    
    # Tarih sütununu indeks olarak ayarlama
    df.set_index("Tarih", inplace=True)
    
    # Saatlik bazda toplam değerleri günlük bazda toplama
    df = df.resample('D').mean(numeric_only=True)
    
    # Tarih sütununu eski formatta ayrı bir sütun olarak ekler
    df['Tarih'] = df.index
    
    # Sıralama ve sütun düzenini düzenleme
    sutunlar = list(df.columns)
    sutunlar.remove('Tarih')
    df = df[['Tarih'] + sutunlar]
    df.reset_index(drop=True, inplace=True)
    
    # Günlük bazda yeni bir df döndürme
    return df

# Girilen tablonun aylık bazda toplamını döndürür
def monthly_sum(df):
    # Tarih sütununu datetime formatına dönüştürme
    df["Tarih"] = pd.to_datetime(df["Tarih"])
    
    # Tarih sütununu indeks olarak ayarlama
    df.set_index("Tarih", inplace=True)
    
    # Saatlik bazda toplam değerleri günlük bazda toplama
    df = df.resample('M').sum(numeric_only=True)
    
    # Tarih sütununu eski formatta ayrı bir sütun olarak ekler
    df['Tarih'] = df.index
    
    # Sıralama ve sütun düzenini düzenleme
    sutunlar = list(df.columns)
    sutunlar.remove('Tarih')
    df = df[['Tarih'] + sutunlar]
    df.reset_index(drop=True, inplace=True)
    
    # Günlük bazda yeni bir df döndürme
    return df

# Girilen tablonun aylık bazda ortalamasını döndürür
def monthly_mean(df):
    # Tarih sütununu datetime formatına dönüştürme
    df["Tarih"] = pd.to_datetime(df["Tarih"])
    
    # Tarih sütununu indeks olarak ayarlama
    df.set_index("Tarih", inplace=True)
    
    # Saatlik bazda toplam değerleri günlük bazda toplama
    df = df.resample('M').mean(numeric_only=True)
    
    # Tarih sütununu eski formatta ayrı bir sütun olarak ekler
    df['Tarih'] = df.index
    
    # Sıralama ve sütun düzenini düzenleme
    sutunlar = list(df.columns)
    sutunlar.remove('Tarih')
    df = df[['Tarih'] + sutunlar]
    df.reset_index(drop=True, inplace=True)
    
    # Günlük bazda yeni bir df döndürme
    return df