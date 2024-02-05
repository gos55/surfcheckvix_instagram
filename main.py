from selenium import webdriver
from time import sleep
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
import pywinauto
import psutil

print('Abrindo chrome')
##acessando o surfguru e capturando a imagem do swell
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
options = ChromeOptions()
options.headless = True
#browser = #webdriver.Firefox(executable_path=r"C:\Users\gabri\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\geckodriver.exe")

browser = webdriver.Chrome(options=chrome_options, executable_path=r'E:\Gabriel\Python\SurfCheckVix\chromedriver.exe')
browser.set_window_size(2000, 2000)

URI = 'https://surfguru.com.br/previsao/brasil/espirito-santo/vitoria/'
browser.get(URI)

sleep(3)

S = lambda X: browser.execute_script('return document.body.parentNode.scroll'+X)

button = browser.find_element(by=By.CSS_SELECTOR, value='#aceitar_cookies_conteudo > button')

button.click()

sleep(1)


#Início do banco de dados
print('Iniciando banco de dados...')

print('Obtendo dados da altura do dia...')
lista_alt = []

diaa = 0
str(diaa)

while (diaa < 5):
    dia = 1
    diaa = diaa + 1


    while dia <= 8:
        css_sel = ('//*[@id="title_dia' + str(diaa)+ '_hora' + str(dia) + '"]')
        print(css_sel)
        wait = WebDriverWait(browser, 3)
        wait.until(EC.element_to_be_clickable((By.XPATH, css_sel)))
        aa = browser.find_element(By.XPATH, css_sel)
        a = ActionChains(browser)
        a.move_to_element(aa).perform()
        sleep(0.05)
        tot_alt = browser.find_element(By.XPATH, '//*[@id="tot_alt"]')
        tot_alt = tot_alt.text
        print(tot_alt)
        tot_alt = tot_alt.replace(' m','')
        sleep(0.05)
        tot_alt = float(tot_alt)
        lista_alt.append(tot_alt)
        dia = dia + 1

print(lista_alt)
alt_max = max(lista_alt)

sleep(1)

#Obtendo dados de potencia do dia
print('Obtendo dados de potência do dia...')
potencia = []
print(potencia)
browser.find_element(by=By.CSS_SELECTOR, value='#btn-barra11 > div:nth-child(1)').click()
sleep(1)

dia_1 = browser.find_element(by=By.CSS_SELECTOR, value='#resumo_energia_1 > label.resumo_energia_en')
print(dia_1)
dia_1 = dia_1.text
print(dia_1)
dia_1 = [int(s) for s in dia_1.split() if s.isdigit()]
potencia.append(dia_1[0])

dia_2 = browser.find_element(by=By.CSS_SELECTOR, value='#resumo_energia_2 > label.resumo_energia_en')
dia_2 = dia_2.text
dia_2 = [int(s) for s in dia_2.split() if s.isdigit()]
potencia.append(dia_2[0])

dia_3 = browser.find_element(by=By.CSS_SELECTOR, value='#resumo_energia_3 > label:nth-child(2)')
dia_3 = dia_3.text
dia_3 = [int(s) for s in dia_3.split() if s.isdigit()]
potencia.append(dia_3[0])

dia_4 = browser.find_element(by=By.CSS_SELECTOR, value='#resumo_energia_4 > label:nth-child(2)')
dia_4 = dia_4.text
dia_4 = [int(s) for s in dia_4.split() if s.isdigit()]
potencia.append(dia_4[0])

dia_5 = browser.find_element(by=By.CSS_SELECTOR, value='#resumo_energia_5 > label:nth-child(2)')
dia_5 = dia_5.text
dia_5 = [int(s) for s in dia_5.split() if s.isdigit()]
potencia.append(dia_5[0])
print(potencia)

sleep(0.5)

#obtendo dados do vento
print('Obtendo dados do vento no dia...')
browser.find_element(by=By.CSS_SELECTOR, value='#aba_unid_nos > a').click()


