from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_cuestionario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cuestionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    que_es_reciclaje = db.Column(db.Text, nullable=False)
    significado_3r = db.Column(db.Text, nullable=False)
    reciclar_correctamente = db.Column(db.Text, nullable=False)
    tipos_de_reciclaje = db.Column(db.Text, nullable=False)
    importancia_reciclar = db.Column(db.Text, nullable=False)
    como_ayuda_contaminacion = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Cuestionario {self.id}>"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/tipos")
def tipos():
    return render_template("tipos.html")

@app.route("/contaminacion")
def contaminacion():
    return render_template("contaminacion.html")

@app.route("/impacto")
def impacto():
    return render_template("impacto.html")

@app.route("/cuestionario", methods=["GET", "POST"])
def cuestionario():
    if request.method == "POST":
        nuevo = Cuestionario(
            que_es_reciclaje=request.form.get("que_es_reciclaje"),
            significado_3r=request.form.get("significado_3r"),
            reciclar_correctamente=request.form.get("reciclar_correctamente"),
            tipos_de_reciclaje=request.form.get("tipos_de_reciclaje"),
            importancia_reciclar=request.form.get("importancia_reciclar"),
            como_ayuda_contaminacion=request.form.get("como_ayuda_contaminacion")
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("cuestionario"))

    registros = Cuestionario.query.all()
    return render_template("cuestionario.html", registros=registros)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    reg = Cuestionario.query.get_or_404(id)
    db.session.delete(reg)
    db.session.commit()
    return redirect(url_for("cuestionario"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

