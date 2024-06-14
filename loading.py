import tkinter as tk
from tkinter import ttk, DoubleVar
from PIL import Image, ImageTk
from time import sleep


class Tela_de_loading(tk.Tk):
    def __init__(self, titulo):
        super().__init__()
        self.title(titulo)
        self.geometry('480x480')
        self.configure(bg='#00BEE0')
        self.overrideredirect(True)
        self.label = tk.Label(self, bg='#00E092',width=480, height=480)
        self.label.pack()
        self.imagem = Image.open('loading.jpg')
        self.imag = ImageTk.PhotoImage(image=self.imagem)
        self.imagquadro =  ttk.Frame(self, width=40, height=40)
        self.imagquadro.place(x=230, y=201)
        self.imglabel = tk.Label(self.imagquadro, image=self.imag, width=100, height=30)
        self.imglabel.place(x=100,y=10)
        self.botao_fechar = tk.Button(width=10, height=1, bg='#00E092', text='X',font=('KoPubBatang Regular', 10 * -1), command=self.close,highlightthickness=0,highlightbackground='white', borderwidth=5, relief=tk.FLAT)
        self.loading = tk.Label(self, text="CARREGANDO", bg='#00E092', font=('RBNo3.1', 20 * -1))
        self.loading.place(x=159, y=330)
        self.botao_fechar.place(x=410, y=0)
        self.botao_fechar.bind('<Enter>', self.on_enter)
        self.botao_fechar.bind('<Leave>', self.on_leave)
        self.label.bind("<ButtonPress-1>",self.iniciar_arrastaesolta)
        self.imglabel.bind("<ButtonPress-1>",self.iniciar_arrastaesolta)
    def iniciar_tela(self):
        self.mainloop()

    def iniciar_arrastaesolta(self, event):
        self._x = event.x
        self._y = event.y
        self.label.bind("<B1-Motion>", self.arrastar)
        self.label.bind('<ButtonRelease-1>', self.soltar)
    def arrastar(self, event):
        delta_x = event.x - self._x
        delta_y = event.y - self._y
        nova_posicao_x = self.winfo_x() + delta_x
        nova_posicao_y = self.winfo_y() + delta_y
        self.geometry(f'+{nova_posicao_x}+{nova_posicao_y}')
    def soltar(self, event):
        self.label.unbind('<B1-Motion>')
        self.label.unbind('<ButtonRelease-1>')
    def close(self):
        self.destroy()

    def progressBar(self, variable):
        self.varbarra=DoubleVar()
        self.varbarra.set(variable)
        self.pb = ttk.Progressbar(self.label, variable=self.varbarra, maximum=100)
        self.pb.place(x=30, y=360,width=400,height=20)   

    def progressbar_status(self,valor):
            self.valor = valor
            if valor <= 10:
                self.progressBar(valor)
                self.loading_carregando()
                self.update()
            elif valor > 10 and valor <= 20:
                self.progressBar(valor)
                self.loading_carregando()
                self.update()
            elif valor > 20 and valor <= 30:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 30 and valor <= 40:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 40 and valor <= 50:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 50 and valor <= 60:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 60 and valor <= 70:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 70 and valor <= 80:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 80 and valor <= 90:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
            elif valor > 90 and valor <= 100:
                self.loading_carregando()
                self.progressBar(valor)
                self.update()
                sleep(3)
                self.destroy()
            else:
                pass
    def loading_carregando(self):

        while 1 < 100:
            print(self.valor)
            for num in range(5):
                if num == 5:
                    num = 0
                sleep(1/2)
                self.loading['text'] = 'carregando' + ("." * num) 
                self.update()
            
    def on_enter(self,event):
        self.botao_fechar['bg'] = 'RED'
    def on_leave(self, event):
        self.botao_fechar['bg'] = '#00E092'     


if __name__ == '__main__':
    tela1 = Tela_de_loading(titulo="Meu titulo teste")
    tela1.mainloop()


