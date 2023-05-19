###
#   Bu dosyanın varlığının tek sebebi project package sistemini birleştirip, bu dosya üstünden projeyi çalıştırabilmek
#   Package structure kullanıyoruz çünkü öteki durumda çok fazla karışıklık oluyor.
###

from dksk1 import app  # Bu __init__ den import edecek

if __name__ == "__main__":
  app.run(debug=True)

