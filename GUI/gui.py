from pathlib import Path
from tkinter import Tk, Canvas, font as tkFont, Frame
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
from datetime import datetime, date
from funcoes_gui import empresa_btn, get_column_names
from PIL import Image, ImageTk



def carregar_imagem(caminho):
    image_pil = Image.open(caminho)
    image_tk = ImageTk.PhotoImage(image_pil)
    return image_tk


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
    data1 = cal.get_date()
    data2 = cal2.get_date()
    global valor
    valor = empresa_btn(empobra=empobra)
    for empresa in lista_empresas:
        if empresa['desc'] == valor:
            print(empresa['cod'])
    print(data2, data1, valor)


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
    relief="ridge"
)
canvas.place(x=0, y=0)

# Criação dos elementos no Canvas
rect1 = canvas.create_rectangle(0.0, 0.0, 384.0, 720.0, fill="#FFFFFF", outline="")
rect2 = canvas.create_rectangle(32.0, 13.0, 352.0, 200.0, fill="#FFFFFF", outline="")
text1 = canvas.create_text(0, 100.0, anchor="nw", text="TS-OBRA", fill="#000000", font=("KoPubBatang Regular", 24 * -1))
text2 = canvas.create_text(0, 220.0, anchor="nw", text="Data-Início", fill="#000000", font=("KoPubBatang Regular", 24 * -1))
text3 = canvas.create_text(0, 480.0, anchor="nw", text="Data-Fim", fill="#000000", font=("KoPubBatang Regular", 24 * -1))

#IMAGEM DE FUNDO
caminho_imagem = 'imagem_prd.jpg'
quadro = Frame(window, width=896, height=720, background='red')
quadro.place(x=384, y=0)
img = carregar_imagem(caminho_imagem)
image = ttk.Label(quadro, image=img)
image.pack()


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
    canvas.coords(text1, (384 / 2 - text1_width / 2), 100.0)
    canvas.coords(text2, (384 / 2 - text2_width / 2), 190.0)
    canvas.coords(text3, (384 / 2 - text2_width / 2), 338.0)

# Chama a função para centralizar os textos
centralize_texts()
box = Frame(window, width=288, height=400, background='darkblue')
box.place(x=80, y=145)

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
frame1 = Frame(window, width=288, height=450, background='darkblue')
#frame1 é o data fim
frame1.place(x=130, y=450)
datar = datetime.now().strftime('%d, %m, %Y')
datahoje = date(int(datar[8:12]), int(datar[5]), int(datar[1]))
# Adiciona o DateEntry no frame usando grid
cal = DateEntry(frame1, width=12, background='darkblue', foreground='white', borderwidth=2,maxdate=datahoje, locale='pt_br')
cal.grid(row=1, column=1, padx=5,pady=5)
datecal2 = date(int(datar[8:12]), int(datar[5]), (int(datar[1]) - 5))
frame2 = Frame(window, width=288, height=400, background='darkblue')
frame2.place(x=130, y=300)
# Adiciona o DateEntry no frame usando grid
cal2 = DateEntry(frame2, width=12, background='darkblue', foreground='white', borderwidth=2,locale='pt_br', maxdate=datecal2)
cal2.grid(row=1, column=1, padx=5,pady=5)

frameb1= Frame(window, width=60,height=30,background='darkblue')
frameb1.place(x=146, y=550)
b1 = tk.Button(frameb1,text='SALVAR',command=on_button)
b1.grid(row=1,column=1,padx=5,pady=5)

# Não permitir redimensionamento da janela
window.resizable(False, False)
window.mainloop()