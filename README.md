# dksk1oyk
Bu repo dksk1 websitesi için geliştirme aşamasında yazılmış kodları içerir. Database olarak sqlite3 kullanıyor ve her yerinde eksik var. Şu an için en temel eksik databasede relationshipleri sağlayamamış olmamda. Aynı zamanda logini de çalıştıramadım (database'deki sebebini anlamadığım bir sorundan dolayı). Register kısmı olması gerektiği gibi çalışıyor. Bu sorunları geride bırakıp diğer eksiklere bakmaya başladım ama zaman alıyor her türlü. Frontendi hemen hemen tamamen dışarıdan aldım. Bootstraple yazılmış kod mobil açısından da iş kolay olur diye düşünmüşyüm.
not: login kısmında geçici bir kod var, database'de en az bir tane member kayıtlı olduğu sürece şifre mail fark etmeksizin giriş başarılı oluyor ama tabi session user i falan yok.

# Projeyi başlatmak için #
1) Proje paketinin içerisinde (dksk1 klasörü) terminali açtıktan sonra database oluşturmak için:
```
from dksk1 import db
from dksk1.models import Member, Activity
db.create_all()
```

2)   ```python run.py```    
Localhostta direkt başlar. 
