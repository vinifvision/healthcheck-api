# 📡 Telemetry & Healthcheck API (GitOps Flow)

Uma API REST assíncrona desenvolvida para monitoramento contínuo de microsserviços, simulando um ambiente de telemetria de produção. 

## 🏗️ Arquitetura e Stack Tecnológica
* **Backend:** Python 3.11, FastAPI
* **Armazenamento (Time-Series Local):** SQLite3
* **Conteinerização:** Docker (Multi-stage build otimizado)
* **CI/CD:** GitHub Actions (Linter Automático + Docker Build)
* **Cloud Hosting:** Microsoft Azure (Container Apps)

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
