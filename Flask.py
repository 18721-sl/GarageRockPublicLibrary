from flask import Flask,g,render_template,request,redirect
#Flask is the main function of my application

import sqlite3
#Database that I used

app = Flask(__name__)

DATABASE = 'database.db'
#Database that I used to store informations (comments, pictures, links)

def get_db():
    db= getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
#This fuction is used to get the data from the database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database' , None)
    if db is not None:
        db.close()
#This fuction is used to close the database after used

@app.route('/')
def home():
    cursor = get_db().cursor()
    sql = 'SELECT * FROM comment'
    cursor.execute(sql)
    comments = cursor.fetchall()
    cursor = get_db().cursor()
    sql = 'SELECT * FROM Song'
    cursor.execute(sql)
    Songs = cursor.fetchall()
    return render_template("Garage Rock Public Library.html"  , comments=comments, Songs=Songs)
# This function is used to connect to the html file, and adding the information in the database to the website   

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cursor = get_db().cursor()
        new_Song = request.form['item_Song']
        new_comment = request.form['item_comment']
        sql = 'INSERT INTO comment(Song,comment) VALUES (?,?)'
        cursor.execute(sql,(new_Song,new_comment))
        get_db().commit()
    return redirect('/')
#This function is used to adding comment to the website and store it in database

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method =='POST':
        cursor = get_db().cursor()
        id = int(request.form['item_Song'])
        sql = 'DELETE FROM comment WHERE id=?'
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/')
#This function is used to delete the comments from the website and the database


if __name__ ==   '__main__':
    app.run(debug=True)
