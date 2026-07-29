import os
import glob
import re
import pandas as pd
import duckdb

# 1. Definição dos diretórios da estrutura Medallion
diretorio_prata = "insira o diretorio"
diretorio_ouro = "insira o diretorio"

os.makedirs(diretorio_ouro, exist_ok=True)

# Função para garantir que os nomes das colunas estejam em snake_case
def formatar_para_snake_case(nome_coluna):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', nome_coluna)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# 2. Dicionários de domínio (conforme o Jupyter Notebook)
legenda_faixa_etaria = {
    1: 'Menor de 17 anos',
    2: '17 anos',
    3: '18 anos',
    4: '19 anos',
    5: '20 anos',
    6: '21 anos',
    7: '22 anos',
    8: '23 anos',
    9: '24 anos',
    10: '25 anos',
    11: 'Entre 26 e 30 anos',
    12: 'Entre 31 e 35 anos',
    13: 'Entre 36 e 40 anos',
    14: 'Entre 41 e 45 anos',
    15: 'Entre 46 e 50 anos',
    16: 'Entre 51 e 55 anos',
    17: 'Entre 56 e 60 anos',
    18: 'Entre 61 e 65 anos',
    19: 'Entre 66 e 70 anos',
    20: 'Maior de 70 anos'
}

legenda_estado_civil = {
    0: 'Não informado',
    1: 'Solteiro(a)',
    2: 'Casado(a)/Em união estável/Mora com companheiro(a)',
    3: 'Divorciado(a)/Desquitado(a)/Separado(a)',
    4: 'Viúvo(a)'
}

legenda_cor_raca = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

legenda_nacionalidade = {
    0: 'Não informado',
    1: 'Brasileiro(a)',
    2: 'Brasileiro(a) Naturalizado(a)',
    3: 'Estrangeiro(a)',
    4: 'Brasileiro(a) Nato(a), nascido(a) no exterior'
}

situacao_ensino_medio = {
    1: "Já concluí o Ensino Médio",
    2: "Estou cursando e concluirei o Ensino Médio em 2025",
    3: "Estou cursando e concluirei o Ensino Médio após 2025",
    4: "Não concluí e não estou cursando o Ensino Médio"
}

ano_conclusao_ensino_medio = {
    0: "Não informado",
    1: "2024",
    2: "2023",
    3: "2022",
    4: "2021",
    5: "2020",
    6: "2019",
    7: "2018",
    8: "2017",
    9: "2016",
    10: "2015",
    11: "2014",
    12: "2013",
    13: "2012",
    14: "2011",
    15: "2010",
    16: "2009",
    17: "2008",
    18: "2007",
    19: "Antes de 2007"
}

tipo_instituicao = {
    1: 'Ensino Regular',
    2: 'Educação Especial - Modalidade Substitutiva'
}

mapeamento_demografico = {
    'nu_ano': 'ano_enem',
    'tp_faixa_etaria': 'faixa_etaria',
    'tp_sexo': 'sexo',
    'tp_estado_civil': 'estado_civil',
    'tp_cor_raca': 'cor_raca',
    'tp_nacionalidade': 'nacionalidade',
    'tp_st_conclusao': 'situacao_conclusao_ensino_medio',
    'tp_ano_concluiu': 'ano_conclusao_ensino_medio',
    'tp_ensino': 'tipo_ensino_instituicao',
    'no_municipio_prova': 'municipio_prova'
}

print("Buscando arquivos da camada Prata...")
arquivos_prata = glob.glob(os.path.join(diretorio_prata, "participantes_filtrados_*.csv"))

if not arquivos_prata:
    print("Nenhum arquivo CSV encontrado na pasta Prata!")
    exit()

lista_dfs = []

# Função auxiliar para mapear apenas o que existe no dicionário e preservar NaN
def aplicar_map_preservando_nan(serie, dicionario):
    return serie.map(dicionario)

for i, arq_csv in enumerate(arquivos_prata):
    match = re.search(r"\d{4}", arq_csv)
    ano = match.group(0) if match else f"ano_{i+1}"
    
    print(f"\n[{i+1}/{len(arquivos_prata)}] Tratando dados do ano {ano}...")
    
    df = pd.read_csv(arq_csv, sep=';')
    
    # 3. Formatação e mapeamento das colunas
    df.columns = [formatar_para_snake_case(col) for col in df.columns]
    df = df.rename(columns=mapeamento_demografico)

    # 4. Aplicação estrita de .map() mantendo NaNs intocados
    if 'faixa_etaria' in df.columns:
        df['faixa_etaria'] = aplicar_map_preservando_nan(df['faixa_etaria'], legenda_faixa_etaria)
    if 'estado_civil' in df.columns:
        df['estado_civil'] = aplicar_map_preservando_nan(df['estado_civil'], legenda_estado_civil)
    if 'cor_raca' in df.columns:
        df['cor_raca'] = aplicar_map_preservando_nan(df['cor_raca'], legenda_cor_raca)
    if 'nacionalidade' in df.columns:
        df['nacionalidade'] = aplicar_map_preservando_nan(df['nacionalidade'], legenda_nacionalidade)
    if 'situacao_conclusao_ensino_medio' in df.columns:
        df['situacao_conclusao_ensino_medio'] = aplicar_map_preservando_nan(df['situacao_conclusao_ensino_medio'], situacao_ensino_medio)
    if 'ano_conclusao_ensino_medio' in df.columns:
        df['ano_conclusao_ensino_medio'] = aplicar_map_preservando_nan(df['ano_conclusao_ensino_medio'], ano_conclusao_ensino_medio)
    if 'tipo_ensino_instituicao' in df.columns:
        df['tipo_ensino_instituicao'] = aplicar_map_preservando_nan(df['tipo_ensino_instituicao'], tipo_instituicao)

    # Exporta CSV individual Ouro
    caminho_ouro_ano = os.path.join(diretorio_ouro, f"dados_enem_ouro_{ano}.csv")
    df.to_csv(caminho_ouro_ano, index=False, sep=';', encoding='utf-8')
    print(f"  └─ CSV Ouro individual salvo: dados_enem_ouro_{ano}.csv")

    lista_dfs.append(df)

# 5. Consolidação e exportações finais
print("\nUnificando dataframes de todos os anos...")
df_geral = pd.concat(lista_dfs, ignore_index=True)

# Exporta CSV unificado
csv_geral_path = os.path.join(diretorio_ouro, "dados_enem_ouro_geral.csv")
df_geral.to_csv(csv_geral_path, index=False, sep=';', encoding='utf-8')
print(f"✓ CSV geral consolidado salvo em: {csv_geral_path}")

# Exporta Parquet para BI
parquet_geral_path = os.path.join(diretorio_ouro, "enem_para_ouro_geral.parquet")
df_geral.to_parquet(parquet_geral_path, index=False, engine='pyarrow', compression='snappy')
print(f"✓ Arquivo Parquet final para BI salvo em: {parquet_geral_path}")

# Atualiza DuckDB
db_ouro_path = os.path.join(diretorio_ouro, "enem_para_ouro.duckdb")
con = duckdb.connect(db_ouro_path)
con.execute("CREATE OR REPLACE TABLE microdados_enem_pa_ouro AS SELECT * FROM df_geral")
con.close()

print("\n" + "="*70)
print("[SUCESSO] Processamento da Camada Ouro concluído sem alterar valores NaN!")
print(f"Total de registros no Parquet final: {len(df_geral):,}".replace(",", "."))
print("="*70)
