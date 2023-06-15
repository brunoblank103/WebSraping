from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
from time import sleep


url = 'https://www.decolar.com/' #Not change

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36z \
'} #Search "myuser agent" in web for get


def definir_cidades():
    global cidade_origem, cidade_destino

    while True:
        try:
            cidade_origem = input(str('Qual a cidade de origem: ')).strip()

            for letra in cidade_origem:
                if letra.isnumeric():
                    raise

                else:
                    pass

            if len(cidade_origem) < 3:
                raise

        except:
            print('Tente novamente')

        else:
            break

    while True:
        try:
            cidade_destino = input(str('Qual a cidade de destino: ')).strip()

            for letra in cidade_destino:
                if letra.isnumeric():
                    raise

                else:
                    pass


            if len(cidade_destino) < 3:
                raise
        
        except:
            print('Tente novamente')

        else:
            break      


def origem(browser):
    origem = browser.find_element(By.XPATH, '//*[@id="searchbox-sbox-box-flights"]/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/input')
    origem.click()
    sleep(1)
    origem.send_keys(Keys.CONTROL+'A', Keys.BACK_SPACE)
    origem.send_keys(cidade_origem)
    sleep(1)
    origem.send_keys(Keys.ENTER)
    sleep(1)


def destino(browser):
    destino = browser.find_element(By.CSS_SELECTOR, 'div.sbox5-segment--2_IQ3:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)')
    destino.click()
    sleep(1)
    destino.send_keys(cidade_destino)
    sleep(1)
    destino.send_keys(Keys.ENTER)
    sleep(1)


def fechar_spans(browser):
    try:
        fechar_span1 = browser.find_element(By.CSS_SELECTOR, 'span.login-incentive--button > em:nth-child(2)')
        if fechar_span1:
            fechar_span1.click()

        fechar_span2 = browser.find_element(By.CSS_SELECTOR, 'svg.Bz112c:nth-child(2)')
        if fechar_span2:
            fechar_span2.click()
    
    except:
        pass

    finally:
        sleep(1)


def buscar_data_mais_barata(browser):
    try:
        data_barata = browser.find_element(By.CSS_SELECTOR, '#searchbox-sbox-box-flights > div > div > div > \
                                                div.sbox5-box-content--2pcCl.sbox5-flightType-roundTrip--fSJm8 > \
                                                div.sbox5-segments--lzKBc > div:nth-child(1) > div.sbox5-flex-dates-wrapper--d__IP \
                                                > span > span > label > span.switch-container')
        data_barata.click()
        sleep(1)

    except Exception as error:
        print(error)


def buscar_passagens(browser):
    try:
        buscar_passagens = browser.find_element(By.CSS_SELECTOR, '#searchbox-sbox-box-flights > div > div > div > \
                                            div.sbox5-box-content--2pcCl.sbox5-flightType-roundTrip--fSJm8 > div.sbox5-button-container--1X4O8 > button > em')
        buscar_passagens.click()  

    except Exception as error:
        print(error)


def scraping_passagens(browser):
    try:
        browser.execute_script('window.scroll(0, 2500)')
        sleep(2)
        browser_content = browser.page_source
        soup = BeautifulSoup(browser_content, 'html.parser')
        viagens = soup.find_all('div', class_='cluster-container border not-overflow')

        lista_viagens = []

        for viagem in viagens:
            datas = viagem.find_all('div', class_='date -eva-3-bold route-info-item-date lowercase')
            count = 1
            for data in datas:
                if count == 1:
                    data_ida = data.text
                if count == 2:
                    data_volta = data.text
                count += 1

            valor = viagem.find('span', class_='pricebox-big-text price').get_text()
            valor = f'R${valor}'
            lista_viagens.append([data_ida, data_volta, valor])
    except Exception as error:
        print(error)

    if len(lista_viagens) != 0:  
        try:
            tabela_valores = pd.DataFrame(lista_viagens, columns=['IDA', 'VOLTA', 'VALOR'])
            tabela_valores.to_csv(f'PASSAGEM_{cidade_origem}_A_{cidade_destino}.csv', index=False)
            print('Arquivo salvo')

        except Exception as error:
            print(error)


definir_cidades()
options = Options()
options.add_argument('--headless') #This function does not open the browser on the pc
browser = webdriver.Firefox(options=options) # If you want to switch firefox to Chrome, change this library "from selenium.webdriver.firefox.options" to "from selenium.webdriver.chrome.options"
browser.get(url)
sleep(2)
origem(browser)
fechar_spans(browser)
destino(browser)
buscar_data_mais_barata(browser)
buscar_passagens(browser)
sleep(3)
scraping_passagens(browser)