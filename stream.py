import streamlit as st
import streamlit_authenticator as stauth
import crud
import pandas as pd

names = ['Josh', "Andre"] #Nomes testes
usernames = ['user1', 'admin1'] #Usuários testes
senhas = ['1234', 'abcd'] #Senhas testes
senhas = stauth.Hasher(senhas).generate()
cargos = ['u','f'] #Cargo testes

credenciais = {'usernames' : {username: {'password': senha, 'name': nome, 'cargo' : cargo}for username, senha, nome, cargo in zip(usernames, senhas, names, cargos)}}

autenticador = stauth.Authenticate(credenciais, 'cookiedemo', 'abcdef', cookie_expiry_days=30)

name, authentication_status, username = autenticador.login("Login", 'main')
try:
    nivel_permissao = credenciais['usernames'][username]['cargo']
except:
    pass
if authentication_status == True and (nivel_permissao == 'f'): 
    autenticador.logout("logout","sidebar") ## se quiser por a opção de logout na siderbar trocar 'main' por 'sidebar'
        # Cria a tabela no banco de dados (certifique-se de que a função esteja implementada no módulo crud)
    crud.create_table()

    # Define as abas da interface
    inserir, visualizar, atualizar, deletar = st.tabs(['Inserir', "Visualizar", "Atualizar", "Deletar"])

    # Aba para visualizar os pets cadastrados
    with visualizar:
        st.title('Visualizar')
        st.write('Aqui você pode visualizar os dados dos pets cadastrados no banco de dados.')

        pets = crud.get_pets()
        if pets:
            df = pd.DataFrame(pets, columns=['ID', 'Nome do dono', 'CPF do dono', 'Nome do pet', 'Raça','Vacinações', 'Descrição', 'Check-in', 'Check-out'])
            st.dataframe(df)
        else:
            st.write('Nenhum pet cadastrado.')

    # Aba para inserir um novo pet
    with inserir:
        st.title('Inserir')
        cpf_dono = st.text_input('CPF do dono')
        nome_dono = st.text_input('Nome do dono')
        nome_pet = st.text_input('Nome do pet')
        raca = st.text_input('Raça')
        descricao = st.text_area('Descrição')
        vaccinations = st.text_area('Vacinações')
        if st.button('Salvar'):
            if crud.insert_pet(nome_dono, cpf_dono, nome_pet, raca, descricao, vaccinations):
                st.success('Pet inserido com sucesso!')
            else:
                st.error('Falha ao inserir o pet. Verifique os dados.')

    # Aba para atualizar os dados de um pet existente
    with atualizar:
        st.title('Atualizar')
        st.write('Aqui você pode atualizar os dados dos pets cadastrados no banco de dados.')

        id_pet = st.number_input("Qual ID você deseja atualizar?", step=1)
        nome_dono = st.text_input('Novo nome do dono')
        nome_pet = st.text_input('Novo nome do pet')
        raca = st.text_input('Nome da raça')
        descricao = st.text_area('Nova descrição')
        vaccinations = st.text_area('Vacinas')
        
        if st.button('Atualizar'):
            pet = crud.get_pet_by_id(id_pet)
            if pet is None:
                st.error('ID não encontrado!')
            else:
                if nome_dono == '':
                    nome_dono = pet[1]
                if nome_pet == '':
                    nome_pet = pet[2]
                if raca == '':
                    raca = pet[3]
                if descricao == '':
                    descricao = pet[4]
                if vaccinations == '':
                    vaccinations = pet[5]
                crud.update_pet(id_pet, nome_dono, nome_pet, raca, descricao, vaccinations)
                st.success('Pet atualizado com sucesso!')

    # Aba para deletar um pet pelo ID
    with deletar:
        st.title('Deletar')
        st.write('Aqui você pode deletar os dados dos pets cadastrados no banco de dados.')

        id_pet_deletar = st.number_input("Qual ID você deseja deletar?", step=1)
        
        if st.button('Deletar'):
            pet = crud.get_pet_by_id(id_pet_deletar)
            if pet is None:
                st.error('ID não encontrado!')
            else:
                crud.delete_pet(id_pet_deletar)
                st.success('Pet deletado com sucesso!')

if authentication_status and (nivel_permissao == 'u'):
    # Define as abas da interface
    visualizar = st.tabs(['1'])
    
    # Aba para visualizar os pets cadastrados
    st.title('Visualizar')   
    st.write('Aqui você pode visualizar os dados dos pets cadastrados no banco de dados.')
    
    pets = crud.get_pets()
    
    if pets:
        df = pd.DataFrame(pets, columns=['ID', 'Nome do dono', 'Nome do pet', 'Raça', 'Vacinações', 'Descrição', 'Check-in', 'Check-out',''])
        st.dataframe(df)
    else:
        st.write('Nenhum pet cadastrado.')

    autenticador.logout("logout","sidebar")
    st.title("Usuário")

if authentication_status == False:
    st.error('Username/password is incorrect')

if authentication_status == None:
    st.warning('Please enter your username and password')

