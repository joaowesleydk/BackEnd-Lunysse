 
# Lunysse API - documentação de rotas
 
**Todas as rotas abaixo estão presentes no sistema lunysse e todas estão funcionando na V1.0 do projeto lunysse**
 
**Framework utilizado para construir o sistema backend lunysse é o fast API por ser API RESTFULL e permitir o uso de Machine Learning no projeto**
 
### Rotas presentes no sistema
 
``` bash
rota raiz
 
    GET localhost:3000/ - rota raiz do servidor
 
auth
 
    POST /auth/login - login de usuario
    POST /auth/register - registra um novo usuario
 
appointments
 
    GET /appointments/ - Lista todos os agendamentos para o usuario logado.
    POST /appointments/ - Cria um novo agendamento para o psycologo logado.
    PUT /appointments/{id} - Atualiza todos os dados de agendamentos.
    DELETE /appointments/{id} - Deleta o agendamento
    GET /appointments/avaliable-slots - retorna os horarios livres de um psicologo para o dia
 
Patients
 
    GET /patients/ - Lista todos os paracientes cadastrados para o psicologo.
    POST /patients/ - Cadastra um novo Paciente
    GET /patients/{id}/sessions - Lista todas as sessões realizadas pelo paciente referente ao psicologo autenticado.
    POST /patients/{id}/notes - psicologo adiciona uma anotação ao paciente
 
Requests
    GET /requests/ - Lista soliciatações para o psicologo autenticado.
    POST /requests/ - Cria uma nova solicitação para o psicologo escolhido cadastrado no banco de dados.
    PUT /requests/{id} - Atualiza o estados da solicitação referente ao psicologo autenticado.
 
Report
 
    GET /reports/{psychologist_id} - Lista todo o relatorio para o psycologo autenticado
 
ML_Analysis
   
    GET /ml/risk-analysis - Lista a analise de risco de todos os paraciente referente ao psycologo logado.
    GET /ml/risk-analysis/{patient_id} - Lista a analise de risco de um paciente especifico de um psycologo autenticado.
 
Psychologist
 
    GET /Psychologists/ - Lista todos os psicologos cadastrados no banco de dados
```
 
**Rota de documentação sweagger**
```
    GET localhost:3000/docs - rota de documentação automatica do FASTAPI
```
 
# Funcionamento interno de cada rota
 
# Auth
 
## 1. POST `/auth/login`
 
### Objetivo
Autenticar um usuário existente e retornar um token JWT.
 
### Funcionamento Interno
1. Recebe `email` e `password`.
2. Chama `authenticate_user`:
   - Verifica se o usuário existe.
   - Valida a senha com o hash armazenado.
3. Se inválido → retorna **401 - Credenciais inválidas**.
4. Se válido:
   - Gera token JWT com `create_access_token` (expiração de 30 min).
   - Retorna token + dados do usuário.
 
### Resposta
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": { ... }
}
```
## 2. POST `/auth/register`
 
### **Objetivo**
Registrar um novo usuário no sistema e retornar automaticamente um token JWT para autenticação.
 
### **Funcionamento Interno**
 
1. **Verificação de e-mail existente**
   - Consulta o banco para saber se já existe um usuário com o e-mail informado.
   - Caso exista → retorna **400 - Email já cadastrado**.
 
2. **Criação do usuário**
   - A senha informada é convertida em hash utilizando `get_password_hash`.
   - Um novo objeto `User` é criado com os dados enviados e salvo no banco.
 
3. **Registro automático de paciente (condicional)**
   - Se o tipo do usuário for `PACIENTE`:
     - A idade é calculada usando `calculate_age`.
     - Um registro é criado na tabela `Patient` com:
       - id do usuário
       - nome, e-mail e telefone
       - data de nascimento e idade
       - status inicial "Ativo"
 
4. **Autenticação imediata**
   - Após salvar o usuário, é gerado um token JWT com `create_access_token`.
   - O token tem expiração definida para 30 minutos.
 
5. **Retorno**
   - O sistema retorna o token e os dados completos do usuário recém-cadastrado.
 
### **Resposta**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": { ... }
}
```
 
# Appointments
 
 
## 1. GET `/appointments/`
 
### **Objetivo**
Retornar todos os agendamentos do usuário autenticado.
 
