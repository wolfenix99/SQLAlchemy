from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:''@localhost/tareas'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Maestros(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    nombre= db.Column(db.String(20),unique=True)
    estado=db.Column(db.String(20),unique=True)
    def __init__(self,nombre,estado):
        self.nombre=nombre
        self.estado=estado

@app.route('/')
def Index():
    return render_template('index.html')
    # return "dea"
@app.route('/addmaestro', methods=['POST'])
def add():
    if request.method=='POST':
        nombre=request.form['nombre']
        estado=request.form['estado']
        me=Maestros(nombre=nombre,estado=estado)
        db.session.add(me)
        db.session.commit()
        print(nombre)
        print(estado)
        return redirect('/consulta')
   
@app.route('/consulta')
def consulta():
    user = Maestros.query.all()
    return render_template('datos.html',user=user,pageTile='maestros')
    
@app.route('/edit/<id>')
def edit(id):
    user = Maestros.query.filter_by(id=id).first()
    return render_template('edit.html',user=user,pageTile='edit')
@app.route('/delete/<id>')
def delete(id):
    user = Maestros.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/consulta')

@app.route('/editmaestro', methods=['POST'])
def editma():
    if request.method=='POST':
        nombre=request.form['nombre']
        estado=request.form['estado']
        ids=request.form['id']
        me=Maestros.query.filter_by(id=ids).first()
        me.nombre=nombre
        me.estado=estado   
        db.session.commit()
        print(nombre)
        print(estado)
        return  redirect('/consulta')

if __name__=='__main__':
    app.run(debug=True)

