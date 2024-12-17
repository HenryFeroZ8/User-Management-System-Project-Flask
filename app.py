from flask import Flask,render_template,redirect,request,url_for,flash
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]= None
app.config["MYSQL_DB"]="flask"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)


@app.route("/")
@app.route("/home")
def home():
    cursor = mysql.connection.cursor()
    query = """ SELECT * FROM users"""
    cursor.execute(query)
    res = cursor.fetchall()
   
    return render_template("home.html",datas = res)


@app.route("/addUsers",methods = ['GET','POST'] )
def addUsers():
    if request.method == "POST":
      
      name = request.form['name']
      age = request.form['age']
      city = request.form['city']

      cursor = mysql.connection.cursor()
      query = " insert into users (NAME,AGE,CITY) values (%s, %s, %s)"
      cursor.execute(query,[name,age,city])
      mysql.connection.commit()
      cursor.close()
      flash("User Details Added")
      
      return redirect(url_for("home"))
    return render_template("addUsers.html")


@app.route("/editUsers/<string:id>",methods = ['GET','POST'] )
def editUsers(id):
    cursor = mysql.connection.cursor()
    if request.method == "POST":
            name = request.form['name']
            age = request.form['age']
            city = request.form['city']

            query = "update users set NAME = %s , AGE = %s, CITY = %s where ID = %s"
            cursor.execute(query,[name,age,city,id])
            cursor.close()
            mysql.connection.commit()
            flash("User Details Updated")
            return redirect(url_for('home'))
    
    query = "SELECT * FROM users WHERE ID = %s"
    cursor.execute(query,id)
    res = cursor.fetchone()    
    mysql.connection.commit()
    cursor.close()
    return render_template("editUsers.html",datas = res)

@app.route("/deleteUsers/<string:id>",methods = ['GET','POST'] )
def deleteUsers(id):
    cursor = mysql.connection.cursor()
    query = "delete from users where ID = %s"
    cursor.execute(query,id)
    mysql.connection.commit()
    cursor.close()
    flash("User Deleted Success")
    return redirect(url_for('home'))
    

if (__name__=="__main__"):
    app.secret_key="abc123"
    app.run(debug=True)