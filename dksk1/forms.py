###
#   Bu dosya web app'imizde kullanacağımız çeşitli formları içerir
###

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dksk1.models import Member  # İmportalamazsak kendi yazdığımız validator fonksiyonlar çalışmaz

class RegistrationForm (FlaskForm): 

  # TODO buraya dropdown menü eklenecek oyk tarafından eklenip daha hesap oluşturmamış kişilerin listesi olacak.
  
  name = StringField("İsim", validators=[DataRequired()])
  surname = StringField("Soyisim", validators=[DataRequired()])

  email = StringField("Email", validators=[DataRequired(), Email()])
  
  tel_no = StringField("Telefon Numaranız", validators=[DataRequired()])

  giris_yili= StringField("Kola Başladığınız Yıl", validators=[DataRequired(), Length(min=4, max=4)]) 

  password = PasswordField("Şifre", validators=[DataRequired(), Length(min=4, max=20)])

  confirmPassword = PasswordField("Şifreyi Doğrula", validators=[DataRequired(), EqualTo("password")])

  submit = SubmitField("Kayıt Ol")

  def validate_tel_no(self, tel_no):
    temp_member = Member.query.filter_by(tel_no = tel_no.data).first() # ilk tel_no filtremiz, ikinci tel_no formda girilen yeni tel_no
    if temp_member:  # Eğer bu tel_no ya sahip başka bir kullanıcı varsa izin vermeyecek
      raise ValidationError("Bu telefon numarası halihazırda kullanımda, bir hata olduğunu düşünüyorsanız SAK'a erişebilirsiniz.")

  def validate_email(self, email):
    temp_member = Member.query.filter_by(email = email.data).first() # ilk tel_no filtremiz, ikinci tel_no formda girilen yeni tel_no
    if temp_member: 
      raise ValidationError("Bu email adresi numarası kullanımda, bir hata olduğunu düşünüyorsanız SAK'a erişebilirsiniz.")



class LoginForm (FlaskForm):  
  email_or_username = StringField("Emailiniz veya Kullanıcı Adınız", validators=[DataRequired()])

  password = PasswordField("Şifre", validators=[DataRequired(), Length(max=20)]) # minimum için bir validator koyamadık çünkü eski hesaplarda şifreler daha kısa hep

  submit = SubmitField("Giriş Yap")

  remember = BooleanField("Remember Me")


class RecoveryForm(FlaskForm):
  email = StringField("Hesabınıza bağlı mail adresiniz", validators=[DataRequired(), Email()])

  submit = SubmitField("Mail Gönder")


class Yeni_ykForm(FlaskForm):
  pass


class Yeni_donem(FlaskForm):
  donem = StringField("Dönemin yılları (örn: 2021-2022)", validators=[DataRequired()])
  
  aktifmi = BooleanField("Dönem aktif mi?")


class Yk_kaldir(FlaskForm):
  ### donem = TODO buraya dropdown şeklinde dönemler eklenecek
  
  submit = SubmitField("Dönem Kaldır")



