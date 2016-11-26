#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, json, session, redirect
#from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sekret'
 


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
    _pesel = request.form['inputPesel']
    _email = request.form['inputEmail']

    # validate the received values
    if _pesel and _email:
        with open("test.txt", 'a+') as plik:
            plik.write(_pesel + ":" + _email + "\n")
    
    
        #plik = open('test.txt', 'a+')
        #plik.write(_pesel + ":" + _email + " \n")
        #plik.close()
            
        
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    n = 0
    _pesel = request.form['inputPesel']
    _password = request.form['inputPassword']
    
    if _pesel and _password:
        with open('test.txt', 'r') as plik:
            for line in plik:
                if _pesel + ":" + _password in line:
                    n = 1
            if n:
                return redirect('/userHome')
            else:
                #return redirect('/error')
                return render_template('error.html', error = "Zły pesel lub hasło!")    
        

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')
        
if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5000)