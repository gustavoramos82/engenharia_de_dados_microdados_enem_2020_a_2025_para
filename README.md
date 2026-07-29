# 🚀 Pipeline de Dados com Arquitetura Medallion: Microdados do ENEM (Estado do Pará) - 2020 a 2025

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/9019869d-3a6f-46bd-989b-60a98775e078" />

## 📌 Sobre o Projeto

Este projeto consiste em um pipeline de **Engenharia de Dados** ponta a ponta construído para realizar o tratamento, filtragem, padronização e consolidação dos **Microdados do ENEM** entre os anos de **2020 e 2025**, com foco específico nos participantes do **Estado do Pará (não-treineiros)**.

O objetivo principal é transformar uma grande massa de dados brutos e não estruturados em uma camada pronta para análise em ferramentas de Business Intelligence (como Power BI, Tableau ou Metabase) de forma performática e otimizada.

Todo o Projeto é pensado numa pipeline que funciona de forma local e o unico momento que precisa internete é qunado se vai fazer o download dos aqruivos, de resto, a ideia é funiconar em computadores com configurações básicas.

> 💡 *Este repositório é uma evolução do projeto focado exclusivamente no ENEM 2025. Confira a versão anterior [clicando aqui](https://github.com/gustavoramos82/engenharia_de_dados_microdados_enem_2025_para).*

---

## 🏗️ Arquitetura Medallion

O processo foi desenhado seguindo as melhores práticas de governança e engenharia de dados, dividindo-se nas três camadas do padrão **Medallion**:

### 1. 🥉 Camada Bronze 
- **Extração em Lote:** Identificação e descompactação automática dos arquivos `.zip` originais do INEP.
- **Organização de Diretórios:** Estruturação automatizada das pastas locais segregando os dados por ano de realização do exame.

### 2. 🥈 Camada Prata
- **Processamento de Alta Performance:** Utilização da engine **DuckDB** para leitura rápida e filtragem eficiente sem estourar a memória RAM.
- **Filtros de Negócio:**
  - Apenas inscritos que realizaram a prova no Pará (`SG_UF_PROVA = 'PA'`).
  - Remoção de treineiros (`IN_TREINEIRO = 0`).
  - Descarte ativo de arquivos auxiliares (itens de prova, gabaritos e cadernos de questões).
- **Seleção de Colunas Categóricas/Demográficas:**
  - `NU_ANO`, `TP_FAIXA_ETARIA`, `TP_SEXO`, `TP_ESTADO_CIVIL`, `TP_COR_RACA`, `TP_NACIONALIDADE`, `TP_ST_CONCLUSAO`, `TP_ANO_CONCLUIU`, `TP_ENSINO`, `NO_MUNICIPIO_PROVA`.
- **Armazenamento:** Exportação de arquivos `.csv` individuais por ano e criação de um banco de dados consolidado `.duckdb`.

### 3. 🥇 Camada Ouro (Analytics Ready)
- **Normalização de Schema:** Conversão dinâmica do nome de todas as colunas para o padrão `snake_case`.
- **Mapeamento de Domínio:** Aplicação de dicionários de dados oficiais do INEP utilizando **Pandas** para traduzir códigos numéricos em legendas descritivas (ex: raça/cor, faixa etária, escolaridade).
- **Preservação da Integridade de Dados:** Manutenção estrita dos valores nulos (`NaN`), garantindo que a tomada de decisão sobre dados ausentes ocorra na fase analítica.
- **Consolidação Temporal:** Unificação de todo o histórico dos anos (2020–2025) em uma única tabela.
- **Otimização para BI:** Exportação final no formato **Parquet**, reduzindo drasticamente o consumo de espaço em disco e garantindo leituras ultrarrápidas no Power BI.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Engines de Processamento:** DuckDB, Pandas
- **Formatos de Armazenamento:** CSV, DuckDB Database,Parquet
- **Estruturação:** Regex, OS, Glob

## 🎯 Próximos Passos

- [ ] Modelagem de dados para BI.
- [ ] Construção de Dashboard interativo.
- [ ] Automação e orquestração do pipeline via Airflow / Prefect.
