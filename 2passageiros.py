#import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
#from dotenv import load_dotenv
import os
import pandas as pd
from unidecode import unidecode
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Configurações do WebDriver
"""options = uc.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--remote-debugging-port=9222")"""

# URL da planilha com "export?format=csv" para transformar em CSV
url_planilha = 'https://docs.google.com/spreadsheets/d/1NifRR6h6MRdegWZYk-yQV6RFawdttxjmi-pB1nTEDms/export?format=csv'
tabela_cliente = pd.read_csv(url_planilha, encoding='utf-8',  dtype={'cpf': str, 'telefone': str, 'cep': str, 'Parcelas': str,}) # dtype serve para transformar cpf e cep em string

driver = webdriver.Firefox()

# Tratamento que remove tudo que não é letra ou espaço
def limpar_nome(Nome):
    nome = unidecode(Nome)  # Remove acentos
    return re.sub(r'[^a-zA-Záàâãéêíóôõúü\s]', '', nome)

def random_sleep():
    time.sleep(random.uniform(25, 30))

def preencher_sexo(driver, Sexo, passenger):
    # Sexo
    wait = WebDriverWait(driver, 75)
    fieldset = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"#accordion-passenger-ADT_{passenger}-content .fullWidth.passenger-form-fieldset")))
    divs = fieldset.find_elements(By.CSS_SELECTOR, ".fullWidth.passenger-form-row")
    
    sex_button = divs[1].find_element(By.CSS_SELECTOR, ".MuiInputBase-root.MuiOutlinedInput-root.sc-pjumZ.gyOYfZ.MuiInputBase-formControl")
    sex_button.click()
    if (Sexo.lower() == "masculino"):
        masc_bottom = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-passengerInfo.gender"]/div[3]/ul/li[1]')))
        masc_bottom.click()
    else:
        femin_bottom = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-passengerInfo.gender"]/div[3]/ul/li[2]')))
        femin_bottom.click()

def fill_fields(name, last_name, date_birth, sex, individual_reg, email, phone, passenger):
    random_sleep()

    # Nome
    name_field = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="passengerDetails-firstName-ADT_{passenger}"]')))
    name_field.clear()
    name_field.send_keys(name)

    # Sobrenome
    last_name_field = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="passengerDetails-lastName-ADT_{passenger}"]')))
    last_name_field.clear()
    last_name_field.send_keys(last_name)

    # Nascimento
    date_birth_field = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="passengerInfo-dateOfBirth-ADT_{passenger}"]')))
    date_birth_field.clear()
    date_birth_field.send_keys(date_birth)

    # Sexo
    preencher_sexo(driver, sex, passenger)

    # CPF
    individual_reg_field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="taxDocument-documentNumber-ADT_{passenger}"]')))
    individual_reg_field.clear()
    individual_reg_field.send_keys(individual_reg)

    # email
    email_field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="passengerInfo-emails-ADT_{passenger}"]')))
    email_field.clear()
    email_field.send_keys(email)

    # numero
    phone_field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="passengerInfo-phones0-number-ADT_{passenger}"]')))
    phone_field.clear()
    phone_field.send_keys(phone)
    print("Dados preenchidos")

    if passenger == 1:
        #Repetir dados de contato nos outros passageiros
        repeat_button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="repeatContactData-ADT_{passenger}-label"]/div/span '))) 
        repeat_button.click()
        print("Dados de contato repetidos para o próximo passageiro")

    # confirmar dados
    confirmation_button = driver.find_element(By.XPATH, f'//*[@id="passengerFormSubmitButtonADT_{passenger}"]')
    confirmation_button.click()
    print(f"Dados passageiro {passenger} confirmados")

# Acessa site na pagina de preenchimento de dados.
#with uc.Chrome(options=options) as driver:
driver.get("https://www.latamairlines.com/br/pt/pagamentos/passageiros?orderId=LA9573348QKTA")

for index, row in tabela_cliente.iterrows():
    try:
        # Verifique e converta os campos para string
        Nome = str(limpar_nome(row['nome'])) if pd.notnull(row['nome']) else ''
        Sobrenome = str(row['sobrenome']) if pd.notnull(row['sobrenome']) else ''
        Nascimento = str(row['dataNascimento']) if pd.notnull(row['dataNascimento']) else ''
        Sexo = str(row['sexo']) if pd.notnull(row['sexo']) else ''
        CPF = str(row['cpf']) if pd.notnull(row['cpf']) else ''
        EmailDados = str(row['email']) if pd.notnull(row['email']) else ''
        Numero = str(row['telefone']) if pd.notnull(row['telefone']) else ''
        
    except Exception as e:
        print(f"Erro ao processar o cliente {index + 1}: {e}")
        
    wait = WebDriverWait(driver, 25)
    cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cookies-politics-button"]/span')))
    cookies_button.click()

    fill_fields(Nome, Sobrenome, Nascimento, Sexo, CPF, EmailDados, Numero, 1)
    fill_fields(Nome, Sobrenome, Nascimento, Sexo, CPF, EmailDados, Numero, 2)