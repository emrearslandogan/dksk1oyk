###
#   Bu dosya web app'imizde kullanacağımız çeşitli formları içerir
###

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dksk1.models import Member  # İmportalamazsak kendi yazdığımız validator fonksiyonlar çalışmaz
from flask_login import current_user
from dksk1 import bcrypt

class RegistrationForm (FlaskForm): 
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
  remember = BooleanField("Beni hatırla")


class EditContact (FlaskForm):
  email = StringField("Email")
  if current_user:
    email.default = current_user.email

  tel_no = StringField("Telefon Numarası")
  if current_user:
    tel_no.default = current_user.tel_no

  submit = SubmitField("Formu Onayla")
  

class UpdatePassword (FlaskForm):
  current_password = PasswordField("Şu anki şifreniz", validators=[DataRequired(), Length(min=4, max=20)])
  
  desired_password = PasswordField("Yeni şifreniz", validators=[DataRequired(), Length(min=4, max=20)])
  confirm_password = PasswordField("Yeni şifreyi doğrulayın", validators=[DataRequired(), EqualTo("desired_password")])

  submit = SubmitField("Şifreyi güncelle")

  def validate_current_password(self, current_password):
    user = Member.query.get(current_user.id)
    if not bcrypt.check_password_hash(bcrypt.generate_password_hash(current_password.data).decode('utf-8'), str(user.password.data)):  
      raise ValidationError("Girdiğiniz eski şifre sizin şifreniz değil")

