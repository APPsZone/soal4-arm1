# app.py

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask import Markup
import matplotlib.pyplot as plt
import numpy as np
import bcrypt
import time
import datetime
import random 
import pandas as pd

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Appjunior123'
app.config['MYSQL_DB'] = 'proyek4'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/user')
def user():
    return render_template("pengguna.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (username, email, password) VALUES (%s,%s,%s)",(username, email, hash_password,))
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user WHERE username=%s", (username,))
        data = curl.fetchone()
        curl.close()

        if len(data) > 0:
            if bcrypt.hashpw(password, data["password"].encode('utf-8')) == data["password"].encode('utf-8'):
                session['username'] = data['username']
                session['email'] = data['email']
                return render_template("home.html")
            else:
                return "Password and email did not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

@app.route('/validasi', methods=["GET", "POST"])
def validasi():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM validasi ")
    data = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM validasi GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)
    return render_template("validasi.html", data=data, chart_data=chart_data, chart_labels=chart_labels) 

@app.route('/validasi2', methods=["GET", "POST"])
def validasi2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM validasi ")
    data = cur.fetchall()
    cur.execute("SELECT status, count(status) as count_status FROM validasi GROUP BY status")
    status_count = cur.fetchall()

    chart_labels = []
    chart_data = []
    for st in status_count:
        chart_labels.append(str(st['status']))
        chart_data.append(st['count_status'])

    print(chart_labels)
    return render_template("validasi2.html", data=data, chart_data=chart_data, chart_labels=chart_labels) 

@app.route("/add_chart_validasi")
def chart_validasi():
    cur = mysql.connection.cursor()
    data_1 = cur.execute('SELECT * FROM validasi WHERE Id = GOOD', (id))
    ok_data = data['data_1'].count()
    data_2 = cur.execute('SELECT * FROM validasi WHERE Id = NOT GOOD', (id))
    reject_data = data['data_2'].count()
    labels = ["GOOD","NOT GOOD"]
    values = int([ok_data, reject_data])
    return render_template('validasi.html', values=values, labels=labels)

@app.route('/edit_validasi/<id>', methods = ['POST', 'GET'])
def edit_validasi(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM validasi WHERE Id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('fly_validasi.html', data = data[0])

@app.route('/update_validasi/<Id>', methods=['POST'])
def update_validasi(Id):
    if request.form['btnradio'] == 'GOOD':
        cur = mysql.connection.cursor()
        letterz = ['GOOD']
        cur.execute( "UPDATE validasi SET status = %s WHERE Id = %s", (letterz, Id))
        mysql.connection.commit()
        return redirect(url_for('validasi'))
    
    if request.form['btnradio'] == 'NOT GOOD':
        cur = mysql.connection.cursor()
        letterz = ['NOT GOOD']
        cur.execute( "UPDATE validasi SET status = %s WHERE Id = %s", (letterz, Id))
        mysql.connection.commit()
        return redirect(url_for('validasi'))
    
@app.route('/add_validasi', methods=["POST"])
def add_validasi():
    n = request.form['btnradio']
    converted_num = int(n)
    for i in range(converted_num):
        letters = ['GOOD', 'NOT GOOD']
        random_index = random.choices(letters)
        letter = ['Upside Ohlins', 'Handle Bar Rizoma', 'Velg Rotobox', 'Kabon Kevlar Parts',]
        random_index1 = random.choices(letter)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO validasi (nama_produk, status) VALUES (%s, %s)", (random_index1, random_index))
        mysql.connection.commit()
        time.sleep(5)
    return redirect(url_for('validasi'))

@app.route('/delete_validasi/<string:id_data>', methods=["GET"])
def delete_validasi(id_data):
    cur= mysql.connection.cursor()
    cur.execute("DELETE FROM validasi WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('validasi'))

@app.route("/add_chart_delivery")
def chart_delivery():
    cur = mysql.connection.cursor()
    data_3 = cur.execute('SELECT * FROM delivery WHERE Id = Delivered', (id))
    delivered_data = data['data_3'].count()
    data_4 = cur.execute('SELECT * FROM delivery WHERE Id = Onhold', (id))
    onhold_data = data['data_4'].count()
    labels2 = ["Delivered","Onhold"]
    values2 = int([delivered_data, onhold_data])
    return render_template('delivery.html', values2=values2, labels2=labels2)

@app.route('/delivery', methods=["GET", "POST"])
def delivery():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM delivery ")
    hasil = cur.fetchall()
    cur.execute("SELECT stat, count(stat) as count_stat FROM delivery GROUP BY stat")
    status_count_delivery = cur.fetchall()
    chart_labels_delivery = []
    chart_data_delivery = []
    for x in status_count_delivery:
        chart_labels_delivery.append(str(x['stat']))
        chart_data_delivery.append(x['count_stat'])

    print(chart_labels_delivery)
    return render_template("delivery.html", hasil=hasil, chart_labels_delivery=chart_labels_delivery, chart_data_delivery=chart_data_delivery) 

@app.route('/delivery2', methods=["GET", "POST"])
def delivery2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM delivery ")
    hasil = cur.fetchall()
    cur.execute("SELECT stat, count(stat) as count_stat FROM delivery GROUP BY stat")
    status_count2 = cur.fetchall()
    chart_labels2 = []
    chart_data2 = []
    for x in status_count2:
        chart_labels2.append(str(x['stat']))
        chart_data2.append(x['count_stat'])

    print(chart_labels2)
    
    return render_template("delivery2.html", hasil=hasil, chart_labels2=chart_labels2, chart_data2=chart_data2) 

@app.route('/edit_delivery/<id>', methods = ['POST', 'GET'])
def edit_delivery(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM delivery WHERE Id = %s', (id))
    hasil = cur.fetchall()
    cur.close()
    print(hasil[0])
    return render_template('fly_delivery.html', hasil = hasil[0])

@app.route('/update_delivery/<Id>', methods=['POST'])
def update_delivery(Id):
    if request.form['btnradiodelivery'] == 'Delivered':
        cur = mysql.connection.cursor()
        letterz2 = ['Delivered']
        cur.execute( "UPDATE delivery SET stat = %s WHERE Id = %s", (letterz2, Id))
        mysql.connection.commit()
        return redirect(url_for('delivery'))
    
    if request.form['btnradiodelivery'] == 'Onhold':
        cur = mysql.connection.cursor()
        letterz2 = ['Onhold']
        cur.execute( "UPDATE delivery SET stat = %s WHERE Id = %s", (letterz2, Id))
        mysql.connection.commit()
        return redirect(url_for('delivery'))

@app.route('/add_delivery', methods=["POST"])
def add_delivery():
    m = request.form['btnradio']
    converted_num = int(m)
    for i in range(converted_num):
        letters = ['Delivered', 'Onhold']
        random_index = random.choices(letters)
        letter = ['Upside Ohlins $', 'Handle Bar Rizoma $', 'Velg Rotobox $', 'Kabon Kevlar Parts $',]
        random_index1 = random.choices(letter)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO delivery (produk, stat) VALUES (%s, %s)", (random_index1, random_index))
        mysql.connection.commit()
        time.sleep(5)
    return redirect(url_for('delivery'))

@app.route('/delete_delivery/<string:id_data>', methods=["GET"])
def delete_delivery(id_data):
    cur= mysql.connection.cursor()
    cur.execute("DELETE FROM delivery WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('delivery'))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")
    
if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(host = '0.0.0.0', debug=True)
