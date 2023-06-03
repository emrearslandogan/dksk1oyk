###
#   Bu dosya web app'imiz içerisinde kullandığımız çeşitli route'ları içerir.
###

from dksk1 import app, db, bcrypt, login_manager
from flask import render_template, url_for, flash, redirect
from dksk1.models import Member, Activity, YK_Listesi
from dksk1.forms import RegistrationForm, LoginForm, EditContact, UpdatePassword
from flask_login import login_user, logout_user, current_user, login_required

# Site için route oluşturma işi
 

@app.route("/")
@app.route("/home")
def startPage():
  return render_template("startPage.html")


@app.route("/register", methods=["GET", "POST"])
def registrationPage():
  if current_user.is_authenticated:  # eğer kullanıcı giriş yapmışsa ve buraya tekrar erişmeye çalışırsa, homepage e gönderilir
    flash("Halihazırda giriş yapıldı", "info")
    return redirect(url_for("startPage"))
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
  if current_user.is_authenticated:  # eğer kullanıcı giriş yapmışsa ve buraya tekrar erişmeye çalışırsa, homepage e gönderilir
    flash("Halihazırda giriş yapıldı", "info")
    return redirect(url_for("startPage"))
  form = LoginForm()
  try: 
    if form.validate_on_submit():
      if form.email_or_username.data.find("@") != -1: # yani giriş için email kullanıldıysa
        user = Member.query.filter_by(email=str(form.email_or_username.data)).first()
        if user and bcrypt.check_password_hash(user.password, str(form.password.data)) :
          login_user(user, remember=form.remember.data)
          flash("Giriş başarılı", "success")
          return redirect(url_for("startPage"))
        else:
          flash("Giriş başarısız, bir daha deneyiniz", "warning")

      elif form.email_or_username.data.find("@") == -1:  # giriş için kullanıcı adı kullanıldıysa
        user = Member.query.filter_by(username=str(form.email_or_username.data)).first()
        if user and bcrypt.check_password_hash(user.password, str(form.password.data)):
          login_user(user, remember=form.remember.data)
          flash("Giriş başarılı", "success")
          return redirect(url_for("startPage"))
        else:
          flash("Giriş başarısız, bir daha deneyiniz", "warning")
  except Exception as e:
    flash(e, "danger")
    flash("Bir hata oluştu, girdiğiniz bilgileri kontrol ederek bir daha deneyiniz. Eğer hata devam ederse SAK ile iletişime geçiniz.", "warning")
  
  return render_template("loginPage.html", title="login", form=form)


@app.route("/logout")
def logoutPage():
  logout_user()
  flash("Başarıyla çıkış yapıldı", "success")
  return redirect(url_for("startPage"))


@app.route("/profile")
@login_required
def profilePage():
  return render_template("profilePage.html", title="profile", userinfo= current_user)

@app.route("/profileedit", methods=["GET", "POST"])
@login_required
def profileeditPage():
  form = EditContact()
  if form.validate_on_submit():
    user = Member.query.get(current_user.id)
    if form.email.data:
      user.email = form.email.data
    if form.tel_no.data:  # boş bırakılırsa iş karışmasın diye
      user.tel_no = form.tel_no.data
    db.session.commit()

    if not (form.tel_no.data and form.email.data):  # yani ne email ne tel no değiştirilmediyse
      flash("Hiçbir şey değiştirilmedi", "info")
      return redirect(url_for("profilePage"))

    flash("Bilgileriniz başarıyla güncellendi!", "success")
    return redirect(url_for("profilePage"))

  return render_template("profileeditPage.html", title="edit", form=form)

@app.route("/updatepassword", methods=["GET", "POST"])
@login_required
def updatepasswordPage():
  form = UpdatePassword()
  if form.validate_on_submit:
    user = Member.query.get(current_user.id)
    if form.desired_password.data:
      user.password = bcrypt.generate_password_hash(form.desired_password.data)
      db.session.commit()

      flash("Şifreniz başarıyla değiştirildi!", "success")
      return redirect(url_for("profilePage"))

  return render_template("passwordchangePage.html", title="password change", form=form)

@app.route("/recovery")
def recoveryPage():
  flash("Şifrenizi unuttuysanız lütfen yk ile iletişime geçiniz", "warning")
  return redirect(url_for("contactPage"))


"""
@app.route("/contact")
def contactPage():
  yklist = []
  yklar = YK_Listesi.query.first()

  for yk in yklar:
    yklist.append({
      "donem": yklar.donem,
      "oyk": yklar.oyk,
      "dyk1": yklar.dyk1,
      "dyk2": yklar.dyk2,
      "kykmuko": yklar.kykmuko,
      "kykkuzey": yklar.kykkuzey,
      "bk1": yklar.bk1,
      "bk2": yklar.bk2,
      "dk1": yklar.dk1,
      "dk2": yklar.dk2,
      "dk3": yklar.dk3
    })

  return render_template("contactPage.hmtl", title="contact", yklist = yklist)
"""

