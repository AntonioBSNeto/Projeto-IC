from tkinter import *
import requests, sys
from PIL import Image, ImageTk
import io


def getImageUrlData(wwwLocationOfImage):
    data = requests.get(wwwLocationOfImage).content
    if sys.version_info[0] < 3:
        # Python 2 approach to handling bytes
        return data.encode("base64")
    else:
        # Python 3 approach to handling bytes
        import base64
        return base64.b64encode(data).decode()


def classify(imageurl):
    #Key do Machine Learning for Kids
    key = "945c4ef0-2c52-11eb-8469-d79f2452462342ae1831-fed8-44f2-94e2-326a66318452"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={"data" : getImageUrlData(imageurl) })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer['padx'] = 20
        self.terceiroContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Quadro")
        self.titulo["font"] = ("Arial", "30", "normal")
        self.titulo.pack()

        self.linkLabel = Label(self.segundoContainer, text="Link do quadro:", font=self.fontePadrao)
        self.linkLabel.pack(side=LEFT)

        self.link = Entry(self.segundoContainer)
        self.link["width"] = 75
        self.link["font"] = self.fontePadrao
        self.link.pack(side=LEFT)

        self.buscar = Button(self.segundoContainer)
        self.buscar["text"] = "Buscar"
        self.buscar["font"] = ("Calibri", "9")
        self.buscar["width"] = 10
        self.buscar["command"] = self.loadImage
        self.buscar.pack(side=RIGHT)

    def loadImage(self):
        try:
            link_img = self.link.get()
            response = requests.get(link_img)
            image_bytes = io.BytesIO(response.content)
            img = Image.open(image_bytes)
            img = img.resize((450, 350), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            try:
                if not self.label is None:
                    self.label.pack_forget()
                if not self.imgClassificationLabel is None:
                    self.imgClassificationLabel.pack_forget()

            except:
                print('Primeira imagem')
            self.label = Label(self.terceiroContainer, image=photo)
            self.label.image = photo
            self.label.pack()

            demo = classify(link_img)

            label_img = demo["class_name"]
            confidence_img = int(demo["confidence"])

            text = ''

            if confidence_img >= 90:
                text = "Essa imagem tem grande chance de pertecenter ao "+label_img
            else:
                text = "Desculpa, eu ainda não sei classificar essa imagem :/"

            self.imgClassificationLabel = Label(self.terceiroContainer, text=text, font=("Arial", "15"))
            self.imgClassificationLabel.pack()
        except :
            print("Link inválido")


root = Tk()
root.title("Impressionista ou cubista?")

root.resizable(False, False)

window_height = 500
window_width = 900

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

Application(root)
root.mainloop()
