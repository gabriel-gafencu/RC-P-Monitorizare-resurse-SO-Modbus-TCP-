from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Client Modbus TCP")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="Informatii mapare")
        lbl.grid(sticky=W, pady=4, padx=5)
        n = Notebook(self)
        f1 = Frame(n)
        f2 = Frame(n)
        f3 = Frame(n)
        f4 = Frame(n)
        n.add(f1, text='Coils')
        n.add(f2, text='Descrete Inputs')
        n.add(f3, text='Input Registers')
        n.add(f4, text='Hold Registers')
        n.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)

        abtn= Radiobutton(self, text="conectat/deconectat")
        abtn.grid(row=1, column=3)

        hbtn = Button(self, text="Info",command=self.about)
        hbtn.grid(row=4, column=3, padx=5)

        cbtn = Button(self, text="Inchidere", command=self.exitapp)
        cbtn.grid(row=5, column=3, pady=4)

        labelc = Label(self, text="Ultima cerere:", anchor=W)
        labelc.grid(row=2, column=3)
        cerere = LabelFrame(self)
        cerere.grid(row=3, column=3, columnspan=2,rowspan=1, sticky=E + W + S + N)

        labels = Label(self, text="Status:", anchor=W)
        labels.grid(row=5, column=0)
        status = LabelFrame(self)
        status.grid(row=5, column=1,columnspan=2,sticky=E+W+S+N)

    def exitapp(self):
        self.destroy()
        sys.exit()
    def about(self):
        messagebox.showinfo("Info", "Proiect realizat de Ichim Ioana si Gafencu Gabriel")

def main():

    root = Tk()
    root.geometry("600x300+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()