### **Funcionamento Interno**
- O sistema identifica o usuário autenticado através de `get_current_user`.
- Se for **psicólogo**:
  - Retorna todos os agendamentos em que `psychologist_id == current_user.id`.
- Se for **paciente**:
  - Busca o registro na tabela `Patient` pelo e-mail.
  - Retorna os agendamentos em que `patient_id == patient.id`.
- Se o paciente não existir → retorna lista vazia.
 
### **Retorno**
Lista de objetos `Appointment`.
 
---
 
## 2. POST `/appointments/`
 
### **Objetivo**
Criar um novo agendamento.
 
### **Funcionamento Interno**
1. Verifica se o horário já está ocupado para o psicólogo:
   - Verifica mesmo dia, mesmo horário e status `AGENDADO`.
   - Se houver conflito → **400 - Horário não disponível**.
2. Cria um novo `Appointment` com status inicial `AGENDADO`.
3. Salva no banco e retorna o agendamento criado.
 
### **Retorno**
Objeto `Appointment`.
 
---
 
## 3. PUT `/appointments/{appointment_id}`
 
### **Objetivo**
Atualizar um agendamento existente.
 
### **Funcionamento Interno**
1. Busca o agendamento pelo `appointment_id`.
   - Se não encontrado → **404 - Agendamento não encontrado**.
2. Verifica permissão:
   - Psicólogo só pode alterar agendamentos do próprio ID.
   - Se não autorizado → **403 - Sem permissão**.
3. Atualiza somente os campos enviados (partial update).
4. Salva e retorna o agendamento atualizado.
 
### **Retorno**
Objeto `Appointment`.
 
---
 
## 4. DELETE `/appointments/{appointment_id}`
 
### **Objetivo**
Cancelar um agendamento.
 
### **Funcionamento Interno**
1. Busca o agendamento.
   - Se não encontrado → **404 - Agendamento não encontrado**.
2. Atualiza o status para `CANCELADO`.
3. Salva no banco.
 
### **Retorno**
```json
{ "message": "Agendamento cancelado com sucesso" }
```
## 5. GET `/appointments/available-slots`
 
### **Objetivo**
Retornar os horários disponíveis para agendamento de um psicólogo em uma data específica.
 
### **Funcionamento Interno**
 
1. **Define a lista de horários fixos do dia**
   - Exemplo: `['09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']`.
 
2. **Consulta horários já ocupados**
   - Busca no banco todos os agendamentos com:
     - Mesma **data** enviada na requisição
     - Mesmo **psychologist_id**
     - Status igual a **AGENDADO**
 
3. **Processamento**
   - Extrai os horários ocupados retornados do banco.
   - Remove esses horários da lista fixa.
 
4. **Retorno**
   - Retorna apenas os horários que não estão ocupados.
 
### **Retorno**
```json
[
  "09:00",
  "10:00",
  "14:00"
]
```
 
# Patients
 
## 1. GET `/patients/`
 
### **Objetivo**
Listar todos os pacientes pertencentes ao psicólogo autenticado.
 
### **Funcionamento Interno**
 
1. Verifica se o usuário autenticado é um **PSICÓLOGO**.  
   - Caso contrário → **403 - Acesso negado**.
 
2. Busca no banco todos os pacientes cujo `psychologist_id` corresponde ao ID do psicólogo atual.
 
3. Para cada paciente:
   - Conta o total de sessões feitas com aquele psicólogo.
   - Adiciona dinamicamente o atributo `total_sessions`.
 
4. Retorna a lista de pacientes com seus respectivos totais de sessões.
 
### **Retorno**
Lista de objetos `Patient`.
 
---
 
## 2. POST `/patients/`
 
### **Objetivo**
Criar um novo paciente vinculado ao psicólogo autenticado.
 
### **Funcionamento Interno**
 
1. Verifica se o usuário autenticado é um **PSICÓLOGO**.  
   - Caso contrário → **403 - Acesso negado**.
 
2. Checa se já existe um paciente com o e-mail informado **para o mesmo psicólogo**.
   - Se existir → **400 - Paciente já cadastrado**.
 
3. Calcula a idade usando `calculate_age`.
 
4. Cria o objeto `Patient` com:
   - nome, e-mail, telefone
   - data de nascimento, idade
   - status “Ativo”
   - id do psicólogo responsável
 
5. Salva no banco e retorna o paciente criado.
 
### **Retorno**
Objeto `Patient`.
 
