from loading import Tela_de_loading
from time import sleep
app = Tela_de_loading('Titulo')


app.progressbar_status(10)
sleep(3)
app.progressbar_status(20)
sleep(3)
app.progressbar_status(50)
sleep(3)
app.progressbar_status(70)
sleep(3)
app.progressbar_status(99)
sleep(3)
app.progressbar_status(100)
sleep(3)
app.mainloop()