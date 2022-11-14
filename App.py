from operator import index
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#esto conecta con mysql
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "tarapatin123"
app.config["MYSQL_DB"] = "stock2" #PONGANLE EL NOMBRE QUE QUIERAN A LA BASE DE DATOS(esto es lo q vincula el programa con la base de datos)
mysql = MySQL(app)

#configuraciones
app.secret_key = "mysecretkey"


#esto vicula el index.html con el App.py
@app.route("/")
def Index():
    cur = mysql.connection.cuusor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    print(data)
    return render_template("index.html", contacts = data)

#aca ceberiamos cambiarlo por productos y el admin ponga los datos del producto que quiere agregar a la base de datos
@app.route("/add_contact", methods=["POST"])
def addContact():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        print(fullname)
        print(phone)
        print(email)
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES(%s, %s, %s)", (fullname, phone, email))
        mysql.connection.commit()
        flash("contacto agregado exitosamente")
        return redirect(url_for(index))

#aca el admin puede deletear cualquier producto tocando el boton delete
@app.route("/delete/<string:id>")
def add_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts where id = {0}", format(id))
    mysql.connection.commit()
    flash("Contact removed saccessfully")
    return redirect(url_for("index"))

# aca puede editar un producto y lo manda a edit.html en donde cambia las cosas
@app.route("/edit_contact/<id>")
def get_contact():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id))
    data = cur.fetchall()
    return render_template("edit.html", contact = data[0])

#aca updatea las cosas que modificas en edit.html
@app.route("/update/<id>", methods = ["POST"])
def update_contact(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cur = mysql.connection.cursor
        cur.execute("""" 
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone))
        flash("Se actualizo corrrectamente")
        mysql.connection.commit()
        return redirect(url_for("index"))
    
#este es el puerto de localhost 
if __name__ == "__main__":
    app.run(port = 33065, debug = True)

#todo producto que sea eliminado o modificado se hace por id 
#que es un dato "invisible" que tiene como punto las posi 0 que se ven en los html
#asi q al modificar algo se hace en base a la primarikey q es el id