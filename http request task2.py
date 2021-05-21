import requests
import os
from os import listdir
from pprint import pprint

# токен и путь к папке можно менять
token_ZDV = "AQAAAABA7143AADLW2WkqJdnPEFlkUF0f_PzSyQ"
files_path = r'C:\Git Practic\Netology\Lesson http task2\files for yandex'


class Yandex:
    def __init__(self, token):
        self.url = "https://cloud-api.yandex.net/v1/disk"
        self.url_upload = '/resources/upload'
        self.url_resources = self.url + '/resources'
        self.headers = {'Authorization': token}

    def get_info(self):
        url_info = self.url + "/resources/files"
        resource = requests.get(url_info, headers=self.headers)
        return resource.json()

    def _get_link_for_download(self, folder_file, file_name):
        # получение URL ссылки
        url_get_link = self.url + self.url_upload
        params = {"path": self._is_folder_exist(folder_file, file_name), "overwrite": "false"}
        link = requests.get(url_get_link, headers=self.headers, params=params).json().get('href', None)
        return link

    def _is_folder_exist(self, folder_file, file_name):
        # Проверка Диска на наличие папок в пути хранения, если нет -создает
        params = {'path': '', "overwrite": "false"}
        for folder in folder_file.split('/'):
            params['path'] += (folder + '/')
            folder_status = requests.get(self.url_resources, headers=self.headers, params=params).json()
            if folder_status != '200':
                requests.put(self.url_resources, headers=self.headers, params=params)
        if folder_file[-1] == '/':
            return f'{folder_file}{file_name}'
        else:
            return f'{folder_file}/{file_name}'

    def upload_file(self, folder_name, file_name):
        # Загрузка файлов с проверкой на наличие файла. программа НЕ перезапишет автоматически!
        if file_name is None:
            return None
        url_upload = self._get_link_for_download(folder_name, file_name.split('\\')[-1])
        if url_upload is None:
            print('Файл уже существует. Программа остановлена')
            return None

        upload = requests.put(url_upload, data=open(file_name, "rb"))
        if upload.status_code == 201:
            print(f"Ваш файл: {file_name}\n"
                  f"успешно передан по ссылке\n"
                  f"{url_upload}")


class File_for_upload:      #класс обработки файлов на закачивание
    def __init__(self, path, file_name):
        self.path = path
        self.path_to_file = self._file_in_folder(file_name)

    def _file_in_folder(self, file_name):  #проверка на наличие файла в указанной папке
        list_files = os.listdir(self.path)
        if file_name in list_files:
            return os.path.join(self.path, file_name)
        else:
            print(f'Указанный файл не найден\n'
                  f'Проверьте корректность указанного имени или пути\n'
                  f'Содерджимое папки: {self.path}\n'
                  f'{str(list_files)}')
            return None


file_upload = '1123.txt'
file_for_download = File_for_upload(files_path, file_upload).path_to_file
Yandex(token_ZDV).upload_file('download/a/eer/', file_for_download)

# если нет указанного пути, программа создат все вложения, указывать в пути имя файла не нужно!!
# программа учитывает оба варианта указания пути как а/б/в/г так и а/б/в/г/
