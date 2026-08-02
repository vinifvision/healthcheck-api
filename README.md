# 📡 Telemetry & Healthcheck API (GitOps Flow)

API experimental para monitoramento de disponibilidade e latência de serviços HTTP, com armazenamento do histórico de verificações.

## 🏗️ Arquitetura e Stack Tecnológica
* **Backend:** Python 3.11, FastAPI
* **Armazenamento (Time-Series Local):** SQLite3
* **Conteinerização:** Docker (Multi-stage build otimizado)
* **CI/CD:** GitHub Actions (Linter Automático + Docker Build)
* **Deploy planejado:** Microsoft Azure Container Apps

## ⚙️ Como executar localmente
\`\`\`bash
# Clone o repositório
git clone https://github.com/seu-usuario/healthcheck-api.git

# Suba a infraestrutura via Docker
docker-compose up --build -d

# Acesse a documentação
http://localhost:8000/docs
\`\`\`

## 📊 Endpoints Principais
* `POST /scan`: Dispara requests em background para os serviços mapeados e registra a latência.
* `GET /logs`: Retorna o histórico de telemetria e o *status code* ordenado por timestamp.
