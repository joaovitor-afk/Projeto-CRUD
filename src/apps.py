def menu():
    criar_tabela()  # garante que a tabela exista
    while True:
        print(''
 MENU 
1 - Cadastrar Usuário
2 - Listar Usuários
3 - Excluir Usuário
4 - Sair

'')

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
                print('ID inválido!')

        elif opc == '4':
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__main__':
    menu()

