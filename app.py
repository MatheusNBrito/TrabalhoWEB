from flask import Flask, render_template, request, url_for, redirect 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Anime(db.Model):

    __tablename__ = 'animes'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    genero = db.Column(db.String)
    tipo = db.Column(db.String)

    def __init__(self, nome, genero, tipo):
        self.nome = nome
        self.genero = genero
        self.tipo = tipo

with app.app_context():
    db.create_all()

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        genero = request.form.get("genero")
        tipo = request.form.get("tipo")
        

        if nome and genero and tipo:
            a = Anime(nome, genero, tipo)
            db.session.add(a)
            db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    animes = Anime.query.all()
    return render_template("lista.html", animes=animes)

@app.route("/excluir/<int:id>")
def excluir(id):
    anime = Anime.query.filter_by(_id=id).first()

    db.session.delete(anime)
    db.session.commit()

    animes = Anime.query.all()
    return render_template("lista.html", animes=animes)

def voltar():
    return render_template("index.html")

@app.route("/atualizar/<int:id>", methods = ['GET', 'POST'])
def atualizar(id):
    anime = Anime.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        genero = request.form.get("genero")
        tipo = request.form.get("tipo")
        

        if nome and genero and tipo:
            anime.nome = nome  
            anime.genero = genero   
            anime.tipo = tipo

            db.session.commit()

            return redirect(url_for("lista"))
    return render_template("atualizar.html", anime=anime)

    
if __name__ == '__main__':
    app.run(debug=True)