lista_vento = []
vento_mouse = 1
str(vento_mouse)
while (vento_mouse <= 8):
    css_sel = ('//*[@id="title_vento_dia1_hora' + str(vento_mouse) + '"]')
    print(css_sel)
    wait = WebDriverWait(browser, 5)
    wait.until(EC.element_to_be_clickable((By.XPATH, css_sel)))
    aa = browser.find_element(By.XPATH, css_sel)
    a = ActionChains(browser)
    a.move_to_element(aa).perform()
    sleep(0.2)
    tot_vento = browser.find_element(By.XPATH, '//*[@id="vento_int2"]')
    tot_vento = tot_vento.text
    print(tot_vento)
    tot_vento = [int(s) for s in tot_vento.split() if s.isdigit()]
    lista_vento.append(tot_vento[0])
    vento_mouse = vento_mouse + 1
print(lista_vento)
menor_vento = min(lista_vento)
index = lista_vento.index(menor_vento)
menor_vento = str(menor_vento)
print(lista_vento)

sleep(0.5)

#obtendo direção direcao_predominante
direcao_manha = browser.find_element(By.XPATH, value='//*[@id="altura_dia1"]/div[11]/div[2]/span')
direcao_manha = direcao_manha.text


#screenshot de cada gráfico
print('Tirando screenshot e editando cada gráfico...\n')

