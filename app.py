from flask import Flask, render_template, request
import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

def crear_app():
    app = Flask(__name__)
    cliente = MongoClient(os.getenv("MONGODB_URI"))
    app.db = cliente.Salon_Eventos


    #entradas=[]
    entradas = [entrada for entrada in app.db.contenido.find({})]
    print(entradas)


    @app.route("/", methods=["GET", "POST"])
    def home():
        print("Estamos en la funcion home()")
        if request.method == "POST":
            print("ENTRAMOS AL METODO POST")
            nombre = request.form.get("name")
            telefono = request.form.get("phone")
            correo = request.form.get("email")
            fecha_login = datetime.datetime.today().strftime("%d-%m-%Y")
            parametros = {"Nombre": nombre, "Telefono": telefono, "Correo": correo, "Fecha_Login": fecha_login}
            entradas.append(parametros)

            # Intentar insertar en MongoDB
            try:
                app.db.contenido.insert_one(parametros)
                print("Datos insertados en MongoDB")
            except Exception as e:
                print("Error al insertar en MongoDB:", e)

            return render_template("index.html", entradas=entradas)

        else:
            print("No entramos al metodo post")
            # Retornar la página para solicitudes GET
            return render_template("index.html", entradas=entradas)
    return app

if __name__ == "__main__":
    app=crear_app()
    app.run


