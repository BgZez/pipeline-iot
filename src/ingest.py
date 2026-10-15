"""
Lê o CSV do Kaggle, trata os dados, grava no PostgreSQL e cria as views SQL.

Uso:  python src/ingest.py [caminho_do_csv]
"""
import sys
from pathlib import Path

import pandas as pd

from config import get_engine

ROOT = Path(__file__).resolve().parent.parent
CSV_PADRAO = ROOT / "data" / "IOT-temp.csv"
VIEWS_SQL = ROOT / "sql" / "views.sql"


def carregar_csv(caminho: Path) -> pd.DataFrame:
    """Lê e limpa o CSV."""
    df = pd.read_csv(caminho)

    # Nomes de colunas do dataset original -> nomes amigáveis para SQL
    df = df.rename(columns={
        "id": "reading_id",
        "room_id/id": "room_id",
        "noted_date": "noted_date",
        "temp": "temperature",
        "out/in": "location",
    })

    # Data no formato dd-mm-aaaa HH:MM
    df["noted_date"] = pd.to_datetime(df["noted_date"], format="%d-%m-%Y %H:%M", errors="coerce")
    df["location"] = df["location"].str.strip().str.capitalize()  # In / Out

    antes = len(df)
    df = df.dropna().drop_duplicates(subset="reading_id")
    print(f"Linhas lidas: {antes} | após limpeza: {len(df)}")
    return df


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else CSV_PADRAO
    if not caminho.exists():
        sys.exit(f"CSV não encontrado em {caminho}. Baixe do Kaggle e coloque em /data.")

    engine = get_engine()
    df = carregar_csv(caminho)

    # Inserção no banco (recria a tabela a cada execução)
    df.to_sql("temperature_readings", engine, if_exists="replace",
              index=False, chunksize=5000, method="multi")
    print("Tabela temperature_readings carregada.")

    # Criação das views
    with engine.begin() as conn:
        conn.exec_driver_sql(VIEWS_SQL.read_text(encoding="utf-8"))
    print("Views criadas.")

    # Verificação rápida
    total = pd.read_sql("SELECT COUNT(*) AS total FROM temperature_readings", engine)
    print("Registros no PostgreSQL:", int(total["total"][0]))


if __name__ == "__main__":
    main()
