# -*- coding: utf-8 -*-
"""Adaptador web para hospedar a Missão Aprovação no Render + PostgreSQL externo."""
import hmac
import json
import os
from functools import wraps

import psycopg
from psycopg.types.json import Jsonb
from flask import Flask, Response, jsonify, request

from estudo_tjsp import PAGE

app = Flask(__name__)


def resposta_auth():
    return Response(
        "Acesso protegido. Informe o usuário e a senha configurados pelo responsável.",
        status=401,
        headers={"WWW-Authenticate": 'Basic realm="Missão Aprovação"'},
        mimetype="text/plain",
    )


@app.before_request
def proteger_app():
    # Endpoint de saúde usado pelo Render; não expõe dados de estudo.
    if request.path == "/healthz":
        return None

    senha_configurada = os.environ.get("APP_PASSWORD", "")
    usuario_configurado = os.environ.get("APP_USER", "estudos")
    if not senha_configurada:
        return Response(
            "Configuração incompleta: defina APP_PASSWORD nas variáveis de ambiente.",
            status=503,
            mimetype="text/plain",
        )

    auth = request.authorization
    if (
        not auth
        or not hmac.compare_digest(auth.username or "", usuario_configurado)
        or not hmac.compare_digest(auth.password or "", senha_configurada)
    ):
        return resposta_auth()
    return None


def conectar():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("A variável DATABASE_URL não foi configurada.")
    # A string do Neon normalmente já inclui sslmode=require; exigimos TLS também
    # quando a URL não especifica um modo SSL.
    if "sslmode=" not in url:
        return psycopg.connect(url, sslmode="require", connect_timeout=15)
    return psycopg.connect(url, connect_timeout=15)


def garantir_tabela(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS app_state (
            id SMALLINT PRIMARY KEY CHECK (id = 1),
            data JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """
    )


@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.get("/")
def index():
    return Response(PAGE, mimetype="text/html; charset=utf-8", headers={"Cache-Control": "no-store"})


@app.get("/api/state")
def get_state():
    try:
        with conectar() as conn:
            garantir_tabela(conn)
            row = conn.execute("SELECT data FROM app_state WHERE id = 1").fetchone()
            data = row[0] if row else {}
        return jsonify(data), 200, {"Cache-Control": "no-store"}
    except Exception:
        app.logger.exception("Falha ao carregar o progresso do PostgreSQL")
        return jsonify({"error": "Não foi possível carregar o progresso. Tente novamente."}), 503


@app.post("/api/state")
def post_state():
    try:
        # O JavaScript original não envia Content-Type: application/json,
        # então lemos o corpo diretamente e validamos como JSON.
        data = json.loads(request.get_data(as_text=True) or "")
        if not isinstance(data, dict):
            return jsonify({"error": "O progresso deve ser um objeto JSON."}), 400
    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
        return jsonify({"error": "JSON inválido."}), 400

    try:
        with conectar() as conn:
            garantir_tabela(conn)
            conn.execute(
                """
                INSERT INTO app_state (id, data, updated_at)
                VALUES (1, %s, NOW())
                ON CONFLICT (id) DO UPDATE
                SET data = EXCLUDED.data, updated_at = NOW()
                """,
                (Jsonb(data),),
            )
        return jsonify({"ok": True}), 200, {"Cache-Control": "no-store"}
    except Exception:
        app.logger.exception("Falha ao salvar o progresso no PostgreSQL")
        return jsonify({"error": "Não foi possível salvar. Confira a conexão e tente novamente."}), 503


if __name__ == "__main__":
    # Execução local opcional. Configure DATABASE_URL e APP_PASSWORD antes.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "8765")), debug=False)
