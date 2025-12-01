import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
# =============================
# CONFIGURAÇÃO DA API
# =============================
load_dotenv()
 
def get_email_client():
    """Retorna o cliente configurado para envio de e-mail."""
    api_key = os.getenv("BREVO_API_KEY")  # SEMPRE usar variável de ambiente!
    if not api_key:
        raise ValueError("A variável de ambiente BREVO_API_KEY não está definida.")
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    return sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )
# =============================
# FUNÇÃO GENÉRICA DE ENVIO
# =============================
def send_email(to_email: str, subject: str, html_content: str,
               sender_email=None, sender_name="Lunysse"):
    if sender_email is None:
        sender_email = os.getenv("EMAIL_SENDER")
    """Função genérica para envio de e-mails transacionais."""
    if not to_email:
        raise ValueError("E-mail do destinatário está vazio.")
    api_instance = get_email_client()
    email_data = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        subject=subject,
        html_content=html_content,
        sender={"email": sender_email, "name": sender_name},
    )
    try:
        api_instance.send_transac_email(email_data)
        print(f"E-mail enviado para {to_email}")
        return True
    except ApiException as e:
        print(f"Erro ao enviar e-mail para {to_email}: {e}")
        return False
 
# =============================
# EMAIL: CONFIRMAÇÃO DE AGENDAMENTO
# =============================
 
def send_email_appointment(client_email: str, client_name: str, date: str, time: str):
    email = os.getenv("EMAIL_DOMAIN")
    html = f"""
        <h3>Olá {client_name},</h3>
        <p>Sua consulta foi agendada com sucesso.</p>
        <p><strong>Data:</strong> {date}</p>
        <p><strong>Horário:</strong> {time}</p>
        <p>Obrigado por utilizar nossa plataforma.</p>
    """
 
    return send_email(
        to_email=client_email,
        subject="Confirmação de Agendamento",
        html_content=html,
        sender_email=email,
        sender_name="Sistema de Agendamentos"
    )
 
 
# =============================
# EMAIL: SOLICITAÇÃO ACEITA
# =============================
 
def send_email_request_accepted(patient_email: str, patient_name: str, psychologist_name: str):
    email = os.getenv("EMAIL_DOMAIN")
    html = f"""
        <h3>Olá {patient_name},</h3>
        <p>Sua solicitação foi aceita pelo psicólogo <strong>{psychologist_name}</strong>.</p>
        <p>Em breve ele entrará em contato para combinar o melhor horário.</p>
        <p>Obrigado por utilizar nossa plataforma.</p>
    """
 
    return send_email(
        to_email=patient_email,
        subject="Sua Solicitação Foi Aceita",
        html_content=html,
        sender_email=email,
        sender_name="Sistema de Agendamentos"
    )
# =============================
# EMAIL: SOLICITAÇÃO REJEITADA
# =============================    
def send_email_request_reject(patient_email: str, patient_name: str, psychologist_name: str):
    email = os.getenv("EMAIL_DOMAIN")
    html = f"""
        <h3>Olá {patient_name},</h3>
        <p>Sua solicitação foi recusada pelo psicólogo <strong>{psychologist_name}</strong>.</p>
        <p>este psicologo nao aceitou sua solicitaçao, voce tera que escolher outro psicologo para enviar uma nova solicitaçao ou tentar novamente a solicitaçao com o mesmo psicologo.</p>
        <p>Obrigado por utilizar nossa plataforma.</p>
    """
 
    return send_email(
        to_email=patient_email,
        subject="Sua Solicitação Foi negada",
        html_content=html,
        sender_email=email,
        sender_name="Sistema de Agendamentos"
    )
# =============================
# EMAIL: SOLICITAÇÃO para psicologo
# =============================    
def send_email_new_request_to_psychologist(psychologist_email: str, psychologist_name: str, patient_name: str):
    email = os.getenv("EMAIL_DOMAIN")
    html = f"""
        <h3>Olá psicologo {psychologist_name},</h3>
        <p>Você possui uma nova solicitação de paciente no sistema, o  <strong>{patient_name}</strong> deseja ser atendido por você.</p>
        <p>Você pode acessar o sistema pelo link abaixo e aceitar ou recusar o paciente.</p>
        <button
            onclick="window.location.href='https://lunysse.vercel.app/login'"
            style="
                background-color: #4A4AFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            ">Entrar</button>
        <p>Obrigado por utilizar nossa plataforma.</p>
    """
    return send_email(
        to_email=psychologist_email,
        subject="Nova solicitação de paciente no sistema",
        html_content=html,
        sender_email=email,
        sender_name="Sistema de Agendamentos"
    )
 
def send_email_appointment_status_update(
    patient_email: str,
    patient_name: str,
    appointment_date: str,
    appointment_time: str,
    old_status: str,
    new_status: str
):
    email = os.getenv("EMAIL_DOMAIN")
   
    html = f"""
        <h3>Olá {patient_name},</h3>
        <p>O status do seu agendamento foi atualizado.</p>
 
        <p><strong>Status anterior:</strong> {old_status}</p>
        <p><strong>Novo status:</strong> {new_status}</p>
       
        <p><strong>Data:</strong> {appointment_date}</p>
        <p><strong>Horário:</strong> {appointment_time}</p>
 
        <p>Qualquer dúvida, entre em contato com seu psicólogo.</p>
    """
 
    return send_email(
        to_email=patient_email,
        subject="Atualização no Status do Agendamento",
        html_content=html,
        sender_email=email,
        sender_name="Sistema de Agendamentos"
    )
 
def send_email_appointment_status_cancel(
    patient_email: str,
    patient_name: str
):
    email = os.getenv("EMAIL_DOMAIN")
 
    html = f"""
        <h3>Olá {patient_name},</h3>
        <p>Seu agendamento foi <strong>cancelado</strong>.</p>
        <p>Se você não solicitou esse cancelamento, entre em contato com seu psicólogo.</p>
    """
 
    return send_email(
        to_email=patient_email,
        subject="Agendamento Cancelado",
        html_content=html,
        sender_email=email,
        sender_name="Sistema de Agendamentos"
    )
 