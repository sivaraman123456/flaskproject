from flask import Flask,render_template,request,flash,redirect,url_for,session
import sqlite3

app=Flask(__name__)
app.secret_key="123"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect('data1.db')
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customers where name=? and mail=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["age"]=data["age"]
            session["contact"]=data["contact"]
            session["mail"]=data["mail"]
            return redirect('customer')
        else:
            flash("mail and password mismatch","danger")
    return redirect(url_for("index"))



@app.route('/customer',methods=['GET','POST'])

def customer():
    return render_template("customer.html")



        
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            age=request.form['age']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail'] 
            con=sqlite3.connect("data1.db")
            con.execute("create table if not exists customers (pid integer primary key,name text,age integer,address text,contact integer,mail text)")
            cur=con.cursor()
            cur.execute("insert into customers (name,age,address,contact,mail)values(?,?,?,?,?)",(name,age,address,contact,mail))
            con.commit()
            flash("Record Added successfully","success")
            
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for('index'))
            con.close()
    return render_template('register.html')


@app.route('/logout',methods=['GET','POST'])

def logout():
    
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)
