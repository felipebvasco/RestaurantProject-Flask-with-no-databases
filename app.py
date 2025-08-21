from flask import Flask, render_template, request, session, flash, redirect, url_for

class Prato():
    def __init__(self, nome, proteina, peso, origem):
        self.nome = nome
        self.proteina = proteina
        self.peso = peso
        self.origem = origem

prato1 = Prato('Yakisoba', 'Vaca e Frango', '500g', 'Chinesa')
prato2 = Prato('Feijoada', 'Proco', '700g', 'Brasileira' )
prato3 = Prato('Croissant', 'N/A', '200g', 'Francês')
lista_pratos = [prato1, prato2, prato3]

class Bebida():
    def __init__(self, nome, base, tamanho, alcool):
        self.nome = nome
        self.base = base
        self.tamanho = tamanho
        self.alcool = alcool

class Usuario():
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Felipe', 'Felipe', '131204')
usuario2 = Usuario('Michelle', 'Naomi', '210604')
usuario3 = Usuario('Master', 'root', 'root')

usuarios = {usuario1.nickname :usuario1,
            usuario2.nickname :usuario2,
            usuario3.nickname :usuario3}
    
bebida1 = Bebida('Chocolate Quente', 'Leite', '200ml','Não')
bebida2 = Bebida('Caipirinha', 'Cachaça ou Vodka', '300ml', 'Sim')
bebida3 = Bebida('PinkPanther', 'Leite de coco', '200ml', 'Não')
lista_bebidas = [bebida1, bebida2, bebida3]

app = Flask(__name__)
app.secret_key = 'senhadificil'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pratos')
def pratos():
    return render_template('pratos.html', pratos=lista_pratos)

@app.route('/bebidas')
def bebidas():
    return render_template('bebidas.html', bebidas=lista_bebidas)

@app.route('/novo_prato', methods=['POST', 'GET'])
def novo_prato():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Necessário fazer login')
        return redirect(url_for('login'))
    return render_template('novo_prato.html')

@app.route('/nova_bebida')
def nova_bebida():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Necessário fazer login')
        return redirect(url_for('login'))
    return render_template('nova_bebida.html')

@app.route('/intermediaria', methods=['POST'])
def intermediaria():
    if request.form['nova_tela']:
        nova_pagina = request.form['nova_tela']
        return redirect(url_for(f'{nova_pagina}'))
    else:
        pass

@app.route('/criar_prato', methods=['POST',])
def criar_prato():
    nome = request.form['nome']
    proteina = request.form['proteina']
    peso = request.form['peso']
    origem = request.form['culinaria']
    prato = Prato(nome, proteina, peso, origem)
    lista_pratos.append(prato)
    return redirect(url_for('index'))

@app.route('/criar_bebida', methods=['POST',])
def criar_bebida():
    nome = request.form['nome']
    base = request.form['base']
    tamanho = request.form['tamanho']
    alcool = request.form['alcool']
    bebida = Bebida(nome, base, tamanho, alcool)
    lista_bebidas.append(bebida)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(f'{usuario.nickname} Logado com sucesso!')
            return redirect(url_for('index'))
        else:
            flash('Usuário não logado!')
            return redirect(url_for('login'))
    else:
            flash('Usuário não logado!')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/autenticar_criacao', methods=['POST',])
def autenticar_criacao():
    if request.form['usuario'] in usuarios:
        flash('Esse usuário já está cadastrado')
        return redirect(url_for('login'))
    elif request.form['senha'] != request.form['senha2']:
        flash('As senhas devem ser iguais')
        return redirect(url_for('signin'))
    else:
        nome = request.form['usuario']
        nickname = request.form['nickname']
        senha = request.form['senha']
        usuario = Usuario(nome, nickname, senha)
        usuarios[request.form['nickname']] = usuario
        flash('Usuário criado com sucesso')
        return redirect(url_for('login'))

@app.route('/quemsomos')
def quem_somos():
    return render_template('quemsomos.html')

app.run(debug=True)