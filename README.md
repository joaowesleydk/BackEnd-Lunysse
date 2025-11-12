# 🧠 Lunysse API — Sistema de Agendamento Psicológico

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-brightgreen?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-orange?logo=databricks)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> **Lunysse API** é o backend de um sistema completo de **gestão e agendamento psicológico**, com autenticação JWT, relatórios dinâmicos, integração com análise preditiva de risco (ML) e suporte multiusuário para psicólogos e pacientes.

---

## 📑 Sumário

1. [📘 Visão Geral](#-visão-geral)
2. [🎯 Objetivos do Projeto](#-objetivos-do-projeto)
3. [🚀 Principais Funcionalidades](#-principais-funcionalidades)
4. [🛠️ Tecnologias Utilizadas](#-tecnologias-utilizadas)
5. [📂 Estrutura do Projeto](#-estrutura-do-projeto)
6. [⚙️ Instalação e Execução](#️-instalação-e-execução)
7. [🌍 Variáveis de Ambiente (.env)](#-variáveis-de-ambiente-env)
8. [🧭 Endpoints Principais](#-endpoints-principais)
9. [🔐 Segurança e Autenticação](#-segurança-e-autenticação)
10. [📊 Relatórios e Machine Learning](#-relatórios-e-machine-learning)
11. [🧪 Testes Automatizados](#-testes-automatizados)
12. [🧱 Boas Práticas e Segurança](#-boas-práticas-e-segurança)
13. [📄 Licença](#-licença)
14. [👨‍💻 Autor e Contato](#-autor-e-contato)

---

## 📘 Visão Geral

O **Lunysse Backend** foi desenvolvido para fornecer a base sólida de uma aplicação moderna para **clínicas psicológicas**, permitindo que **psicólogos e pacientes** realizem:

- 📅 Agendamento e acompanhamento de consultas  
- 👩‍⚕️ Cadastro e autenticação de psicólogos  
- 🧍‍♀️ Gerenciamento de pacientes e histórico clínico  
- 📊 Geração de relatórios e estatísticas personalizadas  
- 🤖 Análise preditiva de risco emocional (via módulo de ML)

---

## 🎯 Objetivos do Projeto

- Automatizar o processo de **agendamento psicológico** com segurança e praticidade.  
- Fornecer **relatórios inteligentes** para acompanhamento de desempenho clínico.  
- Integrar um **módulo de Machine Learning** para análise de risco emocional.  
- Garantir **segurança de dados sensíveis** e conformidade com boas práticas de API REST.  

---

## 🚀 Principais Funcionalidades

✅ Autenticação com **JWT**  
✅ Hash seguro de senhas com **bcrypt (Passlib)**  
✅ Sistema completo de **CRUD** (pacientes, psicólogos, agendamentos)  
✅ **Agendamento inteligente** com status dinâmico  
✅ **Relatórios com métricas de desempenho e risco**  
✅ **Integração com módulo de Machine Learning**  
✅ **Middleware de CORS configurável**  
✅ Estrutura modular e escalável  

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| Linguagem | **Python 3.11+** |
| Framework Web | **FastAPI** |
| ORM / Banco | **SQLAlchemy + PostgreSQL / SQLite** |
| Autenticação | **JWT (Python-JOSE)** |
| Segurança | **Passlib (bcrypt)** |
| Variáveis de Ambiente | **Python-dotenv** |
| ML e Relatórios | **Pandas / Custom ML Services** |
| Documentação | **Swagger UI / ReDoc** |
| Testes | **Pytest** |

---

## 📂 Estrutura do Projeto

```bash
📦 Lunysse-API/    
│
├── main.py                     # Ponto de entrada da aplicação FastAPI
│
├── core/
│   ├── database.py              # Configuração do banco e sessão
│   └── security.py              # Autenticação, JWT, senhas
│
├── models/
│   └── models.py                # Modelos ORM (SQLAlchemy)
│
├── schemas/
│   └── schemas.py               # Schemas Pydantic (validação e resposta)
│
├── routers/
│   ├── auth.py                  # Autenticação e login
│   ├── patients.py              # Rotas de pacientes
│   ├── psychologists.py         # Rotas de psicólogos
│   ├── appointments.py          # Agendamentos
│   ├── reports.py               # Relatórios e estatísticas
│   ├── ml_analysis.py           # Análises preditivas (ML)
│   └── requests.py              # Requisições auxiliares
│
├── services/
│   ├── ml_services.py           # Serviços de Machine Learning
│   └── report_services.py       # Geração de relatórios dinâmicos
│
├── tests/                       # Testes automatizados (Pytest)
│   ├── test_auth.py
│   ├── test_patients.py
│   └── test_appointments.py
│
├── .env                         # Variáveis de ambiente
├── requirements.txt              # Dependências do projeto
└── README.md                     # Documentação principal
````
```bash
Instalação e Execução
1️⃣ Clone o repositório
git clone https://github.com/seu-usuario/lunysse-backend.git
cd lunysse-backend

2️⃣ Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Configure o arquivo .env

Crie o arquivo .env na raiz com:

DATABASE_URL=sqlite:///./lunysse.db
SECRET_KEY=sua_chave_super_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000

5️⃣ Execute o servidor
uvicorn main:app --reload


Acesse:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🌍 Variáveis de Ambiente (.env)
Variável	Descrição	Exemplo
DATABASE_URL	URL do banco de dados	postgresql://user:pass@localhost:5432/lunysse_db
SECRET_KEY	Chave secreta para JWT	supersegredo123
ALGORITHM	Algoritmo de criptografia JWT	HS256
ACCESS_TOKEN_EXPIRE_MINUTES	Tempo de expiração do token (minutos)	60
CORS_ORIGINS	Domínios permitidos	http://localhost:3000
🧭 Endpoints Principais
Método	Rota	Descrição
POST	/auth/login	Login e geração de token
POST	/patients/	Cadastrar novo paciente
GET	/patients/	Listar pacientes
POST	/appointments/	Criar agendamento
GET	/reports/	Gerar relatórios
GET	/ml/analysis	Executar análise preditiva de risco
🔐 Segurança e Autenticação

Arquivo: core/security.py

Responsável por:

Criptografia de senhas (bcrypt)

Criação e validação de tokens JWT

Leitura segura de variáveis do .env

Exemplo:

from core.security import create_access_token

token = create_access_token({"sub": "user@example.com"})

📊 Relatórios e Machine Learning

Os módulos report_services.py e ml_services.py fornecem:

📈 Estatísticas de comparecimento

🔍 Análise de risco com Machine Learning

⚠️ Alertas de pacientes com risco emocional elevado

Exemplo de resposta JSON:

{
  "stats": {
    "active_patients": 14,
    "total_sessions": 52,
    "completed_sessions": 38,
    "attendance_rate": 73.08
  },
  "risk_alerts": [
    { "patient": "Maria", "risk": "Alto", "reason": "Frequência baixa" }
  ]
}



🧱 Boas Práticas e Segurança

✅ Senhas armazenadas com bcrypt
✅ Tokens JWT com expiração automática
✅ Rotas protegidas por autenticação obrigatória
✅ CORS configurado dinamicamente
✅ Variáveis sensíveis mantidas no .env

📄 Licença

Projeto licenciado sob a MIT License — você pode usar, modificar e distribuir livremente com atribuição ao autor original.

👨‍💻 Autor e Contato

João Wesley Damas Kind
📧 Email profissional
💼 GitHub: https://github.com/joaowesleydk