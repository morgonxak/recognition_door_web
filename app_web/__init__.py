from flask import Flask
import socket
from app_web.moduls.database import DataBase


def getIP():
    '''
    получаем IP адрес
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

app = Flask(__name__, static_url_path='/static')
app.config['database'] = DataBase('/home/dima/PycharmProjects/recognition_door_web/rc/database')
#print(app.config['database'].get_users())  #[('213302ef-34d1-4edc-9715-97ac24ab34f7', 'test', 'tesr', 'test', 1, None, 1), ('bcd76e17-6b70-4dcf-ba99-b24dc3c1d0c1', 'test', 'test', 'test', 1, None, 1)]


#settings server
IP = getIP()
print("IP: {}".format(IP))
app.config['IP_Server'] = IP
app.config['PORT_server'] = 2561
app.config['TEMP'] = '/home/dima/PycharmProjects/recognition_door_web/temp'

app.config['PATH_SAVE_MODEL'] = '/home/dima/PycharmProjects/recognition_door_web/rc'


from app_web import routing
