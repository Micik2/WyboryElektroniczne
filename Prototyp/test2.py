#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask, render_template, request, json, session, redirect, url_for, send_from_directory
from pony.orm import *
from werkzeug import secure_filename
from flask_images import *
import os
import sys
import random
import smtplib
from datetime import date
reload(sys)  
sys.setdefaultencoding("utf8")

app = Flask(__name__)
app.secret_key = "sekret"
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "static/"
#app.config["ALLOWED_EXTENSIONS"] = set(["png", "jpg", "jpeg"])

images = Images(app)

tas = Database()

class Obywatele(tas.Entity):
    PESEL = PrimaryKey(str)
    #email = Required(str)
    email = Optional(str)
    haslo = Optional(str)
    wyborcy = Optional("Wyborcy")
    zdjecie = Required(unicode, default="default.jpg")
class Wyborcy(tas.Entity):
    imie = Optional(unicode)
    nazwisko = Optional(unicode)
    nr_dowodu = Optional(str, unique=True)
    ulica = Optional(unicode)
    nr_lokalu = Optional(str)
    kod_pocztowy = Optional(str)
    miejscowosc = Optional(unicode)
    czy_glosowal = Optional(bool)
    wyksztalcenie = Optional(unicode)
    kraj_pochodzenia = Optional(str)
    wiek = Optional(int)
    czy_ubezwlasnowolniony = Optional(bool, default=0)
    #haslo_tymczasowe = Required(str)
    haslo_tymczasowe = Optional(str)
    nr_telefonu = Optional(int, unique=True)
    OBYWATELE_PESEL = PrimaryKey(Obywatele)

#tas.bind("mysql", host = "localhost", user = "root", passwd = "localhost", db = "tas")
tas.bind("sqlite", "database.sqlite", create_db=True)
tas.generate_mapping(create_tables=True)  

def format(nazwa_pliku):
    return '.' in nazwa_pliku and nazwa_pliku.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]
    
@app.route('/')
def main():
    if "username" in session:
        pesel = session["username"]
        return render_template("index.html", pesel = pesel)
    return render_template("index.html")

@app.route("/wybory")
def wybory():  
    if "username" in session:
        pesel = session["username"]
        lista_wyborow = []
        # ze względu na wymóg braku spacji w linku musiałem dodać '_'
        lista_wyborow.append("wybory_na_kanclerza")
        lista_wyborow.append("wybory_na_prezydenta")
        return render_template("wybory.html", pesel = pesel, wyb = lista_wyborow)
    else:
        return redirect("main")
    #lista_wyborow = []
    # z bazy trzeba będzie pobierać wszystkie wybory dziejące się aktualnie
    # aktualnie przykładowe, bez użycia bazy
    #lista_wyborow.append("Wybory na kanclerza")
    #lista_wyborow.append("Wybory na prezydenta")
    #return redirect("wylistowanieWyborow")
    #return render_template("wybory.html", wyb = lista_wyborow, pesel = session["username"]   

'''
@app.route("/kandydaci")
def kandydaci():

@app.route("/kandydat")
def kandydat():

@app.route("/glosowanie")
def glosowanie():

#@app.route("/panel")
#def panel():   
'''

@app.route("/pokazLogowanie/")
def pokazLogowanie():
    return render_template("logowanie.html")

@app.route("/pokazRejestracja/")
def pokazRejestracja():
    return render_template("rejestracja.html")    

