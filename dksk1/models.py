###
#   Bu dosya web app'imizde kullanmak üzere yarattığımız database model lerini içerir.
###

from datetime import datetime
from dksk1 import db, login_manager
from flask_login import UserMixin

# Bu parça flask_login in çalışması için. Nasıl çalışıyor ben de bilmiyorum.
@login_manager.user_loader
def load_user(user_id):
  return Member.query.get(int(user_id))

def get_year():
  return datetime.utcnow().year

class Member(UserMixin, db.Model):   # SQLAlchemy databasei oop tipi araçlarla yönetmemize olanak tanır. Burada kullanıcılar için bir model oluşturduk ve bunların özelliklerini ekledik.
  id = db.Column(db.Integer, primary_key = True) # it means that the main thing we will look for in a element is it's id (bcs it is primary key)
  username = db.Column(db.String, unique = True, nullable = False)  # username i sistem otomatik atacayacak. ascii standartında isimler+soyisim+giriş yılının son iki hanesi şeklinde. Yani emrearslandogan22 olacak. 
  # TODO burada dropdown menü olacak name surname oradan çekilecek
  #name = db.Column(db.String(20), unique = False, nullable = False)
  #surname = db.Column(db.String(20), unique = False, nullable = False)
  email = db.Column(db.String(120), unique = True, nullable = False)
  tel_no = db.Column(db.String, unique = True, nullable = False)  # zaten site üstünden sms atma imkanı falan olmadığı için string olarak depoluyoruz. 
  giris_yili = db.Column(db.Integer, unique = False, nullable = False, default= datetime.now().year)  # kişinin kola giriş yılı. Değer verilmemişse hesabın oluşturulduğu yıl.
  password = db.Column(db.String, nullable = False)  # şifre şu anda düzyazı şeklinde depolanıyor. şifresini unutana mail gidecek direkt.
  
  # TODO relationship işleri bundan anlayan biri bulup yaptırılacak
  #teknik_sorumluluklari = db.relationship('Activity', backref='teknik_sorumlusu', lazy=True, foreign_keys='Activity.teknik_sorumlu_id')
  #responsible_activities = db.relationship('Activity', backref='etkinlik_sorumlusu', lazy=True, foreign_keys='Activity.etkinlik_sorumlu_id')

  def __repr__(self):
    return f"Üye('{self.username}','{self.tel_no}')"  # bu satır biz databasei query den direkt çekmek istediğimizde nasıl gözükeceğini gösteriyor.  

class Activity(db.Model):    # topluluk bünyesinde gidilen etkinlikler için yaratılan table
  id = db.Column(db.Integer, primary_key = True)
  starting_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())   # etkinlik için tarih verilmezse bugün gidilmiş şeklinde alınır.
  ending_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())   
  location = db.Column(db.String, nullable = False, default = "Ankara")
  ## TODO etkinlik raporu için yer eklenecek
  malzeme_sorumlusu = db.Column(db.String, nullable = True, default = "OYK")  # TODO buraya default olarak aktif yk ları yazdır
  
  #teknik_sorumlu_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable = False)  # burada relationship kullanacağız. Yani user modelinden bir elemanı direkt buraya bağlayacağız
  #etkinlik_sorumlu_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable = False)  # es ve ts için one-to many relationship kullandık. Çünkü bir etkinliğin sadece bir ts'si veya es si olur. ms yi farklı yazacağız çünkü birden fazla ms oluyor.

  #teknik_sorumlu = db.relationship('Member', foreign_keys=[teknik_sorumlu_id])
  #etkinlik_sorumlu = db.relationship('Member', foreign_keys=[etkinlik_sorumlu_id])

  def __repr__(self):
    return f"Etkinlik('{self.location}', '{self.date}')"
  #  return f"Etkinlik('{self.location}')"


class YK_Listesi(db.Model):   # relationship kullanmak yerine basit bir table oluşturduk, buraya da dict halinde yk üyelerini yükleyeceğiz
  id = db.Column(db.Integer, primary_key = True)
  donem = db.Column(db.String(), nullable = False, default = str(get_year()) + str(get_year()+1) )
  oyk = db.Column(db.PickleType(), nullable = False) 
  dyk1 = db.Column(db.PickleType(), nullable = False)
  dyk2 = db.Column(db.PickleType(), nullable = False) 
  kykmuko = db.Column(db.PickleType(), nullable = False) 
  kykkuzey = db.Column(db.PickleType(), nullable = False) 
  bk1 = db.Column(db.PickleType(), nullable = False) 
  bk2 = db.Column(db.PickleType(), nullable = False) 
  dk1 = db.Column(db.PickleType(), nullable = False)
  dk2 = db.Column(db.PickleType(), nullable = False) 
  dk3 = db.Column(db.PickleType(), nullable = False) 


"""
    oyk: ortak yürütme kurulu üyesi
    dyk = dağcılık yürütme kurulu üyesi
    kykmuko = muko kayak yürütme kurulu
    kykkuzey = kuzey kayak yürütme kurulu
    bk = basın kurulu üyesi
    dyk = denetleme kurulu üyesi 
"""

###
#   Buradan sonrası normalde ayrılması gereken, 
#   ancak circular import sorununu çözemediğim için buraya attığım fonksiyonlar
###

def get_dict_by_tag(dict_list, tag):
  for d in dict_list:
    if d["tag"] == tag:
      return d
    else: 
      continue

def yk_olustur(tag, name, surname, tel_no, email): # yk 
  yk = {
    "tag" : tag,  # yk'nın görevi: oyk, dyk(1-2), kykmuko, kykkuzey, bk(1-2), dyk(1-2-3) olabilir
    "name" : name,
    "surname" : surname,
    "tel_no" : tel_no,
    "email" : email
  }
  return yk

def yk_db_isle(yk_liste):
  donem = YK_Listesi(
    oyk=get_dict_by_tag(yk_liste, "oyk"), 
    dyk1=get_dict_by_tag(yk_liste, "dyk1"), 
    dyk2=get_dict_by_tag(yk_liste, "dyk2"), 
    kykmuko=get_dict_by_tag(yk_liste, "kykmuko"), 
    kykkuzey=get_dict_by_tag(yk_liste, "kykkuzey"), 
    bk1=get_dict_by_tag(yk_liste, "bk1"), 
    bk2=get_dict_by_tag(yk_liste, "bk2"), 
    dk1=get_dict_by_tag(yk_liste, "dk1"), 
    dk2=get_dict_by_tag(yk_liste, "dk2"), 
    dk3=get_dict_by_tag(yk_liste, "dk3"))
    
  db.session.add()
  db.session.commit()















