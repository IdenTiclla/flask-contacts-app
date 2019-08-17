from flask import Flask, render_template, request, redirect, url_for, flash
# flash -> mensajes entre vistas
from flask_mysqldb import MySQL

app = Flask(__name__)
# Mysql connection
app.config["MYSQL_HOST"] = '127.0.0.1'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'flaskcontacts'

# settings
app.secret_key = 'mysecretkey'
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return render_template("index.html",contacts=data)

@app.route('/add_contact',methods=["POST"])
def add_contact():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)",(fullname, phone, email))
        mysql.connection.commit()
        flash('Contact added')
        return redirect(url_for("index"))

@app.route('/edit_contact/<int:id>')
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    data = cursor.fetchall()
    return render_template("edit_contact.html", contact=data[0])

@app.route('/update/<id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
            """,(fullname,email,phone,id))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for("index"))
@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id={0}'.format(id))    
    mysql.connection.commit()
    flash('Contact removed successfully')
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)