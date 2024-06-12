from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='cadastro_usuarios'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print("Erro ao conectar ao MySQL", e)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conexao = conectar_bd()
        if conexao:
            try:
                cursor = conexao.cursor()
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hash))
                conexao.commit()
                cursor.close()
                conexao.close()
                flash('Usuário registrado com sucesso!')
                return redirect(url_for('index'))
            except Error as e:
                print("Erro ao inserir usuário", e)
                flash('Erro ao registrar usuário.')
                return redirect(url_for('registrar_usuario'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def verificar_login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conexao = conectar_bd()
        if conexao:
            try:
                cursor = conexao.cursor()
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
                resultado = cursor.fetchone()
                cursor.close()
                conexao.close()
                if resultado:
                    flash('Login realizado com sucesso!')
                    return redirect(url_for('index'))
                else:
                    flash('Email ou senha incorretos!')
                    return redirect(url_for('verificar_login'))
            except Error as e:
                print("Erro ao verificar login", e)
                flash('Erro ao realizar login.')
                return redirect(url_for('verificar_login'))
    return render_template('login.html')

@app.route('/alterar_senha', methods=['GET', 'POST'])
def alterar_senha():
    if request.method == 'POST':
        email = request.form['email']
        senha_atual = request.form['senha_atual']
        nova_senha = request.form['nova_senha']
        conexao = conectar_bd()
        if conexao:
            try:
                cursor = conexao.cursor()
                senha_atual_hash = hashlib.sha256(senha_atual.encode()).hexdigest()
                nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
                cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s AND senha = %s", (nova_senha_hash, email, senha_atual_hash))
                if cursor.rowcount > 0:
                    conexao.commit()
                    flash('Senha alterada com sucesso!')
                else:
                    flash('Email ou senha atual incorretos.')
                cursor.close()
                conexao.close()
                return redirect(url_for('index'))
            except Error as e:
                print("Erro ao alterar senha", e)
                flash('Erro ao alterar senha.')
                return redirect(url_for('alterar_senha'))
    return render_template('change_password.html')

@app.route('/alterar_email', methods=['GET', 'POST'])
def alterar_email():
    if request.method == 'POST':
        email_atual = request.form['email_atual']
        senha = request.form['senha']
        novo_email = request.form['novo_email']
        conexao = conectar_bd()
        if conexao:
            try:
                cursor = conexao.cursor()
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                cursor.execute("UPDATE usuarios SET email = %s WHERE email = %s AND senha = %s", (novo_email, email_atual, senha_hash))
                if cursor.rowcount > 0:
                    conexao.commit()
                    flash('E-mail alterado com sucesso!')
                else:
                    flash('Email atual ou senha incorretos.')
                cursor.close()
                conexao.close()
                return redirect(url_for('index'))
            except Error as e:
                print("Erro ao alterar e-mail", e)
                flash('Erro ao alterar e-mail.')
                return redirect(url_for('alterar_email'))
    return render_template('change_email.html')

@app.route('/excluir_usuario', methods=['GET', 'POST'])
def excluir_usuario():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conexao = conectar_bd()
        if conexao:
            try:
                cursor = conexao.cursor()
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                cursor.execute("DELETE FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
                if cursor.rowcount > 0:
                    conexao.commit()
                    flash('Usuário excluído com sucesso!')
                else:
                    flash('Email ou senha incorretos.')
                cursor.close()
                conexao.close()
                return redirect(url_for('index'))
            except Error as e:
                print("Erro ao excluir usuário", e)
                flash('Erro ao excluir usuário.')
                return redirect(url_for('excluir_usuario'))
    return render_template('delete_user.html')

if __name__ == '__main__':
    app.run(debug=True)
