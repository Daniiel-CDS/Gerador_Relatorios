from pathlib import Path
from tkinter import Tk, Canvas, font as tkFont, Frame
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
from funcoes_gui import empresa_btn, get_column_names
from PIL import Image, ImageTk
import sys
import os
# from loading import start_loading
from main import execute_main

label_resultado = None

def carregar_imagem(caminho):
    image_pil = Image.open(caminho)
    image_tk = ImageTk.PhotoImage(image_pil)
    return image_tk



def update_empobra(*args):
    # Obtém o texto digitado na empobra
    typed_text = empobra.get()
    
    # Filtra a lista de valores
    if typed_text == '':
        empobra['values'] = valores  # Exibe todos os valores se não houver texto digitado
    else:
        filtered_values = [item for item in valores if typed_text.lower() in item.lower()]
        empobra['values'] = filtered_values
    empobra.icursor(tk.END)
    # Abre a lista de opções da empobra
    empobra.event_generate('<Down>')

# Função para calcular o caminho relativo dos ativos
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_init():
    global lista_empresas    
    lista_empresas = get_column_names()
    print(lista_empresas)
# Função para simular um clique no DateEntry
def open_calendar(event):
    cal.event_generate('<Button-1>')

#def on_event(*args):
  
def on_button():
    global data1,data2
    global label_resultado
    data2 = cal.get_date()
    data1 = cal2.get_date()
    global valor
    global valor_nome
    valor = None
    valor_nome = None
    valor = empresa_btn(empobra=empobra)
    if label_resultado:
        label_resultado.destroy()
    else:
        pass
    for empresa in lista_empresas:
        if empresa['desc'] == valor:
            valor = empresa['cod']
            valor_nome = str(valor)
            valor = '245|'+str(valor)
    for empresa in lista_empresas:
        if empresa['desc'] == valor:
           valor = empresa['cod']
           valor_nome = str(valor)
           valor = '245|'+str(valor)
    resultado = execute_main(data1, data2, valor, valor_nome)
    if resultado:
        label_resultado = tk.Label(window,text='relatorio gerado com sucesso', background='white',fg='green',font=('Trebuchet Ms', 8, 'bold'))
        label_resultado.place(x=110, y=600)
    else:
        label_resultado = tk.Label(window,text='nenhum dado encontrado para o período especificado.', background='white', fg='red',font=('Trebuchet Ms', 8, 'bold'))
        label_resultado.place(x=50, y=600)
    
    
    


on_init()

# Configuração da janela principal
window = Tk()
window.geometry("1280x720")
window.configure(bg="#001069")
icone = carregar_imagem(caminho='maua.png')
window.wm_iconbitmap('grupo_toctao_logo.ico')
window.title('Gerador de Relatórios')
window.wm_iconphoto(False, icone)


# Criação do Canvas
canvas = Canvas(
    window,
    bg="#001069",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
canvas.place(x=0, y=0)

# Criação dos elementos no Canvas
rect1 = canvas.create_rectangle(0.0, 0.0, 384.0, 720.0, fill="#FFFFFF", outline="")
rect2 = canvas.create_rectangle(32.0, 13.0, 352.0, 200.0, fill="#FFFFFF", outline="")
text1 = canvas.create_text(0, 100.0, anchor="nw", text="TS-OBRA", fill="#1f4164", font=("KoPubBatang Regular", 24 * -1))
text2 = canvas.create_text(0, 350.0, anchor="nw", text="Data-Início", fill="#1f4164", font=("KoPubBatang Regular", 24 * -1))
text3 = canvas.create_text(0, 480.0, anchor="nw", text="Data-Fim", fill="#1f4164", font=("KoPubBatang Regular", 24 * -1))

#IMAGEM DE FUNDO
caminho_imagem = 'imagem_prd.jpg'
quadro = Frame(window, width=896, height=720, background='red')
quadro.place(x=384, y=0)
img = carregar_imagem(caminho_imagem)
image = ttk.Label(quadro, image=img)
image.pack()

logo_ts = 'toctao_ts.jpeg'
quadro_ts = Frame(window, width=280, height=190,background='black')
quadro_ts.place(x=86,y=25)
img2 = carregar_imagem(logo_ts)
image2 = ttk.Label(quadro_ts, image=img2)
image2.pack()



# Função para centralizar os textos horizontalmente na barra branca
def centralize_texts():
    # Ajuste do tamanho da fonte proporcionalmente
    font_size = 24  # Tamanho fixo da fonte
    custom_font = tkFont.Font(family="KoPubBatang Regular", size=font_size)
    
    # Ajuste dos textos conforme o redimensionamento
    canvas.itemconfig(text1, font=custom_font)
    canvas.itemconfig(text2, font=custom_font)
    canvas.itemconfig(text3, font=custom_font)
    
    # Obter a largura dos textos
    text1_width = custom_font.measure("TS-OBRA")
    text2_width = custom_font.measure("Data-Início")
    text3_width = custom_font.measure("Data-Fim")
    
    # Centralizar os textos horizontalmente na barra branca
    canvas.coords(text1, (384 / 2 - text1_width / 2), 250.0)
    canvas.coords(text2, (184 / 2 - text2_width / 2), 345)
    canvas.coords(text3, (164 / 2 - text3_width / 2), 390)

# Chama a função para centralizar os textos
centralize_texts()
box = Frame(window, width=288, height=400, background='#1f4164')
box.place(x=90, y=300)

valores = []
# sel = tk.StringVar()
for descricao in lista_empresas:
    print(descricao['desc'])
    valores.append(descricao['desc'])
    print("valores = ", valores)
print(f"\n \n \n",valores)
empobra = ttk.Combobox(box, values=valores, width=30)
empobra.grid(row=1,column=1,padx=3,pady=3)

# sel.trace('w', on_event)



# Criação de um frame para posicionar o DateEntry
frame1 = Frame(window, width=288, height=450, background='#1f4164')
#frame1 é o data fim
frame1.place(x=190, y=395)
datar = datetime.now().strftime('%d, %m, %Y')
dia, mes, ano = datar.split(',')
datahoje = date(int(ano), int(mes), int(dia))
# Adiciona o DateEntry no frame usando grid
cal = DateEntry(frame1, width=12, background='#1f4164', foreground='white', borderwidth=2,maxdate=datahoje, locale='pt_br')
cal.grid(row=1, column=1, padx=2,pady=2)
datecal2 = date(int(ano), int(mes), (int(dia) - 5))
frame2 = Frame(window, width=288, height=400, background='#1f4164')
frame2.place(x=190, y=345)
# Adiciona o DateEntry no frame usando grid
cal2 = DateEntry(frame2, width=12, background='#1f4164', foreground='white', borderwidth=2,locale='pt_br', maxdate=datecal2)
cal2.grid(row=1, column=1, padx=2,pady=2)

frameb1= Frame(window, width=60,height=30,background='#1f4164')
frameb1.place(x=146, y=550)
b1 = tk.Button(frameb1,text='SALVAR',command=on_button)
b1.grid(row=1,column=1,padx=2,pady=2)

# Não permitir redimensionamento da janela
empobra.bind('<KeyRelease>', update_empobra)
window.resizable(False, False)
window.mainloop()