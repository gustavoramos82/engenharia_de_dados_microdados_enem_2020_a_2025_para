import os
import glob
import re
import duckdb

# Diretórios da estrutura Medallion
diretorio_bronze = "/home/gustavor/Enem/Medalion/Bronze"
diretorio_prata = "/home/gustavor/Enem/Medalion/Prata"
db_destino = os.path.join(diretorio_prata, "enem_para_prata.duckdb")
tabela_destino = "microdados_enem_pa"

# Garante que a pasta Prata exista
os.makedirs(diretorio_prata, exist_ok=True)

print(f"Buscando arquivos da camada Bronze em: {diretorio_bronze}")

# Busca todos os CSVs dentro do diretório DADOS
padrao_busca = os.path.join(diretorio_bronze, "dados_enem_*/**/DADOS/*.csv")
todos_csvs = glob.glob(padrao_busca, recursive=True)

# FILTRO AJUSTADO:
# Filtra apenas os arquivos referentes a PARTICIPANTES / MICRODADOS
# Ignora explicitamente ITENS, PROVA, PROVAS, GABARITO, etc.
arquivos_csv = []
for f in todos_csvs:
    nome_arquivo = os.path.basename(f).upper()
    
    # Descarta arquivos que não sejam dos participantes
    if any(termo in nome_arquivo for termo in ["ITEM", "ITENS", "PROVA", "GABARITO"]):
        continue
        
    # Garante que seja um arquivo principal de microdados/participantes
    if "MICRODADOS" in nome_arquivo or "PARTICIPANTES" in nome_arquivo or nome_arquivo.startswith("ENEM"):
        arquivos_csv.append(f)

if not arquivos_csv:
    print("Nenhum arquivo CSV de participantes encontrado! Verifique o nome dos arquivos na pasta Bronze.")
    exit()

print(f"Encontrados {len(arquivos_csv)} arquivo(s) de participantes para processar:\n")
for csv in arquivos_csv:
    print(f" - {os.path.basename(csv)}")
print()

# Conecta ao DuckDB
con = duckdb.connect(db_destino)
con.execute(f"DROP TABLE IF EXISTS {tabela_destino}")

# Query base para seleção, renomeação de colunas e filtros
def get_query_base(csv_path):
    return f"""
        SELECT 
            NU_ANO AS ano_enem,
            TP_FAIXA_ETARIA AS faixa_etaria,
            TP_SEXO AS sexo,
            TP_ESTADO_CIVIL AS estado_civil,
            TP_COR_RACA AS cor_raca,
            TP_NACIONALIDADE AS nacionalidade,
            TP_ST_CONCLUSAO AS situacao_conclusao_ensino_medio,
            TP_ANO_CONCLUIU AS ano_conclusao_ensino_medio,
            TP_ENSINO AS tipo_ensino_instituicao,
            NO_MUNICIPIO_PROVA AS municipio_prova
        FROM read_csv_auto('{csv_path}', sep=';', encoding='latin-1', ignore_errors=true)
        WHERE SG_UF_PROVA = 'PA'
          AND IN_TREINEIRO = 0
    """

for i, csv_path in enumerate(arquivos_csv):
    # Extrai o ano a partir do nome do arquivo ou da pasta
    match = re.search(r"\d{4}", csv_path)
    ano = match.group(0) if match else f"desconhecido_{i+1}"
    
    # Caminho do CSV individual exportado para a camada Prata
    csv_prata_destino = os.path.join(diretorio_prata, f"participantes_filtrados_{ano}.csv")
    
    print(f"[{i+1}/{len(arquivos_csv)}] Processando ano {ano}...")
    print(f"  └─ Origem: {os.path.basename(csv_path)}")
    
    # 1. Exporta o CSV individual filtrado daquele ano específico para a Prata
    query_export_csv = f"""
    COPY (
        {get_query_base(csv_path)}
    ) TO '{csv_prata_destino}' (HEADER, DELIMITER ';');
    """
    con.execute(query_export_csv)
    print(f"  └─ CSV Prata gerado: participantes_filtrados_{ano}.csv")

    # 2. Consolida também no banco DuckDB da Prata
    if i == 0:
        con.execute(f"CREATE TABLE {tabela_destino} AS {get_query_base(csv_path)}")
    else:
        con.execute(f"INSERT INTO {tabela_destino} {get_query_base(csv_path)}")

print("\n" + "="*65)
print("[Sucesso] Processamento da Camada Prata concluído!")
print(f"1. Arquivos CSV individuais salvos em: {diretorio_prata}")
print(f"2. Banco DuckDB consolidado salvo em: {db_destino}")
print("="*65)

# Fecha a conexão com o DuckDB
con.close()