import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from dotenv import load_dotenv
import os
import pandas as pd
from unidecode import unidecode
import re

# Configurações do WebDriver
options = uc.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
options.add_argument("--remote-debugging-port=9222")

# URL da planilha com "export?format=csv" para transformar em CSV
url_planilha = 'https://docs.google.com/spreadsheets/d/1NifRR6h6MRdegWZYk-yQV6RFawdttxjmi-pB1nTEDms/export?format=csv'
tabela_cliente = pd.read_csv(url_planilha, encoding='utf-8',  dtype={'cpf': str, 'telefone': str, 'cep': str, 'Parcelas': str,}) # dtype serve para transformar cpf e cep em string

# Tratamento que remove tudo que não é letra ou espaço
def limpar_nome(Nome):
    nome = unidecode(Nome)  # Remove acentos
    return re.sub(r'[^a-zA-Záàâãéêíóôõúü\s]', '', nome)

def random_sleep():
    time.sleep(random.uniform(25, 30))
    
def preencher_sexo(driver, Sexo):
    # Sexo
    wait = WebDriverWait(driver, 25)
    sexo_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mui-component-select-passengerInfo.gender"]')))
    sexo_button.click()
    if (Sexo.lower() == "masculino"):
        masc_bottom = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-passengerInfo.gender"]/div[3]/ul/li[1]')))
        masc_bottom.click()
    else:
        femin_bottom = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-passengerInfo.gender"]/div[3]/ul/li[2]')))
        femin_bottom.click()


# Acessa site na pagina de preenchimento de dados.
with uc.Chrome(options=options) as driver:
    driver.get("https://www.latamairlines.com/br/pt/pagamentos/passageiros?orderId=LA9577335LCHR")

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
    
    random_sleep()
    # Nome
    name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passengerDetails-firstName-ADT_1"]')))
    name_field.send_keys(Nome)

    # Sobrenome
    Sobrenome_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passengerDetails-lastName-ADT_1"]')))
    Sobrenome_field.send_keys(Sobrenome)

    # Nascimento
    nasci_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passengerInfo-dateOfBirth-ADT_1"]')))
    nasci_field.send_keys(Nascimento)

    # Sexo
    preencher_sexo(driver, Sexo)
    
    # CPF
    cpf_fiel = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="taxDocument-documentNumber-ADT_1"]')))
    cpf_fiel.send_keys(CPF)

    # email
    emailDados_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passengerInfo-emails-ADT_1"]')))
    emailDados_field.send_keys(EmailDados)

    # numero
    number_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="passengerInfo-phones0-number-ADT_1"]')))
    number_field.send_keys(Numero)
    print("Dados preenchidos")

    #Repetir dados de contato nos outros passageiros
    repeat_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="repeatContactData-ADT_1-label"]/div/span '))) 
    repeat_button.click()
    print("Dados de contato repetidos para o próximo passageiro")

    # confirmar dados
    confirmacao_botton = driver.find_element(By.XPATH, '//*[@id="passengerFormSubmitButtonADT_1"]')
    confirmacao_botton.click()
    print("Dados passageiro 1 confirmados")
    random_sleep()
# ----------------------------------------------------------------------------------------------------------------------------------------------

    # # Clica no passageiro 2
    # botao_passageiro2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="accordion-passenger-ADT_2"]')))
    # botao_passageiro2.click()

    # Preenche dados do passageiro 2
    # Nome
    name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passengerDetails-firstName-ADT_2"]')))
    name_field.send_keys(Nome)

    # Sobrenome
    Sobrenome_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passengerDetails-lastName-ADT_2"]')))
    Sobrenome_field.send_keys(Sobrenome)

    # Nascimento
    nasci_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="passengerInfo-dateOfBirth-ADT_2"]  ')))
    nasci_field.send_keys(Nascimento)

    # Sexo
    preencher_sexo(driver, Sexo)
    
    # CPF
    cpf_fiel = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="taxDocument-documentNumber-ADT_2"]')))
    cpf_fiel.send_keys(CPF)

    # # confirmar dados
    # confirmacao_botton = driver.find_element(By.XPATH, '//*[@id="passengerFormSubmitButtonADT_2"]')
    # confirmacao_botton.click()
    # print("Dados passageiro 2 confirmados")
    # random_sleep()

    # # Continuar operação
    # continuar_botton = driver.find_element(By.XPATH, '//*[@id="undefined--button-wrapper"]/button')
    # continuar_botton.click()
    # random_sleep()
