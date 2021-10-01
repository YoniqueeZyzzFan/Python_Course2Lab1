import zipfile
import os
import hashlib
import requests
import re

# директория извлечения файлов архива
directory_to_extract_to = 'G:\\PrikladnoePrLab1\\MATERIAL'
# путь к архиву
arch_file = 'G:\\PrikladnoePrLab1\\MATERIAL\\lab1.zip'

"""
#Создать новую директорию, в которую будет распакован архив
#С помощью модуля zipfile извлечь содержимое архива в созданную директорию
"""

path = "G:\\PrikladnoePrLab1\\MATERIAL\\Try1"
try:
    os.mkdir(path)
except OSError:
    print("Не получилось создать директорию (возможно она уже существует) %s " % path)
else:
    print("Директория %s была успешно создана" % path)
if not os.listdir(path):
    material = zipfile.ZipFile(arch_file)
    material.extractall(directory_to_extract_to)
    material.close()
else:
    print("Директория не пуста")

""""
#Получить список файлов (полный путь) формата txt, находящихся в directory_to_extract_to.
#Сохранить полученный список в txt_files
"""

txt_files = []
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        if file.endswith(".txt"):
            txt_files.append(os.path.join(root, file))
print(txt_files)

# Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.
for file in txt_files:
    target_file = file
    target_file_data = open(target_file, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()
    print(result)

# Найти файл MD5 хеш которого равен target_hash в directory_to_extract_to

target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''  # полный путь к искомому файлу
target_file_data = ''  # содержимое искомого файлy
flag = True
for root, dirs, files in os.walk(directory_to_extract_to):
    for file in files:
        txt_single = os.path.join(root, file)
        txt_single_data = open(txt_single, 'rb').read()
        if target_hash == hashlib.md5(txt_single_data).hexdigest():
            target_file = txt_single
            target_file_data = open(txt_single, 'rb').read()
            flag = False
            break
    if not flag:
        break
# Отобразить полный путь к искомому файлу и его содержимое на экране
print(target_file)
print(target_file_data)
""""
Ниже представлен фрагмент кода парсинга HTML страницы с помощью регулярных выражений
Возможно выполнение этого задания иным способом (например, с помощью сторонних модулей)
"""

r = requests.get(target_file_data)
result_dct = {}  # словарь для записи содержимого таблицы

counter = 0
headers = []
# Получение списка строк таблицы
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    # извлечение заголовков таблицы
    if counter == 0:
        # Удаление тегов
        headers = re.sub("<.*?>", " ", line)
        # Извлечение списка заголовков
        headers = re.findall("[А-Яа-я]+\s?", headers)
        headers[-2] = headers[-2] + headers[-1]
        headers.pop(-1)
        counter += 1
        continue
    # Удаление тегов
    temp = re.sub("<.*?>", ';', line)
    # Значения в таблице, заключенные в скобках, не учитывать. Для этого удалить скобки и символы между ними.
    temp = re.sub("\(.*?\)", "", temp)
    # Замена последовательности символов ';' на одиночный символ
    temp = re.sub(";+", ';', temp)
    # Удаление символа ';' в начале и в конце строки
    temp = re.sub("^;", "", temp)
    temp = re.sub(";$", "", temp)
    temp = re.sub(";Всего", "Всего", temp)
    # Разбитие строки на подстроки
    tmp_split = re.split(r";", temp)
    # Извлечение и обработка (удаление "лишних" символов) данных из первого столбца
    country_name = tmp_split[0]
    first = 0
    for i in (tmp_split[0]):
        if i == " ":
            first = tmp_split[0].index(i)+2
            break
    country_name = tmp_split[0][first::]

    # Извлечение данных из оставшихся столбцов.
    # Данные из этих столбцов должны иметь числовое значение (прочерк можно заменить на -1).
    # Некоторые строки содержат пробелы в виде символа '\xa0'.

    col1_val = re.sub(u"\xa0", "", tmp_split[1])
    col2_val = re.sub(u"\xa0", "", tmp_split[2])
    col3_val = re.sub(u"\xa0", "", tmp_split[3])
    col4_val = re.sub(u"\xa0", "", tmp_split[4])
    for i in col3_val:
        if i == " *":
            col3_val = -1
        if i == "0":
            col3_val = -1
    for i in col4_val:
        if i == "_":
            col4_val = -1
    # Запись извлеченных данных в словарь
    result_dct[country_name] = {}
    result_dct[country_name][headers[0]] = int(col1_val)
    result_dct[country_name][headers[1]] = int(col2_val)
    result_dct[country_name][headers[2]] = int(col3_val)
    result_dct[country_name][headers[3]] = int(col4_val)
# Запись данных из полученного словаря в файл

output = open(directory_to_extract_to+'\\data.csv', 'w')
flag = True
strh = ";".join(headers)
for key in result_dct.keys():
    if flag:
        strh = "Название страны" + strh
        output.write(strh + "\n")
        flag = False
    output.write(key+";")
    for i in range(0, 4):
        string_to_write = str(result_dct[key][headers[i]]) + ";"
        output.write(string_to_write)
    output.write("\n")
output.close()

# Вывод данных на экран для указанного первичного ключа (первый столбец таблицы)
target_country = input("Введите название страны: ")
try:
    string = str(result_dct[target_country])
    print(string)
except KeyError:
    print("Страны с указанным именем не существует")