browser.find_element(by=By.CSS_SELECTOR, value='#altura_display').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p1.png')
#edição do gráfico obtido
grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p1.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p1.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-130))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((250, 35), 'Tamanho', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d1.png')

sleep(1)

vagas = browser.find_element(by=By.XPATH, value='//*[@id="aba_grafico_vagas"]/a')
browser.execute_script("arguments[0].click();", vagas)

sleep(1)

browser.find_element(by=By.CSS_SELECTOR, value='#altura_display').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p2.png')

grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p2.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p2.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-130))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((250, 35), 'VAGAS', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d2.png')

sleep(1)

sweel_sul = browser.find_element(by=By.XPATH, value='//*[@id="aba_grafico_sul"]/a')
browser.execute_script("arguments[0].click();", sweel_sul)
sleep(1)

browser.find_element(by=By.CSS_SELECTOR, value='#altura_display').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p3.png')

grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p3.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p3.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-130))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((250, 35), 'Sweel de Sul', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d3.png')

sleep(1)

grafico_norte = browser.find_element(by=By.XPATH, value='//*[@id="aba_grafico_norte"]/a')
browser.execute_script("arguments[0].click();", grafico_norte)
browser.find_element(by=By.CSS_SELECTOR, value='#altura_display').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p4.png')

grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p4.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p4.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-130))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((250, 35), 'Sweel de Norte', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d4.png')

sleep(0.5)
browser.find_element(by=By.CSS_SELECTOR, value='#resumo-box11').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p5.png')

grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p5.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p5.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-230))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((135, 70), 'Energia e Potência', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d5.png')

sleep(1)

vento_click = browser.find_element(by=By.CSS_SELECTOR, value = '#aba_unid_nos > a')
browser.execute_script("arguments[0].click();", vento_click)

browser.find_element(by=By.XPATH, value='//*[@id="vento_display"]').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p7.png')

grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p7.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p7.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-130))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((250, 35), 'Vento', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d7.png')


sleep(1)


aba_mare = browser.find_element(by=By.CSS_SELECTOR, value='#aba_mare_1 > a')
browser.execute_script("arguments[0].click();", aba_mare)
browser.find_element(by=By.CSS_SELECTOR, value='#area_mares').screenshot('E:\Gabriel\Python\SurfCheckVix\Screenshots\p8.png')

grafico = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\p8.png')
fundo = Image.open('E:\Gabriel\Python\SurfCheckVix\Screenshots\pfundo.png')
grafico.thumbnail((600,600))
grafico.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\p8.png')
grafico_copy = grafico.copy()
position = ((fundo.width - grafico_copy.width), (fundo.height - grafico_copy.height-130))
fundo.paste(grafico_copy, position)
tratada = ImageEnhance.Contrast(fundo)
tratada.enhance(1.5)
img_draw = ImageDraw.Draw(fundo)
font = ImageFont.truetype(r'E:\Gabriel\Python\SurfCheckVix\Screenshots\OpenSans-Bold.ttf', 40)
img_draw.text((250, 35), 'Maré', font = font, fill='black')
fundo.save('E:\Gabriel\Python\SurfCheckVix\Screenshots\d8.png')

sleep(1)

#Criando a legenda

print('Criando a legenda...')

#LEGENDA -   Definindo maior altura

maior_altura = max(lista_alt[:7])
maior_altura = str(maior_altura)
#LEGENDA - Potência
max_potencia = max(potencia)
max_potencia = str(max_potencia)

if potencia[0] > 2500:
    ressaca_alert = '! ! ! RESSACA ALERT ! ! !\nNa dúvida, não entre no mar!\n\n'
else:
    ressaca_alert = '.\n\n'

#LEGENDA - vento
if index <= 5 :
    vento_descricao =  menor_vento + ' nós pela manhã'
else:
    vento_descricao =  menor_vento + ' nós após o meio dia'

#lEGENDA - direcao
at = browser.find_element(By.CSS_SELECTOR, value='#aba_grafico_total > a')
browser.execute_script("arguments[0].click();", at)
direcao_manha = browser.find_element(By.CSS_SELECTOR, value='#altura_dia1 > div.direcoes_dia > div.direcao2 > span').get_attribute("title")
direcao_manha = direcao_manha.replace(' |',', ')

direcao_tarde = browser.find_element(By.CSS_SELECTOR, value='#altura_dia1 > div.direcoes_dia > div.direcao3 > span').get_attribute("title")
direcao_tarde = direcao_tarde.replace(' |',', ')

print(direcao_manha)
print(direcao_tarde)

#LEGENDA - energia_dia
energia_dia = browser.find_element(by=By.XPATH, value= '//*[@id="resumo_energia_1"]/label[3]')
energia_dia = browser.find_element(by=By.XPATH, value= '//*[@id="resumo_energia_1"]/label[3]')
print(energia_dia)
energia_dia = energia_dia.text
print(energia_dia)
energia_dia = energia_dia[:-2]
print(energia_dia)

#LEGENDA - Vento manha e vento_tarde
vento_manha = browser.find_element(By.CSS_SELECTOR, value='#casa_vento_dia1 > div.direcoes_dia_vento > div.direcao2 > span').get_attribute("title")
vento_manha = vento_manha.replace(' |',', ')

vento_tarde = browser.find_element(By.CSS_SELECTOR, value='#casa_vento_dia1 > div.direcoes_dia_vento > div.direcao3 > span').get_attribute("title")
vento_tarde = vento_tarde.replace(' |',', ')

print(vento_manha)
print(vento_tarde)

#LEGENDA - Maré
aba_mare = browser.find_element(by=By.CSS_SELECTOR, value='#aba_mare_1 > a')
browser.execute_script("arguments[0].click();", aba_mare)
hora_1 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare1 > div.hora_mare')
print(hora_1)
hora_1 = hora_1.text
print(hora_1)
hora_1 = str(hora_1)
print(hora_1)

mare_1 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare1 > div.altura_mare')
print(mare_1)
mare_1 = mare_1.text
print(mare_1)
mare_1 = str(mare_1)
print(mare_1)

hora_2 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare2 > div.hora_mare')
hora_2 = hora_2.text
hora_2 = str(hora_2)

mare_2 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare2 > div.altura_mare')
mare_2 = mare_2.text
mare_2 = str(mare_2)

hora_3 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare3 > div.hora_mare')
hora_3 = hora_3.text
hora_3 = str(hora_3)

mare_3 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare3 > div.altura_mare')
mare_3 = mare_3.text
mare_3 = str(mare_3)

try:
    hora_4 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare4 > div.hora_mare')
    hora_4 = hora_4.text
    hora_4 = str(hora_4)
    mare_4 = browser.find_element(By.CSS_SELECTOR, value='#dia1_horaMare4 > div.altura_mare')
    mare_4 = mare_4.text
    mare_4 = str(mare_4)
except:
    mare_4 = ''
    mare_4 = str(mare_4)
    hora_4 = ''
    hora_4 = str(hora_4)
    print('3 marés no dia apenas')

potencia_0 = potencia[0]
potencia_0 = str(potencia_0)
alt_max = str(alt_max)

print(type(ressaca_alert))
print(type(maior_altura))
print(type(direcao_manha))
print(type(direcao_tarde))
print(type(potencia_0))
print(type(energia_dia))
print(type(vento_descricao))
print(type(vento_manha))
print(type(vento_tarde))
print(type(mare_1))
print(type(hora_1))
print(type(mare_2))
print(type(hora_2))
print(type(mare_3))
print(type(hora_3))
print(type(mare_4))
print(type(hora_4))
print(type(alt_max))



descricao = 'Bom Dia!\n\nSegue o boletim matinal do surf para o ES\n\n' + ressaca_alert + 'Durante o dia de hoje teremos uma altura máxima de ondas oceânicas de ' + maior_altura + ' metros, direção predominante pela ' + direcao_manha + ' e pela ' + direcao_tarde +', potência de ' + potencia_0 + 'J e energia em ' + energia_dia + '. O horário de menor vento é ' + vento_descricao + ' direção pela ' + vento_manha + ' e pela ' + vento_tarde + '.' + '\n\nA variação de maré hoje será: ' + mare_1 + ' às ' + hora_1 + ', '  + mare_2 + ' às ' + hora_2 + ', '  + mare_3 + ' às ' + hora_3 + ' e '  + mare_4 + ' às ' + hora_4 + '.'  +  '\n\nDentro dos próximos 5 dias teremos uma altura máxima de ' + alt_max + 'm e potência de ' + max_potencia + 'J.' '\n\nImagens: @Surfgurupro '

print(descricao)


#acessando instagram
options = ChromeOptions()
options.headless = True
browser2 = webdriver.Firefox(executable_path=r"C:\Users\gabri\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\geckodriver.exe")
URI2 = 'https://www.instagram.com/accounts/login/'
browser2.get(URI2)


sleep(2)

username = 'SurfCheckVix'
password = password

#login
find_username = browser2.find_element(by=By.NAME, value='username')
find_username.send_keys(username)
sleep(1)
find_password = browser2.find_element(by=By.NAME, value='password')
find_password.send_keys(password)
sleep(1)
click_login = browser2.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button/div')
browser2.execute_script("arguments[0].click();", click_login)

sleep(5)

#sleep(6)

find_post_plus = browser2.find_element(by=By.XPATH, value='/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button')
browser2.execute_script("arguments[0].click();", find_post_plus)


sleep(2)
#selecionar do computador botão
post_image = browser2.find_element(by=By.CSS_SELECTOR, value="button.L3NKy:nth-child(1)" )
browser2.execute_script("arguments[0].click();", post_image)
sleep(1)

#selecionar as imagens do computador
app = pywinauto.application.Application()
proc = psutil.Process(browser2.service.process.pid).children()[0].pid
app.connect(process=proc)
dialog = app.top_window()
sleep(1)
dialog.Edit.TypeKeys('E:\Gabriel\Python\SurfCheckVix\Screenshots\ "d1" "d2" "d3" "d4" "d5" "d7" "d8"')
sleep(0.5)

sleep(0.5)
dialog['&OpenButton'].click()

sleep(5)

#redimensionar_imagem = browser.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]')
#redimensionar_imagem.click()

sleep(1)
#imagem_169 = browser.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[4]/div')
#imagem_169.click()

post_avancar = browser2.find_element(by=By.CSS_SELECTOR, value='.XfCBB > button:nth-child(1)')
post_avancar.click()

post_avancar2 = browser2.find_element(by=By.CSS_SELECTOR, value='.XfCBB > button:nth-child(1)')
post_avancar2.click()

legenda = browser2.find_element(by=By.XPATH, value='/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea')
legenda.send_keys(descricao)

compartilhar = browser2.find_element(by=By.CSS_SELECTOR, value='.XfCBB > button:nth-child(1)')
compartilhar.click()

print('done')
