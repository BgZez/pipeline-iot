# Pipeline de Dados com IoT e Docker

Pipeline que lê leituras de temperatura de dispositivos IoT (dataset do Kaggle),
armazena em PostgreSQL (Docker), cria views SQL e exibe um dashboard em Streamlit.

**Disciplina:** Disruptive Architectures: IoT, Big Data e IA — UniFECAF

## Tecnologias
Python 3 · pandas · SQLAlchemy · PostgreSQL 16 · Docker / Docker Compose · Streamlit · Plotly · Git/GitHub

## Estrutura
```
├── data/              # CSV do Kaggle (IOT-temp.csv)
├── docs/              # capturas de tela
├── sql/views.sql      # 3 views SQL
├── src/
│   ├── config.py      # conexão com o banco
│   ├── ingest.py      # ETL: CSV -> PostgreSQL + views
│   └── dashboard.py   # dashboard Streamlit
├── docker-compose.yml
└── requirements.txt
```

## Dataset
[Temperature Readings: IoT Devices](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)
— baixe o CSV e salve como `data/IOT-temp.csv`.

## Como executar
```bash
# 1. Ambiente virtual e dependências
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Subir o PostgreSQL
docker compose up -d
# (alternativa) docker run --name postgres-iot -e POSTGRES_USER=iot \
#   -e POSTGRES_PASSWORD=iot_pass -e POSTGRES_DB=iotdb -p 5432:5432 -d postgres

# 3. Carregar os dados e criar as views
python src/ingest.py

# 4. Abrir o dashboard
streamlit run src/dashboard.py
```

Verificar os dados no banco:
```bash
docker exec -it postgres-iot psql -U iot -d iotdb -c "SELECT COUNT(*) FROM temperature_readings;"
```

## Views SQL
| View | Propósito |
|------|-----------|
| `avg_temp_por_local` | Média, mínima, máxima e contagem de leituras por local (In/Out). |
| `leituras_por_hora` | Volume de leituras e temperatura média por hora do dia. |
| `temp_max_min_por_dia` | Evolução diária das temperaturas máxima, mínima e média. |

## Capturas de tela
![Dashboard](docs/dashboard1.png)
![Dashboard](docs/dashboard2.png)

## Insights
_(preencha com o que você observou nos gráficos)_

## Comandos Git utilizados
```bash
git init
git add .
git commit -m "Projeto inicial: Pipeline de Dados IoT"
git remote add origin URL_DO_SEU_REPOSITORIO
git branch -M main
git push -u origin main
git pull
```
