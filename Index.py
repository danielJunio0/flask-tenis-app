from flask import Flask, render_template, url_for, session, redirect, request, flash
import psycopg2 as pg
import random
import json
import zipfile as zip
import os
from urllib.request import Request, urlopen

app = Flask(__name__)
app.secret_key = "daniel"

conn = pg.connect(
        database="db_loja_tenis",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )
imagens = [
    'https://images.lojanike.com.br/320x320/produto/tenis-nike-air-zoom-pegasus-39-flyease-masculino-DJ7381-002-1-11651168983.jpg',
    'https://images.lojanike.com.br/320x320/produto/tenis-nike-react-miler-3-DD0490-003-1-11645798431.jpg',
    'https://images.lojanike.com.br/320x320/produto/tenis-nike-zoomx-vaporfly-next-2-masculino-CU4111-600-1-11655139399.jpg',
    'https://images.lojanike.com.br/320x320/produto/tenis-nike-renew-ride-3-masculino-DC8185-100-1-11649248278.jpg',
    'https://images.lojanike.com.br/320x320/produto/tenis-nike-zoomx-invincible-run-flyknit-2-masculino-DH5425-600-1-11647976387.jpg'
    ]

@app.route("/")
def homepage():
    if "logado" in session:
        cursor = conn.cursor()
        cursor.execute("Select * from produtos")
        email = session["email"]
        produtos = cursor.fetchall()
        print(produtos)
        return render_template("homepage.html", produtos=produtos, email = email )
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["POST","GET"])
def login():
    cursor = conn.cursor()
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute("Select * from usuarios WHERE email = %s and senha = %s",(email, senha))

        conta = cursor.fetchone()
        print(conta)
        if conta:
            session['logado'] = True
            session['nome'] = conta[1]
            session['email'] = conta[2]
            return redirect(url_for('homepage'))
        else:
            flash('Usuário ou senha inválido!')
    
    return render_template('login.html')


@app.route("/cadastro", methods=["POST","GET"])
def cadastro():
    cursor = conn.cursor()
    if request.method == 'POST' and 'nome' in request.form and 'email' in request.form and 'senha' in request.form:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))

        conta = cursor.fetchone()

        if conta:
            flash("Usuário já existe!")
        else:
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",(nome, email, senha))
            conn.commit()
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('homepage'))    

    return render_template("cadastro.html")

@app.route("/cadastroproduto", methods=["POST","GET"])
def cadastroproduto():
    cursor = conn.cursor()
    if request.method == 'POST' and 'nome' in request.form and 'descricao' in request.form and 'marca' in request.form and 'preco' in request.form:
        nome = request.form['nome']
        descricao = request.form['descricao']
        marca = request.form['marca']
        preco = request.form['preco']
        imagem = random.choice(imagens)        

        cursor.execute("INSERT INTO produtos (nome, descricao, marca, imagem, preco) VALUES (%s, %s, %s, %s, %s)",(nome, descricao, marca, imagem, preco))
        conn.commit()
        return redirect(url_for('homepage'))

    return render_template("cadastro-produto.html")

@app.route('/deletar/<id>')
def deletar(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos Where id = %s",(id))

    conn.commit()
    return redirect(url_for("homepage"))

@app.route("/logout")
def logout():
    session.pop("logado", None)
    session.pop("nome", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/exportar", methods=["POST","GET"])
def exportar():
    if request.method == 'POST':
        cursor = conn.cursor()
        cursor.execute("SELECT row_to_json(p) FROM produtos AS p")

        produtosJson = cursor.fetchall()
        print(produtosJson)

        with open('produtos.json', 'w') as fp:
            json.dump(produtosJson, fp)

        path_zip = os.path.join(os.sep, os.getcwd(),"arquivoJson.zip")
        zf = zip.ZipFile(path_zip, "w")

        zf.write(os.path.join(os.getcwd(),"produtos.json"))

        zf.close()

        return redirect(url_for("exportar"))
    return render_template("exportar.html")

@app.route("/importar", methods=["POST","GET"])
def importar():    
    cursor = conn.cursor()
    if request.method == 'POST':
        URL = request.form['url']
        req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req).read()
        print(response)
        if response:
            cursor.execute("INSERT INTO Importados (valor) VALUES (%s)",(response))
            conn.commit()
        return render_template("importar.html", valores=response)
    else:
        return render_template("importar.html")

@app.route("/perfil/<email>")
def perfil(email):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    return render_template("perfil.html", usuario=usuario)



if __name__ == "__main__":
    app.run(debug=True)