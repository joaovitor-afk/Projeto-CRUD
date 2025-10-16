#NOTE - importar as conexoes 

from connection import get_connect
from passlib.hash import pbkdf2_sha256 as sha256

#NOTE - funçao de criaçao de usuario 

def criar_usuario(nome, email, senha):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO TB_USUARIO(nome, email, senha) VALUES (?, ?, ?)',
                        (nome, email, senha)
        )

        conn.commit()
        print('Usuário cadastrado com sucesso!')

    except Exception as e:
        print(f'Falha ao criar tabela: {e}')


#NOTE - funçao de criaçao de listar

def listar_usuario():
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute('SELECT NOME, EMAIL, SENHA FROM TB_USUARIO')
        usuarios = cursor.fetchall()

        if usuarios:
            print(f'{30*'-'}Lista de usuarios!{30*'-'}')
            for u in usuarios:
                print(f'| {u}')
        else:
            print('nenhum usuario encontrado')
    except Exception as e:
        print(f'Falha ao listar: {e}')
    

def excluir_usuario(id):
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM TB_USUARIO WHERE ID=?, (ID,)           
        """, (id))
        
        conn.commit()

    except Exception as e:
        print(f'Falha ao criar usuario: {e}')


def editar_usuario(id):
    ...

def listar_usuario_email(email):
    ... 

def criar_tabela():
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE TB_USUARIO(
	        ID INTEGER PRIMARY KEY ,
            NOME VARCHAR(120) NOT NULL,
            EMAIL VARCHAR(120) UNIQUE,
            SENHA VARCHAR(255)               
                       
        );                            
        ''')

    except Exception as e:
        print(f'Falha ao criar tabela: {e}')
    
if __name__ == '__main__':
    criar_tabela()
    nome = input('Digite um nome: ').strip().title()
    email = input('Digite o email: ').strip()
    senha = input('Digite uma senha: ').strip()
    senha = sha256.hash(senha)

    criar_usuario(nome, email, senha)
    listar_usuario()