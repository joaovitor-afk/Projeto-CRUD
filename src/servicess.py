from connection import get_connect
from passlib.hash import pbkdf2_sha256 as sha256



def criar_tabela():
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TB_USUARIO (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME VARCHAR(120) NOT NULL,
            EMAIL VARCHAR(120) UNIQUE NOT NULL,
            SENHA VARCHAR(255) NOT NULL
        );
        ''')
        conn.commit()
        print("Tabela criada/verificada com sucesso!")

    except Exception as e:
        print(f'Falha ao criar tabela: {e}')
    finally:
        conn.close()



def criar_usuario(nome, email, senha):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO TB_USUARIO (NOME, EMAIL, SENHA) VALUES (?, ?, ?)',
            (nome, email, senha)
        )

        conn.commit()
        print('Usuário cadastrado com sucesso!')

    except Exception as e:
        print(f'Falha ao criar usuário: {e}')
    finally:
        conn.close()



def listar_usuario():
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('SELECT ID, NOME, EMAIL FROM TB_USUARIO')
        usuarios = cursor.fetchall()

        if usuarios:
            print(f"{'-'*30} Lista de Usuários {'-'*30}")
            for u in usuarios:
                print(f"ID: {u[0]} | Nome: {u[1]} | Email: {u[2]}")
            print('-'*80)
        else:
            print('Nenhum usuário encontrado.')

    except Exception as e:
        print(f'Falha ao listar usuários: {e}')
    finally:
        conn.close()



def excluir_usuario(id):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM TB_USUARIO WHERE ID = ?', (id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Usuário excluído com sucesso!")
        else:
            print("Usuário não encontrado.")

    except Exception as e:
        print(f'Falha ao excluir usuário: {e}')
    finally:
        conn.close()



def menu():
    criar_tabela()
    while True:
        print(f"""
{'-'*30} MENU {'-'*30}
1 - Cadastrar Usuário
2 - Listar Usuários
3 - Excluir Usuário
4 - Sair
{'-'*66}
""")

        opc = input('Escolha uma opção: ').strip()

        if opc == '1':
            nome = input('Nome: ').strip().title()
            email = input('Email: ').strip()
            senha = input('Senha: ').strip()
            senha_hash = sha256.hash(senha)
            criar_usuario(nome, email, senha_hash)

        elif opc == '2':
            listar_usuario()

        elif opc == '3':
            try:
                id = int(input('ID do usuário para excluir: '))
                excluir_usuario(id)
            except ValueError:
                print('ID inválido! Digite um número inteiro.')

        elif opc == '4':
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida. Tente novamente.')

menu()