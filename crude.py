import re
import sqlite3
from datetime import datetime

# Função para validar o formato de CPF
def is_valid_cpf(cpf):
    pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    return pattern.match(cpf)

# Função para validar o comprimento máximo de strings
def is_valid_length(value, max_length):
    return len(value) <= max_length

# Função para validar dados antes de inserir um pet
def validate_pet_data(owner_name, owner_cpf, pet_name, breed, description, vaccinations):
    if not owner_name or not owner_cpf or not pet_name or not breed:
        return False  # Campos obrigatórios não preenchidos

    if not is_valid_cpf(owner_cpf):
        return False  # CPF no formato inválido

    if not is_valid_length(owner_name, 100) or not is_valid_length(pet_name, 100) or not is_valid_length(breed, 50):
        return False  # Comprimento máximo excedido para algum campo

    return True  # Dados válidos

# Função para criar a tabela no banco de dados
def create_table():
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT,
            owner_cpf TEXT,
            pet_name TEXT,
            breed TEXT,
            description TEXT,
            vaccinations TEXT,  -- Nova coluna para armazenar informações de vacinação
            check_in TEXT,
            check_out TEXT  -- Adiciona colunas para registro de check-in e check-out
        )
    ''')
    conn.commit()
    conn.close()

# Função para inserir um pet no banco de dados
def insert_pet(owner_name, owner_cpf, pet_name, breed, description, vaccinations):
    if validate_pet_data(owner_name, owner_cpf, pet_name, breed, description, vaccinations):
        conn = sqlite3.connect('pets.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pets (owner_name, owner_cpf, pet_name, breed, description, vaccinations)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (owner_name, owner_cpf, pet_name, breed, description, vaccinations))
        conn.commit()
        conn.close()
        return True  # Inserção bem-sucedida
    else:
        return False  # Dados inválidos, não inserir

# Função para realizar o check-in de um pet
def check_in_pet(id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    
    # Obtém a data e hora atual como string
    check_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Executa a consulta SQL para atualizar o check-in do pet pelo ID
    cursor.execute('UPDATE pets SET check_in=? WHERE id=?', (check_in_time, id))
    
    conn.commit()
    conn.close()

# Função para realizar o check-out de um pet
def check_out_pet(id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    
    # Obtém a data e hora atual como string
    check_out_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Executa a consulta SQL para atualizar o check-out do pet pelo ID
    cursor.execute('UPDATE pets SET check_out=? WHERE id=?', (check_out_time, id))
    
    conn.commit()
    conn.close()

# Função para recuperar todos os pets do banco de dados
def get_pets():
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pets')
    pets = cursor.fetchall()
    conn.close()
    return pets

# Função para recuperar um pet específico do banco de dados pelo ID do pet
def get_pet_by_id(id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    
    # Executa a consulta SQL para buscar o pet pelo ID
    cursor.execute('SELECT * FROM pets WHERE id=?', (id,))
    
    # Recupera o resultado da consulta (um único pet)
    pet = cursor.fetchone()
    
    # Fecha a conexão com o banco de dados
    conn.close()
    
    # Retorna o pet encontrado (ou None se não encontrado)
    return pet

# Função para recuperar um pet específico do banco de dados pelo CPF do proprietário
def get_pet_by_cpf(owner_cpf):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    
    # Executa a consulta SQL para buscar o pet pelo CPF do proprietário
    cursor.execute('SELECT * FROM pets WHERE owner_cpf=?', (owner_cpf,))
    
    # Recupera o resultado da consulta (um único pet)
    pet = cursor.fetchone()
    
    # Fecha a conexão com o banco de dados
    conn.close()
    
    # Retorna o pet encontrado (ou None se não encontrado)
    return pet

# Função para deletar um pet do banco de dados
def delete_pet(id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pets WHERE id=?', (id,))
    conn.commit()
    conn.close()

# Função para atualizar os dados de um pet no banco de dados
def update_pet(id, owner_name, pet_name, breed, description, vaccinations):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pets
        SET owner_name=?, pet_name=?, breed=?, description=?, vaccinations=?
        WHERE id=?
    ''', (owner_name, pet_name, breed, description, vaccinations, id))
    conn.commit()
    conn.close()