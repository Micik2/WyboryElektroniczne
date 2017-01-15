#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, json, session, redirect
from flask.ext.mysql import MySQL
import random
import smtplib
from pony.orm import *
#from werkzeug import generate_password_hash, check_password_hash
# sql alchemy  i sql object
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'sekret'

tas = Database()
 
class Obywatele(tas.Entity):
    PESEL = PrimaryKey(str)
    email = Required(str, unique=True)
    haslo = Optional(str)
    wyborcy = Optional("Wyborcy")
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
    haslo_tymczasowe = Required(str)
    nr_telefonu = Optional(int, unique=True)
    OBYWATELE_PESEL = PrimaryKey(Obywatele)
    

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_USER'] = 'Micik'
app.config['MYSQL_DATABASE_PASSWORD'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'tas'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

tas.bind("mysql", host = "localhost", user = "root", passwd = "localhost", db = "tas")
tas.generate_mapping(create_tables = True)  

@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    
@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')
    
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _pesel = request.form['inputPesel']
        _email = request.form['inputEmail']

        # validate the received values
        if _pesel and _email:
            '''with open("test.txt", 'a+') as plik:
                plik.write(_pesel + ":" + _email + "\n")'''
        
        
            #plik = open('test.txt', 'a+')
            #plik.write(_pesel + ":" + _email + " \n")
            #plik.close()
            haslo = random.getrandbits(128)
            #print "haslo value: %032x" % haslo
            h = "%032x" % haslo
            has = str(h)
            
            link = "127.0.0.1:5000/showSignIn"
            #link = "127.0.0.1:5000/showSignIn/" + str(h)
            
            wiadomosc = ["From: Wybory Elektroniczne", 
            #"To: /email/", 
            "Subject: Rejestracja",
            "",
            "Do zalogowania się użyj podanego niżej hasła:",
            has,
            "Wchodząc w ten link:",
            link]

            msg = "\r\n".join(wiadomosc)#[
              #"From: WyboryElektroniczne",
              #"To: /email/",
              #"Subject: Rejestracja na Wyborcę",
              #"",
              #"Why, oh why"
              #])
              
            fromaddr = 
            toaddrs  = _email
            username = 
            password = 
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
            
            # All Good, let's call MySQL
            '''
            conn = mysql.connect()
            cursor = conn.cursor()
            #_hashed_password = generate_password_hash(_password)
            #cursor.callproc('rejestracja4',(_name,_email,_hashed_password))
            #cursor.callproc('rejestracja4',(_name,_email,_password))
            
            insert_stmt = (
              "INSERT INTO Obywatele (PESEL, email, haslo) "
              "VALUES (%s, %s, %s)"
            )
            data = (_pesel, _email, has)
            cursor.execute(insert_stmt, data)
            
            #cursor.execute("INSERT INTO WYBORCY(PESEL, email, haslo) values ")
            #cursor.callproc('dodajUzytkownika', (_email, _password, _type, _organization, _name, _surname))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
'''
            with db_session:
                Obywatele(PESEL = _pesel, email = _email, haslo = has)
                commit()
            
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()    
        
'''@app.route('/error')
def err():
    return render_template('error.html')      '''  
      
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    
    n = 0
    _pesel = request.form['inputPesel']
    _password = request.form['inputPassword']
        
    try:
        
        if _pesel and _password:
            '''with open('test.txt', 'r') as plik:
                for line in plik:
                    if _pesel + ":" + _password in line:
                        n = 1
                if n:
                    return redirect('/userHome')
                else:
                    #return redirect('/error')
                    return render_template('error.html', error = "Zły pesel lub hasło!") 
            
            #////////////////////////////////////////////////////////////////////////
            con = mysql.connect()
            cursor = con.cursor()
            #cursor.callproc('logowanie',(_username,))
            select_stmt = "SELECT * FROM Obywatele WHERE PESEL = " + _pesel
            cursor.execute(select_stmt)
            print "HALO"
            
            data = cursor.fetchall()
            
            if len(data) > 0:
                #if check_password_hash(str(data[0][3]),_password):
                if str(data[0][2]) == _password:
                    session['user'] = data[0][0]
                    #return render_template('userHome.html')
                    return redirect('/userHome')
                else:
                    return render_template('error.html',error = 'Zły PESEL lub hasło!')
            else:
                return render_template('error.html',error = 'Zły PESEL lub hasło!')'''
                
            with db_session:
                h = tas.select("haslo from Obywatele where PESEL = $_pesel")
                print h[0]
                print _password
                print type(h[0])
                print type(_password)
                #r = select(p for p in Person if p.PESEL==_pesel)[:]
                #commit()
                #u = r[0]
                #print u.haslo
                #if u.haslo == _password:
                if h[0] == _password:
                    print "TU JESTEM"   
                    session['user'] = _pesel
                    return redirect('/userHome')
                else:
                    return render_template("error.html", error = "Zły PESEL lub hasło!")
        else:
            return render_template("error.html", error = "Zły PESEL lub hasło!")
            
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):        
        return render_template('userHome.html')
    else:
        return render_template('error.html', error = 'Nieautoryzowany dostep!')
    return render_template('userHome.html')
        
if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port = 5000)