from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import psycopg2



app = Flask(__name__)

#Connection to postgresql

conn = psycopg2.connect(database="researchManagement", 
                        user="zackery",
                        password="zackery1234", 
                        host="localhost", port="5432")

#######################======================
# create a cursor
cur = conn.cursor()
  
# if you already have any table or not id doesnt matter this 
# will create a products table for you.
cur.execute(
    '''CREATE TABLE IF NOT EXISTS products (id serial \
    PRIMARY KEY, name varchar(100), price float);''')
  
# Insert some data into the table
cur.execute(
    '''INSERT INTO products (name, price) VALUES \
    ('Apple', 1.99), ('Orange', 0.99), ('Banana', 0.59);''')
  
# commit the changes
conn.commit()
  
# close the cursor and connection
cur.close()
conn.close()

########################=======================
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zackery:zackery1234@localhost/researchManagement'
# db=SQLAlchemy(app)

#db model
# class Students(db.Model, UserMixin):
#     __tablename__="students"
#     id = db.Column(db.Integer, primary_key=True)
#     fname = db.Column(db.String(20), nullable=False)
#     mname = db.Column(db.String(20), nullable=True)
#     lname = db.Column(db.String(20), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     username = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(80), nullable=False)
    
#     def __init__(self, fname,mname,lname,age,username,password):
#         self.fname=fname
#         self.mname=mname
#         self.lname=lname
#         self.age=age
#         self.username=username
#         self.password=password


#Routing
# @app.get("/")
# def home():
#     return render_template("main.html")  


# @app.route("/login")
# def login():
#     return render_template("login.html")  


# @app.route("/signup")
# def signup():
#     return render_template("signup.html")  

@app.route('/')
def index():
    # Connect to the database
    conn = psycopg2.connect(database="researchManagement", 
                        user="zackery",
                        password="zackery1234", 
                        host="localhost", port="5432")
    # create a cursor
    cur = conn.cursor()
    # Select all products from the table
    cur.execute('''SELECT * FROM products''')
    # Fetch the data
    data = cur.fetchall()
    # close the cursor and connection
    cur.close()
    conn.close()
    return render_template('index.html', data=data)


#Route Submit
# @app.route("/submit", methods=['GET', 'POST'])
# def submit():
#     if request.method == 'POST':
#         fname = request.form['fname']
#         mname = request.form['mname']
#         lname = request.form['lname']
#         age = request.form['age']
#         username = request.form['username']
#         password = request.form['password']
        
#         student = Students(fname,mname,lname,age,username,password)
#         db.session.add(student)
#         db.session.commit()


@app.route('/create', methods=['POST'])
def create():
    conn = psycopg2.connect(database="researchManagement", 
                        user="zackery",
                        password="zackery1234", 
                        host="localhost", port="5432")
  
    cur = conn.cursor()
  
    # Get the data from the form
    name = request.form['name']
    price = request.form['price']
  
    # Insert the data into the table
    cur.execute(
        '''INSERT INTO products \
        (name, price) VALUES (%s, %s)''',
        (name, price))
  
    # commit the changes
    conn.commit()
  
    # close the cursor and connection
    cur.close()
    conn.close()
  
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn = psycopg2.connect(database="researchManagement", 
                        user="zackery",
                        password="zackery1234", 
                        host="localhost", port="5432")
  
    cur = conn.cursor()
  
    # Get the data from the form
    name = request.form['name']
    price = request.form['price']
    id = request.form['id']
  
    # Update the data in the table
    cur.execute(
        '''UPDATE products SET name=%s,\
        price=%s WHERE id=%s''', (name, price, id))
  
    # commit the changes
    conn.commit()
    return redirect(url_for('index'))



#CRUD



@app.route('/delete', methods=['POST'])
def delete():
    conn = psycopg2.connect(database="researchManagement", 
                        user="zackery",
                        password="zackery1234", 
                        host="localhost", port="5432")
    cur = conn.cursor()
  
    # Get the data from the form
    id = request.form['id']
  
    # Delete the data from the table
    cur.execute('''DELETE FROM products WHERE id=%s''', (id,))
  
    # commit the changes
    conn.commit()
  
    # close the cursor and connection
    cur.close()
    conn.close()
  
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)