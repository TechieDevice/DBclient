#Импорт библиотеки для работы с оконными приложениями
from tkinter import *
#Импорт библиотеки для вывода ошибок
import traceback
#Импорт модуля для выполения запросов
import socket
import time
#from databaseConn import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
role = ""

class mainWindow:
    global role
    #Параметры окна\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\    
    window = Tk()
    window.title('SCADA')                              
    window.geometry('520x320')       
    


    #tester\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    testercanvas = Canvas(window, width=1020, height=720, bg='#ddd')  

    #reqLabel = Label(testercanvas, text='', bg='#ddd')
    #reqLabel.place(x=15, y=10, anchor="nw")
    #testerRequest = StringVar()
    #requestEntry = Entry(testercanvas, textvariable=testerRequest, width=36)
    #requestEntry.place(x=15, y=30, anchor="nw")

    textLabel = Label(testercanvas, wraplength=555, width=80, height=4, justify=LEFT, anchor="nw")
    textLabel.place(x=265, y=60)
    
    nameLabel = Label(testercanvas, width=40, justify=LEFT)
    nameLabel.place(x=265, y=30)
    

    #check = BooleanVar()
    #check.set(0)
    #checkSegment = Checkbutton(testercanvas, text="", variable=check, onvalue=1, offvalue=0, bg='#ddd')
    #checkSegment.place(x=15, y=52)

    #fileLabel = Label(testercanvas, text='', bg='#ddd')
    #fileLabel.place(x=15, y=150, anchor="nw")
    #filename = StringVar()
    #pathEntry = Entry(testercanvas, textvariable=filename, width=36)
    #pathEntry.place(x=15, y=170, anchor="nw")

    selectButton = Button(testercanvas, text = 'Запрос', width=30, height=2)

    def selectfile():
        try:
            global role
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.send("get".encode())
            print("get send")
            time.sleep(1)
            data = role
            sock.send(data.encode())
            print(data)
            resb = sock.recv(1024)
            res = resb.decode() 
            time.sleep(1)
            sock.send("nxt".encode())
            mainWindow.textLabel.config(text = res)
        except Exception as e:
            mainWindow.textLabel.config(text = traceback.format_exc())

    selectButton.config(command=selectfile)
    selectButton.place(x=15, y=80, anchor="nw")
    

    grafcanvas = Canvas(testercanvas, width=1000, height=500, bg='#555')
    grafcanvas.place(x=7, y=205, anchor="nw")

    grafButton = Button(testercanvas, text = 'Топология', width=20, height=1)
    #grafButton.place(x=1005, y=170, anchor="ne")


    disconnUserButton = Button(testercanvas, text = 'Отключиться', width=20, height=1)

    def Userdisconnection():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.close()
            mainWindow.loginCanvas.pack()
            #mainWindow.testerRequest.set("")
            mainWindow.testercanvas.pack_forget()
            mainWindow.window.geometry('520x320')
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())

    disconnUserButton.config(command=Userdisconnection)
    disconnUserButton.place(x=1005, y=10, anchor="ne")



    #admin\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    admincanvas = Canvas(window, width=820, height=320, bg='#ddd') 

    FLabel = Label(admincanvas, text='Поля', bg='#ddd')
    FLabel.place(x=15, y=20, anchor="nw")
    fieldRequest = StringVar()
    fieldEntry = Entry(admincanvas, textvariable=fieldRequest, width=36)
    fieldEntry.place(x=15, y=40, anchor="nw")

    TLabel = Label(admincanvas, text='Таблица', bg='#ddd')
    TLabel.place(x=245, y=20, anchor="nw")
    tableRequest = StringVar()
    tableEntry = Entry(admincanvas, textvariable=tableRequest, width=16)
    tableEntry.place(x=245, y=40, anchor="nw")

    VLabel = Label(admincanvas, text='Значения', bg='#ddd')
    VLabel.place(x=355, y=20, anchor="nw")
    valuesRequest = StringVar()
    valuesEntry = Entry(admincanvas, textvariable=valuesRequest, width=46)
    valuesEntry.place(x=355, y=40, anchor="nw")

    resultLabel = Label(admincanvas, wraplength=420, width=60, height=11, justify=LEFT, anchor="nw")
    resultLabel.place(x=15, y=130)

    writeButton = Button(admincanvas, text = 'Добавить запись', width=20, height=2)

    def write():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.send("add".encode())
            print("add send")
            time.sleep(1)
            data = mainWindow.tableRequest.get() + "|" + \
                   mainWindow.fieldRequest.get() + "|" + \
                   mainWindow.valuesRequest.get()
            sock.send(data.encode())
            print(data)
            time.sleep(1)
            sock.send("nxt".encode())
            mainWindow.resultLabel.config(text = '')
        except Exception as e:
            mainWindow.resultLabel.config(text = traceback.format_exc())

    writeButton.config(command=write)
    writeButton.place(x=15, y=80, anchor="nw")

    selButton = Button(admincanvas, text = 'Запрос', width=20, height=2)

    def sel():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.send("sel".encode())
            print("sel send")
            time.sleep(1)
            data = mainWindow.tableRequest.get() + "|" + \
                   mainWindow.fieldRequest.get() + "|" + \
                   mainWindow.valuesRequest.get()
            sock.send(data.encode())
            print(data)
            resb = sock.recv(1024)
            res = resb.decode() 
            time.sleep(1)
            sock.send("nxt".encode())
            mainWindow.resultLabel.config(text = res)
        except Exception as e:
            mainWindow.resultLabel.config(text = traceback.format_exc())
            print('Ошибка:\n', traceback.format_exc())

    selButton.config(command=sel)
    selButton.place(x=175, y=80, anchor="nw")

    deleteButton = Button(admincanvas, text = 'Удалить', width=20, height=2)

    def delete():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.send("del".encode())
            print("del send")
            time.sleep(1)
            data = mainWindow.tableRequest.get() + "|" + \
                   mainWindow.fieldRequest.get() + "|" + \
                   mainWindow.valuesRequest.get()
            sock.send(data.encode())
            print(data)
            time.sleep(1)
            sock.send("nxt".encode())
            mainWindow.resultLabel.config(text = '')
        except Exception as e:
            mainWindow.resultLabel.config(text = traceback.format_exc())
            print('Ошибка:\n', traceback.format_exc())

    deleteButton.config(command=delete)
    deleteButton.place(x=335, y=80, anchor="nw")

    idRequest = StringVar()
    idEntry = Entry(admincanvas, textvariable=idRequest, width=16)
    idEntry.place(x=670, y=50, anchor="nw")

    idLabel = Label(admincanvas, text='id для UPDATE', bg='#ddd')
    idLabel.place(x=670, y=70, anchor="nw")

    idnumRequest = StringVar()
    idnumEntry = Entry(admincanvas, textvariable=idnumRequest, width=16)
    idnumEntry.place(x=670, y=90, anchor="nw")

    updateButton = Button(admincanvas, text = 'Обновить', width=20, height=2)

    def update():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.send("upd".encode())
            print("upd send")
            time.sleep(1)
            data = mainWindow.tableRequest.get() + "|" + \
                   mainWindow.fieldRequest.get() + "|" + \
                   mainWindow.valuesRequest.get() + "|" + \
                   mainWindow.idRequest.get() + "|" + \
                   mainWindow.idnumRequest.get()
            sock.send(data.encode())
            print(data)
            time.sleep(1)
            sock.send("nxt".encode())
            mainWindow.resultLabel.config(text = '')
        except Exception as e:
            mainWindow.resultLabel.config(text = traceback.format_exc())
            print('Ошибка:\n', traceback.format_exc())
        
    updateButton.config(command=update)
    updateButton.place(x=495, y=80, anchor="nw")

    userAddCanvas = Canvas(admincanvas, width=330, height=180, bg='#ccc')
    userAddCanvas.place(x=480, y=130, anchor="nw")

    userAdd = StringVar()
    userAddEntry = Entry(admincanvas, textvariable=userAdd, width=36)
    userAddEntry.place(x=795, y=170, anchor="ne")

    passwordAdd = StringVar()
    passAddEntry = Entry(admincanvas, textvariable=passwordAdd, width=36)
    passAddEntry.place(x=795, y=200, anchor="ne")

    UALabel = Label(admincanvas, text = 'Логин', justify=LEFT, bg='#ccc')
    UALabel.place(x=560, y=170, anchor="ne")
    PALabel = Label(admincanvas, text = 'Пароль', justify=LEFT, bg='#ccc')
    PALabel.place(x=560, y=200, anchor="ne")

    regButton = Button(admincanvas, text = 'Регистрация', width=30, height=2)

    def regUser():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.send("adu".encode())
            print("adu send")
            time.sleep(1)
            data = mainWindow.userAdd.get() + "|" + \
                   mainWindow.passwordAdd.get()
            sock.send(data.encode())
            print(data)
            time.sleep(1)
            sock.send("nxt".encode())
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc()) 
    
    regButton.config(command=regUser)
    regButton.place(x=660, y=250, anchor="c")


    disconnButton = Button(admincanvas, text = 'Отключиться', width=20, height=1)

    def disconnection():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            sock.close()
            mainWindow.loginCanvas.pack()
            mainWindow.admincanvas.pack_forget()
            mainWindow.window.geometry('520x320')
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())

    disconnButton.config(command=disconnection)
    disconnButton.place(x=805, y=10, anchor="ne")



    #connection\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    user = StringVar()
    password = StringVar()

    loginCanvas = Canvas(window, width=520, height=320, bg='#eee')
    
    ULabel = Label(loginCanvas, text = 'Логин', justify=LEFT)
    ULabel.place(relx=.3, rely=.35, anchor="w")
    PLabel = Label(loginCanvas, text = 'Пароль', justify=LEFT)
    PLabel.place(relx=.3, rely=.45, anchor="w")

    userEntry = Entry(loginCanvas, textvariable=user, width=30)
    userEntry.place(relx=.6, rely=.35, anchor="c")
    passEntry = Entry(loginCanvas, textvariable=password, width=30)
    passEntry.place(relx=.6, rely=.45, anchor="c")

    connButton = Button(loginCanvas, text = 'Подключиться к базе', width=40, height=2)

    f = None
    def connection():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("192.168.56.2", 9090))
            print("connected")
            sock.send("con".encode())
            print("con send")
            time.sleep(1)
            sock.send(("c" + mainWindow.user.get()).encode())
            print(mainWindow.user.get())
            time.sleep(1)
            sock.send(("c" + mainWindow.password.get()).encode())
            print(mainWindow.password.get())

            roleb = sock.recv(1024)
            global role
            role = roleb.decode()         
            print(role)
            time.sleep(1)
            sock.send("nxt".encode())

            mainWindow.f = open('user.txt', 'w')
            mainWindow.f.write(mainWindow.user.get())
            mainWindow.f.close()

            mainWindow.password.set("")

            if role == "admin":
                mainWindow.loginCanvas.pack_forget()
                mainWindow.window.geometry('820x320')
                mainWindow.testercanvas.pack_forget()
                mainWindow.admincanvas.pack()
            elif role == "":
                pass
            else:
                mainWindow.loginCanvas.pack_forget()
                mainWindow.window.geometry('1020x720')
                mainWindow.admincanvas.pack_forget()
                mainWindow.testercanvas.pack()
                mainWindow.nameLabel.config(text = 'Трасформатор №'+role)

        except Exception as e:
            sock.close()
            print('Ошибка:\n', traceback.format_exc()) 
    
    connButton.config(command=connection)
    connButton.place(relx=0.5, rely=0.6, anchor="c")

    def main():
        #Отображение окна
        mainWindow.f = open('user.txt', 'r')
        mainWindow.user.set(mainWindow.f.read())
        mainWindow.f.close()
        mainWindow.loginCanvas.pack()
        mainWindow.window.mainloop()


if __name__ == '__main__':
    try:
        sys.exit(mainWindow.main())
    except Exception as e:
        sock.close()
        print('Ошибка:\n', traceback.format_exc()) 
    except:
        pass