---
 
## 3. GET `/patients/{patient_id}/sessions`
 
### **Objetivo**
Listar todas as sessões (agendamentos) de um paciente específico.
 
### **Funcionamento Interno**
 
1. Verifica se o usuário autenticado é psicólogo.  
   - Caso contrário → **403 - Acesso negado**.
 
2. Busca todos os agendamentos onde:
   - `patient_id` corresponde ao informado na rota  
   - `psychologist_id` corresponde ao psicólogo autenticado
 
3. Retorna a lista de sessões.
 
### **Retorno**
Lista de objetos `Appointment`.
 
---
 
## 4. POST `/patients/{patient_id}/notes`
 
### **Objetivo**
Adicionar uma anotação a um paciente.
 
### **Funcionamento Interno**
 
1. Verifica se o usuário autenticado é psicólogo.  
   - Caso contrário → **403 - Acesso negado**.
 
2. Checa se o paciente pertence ao psicólogo autenticado.
   - Caso não exista → **404 - Paciente não encontrado**.
 
3. (Ainda não implementado no banco)  
   Apenas retorna uma confirmação de que a anotação foi registrada.
 
### **Retorno**
```json
{
  "id": patient_id,
  "message": "Anotação adicionada com sucesso"
}
```
# Requests
 
## 1. GET `/requests/`
 
### **Objetivo**
Listar todas as solicitações destinadas ao psicólogo autenticado.
 
### **Funcionamento Interno**
 
1. Verifica o tipo do usuário:
   - Apenas usuários do tipo **PSICOLOGO** podem acessar.
   - Caso contrário → **403 - Apenas psicólogos podem acessar solicitações**.
 
2. Busca no banco todas as solicitações onde:
   - `preferred_psychologist == current_user.id`.
 
3. Conversão de dados:
   - Campos `preferred_dates` e `preferred_times` são strings JSON no banco.
   - Convertidos para listas antes do retorno.
 
### **Retorno**
Lista de objetos `Request`.
 
---
 
## 2. POST `/requests/`
 
### **Objetivo**
Criar uma nova solicitação de atendimento para um psicólogo.
 
### **Funcionamento Interno**
 
1. Verifica se já existe uma solicitação pendente do mesmo paciente para o mesmo psicólogo:
   - Se existir → **400 - Solicitação pendente já existente**.
 
2. Cria o objeto `Request` com:
   - Dados do paciente.
   - Psicólogo preferido.
   - Descrição e urgência.
   - Datas e horários preferidos (salvos como JSON string).
   - Status inicial: `PENDENTE`.
 
3. Salva no banco.
 
4. Converte os campos JSON de volta para listas para o retorno.
 
### **Retorno**
Objeto `Request`.
 
---
 
## 3. PUT `/requests/{request_id}`
 
### **Objetivo**
Atualizar o status e as observações de uma solicitação.
 
### **Funcionamento Interno**
 
1. Verifica se o usuário é **PSICOLOGO**:
   - Caso contrário → **403 - Apenas psicólogos podem atualizar solicitações**.
 
2. Busca a solicitação pelo ID e pelo psicólogo autenticado.
   - Se não encontrar → **404 - Solicitação não encontrada**.
 
3. Atualiza:
   - `status`
   - `notes`
   - `updated_at` com a data/hora atual
 
4. Salva no banco.
 
5. Converte `preferred_dates` e `preferred_times` de JSON para listas.
 
### **Retorno**
Objeto `Request`.
 
---
 
## 4. Regras Gerais do Módulo
 
- Apenas psicólogos podem listar ou atualizar solicitações.
- Pacientes podem criar apenas solicitações para psicólogos específicos.
- JSON é utilizado para armazenar listas no banco.
- Status possíveis:
  - `PENDENTE`
  - `APROVADA`
  - `RECUSADA`
 
 
# Reports
 
## 1. GET `/reports/{psychologist_id}`
 
### **Objetivo**
Retornar os dados consolidados de relatórios referentes a um psicólogo específico.
 
### **Funcionamento Interno**
 
1. **Autenticação e Autorização**
   - Obtém o usuário autenticado via `get_current_user`.
   - Verifica se o usuário é do tipo **PSICOLOGO**.
     - Se não for → **403 - Apenas psicólogos podem acessar relatórios**.
   - Verifica se o psicólogo autenticado está solicitando **seus próprios relatórios**.
     - Se `current_user.id != psychologist_id` → **403 - Você só pode acessar seus próprios relatórios**.
 
