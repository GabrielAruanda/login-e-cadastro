import mysql.connector
from mysql.connector import Error
import hashlib

# Função para conectar ao banco de dados
def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',  # Substitua pelo seu usuário do MySQL
            password='',  # Substitua pela sua senha do MySQL
            database='usuarios_db'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print("Erro ao conectar ao MySQL", e)
    return None

# Função para registrar um novo usuário
def registrar_usuario(nome, email, senha):
    conexao = conectar_bd()
    if conexao:
        try:
            cursor = conexao.cursor()
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()  # Hash da senha
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha_hash))
            conexao.commit()
            cursor.close()
            conexao.close()
            print("Usuário registrado com sucesso!")
        except Error as e:
            print("Erro ao inserir usuário", e)

# Função para verificar o login do usuário
def verificar_login(email, senha):
    conexao = conectar_bd()
    if conexao:
        try:
            cursor = conexao.cursor()
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()  # Hash da senha
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
            resultado = cursor.fetchone()
            cursor.close()
            conexao.close()
            return resultado is not None
        except Error as e:
            print("Erro ao verificar login", e)
    return False

# Função para alterar a senha do usuário
def alterar_senha(email, senha_atual, nova_senha):
    conexao = conectar_bd()
    if conexao:
        try:
            cursor = conexao.cursor()
            senha_atual_hash = hashlib.sha256(senha_atual.encode()).hexdigest()
            nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
            cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s AND senha = %s", (nova_senha_hash, email, senha_atual_hash))
            if cursor.rowcount > 0:
                conexao.commit()
                print("Senha alterada com sucesso!")
            else:
                print("Email ou senha atual incorretos.")
            cursor.close()
            conexao.close()
        except Error as e:
            print("Erro ao alterar senha", e)

# Função para alterar o e-mail do usuário
def alterar_email(email_atual, novo_email, senha):
    conexao = conectar_bd()
    if conexao:
        try:
            cursor = conexao.cursor()
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            cursor.execute("UPDATE usuarios SET email = %s WHERE email = %s AND senha = %s", (novo_email, email_atual, senha_hash))
            if cursor.rowcount > 0:
                conexao.commit()
                print("E-mail alterado com sucesso!")
            else:
                print("Email atual ou senha incorretos.")
            cursor.close()
            conexao.close()
        except Error as e:
            print("Erro ao alterar e-mail", e)

# Função para excluir um usuário
def excluir_usuario(email, senha):
    conexao = conectar_bd()
    if conexao:
        try:
            cursor = conexao.cursor()
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            cursor.execute("DELETE FROM usuarios WHERE email = %s AND senha = %s", (email, senha_hash))
            if cursor.rowcount > 0:
                conexao.commit()
                print("Usuário excluído com sucesso!")
            else:
                print("Email ou senha incorretos.")
            cursor.close()
            conexao.close()
        except Error as e:
            print("Erro ao excluir usuário", e)

# Função principal
def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Registrar novo usuário")
        print("2. Fazer login")
        print("3. Alterar senha")
        print("4. Alterar e-mail")
        print("5. Excluir usuário")
        print("6. Sair")

        opcao = input("Opção: ")

        if opcao == '1':
            nome = input("Digite seu nome: ")
            email = input("Digite seu e-mail: ")
            senha = input("Digite sua senha: ")
            registrar_usuario(nome, email, senha)
        elif opcao == '2':
            email = input("Digite seu e-mail: ")
            senha = input("Digite sua senha: ")
            if verificar_login(email, senha):
                print("Login realizado com sucesso!")
            else:
                print("Email ou senha incorretos!")
        elif opcao == '3':
            email = input("Digite seu e-mail: ")
            senha_atual = input("Digite sua senha atual: ")
            nova_senha = input("Digite sua nova senha: ")
            alterar_senha(email, senha_atual, nova_senha)
        elif opcao == '4':
            email_atual = input("Digite seu e-mail atual: ")
            senha = input("Digite sua senha: ")
            novo_email = input("Digite seu novo e-mail: ")
            alterar_email(email_atual, novo_email, senha)
        elif opcao == '5':
            email = input("Digite seu e-mail: ")
            senha = input("Digite sua senha: ")
            excluir_usuario(email, senha)
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    main()
