#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import Flask, render_template, request, json, session, redirect, url_for, send_from_directory
from pony.orm import *
from werkzeug import secure_filename
from flask_images import *
import os
import sys
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
    email = Required(str)
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
    czy_ubezwlasnowolniony = Optional(bool)
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
        return render_template("profil.html", pesel = session["username"], imie = "Jan", 
                                            nazwisko = "Nowak", img_url = img_url)
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

@app.route("/edycjaProfilu")
def edycjaProfilu():
    return render_template("edycjaProfilu.html")

@app.route("/rejestracja", methods = ["POST", "GET"])  
def rejestracja():  
    _pesel = request.form["inputPesel"]
    _email = request.form["inputEmail"]
    _haslo = request.form["inputPassword"]
    print "Wpisany PESEL: " + _pesel

    if _pesel and _email and _haslo:
        with db_session:
            Obywatele(PESEL = _pesel, email = _email, haslo = _haslo)
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
        return redirect("pokazProfil")
    else:
        return json.dumps({"message": "Błędne dane!"}).encode("utf8")
    '''return render_template("profil.html", pesel = session["username"], imie = "Jan", 
                            nazwisko = "Nowak", nr_dowodu = "ABC123456", 
                            ulica = "Testowa", nr_lokalu = "0", 
                            kod_pocztowy = "12-345", miejscowosc = "ąćęłńóśżź", 
                            wyksztalcenie = "Podstawowe", 
                            kraj_pochodzenia = "Polska", wiek = "20",
                            nr_telefonu = "123456789")'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)