@app.route("/pokazProfil", methods = ["POST", "GET"]) 
def pokazProfil():
    with db_session:
        obywatel = Obywatele.get(PESEL = session["username"])
        wyborca = Wyborcy.get(OBYWATELE_PESEL = session["username"])
        img_url = url_for("static", filename = obywatel.zdjecie)
        if obywatel:
            return render_template("profil.html", pesel = session["username"], 
                imie = wyborca.imie, nazwisko = wyborca.nazwisko, nr_dowodu = wyborca.nr_dowodu,
                ulica = wyborca.ulica, nr_lokalu = wyborca.nr_lokalu, 
                kod_pocztowy = wyborca.kod_pocztowy, miejscowosc = wyborca.miejscowosc,
                wyksztalcenie = wyborca.wyksztalcenie, 
                kraj_pochodzenia = wyborca.kraj_pochodzenia, wiek = wyborca.wiek, 
                nr_telefonu = wyborca.nr_telefonu, img_url = img_url)
        #return render_template("profil.html", pesel = session["username"], imie = "Jan", 
        #                                    nazwisko = "Nowak", img_url = img_url)
        else:
        #return redirect("edycjaProfilu")
            return redirect("main")

@app.route("/zmianaZdjecia", methods = ["POST", "GET"])
def zmianaZdjecia():
    f = request.files["zdjecie"]
    nazwa = secure_filename(f.filename)
    #f.save(secure_filename(f.filename))
    #f.save(secure_filename(os.path.join(app.config["UPLOAD_FOLDER"], nazwa)))
    f.save("static/" + secure_filename(nazwa))
    with db_session:
        Obywatele[session["username"]].zdjecie = nazwa
        commit()
    return redirect("pokazProfil")

@app.route("/pokazEdycjaProfilu")
def pokazEdycjaProfilu():
    return render_template("edycjaProfilu.html", wiadomosc = "Uzupełnij swoje dane, aby mieć możliwość brania udziału w głosowaniach")

@app.route("/edycjaProfilu", methods = ["POST", "GET"])
def edycjaProfilu():
    dzisiaj = date.today()
    rok = dzisiaj.year
    miesiac = dzisiaj.month
    dzien = dzisiaj.day

    #Ze względu na to, że nie żyje żaden obywatel Polski urodzony w XVIII wieku, dodaję 1900
    rok_urodzenia = 1900 + int(session["username"][:2])
    miesiac_urodzenia = int(session["username"][2:4])
    dzien_urodzenia = int(session["username"][4:6])

    lata = dzisiaj.year - rok_urodzenia
    if miesiac_urodzenia > miesiac:
        lata -= 1
    elif miesiac_urodzenia == miesiac:
        if dzien_urodzenia > dzien:
            lata -= 1

    _imie = request.form["imie"]
    _nazwisko = request.form["nazwisko"]
    _nr_dowodu = request.form["nr_dowodu"]
    _ulica = request.form["ulica"]
    _nr_lokalu = request.form["nr_lokalu"]
    _kod_pocztowy = request.form["kod_pocztowy"]
    _miejscowosc = request.form["miejscowosc"]
    _wyksztalcenie = request.form["wyksztalcenie"]
    _kraj_pochodzenia = request.form["kraj_pochodzenia"]
    _haslo_tymczasowe = session["password"]
    _nr_telefonu = request.form["nr_telefonu"]
    
    with db_session:
        #Wybory(imie = _imie, nazwisko = _nazwisko, nr_dowodu = _nr_dowodu, ulica = _ulica, 
        #        nr_lokalu = _nr_lokalu, kod_pocztowy = _kod_pocztowy, 
        #        miejscowosc = _miejscowosc, czy_glosowal = 0, wyksztalcenie = _wyksztalcenie,
        #        kraj_pochodzenia = _kraj_pochodzenia, wiek = lata,
        #        haslo_tymczasowe = session["password"], nr_telefonu = _nr_telefonu, )
        obywatel = Obywatele.get(PESEL = session["username"])
        img_url = url_for("static", filename = obywatel.zdjecie)
        Wyborcy[session["username"]].imie = _imie
        Wyborcy[session["username"]].nazwisko = _nazwisko
        Wyborcy[session["username"]].nr_dowodu = _nr_dowodu
        Wyborcy[session["username"]].ulica = _ulica
        Wyborcy[session["username"]].nr_lokalu = _nr_lokalu
        Wyborcy[session["username"]].kod_pocztowy = _kod_pocztowy
        Wyborcy[session["username"]].miejscowosc = _miejscowosc
        Wyborcy[session["username"]].czy_glosowal = 0
        Wyborcy[session["username"]].wyksztalcenie = _wyksztalcenie
        Wyborcy[session["username"]].kraj_pochodzenia = _kraj_pochodzenia
        Wyborcy[session["username"]].wiek = lata
        Wyborcy[session["username"]].haslo_tymczasowe = session["password"]
        Wyborcy[session["username"]].nr_telefonu = _nr_telefonu
        commit()
    return redirect("pokazProfil")

