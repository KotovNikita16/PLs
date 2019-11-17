#Скрипт работает с файлами и папками, находясь в той же директории, что и папка с файлами (по умолчанию папка space). Клиент - localhost
#Скачать файл или перейти в папку - кликнуть по привязанной к имени ссылке. Сверху указана текущая директория.
#Удалить пустую папку или файл - кликнуть по ссылке [DELETE] рядом с именем файла или папки, которую нужно удалить. После перехода на страницу с сообщением об успешном удалении вернуться на предыдущую странуицу и обновить.

from http.server import BaseHTTPRequestHandler,HTTPServer
import os
import shutil
import urllib.parse

hostName = "localhost"
hostPort = 80
Space_name = '/space'
access = os.path.abspath(os.path.dirname(__file__)) + Space_name

class HttpProcessor(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
    
    def do_GET(self):
            directory = urllib.parse.unquote(self.path)
            if directory != '/favicon.ico': 
                if directory[1:3] == "r/":
                    self._set_response()
                    directory = (access + directory[2:])
                    try:
                        os.remove(directory)
                        self.wfile.write('<!DOCTYPE html><html><head><meta charset="UTF-8"/><title>DRIVE</title></head><body>File "{}" deleted</body></html>'.format(os.path.basename(directory)).encode())
                    
                    except OSError:
                        os.rmdir(directory)
                        self.wfile.write('<!DOCTYPE html><html><head><meta charset="UTF-8"/><title>DRIVE</title></head><body>Folder "{}" deleted</body></html>'.format(os.path.basename(directory)).encode())
                    
                else:
                    directory = access + directory
                    if os.path.isdir(directory):
                            self._set_response()
                            files = os.listdir(directory)
                            stroka = '<body>' + Space_name[1:] + urllib.parse.unquote(self.path if self.path != '/' else '') + '</br>'
                            for ele in files:
                                stroka += '<li><a href="http://' + hostName + (self.path if self.path != '/' else '') + '/' + ele + '">' + ele + '</a>'
                                if os.path.isfile(directory + '/' + ele):
                                    stroka += '<a href="http://' + hostName + '/r' + (self.path if self.path != '/' else '') + '/' + ele + '">[DELETE]</a>'
                                elif os.listdir(directory + '/' + ele) == []:
                                    stroka += '<a href="http://' + hostName  + '/r' + (self.path if self.path != '/' else '') + '/' + ele + '">[DELETE]</a>'
                                stroka += '</li>'
                            self.wfile.write(('<!DOCTYPE html><html><head><meta charset="UTF-8"/><title>DRIVE</title></head>' + stroka + '</body></html>').encode())
                    else:
                        with open(directory, 'rb') as f:
                            self.send_response(200)
                            self.send_header("Content-Type", 'application/octet-stream')
                            self.send_header("Content-Disposition", 'attachment; filename="' + urllib.parse.quote(os.path.basename(directory)) + '"')
                            fs = os.fstat(f.fileno())
                            self.send_header("Content-Length", str(fs.st_size))
                            self.end_headers()
                            shutil.copyfileobj(f, self.wfile)

serv = HTTPServer((hostName,hostPort),HttpProcessor)
serv.serve_forever()
