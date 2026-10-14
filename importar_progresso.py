# Execute UMA VEZ no seu computador para importar progresso_tjsp.json para o Neon.
# Uso: configure DATABASE_URL e rode: python importar_progresso.py caminho/para/progresso_tjsp.json
import json
import os
import sys
from pathlib import Path

import psycopg
from psycopg.types.json import Jsonb


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python importar_progresso.py caminho/para/progresso_tjsp.json")
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("Defina DATABASE_URL com a URL do seu banco Neon antes de executar.")
    arquivo = Path(sys.argv[1]).expanduser()
    if not arquivo.is_file():
        raise SystemExit(f"Arquivo não encontrado: {arquivo}")
    with arquivo.open("r", encoding="utf-8") as f:
        dados = json.load(f)
    if not isinstance(dados, dict):
        raise SystemExit("O arquivo de progresso precisa conter um objeto JSON.")
    with psycopg.connect(url, connect_timeout=15) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS app_state (
                id SMALLINT PRIMARY KEY CHECK (id = 1),
                data JSONB NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)
        conn.execute("""
            INSERT INTO app_state (id, data, updated_at) VALUES (1, %s, NOW())
            ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data, updated_at = NOW()
        """, (Jsonb(dados),))
    print("Progresso importado com sucesso. Abra o aplicativo hospedado e confira os dados.")
    print("Atenção: a importação substitui o estado atual salvo no banco.")


if __name__ == "__main__":
    main()
