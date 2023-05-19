from datetime import datetime, date
from forex_python.converter import CurrencyRates  # enflasyon hesabını dolar bazlı yapıyoruz

class borcHelper:
  def __init__(self, borc_miktar, borc_yili):
    self.borc_miktar = borc_miktar
    self.borc_yili = borc_yili
  

  def enflasyon_duzeltici(borc_miktar, borc_yili):
    simdi_yil = datetime.utcnow().year
    c = CurrencyRates()
    eski_borc_usd = borc_miktar / c.get_rate("USD", "TRY", date(borc_yili, 1, 1)) # o yılın 1 ocak'ının dolar kuru alınıyor
    yeni_borc = eski_borc_usd * c.get_rate("USD", "TRY", date(simdi_yil, 1, 1)) # her dk dolar değişebildiği için sabit şekilde yine 1 ocak

    return yeni_borc
    

    