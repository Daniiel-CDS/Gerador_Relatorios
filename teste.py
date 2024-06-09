import chardet
import os

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

project_path = '.'  # Caminho do seu projeto

for root, dirs, files in os.walk(project_path):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            encoding = detect_encoding(file_path)
            if encoding != 'utf-8':
                print(f'{file_path}: {encoding}')
        except Exception as e:
            print(f'Erro ao processar {file_path}: {e}')