@app.route("/rejestracja", methods = ["POST", "GET"])  
def rejestracja():  
    _pesel = request.form["inputPesel"]
    _email = request.form["inputEmail"]
    #_haslo = request.form["inputPassword"]
    haslo = random.getrandbits(128)
    h = "%032x" % haslo
    has = str(h)

    link = "127.0.0.1:5000/pokazLogowanie"

    wiadomosc = ["From: Wybory Elektroniczne", 
            "To: micik220@gmail.com", 
            "Subject: Rejestracja",
            "",
            "Do zalogowania się użyj podanego niżej hasła:",
            has,
            "Wchodząc w ten link:",
            link]

    msg = "\r\n".join(wiadomosc)

    fromaddr = "wyboryelektroniczne@gmail.com"
    toaddrs  = _email
    username = "wyboryelektroniczne@gmail.com"
    password = "blacktron"
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

    #if _pesel and _email and _haslo:
    if _pesel and _email:
        with db_session:
            #Obywatele(PESEL = _pesel, email = _email, haslo = _haslo)
            Obywatele(PESEL = _pesel, email = _email, haslo = has)
            Wyborcy(OBYWATELE_PESEL = _pesel)
            #Wyborcy(OBYWATELE_PESEL = _pesel)
            commit()
    #return json.dumps({"message": "Użytkownik stworzony pomyślnie."})
    return json.dumps("Użytkownik stworzony pomyślnie.").encode("utf8")

@app.route("/logowanie", methods = ["POST"])
def logowanie():
    _pesel = request.form["inputPesel"]
    _haslo = request.form["inputPassword"]
    #haslo = ""
    pro = ""
    wynik = ""

    if _pesel and _haslo:
        with db_session:
            wynik = Obywatele.get(PESEL = _pesel, haslo = _haslo)
    if wynik:
        session["username"] = wynik.PESEL
        session["password"] = wynik.haslo
        with db_session:
            pro = Wyborcy.get(OBYWATELE_PESEL = wynik.PESEL)
        # return render_template("profil.html", pesel = wynik.PESEL, imie = pro.imie, 
        #                         nazwisko = pro.nazwisko, nr_dowodu = pro.nr_dowodu, 
        #                         ulica = pro.ulica, nr_lokalu = pro.nr_lokalu, 
        #                         kod_pocztowy = pro.kod_pocztowy, miejscowosc = pro.miejscowosc, 
        #                         wyksztalcenie = pro.wyksztalcenie, 
        #                         kraj_pochodzenia = pro.kraj_pochodzenia, wiek = pro.wiek,
        #                         nr_telefonu = pro.nr_telefonu)
        #return redirect("profil")
            if pro.imie:
                return redirect("pokazProfil")
            return redirect("pokazEdycjaProfilu")
    else:
        return render_template("error.html", error = "Błędne dane!")
        #return json.dumps({"message": "Błędne dane!"}).encode("utf8")
    '''return render_template("profil.html", pesel = session["username"], imie = "Jan", 
                            nazwisko = "Nowak", nr_dowodu = "ABC123456", 
                            ulica = "Testowa", nr_lokalu = "0", 
                            kod_pocztowy = "12-345", miejscowosc = "ąćęłńóśżź", 
                            wyksztalcenie = "Podstawowe", 
                            kraj_pochodzenia = "Polska", wiek = "20",
                            nr_telefonu = "123456789")'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)
