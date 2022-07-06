from turtle import title
from unittest import result
from flask import Flask, redirect, request, session
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.Text, unique = True)
    password = db.Column(db.Text)
    designation = db.Column(db.String(100))

    company = db.Column(db.String(100))
    status = db.Column(db.String, default = True)
    registered = db.Column(db.Date, default = datetime.utcnow)




class Profile(db.Model):
    name = db.Column(db.String(100),primary_key=True)
    email = db.Column(db.Text, unique=True)
    mobile = db.Column(db.Text)
    designation = db.Column(db.String(50))
    about = db.Column(db.String(250))

    



    


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/templates/sign-up.html', methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        rows = User(name = name, email = email, password = password)
        db.session.add(rows)          
        db.session.commit()
        return redirect("/templates/profile.html")

    return render_template('sign-up.html')


@app.route('/templates/sign-in.html', methods=['POST','GET'])
def sign_in():
    r = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        User.query.filter_by(email='email').first()
        for i in r:
            if(email == i[0] and password == i[1]):
                db.session["signedin"] = True
                db.session["email"] = email
        return redirect("/templates/profile.html")

    return render_template('sign-in.html')

@app.route("/templates/tables.html")  
def view():
    rows = User.query.all()
    return render_template("tables.html", rows = rows)

'''
@app.route('/edit/<id>/',methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        rows = User.query.get(id)
        rows.name = request.form['name']
        rows.email = request.form['email']
        rows.designation = request.form['designation']
        rows.company = request.form['company']
        db.session.commit() 
    return redirect("/templates/tables.html") 

'''



    
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    row = User.query.filter_by(id=id).first()

    if request.method == 'POST':
        if row:
            db.session.delete(row)
            db.session.commit()

            name = request.form['name']
            email = request.form['email']
            designation = request.form['designation']
            company = request.form['company']
            row = User(id=id, name=name, email=email, designation=designation, company=company)

            db.session.add(row)
            db.session.commit()
            return redirect("/templates/tables.html") 
        return f"row with id = {id} Does not Exist"    
    return redirect("/templates/tables.html") 





@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    rows = User.query.filter_by(id=id).first()
    db.session.delete(rows) 
    db.session.commit()

    return redirect("/templates/tables.html")

@app.route('/templates/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/templates/profile.html')
def profile():
    return render_template('profile.html')    

@app.route('/editprofile.results/',methods=['GET','POST'])
def editprofile():
    results=Profile.query.all()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        designation = request.form['designation']
        about =  request.form['about']
        results = Profile(name=name, email=email, mobile=mobile, designation=designation, about=about)
        db.session.add(Profile)
        db.session.commit()
    return render_template('profile.html', results=results) 



@app.route('/tables.html')
def tables():
    return render_template('tables.html')

@app.route('/templates/billing.html')
def billing():
    return render_template('billing.html')

@app.route('/templates/rtl.html')
def rtl():
    return render_template('rtl.html')

@app.route('/templates/virtual-reality.html')
def virtual_reality():
    return render_template('virtual-reality.html')




def logout():
    render_template('index.html')   



if __name__ == '__main__':
    app.run(debug = True)
