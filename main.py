from fastapi import FastAPI, BackgroundTasks
import requests
import sqlite3
import time
from datetime import datetime

app = FastAPI(title="Healthcheck & Telemetry API", version="1.0")

# Configuração simples do Banco de Dados SQLite
def init_db():
    conn = sqlite3.connect("telemetry.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_url TEXT,
            status_code INTEGER,
            latency_ms REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Lista de "Microserviços" críticos para monitorar
TARGETS = [
    "https://api.github.com",                                       # API Padrão Rest
    "https://api.mcsrvstat.us/2/mc.hypixel.net",                    # Monitoramento de Game Server
    "https://store.steampowered.com/api/appdetails?appids=460950"   # API de Loja/E-commerce
]

# A lógica de negócio (o ping)
def ping_targets():
    conn = sqlite3.connect("telemetry.db")
    cursor = conn.cursor()

    for url in TARGETS:
        start_time = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = (time.time() - start_time) * 1000 # Converte para milisegundos
            status = response.status_code
        except requests.RequestException:
            latency = 0.0
            status = 500 # Erro interno/timeout

        timestamp = datetime.now().isoformat()

        # Salva os resultados no banco de dados
        cursor.execute(
            "INSERT INTO logs (target_url, status_code, latency_ms, timestamp) VALUES (?, ?, ?, ?)",
            (url, status, round(latency, 2), timestamp)
        )
    conn.commit()
    conn.close()

# Endpoints da nossa API
@app.post("/scan")
async def trigger_scan(background_tasks: BackgroundTasks):
    """Dispara uma varredura manual em todos os serviços listados."""
    background_tasks.add_task(ping_targets)
    return {"message": "Varredura iniciada em segundo plano. Verifique os logs em breve."}

@app.get("/logs")
async def get_logs():
    """Retorna os últimos 10 registros de telemetria do banco."""
    conn = sqlite3.connect("telemetry.db")
    cursor = conn.cursor()
    cursor.execute("SELECT target_url, status_code, latency_ms, timestamp FROM logs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"url": row[0], "status": row[1], "latency_ms": row[2], "timestamp": row[3]}
        for row in rows
    ]
