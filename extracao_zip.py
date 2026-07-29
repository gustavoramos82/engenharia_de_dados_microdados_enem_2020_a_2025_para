import os
import re
import zipfile

# 1. ESPECIFIQUE AQUI O DIRETÓRIO ONDE ESTÃO OS ARQUIVOS .ZIP
diretorio_origem = r"insira o diretorio de origem"

# Se desejar salvar a extração em outro lugar, altere diretorio_destino.
# Por padrão, salvará na mesma pasta de origem.
diretorio_destino = r"insira o diretorio de destino" 

print(f"Buscando arquivos ZIP em: {diretorio_origem}\n")

try:
    if not os.path.exists(diretorio_origem):
        print(f"Erro: O diretório informado '{diretorio_origem}' não existe.")
        exit()

    # Lista todos os arquivos da pasta especificada que terminam com .zip
    zip_files = [f for f in os.listdir(diretorio_origem) if f.lower().endswith(".zip")]

    if not zip_files:
        print("Nenhum arquivo .zip encontrado na pasta especificada.")
    else:
        for zip_filename in zip_files:
            # Busca o ano (4 dígitos) no nome do arquivo
            match = re.search(r"\d{4}", zip_filename)
            
            if match:
                ano = match.group(0)
                extract_folder = os.path.join(diretorio_destino, f"dados_enem_{ano}")
            else:
                folder_name = os.path.splitext(zip_filename)[0]
                extract_folder = os.path.join(diretorio_destino, folder_name)

            zip_path = os.path.join(diretorio_origem, zip_filename)

            print(f"--> Processando: {zip_filename}")
            print(f"    Extraindo em: {extract_folder}")

            try:
                os.makedirs(extract_folder, exist_ok=True)
                
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_folder)
                    
                print(f"    ✓ Concluído!\n")

            except Exception as e:
                print(f"    ✗ Erro ao extrair '{zip_filename}': {e}\n")

        print("Processamento de todos os arquivos concluído!")

except Exception as e:
    print(f"Erro no processamento: {e}")
