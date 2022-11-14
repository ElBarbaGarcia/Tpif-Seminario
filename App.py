from operator import index
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#esto conecta con mysql
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "mike190099"
app.config["MYSQL_DB"] = "stock" #PONGANLE EL NOMBRE QUE QUIERAN A LA BASE DE DATOS(esto es lo q vincula el programa con la base de datos)
mysql = MySQL()


#configuraciones
app.secret_key = "mysecretkey"


#esto vicula el index.html con el App.py
@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    print(data)
    return render_template("index.html", productos = data)

#aca ceberiamos cambiarlo por productos y el admin ponga los datos del producto que quiere agregar a la base de datos
@app.route("/add_producto", methods=["POST"])
def addProducto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        tipo = request.form["tipo"]
        print(nombre)
        print(marca)
        print(modelo)
        print(precio)
        print(cantidad)
        print(tipo)
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO productos (nombre, marca, modelo, precio, cantidad, tipo) VALUES(%s, %s, %s, %s, %s, %s)", (nombre, marca, modelo, precio, cantidad, tipo))
        mysql.connection.commit()
        flash("producto agregado exitosamente")
        return redirect(url_for(index))

#aca el admin puede deletear cualquier producto tocando el boton delete
@app.route("/delete/<int:id>")
def add_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos where id = {0}", format(id))
    mysql.connection.commit()
    flash("Product removed saccessfully")
    return redirect(url_for("index"))

# aca puede editar un producto y lo manda a edit.html en donde cambia las cosas
@app.route("/edit_producto/<id>")
def get_producto():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id))
    data = cur.fetchall()
    return render_template("edit.html", producto = data[0])

#aca updatea las cosas que modificas en edit.html
@app.route("/update/<id>", methods = ["POST"])
def update_producto(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        tipo = request.form["tipo"]
        cur = mysql.connection.cursor
        cur.execute("""" 
        UPDATE productos
        SET nombre = %s,
            marca = %s,
            modelo = %s,
            precio = %s,
            cantidad = %s,
            tipo = %s
        WHERE id = %s
        """, (nombre, marca, modelo, precio, cantidad, tipo))
        flash("Se actualizo corrrectamente")
        mysql.connection.commit()
        return redirect(url_for("index"))
    
#este es el puerto de localhost 
if __name__ == "__main__":
    app.run(port = 33065, debug = True)

#todo producto que sea eliminado o modificado se hace por id 
#que es un dato "invisible" que tiene como punto las posi 0 que se ven en los html
#asi q al modificar algo se hace en base a la primarikey q es el id