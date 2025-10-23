from connection import get_connect
from passlib.hash import pbkdf2_sha256 as sha256
import pwinput

def criar_tabela2():
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TB_USER (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME VARCHAR(120) NOT NULL,
            EMAIL VARCHAR(120) UNIQUE NOT NULL,
            SENHA VARCHAR(255) NOT NULL
        );
        ''')
        conn.commit()
        print("Tabela 2 criada/verificada com sucesso")

    except Exception as e:
        print(f'Falha ao criar tabela: {e}')
    finally:
        conn.close()

def criar_tabela():
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS TB_PRODUTOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            DESCRICAO VARCHAR(120) NOT NULL,
            VALOR DECIMAL(120) NOT NULL,
            QUANTIDADE DECIMAL(120) NOT NULL
        );
        ''')
        conn.commit()
        print("Tabela criada/verificada com sucesso")

    except Exception as e:
        print(f'Falha ao criar tabela: {e}')
    finally:
        conn.close()



def criar_produto(descricao, valor, quatidado):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO TB_PRODUTOS (DESCRICAO, VALOR, QUANTIDADE) VALUES (?, ?, ?)',
            (descricao, valor, quatidado)
        )

        conn.commit()
        print('Produto cadastrado com sucesso')

    except Exception as e:
        print(f'Falha ao criar produto: {e}')
    finally:
        conn.close()

def criar_user(nome, email, senha):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO TB_USER (NOME, EMAIL, SENHA) VALUES (?, ?, ?)',
            (nome, email, senha)
        )

        conn.commit()
        print('Usuário cadastrado com sucesso')

    except Exception as e:
        print(f'Falha ao criar usuário: {e}')
    finally:
        conn.close()

def listar_produto():
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('SELECT ID, DESCRICAO, VALOR, QUANTIDADE FROM TB_PRODUTOS')
        produto = cursor.fetchall()

        if produto:
            print(f"{'-'*30} Lista de Produtos {'-'*30}")
            for u in produto:
                print(f"ID: {u[0]} | Descriçao: {u[1]} | Valor: {u[2]} | Quantidade: {u[3]}")
            print('-'*80)
        else:
            print('Nenhum produt encontrado.')

    except Exception as e:
        print(f'Falha ao listar produtos: {e}')
    finally:
        conn.close()



def vender_produto(id):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        id_produto = int(input("Digite o ID do produto que deseja vender: "))
        quantidade_venda = int(input("Digite a quantidade que deseja vender: "))

        cursor.execute("SELECT DESCRICAO, QUANTIDADE FROM TB_PRODUTOS WHERE ID = ?", (id_produto,))
        produto = cursor.fetchone()

        if produto:
            descricao, quantidade_atual = produto
            print(f"Produto: {descricao} | Quantidade em estoque: {quantidade_atual}")

            if quantidade_venda <= quantidade_atual:
                nova_quantidade = quantidade_atual - quantidade_venda
                cursor.execute("UPDATE TB_PRODUTOS SET QUANTIDADE = ? WHERE ID = ?", (nova_quantidade, id_produto))
                conn.commit()
                print(f"Venda realizada com sucesso Novo estoque: {nova_quantidade}")
            else:
                print("Quantidade insuficiente em estoque.")
        else:
            print("Produto não encontrado.")

    except Exception as e:
        print(f'Falha ao vender produto: {e}')
    finally:
        conn.close()

def login_user(email, senha):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('SELECT ID, NOME, SENHA FROM TB_USER WHERE EMAIL = ?', (email,))
        user = cursor.fetchone()

        if user and sha256.verify(senha, user[2]):
            print(f'Bem-vindo, {user[1]}\n')
            return True, user[0] 
        else:
            print('Email ou senha incorretos.')
            return False, None

    except Exception as e:
        print(f'Erro ao fazer login: {e}')
    finally:
        conn.close()


def alterar_nome(user_id, novo_nome):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        cursor.execute('UPDATE TB_USER SET NOME = ? WHERE ID = ?', (novo_nome, user_id))
        conn.commit()
        print('Nome atualizado com sucesso')

    except Exception as e:
        print(f'Erro ao alterar nome: {e}')
    finally:
        conn.close()



def alterar_senha(user_id, nova_senha):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        senha_hash = sha256.hash(nova_senha)
        cursor.execute('UPDATE TB_USER SET SENHA = ? WHERE ID = ?', (senha_hash, user_id))
        conn.commit()
        print('Senha atualizada com sucesso')

    except Exception as e:
        print(f'Erro ao alterar senha: {e}')
    finally:
        conn.close()

def menu2():
    criar_tabela2()
    while True:
        print(f"""
{'-'*30} LOGIN {'-'*30}
1 - Cadastrar user
2 - logar user
3 - Sair
{'-'*66}
""")

        opc2 = input('Escolha uma opção: ').strip()

        if opc2 == '1':
           nome = input('Nome: ').strip().title()
           email = input('Email: ').strip()
           senha = pwinput.pwinput('Senha: ', mask='~').strip()
           senha_hash = sha256.hash(senha)
           criar_user(nome, email, senha_hash) 

        elif opc2 == '2':
            email = input('Email: ').strip()
            senha = pwinput.pwinput('Senha: ', mask='~').strip()

            check, user_id = login_user(email, senha)
            if check == True:
                menu_pos_login(user_id)
            else:
                continue
                

        elif opc2 == '3':
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida. Tente novamente.')

def menu():
    criar_tabela()
    while True:
        print(f"""
{'-'*30} MENU {'-'*30}
1 - Cadastrar Produto
2 - Listar Produtos
3 - Vender Produto
4 - Sair
{'-'*66}
""")
        
        opc = input('Escolha uma opção: ').strip()

        if opc == '1':
            Descriçao = input('Descriçao: ').strip().title()
            Valor = input('Valor: ').strip()
            Quantidade = input('Quantidade: ').strip()
            criar_produto(Descriçao, Valor, Quantidade)

        elif opc == '2':
            listar_produto()

        elif opc == '3':
            try:
                id = int(input('ID do Produto para vender: '))
                vender_produto(id)
            except ValueError:
                print('ID inválido Digite um número inteiro.')

        elif opc == '4':
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida. Tente novamente.')

def menu_pos_login(user_id):
    while True:
        print(f"""
{'-'*30} MENU DO USUÁRIO {'-'*30}
1 - Alterar Nome
2 - Alterar Senha
3 - Acessar Menu de Produtos
4 - Logout
{'-'*74}
""")
        opc = input('Escolha uma opção: ').strip()

        if opc == '1':
            novo_nome = input('Novo nome: ').strip().title()
            alterar_nome(user_id, novo_nome)

        elif opc == '2':
            nova_senha = input('Nova senha: ').strip()
            alterar_senha(user_id, nova_senha)

        elif opc == '3':
            menu()

        elif opc == '4':
            print('Logout realizado com sucesso')
            break

        else:
            print('Opção inválida. Tente novamente.')



if __name__ == '__main__':
    menu2()


