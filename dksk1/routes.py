###
#   Bu dosya web app'imiz içerisinde kullandığımız çeşitli route'ları içerir.
###

from dksk1 import app, db, bcrypt, login_manager
from flask import render_template, url_for, flash, redirect
from dksk1.models import Member, Activity
from dksk1.forms import RegistrationForm, LoginForm, RecoveryForm
from flask_login import login_user

# Site için route oluşturma işi
 



@app.route("/")
@app.route("/home")
def startPage():
  return render_template("startPage.html")


@app.route("/register", methods=["GET", "POST"])
def registrationPage():
  form = RegistrationForm() # burada forms.py dan bir instance oluşturduk bunu da html renderera geçireceğiz  
  if form.validate_on_submit():
    try:
      hashed_pw = bcrypt.generate_password_hash(form.password.data)
      kullanici_adi = str(form.email.data)[:form.email.data.index("@")] + form.giris_yili.data[2:] # baştan @ olan kısma kadar maili ve giris yılının son iki hanesini alıp username yapıyor
      user = Member(name= form.name.data, surname = form.surname.data, username=kullanici_adi, email = form.email.data, tel_no = form.tel_no.data, giris_yili = form.giris_yili.data, password = hashed_pw)  # user i database a kaydetmek için oluşturduk
      db.session.add(user)
      db.session.commit()
      flash(f"{kullanici_adi} kullanıcı adlı hesap başarıyla oluşturuldu!, giriş yapabilirsiniz", "success")
      return redirect(url_for("loginPage"))
    except Exception as e:
      flash(e, "danger")
      flash("Bir hata oluştu, bir daha deneyiniz. Devam ederse SAK ile iletişime geçiniz", "warning")

  return render_template("registrationPage.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def loginPage():
  form = LoginForm()

  if form.validate_on_submit():
    if form.email_or_username.data.find("@") != -1: # yani giriş için email kullanıldıysa
      user = Member.query.filter_by(email=str(form.email_or_username.data)).first()
      if bcrypt.check_password_hash(user.password, str(form.password.data)) :
        login_user(user)
        flash("Giriş başarılı", "success")
        return redirect(url_for("startPage"))
      else:
        flash("Giriş başarısız, bir daha deneyiniz", "warning")

    elif form.email_or_username.data.find("@") == -1:  # giriş için kullanıcı adı kullanıldıysa
      user = Member.query.filter_by(username=str(form.email_or_username.data)).first()
      if bcrypt.check_password_hash(user.password, str(form.password.data)):
        login_user(user)
        flash("Giriş başarılı", "success")
        return redirect(url_for("startPage"))
      else:
        flash("Giriş başarısız, bir daha deneyiniz", "warning")

  return render_template("loginPage.html", title="login", form=form)


@app.route("/recovery", methods=["GET", "POST"])
def recoveryPage():
  form = recoveryForm()
  if form.validate_on_submit():
    flash(f"Hesabınız varsa, {form.email.data} mailine şifreniz gönderildi", "success")
    return redirect(url_for("loginPage"))
  return render_template("recoveryPage.html", title="login", form=form)