2. **Geração dos relatórios**
   - Chama o serviço `generate_reports_data(db, psychologist_id)`.
   - Esse serviço retorna métricas e dados estruturados para o dashboard ou tela de relatórios.
 
3. **Retorno**
   - Retorna um objeto no formato do schema `ReportsData`.
 
### **Retorno**
```json
{
  "total_appointments": 0,
  "completed_appointments": 0,
  "canceled_appointments": 0,
  "patients_count": 0,
  "appointments_by_month": [],
  "appointments_by_status": []
}
```
 
# ML_Analysis
 
## 1. GET `/ml/risk-analysis`
 
### **Objetivo**
Retornar uma análise geral de risco dos pacientes atendidos pelo psicólogo autenticado.
 
### **Funcionamento Interno**
 
1. **Validação de permissão**
   - Apenas usuários do tipo **PSICÓLOGO** podem acessar.
   - Caso contrário → **403 - Acesso negado**.
 
2. **Geração da análise via ML**
   - Chama `calculate_patient_risk(db, psychologist_id)`.
   - A função retorna uma lista contendo:
     - ID do paciente
     - Nome
     - Número de consultas
     - Score de risco
     - Classificação: *Baixo*, *Moderado* ou *Alto*
 
3. **Geração de estatísticas**
   - Conta número total de pacientes analisados.
   - Conta quantos estão em cada categoria de risco.
   - Calcula a distribuição percentual.
 
4. **Retorno**
   - Um resumo geral (`summary`)
   - Lista de pacientes analisados (`patients`)
 
### **Exemplo de Retorno**
```json
{
  "summary": {
    "total_patients": 12,
    "high_risk": 3,
    "moderate_risk": 4,
    "low_risk": 5,
    "risk_distribution": {
      "Alto": "25.0%",
      "Moderado": "33.3%",
      "Baixo": "41.7%"
    }
  },
  "patients": [
    {
      "id": 1,
      "name": "Paciente A",
      "sessions": 2,
      "risk": "Alto",
      "score": 0.87
    }
  ]
}
```
---
### 2. GET /ml/risk-analysis/{patient_id}
 
#### **Objetivo**
Retornar a análise detalhada de risco de um paciente específico.
 
---
 
#### **Funcionamento Interno**
 
##### **1. Validação de permissão**
- Apenas psicólogos podem acessar.
- Caso contrário → **403 - Acesso negado**.
 
##### **2. Geração da análise global**
- A rota recalcula a lista completa usando **calculate_patient_risk**.
 
##### **3. Busca do paciente**
- Localiza o paciente pelo **patient_id**.
- Se não encontrado → **404 - Paciente não encontrado**.
 
---
 
#### **Retorno**
- Retorna somente o registro correspondente ao paciente solicitado.
 
---
 
#### **Exemplo de Retorno**
```json
{
  "id": 3,
  "name": "Paciente X",
  "sessions": 1,
  "risk": "Alto",
  "score": 0.92
}
```
# Psychologist
 
## GET `/psychologists/`
 
## **Objetivo**
Retornar a lista de todos os psicólogos cadastrados no sistema.
 
---
 
## **Funcionamento Interno**
 
1. **Abertura da conexão com o banco**
   - A função recebe a sessão do banco (`db`) através da dependência `get_db`.
 
2. **Consulta no banco**
   - Busca todos os usuários (`User`) cujo tipo (`User.type`) seja igual a **PSICOLOGO**.
 
3. **Mapeamento dos dados**
   - Para cada registro encontrado:
     - Cria um objeto baseado no schema `Psychologist`.
     - Preenche:
       - `id`
       - `name`
       - `specialty` (string vazia se for `None`)
       - `crp` (string vazia se for `None`)
 
4. **Retorno**
   - Retorna uma lista contendo todos os psicólogos formatados conforme o schema da API.
 
---
 
## **Retorno (Exemplo)**
```json
[
  {
    "id": 1,
    "name": "Dra. Maria Silva",
    "specialty": "Terapia Cognitivo-Comportamental",
    "crp": "12345-XX"
  },
  {
    "id": 2,
    "name": "Dr. João Souza",
    "specialty": "",
    "crp": ""
  }
]
```
 