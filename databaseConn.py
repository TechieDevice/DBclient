#Импорт библиотеки для работы с СУБД PostgreSQL
import psycopg2
from psycopg2 import sql
#Импорт библиотеки для вывода ошибок
import traceback
import socket

class dbConn():
    voltId = 1
#Инициализация подключения\\\\\\\\\\\\\\\\\\\\\\
    def __init__(self, User, Password):         
        self.conn = psycopg2.connect(
            dbname = "SCADA",
            user = User,
            password = Password
        )

        self.conn.set_isolation_level(0)
        self.cursor = self.conn.cursor()        

#Стандартный запрос на поиск\\\\\\\\\\\\\\\\\\\\
    #def getInfo(self, table, field, whereLike, value):       
    #    self.cursor.execute(sql.SQL("SELECT {field} FROM sensor_info.{table} {whereLike} {value}").format(
    #        table = sql.SQL(table),             
    #        field = sql.SQL(field),             
    #        whereLike = sql.SQL(whereLike),     
    #        value = sql.SQL(value)))                        
    #Результаты
    #    rows = self.cursor.fetchall()      
    #    return rows

#Отключение от базы\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def DBConnClose(self):
        self.cursor.close()
        self.conn.close()

#Поиск и выдача файла по названию\\\\\\\\\\\\\\\
    def getInfo(self, role):
        table = "Transformer_" + role
        self.cursor.execute(sql.SQL("SELECT * FROM sensor_info.{table} WHERE id = {value}").format(
            table = sql.SQL(table),                               
            value = sql.SQL(str(self.voltId))))

        #row = self.select('"speech"', '"filename", "speaker_id", "text_id"', 'WHERE "filename" LIKE', "'"+file+"%'")
        row = self.cursor.fetchall()
        results = 'Нет результатов'
        for r in row:
            results = "signal - " + str(r[2]) + "\n" + "in voltage - " + str(r[1]) + "\n" + "out voltage - " + str(r[3])
        #row = self.select('"speaker"', '"name", "family_name"', 'WHERE cast("speaker_id" as text) LIKE', "'"+str(results[1])+"'")
        
        #for r in row:
        #    results[1] = r[0] + ' ' + r[1]
        #if(check == 0):
        #    row = self.select('"text"', '"spelling_record"', 'WHERE cast("text_id" as text) LIKE', "'"+str(results[2])+"'")
        #else:
        #    row = self.select('"text"', '"transcription"', 'WHERE cast("text_id" as text) LIKE', "'"+str(results[2])+"'")
        #for r in row:
        #    results[2] = r[0]
        self.voltId = self.voltId + 1
        return results

#Проверка роли\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def currentRole(self, username):
        self.cursor.execute("SELECT groname FROM pg_group WHERE (SELECT usesysid FROM pg_user WHERE usename = %s) = ANY (grolist)",[username])
        row = self.cursor.fetchall() 
        userrol = ''
        for r in row:
            userrol = r[0]
        if userrol:
            self.cursor.execute("SELECT id FROM sensor_info.workers WHERE user = %s",[username])
            row = self.cursor.fetchall() 
            for r in row:
                userrol = r[0]
        else:
            userrol = "admin"
        return userrol

#Вставка\\\\\\\\\\\\\\\\\\
    def write(self, table, fields, values):
        self.cursor.execute(sql.SQL("INSERT INTO sensor_info.{table} ({fields}) VALUES ({values})").format(
            table = sql.SQL(table),             
            fields = sql.SQL(fields),                  
            values = sql.SQL(values)))

#Список чего угодно\\\\\\\\\\\\\\\
    def selectAdmin(self, table, field, value):

        self.cursor.execute(sql.SQL("SELECT * FROM sensor_info.{table} WHERE {field} = {value}").format(
            table = sql.SQL(table),             
            field = sql.SQL(field),                  
            value = sql.SQL(value)))

        #row = self.select(table, '*', 'WHERE cast("'+field+'" as text) LIKE', value)
        row = self.cursor.fetchall() 
        results = ''
        for r in row:
            if table != "devices":
                results = results + str(r[0]) + ' ' + str(r[1]) + '\n'
            else:
                results = results + str(r[0]) + ' ' + str(r[1]) + ' ' + str(r[2]) + '\n'
        if (results == ''):
            results = 'Нет результатов'

        return results

#Создание юзера\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def addWorker(self, username, password):
        self.cursor.execute(sql.SQL("CREATE USER {name} WITH PASSWORD '{password}'; GRANT workers TO {name};").format(
            name = sql.SQL(username),
            password = sql.SQL(password)))

#Обновление\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def update(self, table, field, value, id, idnum):
        self.cursor.execute(sql.SQL("UPDATE sensor_info.{table} SET {field} = {value} WHERE {id} = {idnum}").format(
            table = sql.SQL(table),             
            field = sql.SQL(field),                  
            value = sql.SQL(value),
            id = sql.SQL(id),                  
            idnum = sql.SQL(idnum)))

#Удаление\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    def delete(self, table, field, value):
        self.cursor.execute(sql.SQL("DELETE FROM sensor_info.{table} WHERE {field} = {value}").format(
            table = sql.SQL(table),             
            field = sql.SQL(field),                  
            value = sql.SQL(value)))


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind(("", 9090))
print("server start")
print(conn)

dbconn = None

while True:
    try:
        print("listen")
        conn.listen(1)
        sock, addr = conn.accept()
        print("connected")
        print(addr)
        connected = True
        while connected:
            datab = sock.recv(1024)
            data = datab.decode() 
            print("get " + data)

            if data[:3] == "get":
                datab = sock.recv(1024)
                data = datab.decode()
                print(data)
                sock.send(str(dbconn.getInfo(data)).encode())
                print("send")

            elif data[:3] == "sel":
                datab = sock.recv(1024)
                data = datab.decode().split('|')
                print(data)
                sock.send(str(dbconn.selectAdmin(data[0], data[1], data[2])).encode())
                print("send")

            elif data[:3] == "add":
                datab = sock.recv(1024)
                data = datab.decode().split('|')
                print(data)
                dbconn.write(data[0], data[1], data[2])
                print("done")

            elif data[:3] == "upd":
                datab = sock.recv(1024)
                data = datab.decode().split('|')
                print(data)
                dbconn.update(data[0], data[1], data[2], data[3], data[4])
                print("done")

            elif data[:3] == "del":
                datab = sock.recv(1024)
                data = datab.decode().split('|')
                print(data)
                dbconn.delete(data[0], data[1], data[2])
                print("done")

            elif data[:3] == "adu":
                datab = sock.recv(1024)
                data = datab.decode().split('|')
                print(data)
                dbconn.addWorker(data[0], data[1])
                print("done")

            elif data[:3] == "con":
                userb = sock.recv(1024)
                user = userb.decode()
                print(user[1:])
                passwordb = sock.recv(1024)
                password = passwordb.decode()
                print(password[1:])
                dbconn = dbConn(user[1:], password[1:])
                print("db connect")
                sock.send(str(dbconn.currentRole(user[1:])).encode())
                print("role send") 
            elif data[:3] == "nxt":
                sock.close()
                print("wait")
                connected = False
            else:
                connected = False
                dbconn.DBConnClose() 
                sock.close()
                print("disconnected")

    except Exception as e:
        sock.close()
        print('Ошибка:\n', traceback.format_exc()) 
