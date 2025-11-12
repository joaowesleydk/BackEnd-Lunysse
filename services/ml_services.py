 
from sqlalchemy.orm import Session
from models.models import Patient, Appointment, AppointmentStatus
from datetime import datetime
from typing import List, Dict
 
# ============================================================
# NÍVEIS DE RISCO
# ============================================================
 
class RiskLevel:
    BAIXO = "Baixo"
    MODERADO = "Moderado"
    ALTO = "Alto"
 
# ============================================================
# FUNÇÃO PRINCIPAL: calcula risco de todos os pacientes
# ============================================================
 
def calculate_patient_risk(db: Session, psychologist_id: int) -> List[Dict]:
    """
    Calcula risco dos pacientes com base no histórico de consultas
    Retorna uma lista com risco, score e motivos.
    """
 
    patients = (
        db.query(Patient)
        .filter(Patient.psychologist_id == psychologist_id)
        .all()
    )
 
    risk_analysis = []
 
    for patient in patients:
        # Buscar todos os agendamentos do paciente
        appointments = (
            db.query(Appointment)
            .filter(Appointment.patient_id == patient.id,
                    Appointment.psychologist_id == psychologist_id)
            .order_by(Appointment.date.desc())
            .all()
        )
 
        if not appointments:
            continue  # paciente sem histórico não entra na análise
 
        # Extrair métricas do comportamento
        metrics = _extract_patient_metrics(appointments)
 
        # Calcular score numérico
        risk_score = _calculate_risk_score(metrics)
 
        # Determinar nível
        risk_level = _determine_risk_level(risk_score)
 
        # Pegar motivo principal
        risk_reason = _identify_risk_reason(metrics)
 
        risk_analysis.append({
            "id": patient.id,
            "patient": patient.name,
            "risk": risk_level,
            "risk_score": risk_score,
            "reason": risk_reason,
            "last_appointment": appointments[0].date.isoformat(),
            "metrics": metrics
        })
 
    # Ordenar por maior risco primeiro
    return sorted(risk_analysis, key=lambda x: x["risk_score"], reverse=True)
 
# ============================================================
# EXTRAI MÉTRICAS IMPORTANTES DE UM PACIENTE
# ============================================================
 
def _extract_patient_metrics(appointments: List[Appointment]) -> Dict:
    """Extrai métricas relevantes do comportamento do paciente."""
 
    now = datetime.now().date()
 
    # Separar por status
    completed = [a for a in appointments if a.status == AppointmentStatus.CONCLUIDO]
    canceled = [a for a in appointments if a.status == AppointmentStatus.CANCELADO]
    scheduled = [a for a in appointments if a.status == AppointmentStatus.AGENDADO]
 
    # Últimos X dias
    last_30 = [a for a in appointments if (now - a.date).days <= 30]
    last_60 = [a for a in appointments if (now - a.date).days <= 60]
    last_90 = [a for a in appointments if (now - a.date).days <= 90]
 
    # Dias sem consulta
    days_since_last = (now - appointments[0].date).days
 
    total = len(appointments)
    cancel_rate = len(canceled) / total if total > 0 else 0
 
    # Frequência mensal
    if total > 0:
        first = min(a.date for a in appointments)
        months_active = max(1, (now - first).days / 30)
        freq_month = len(completed) / months_active
    else:
        freq_month = 0
 
    # Tendência recente
    recent_completed = len([a for a in completed if (now - a.date).days <= 30])
    previous_completed = len([a for a in completed if 30 < (now - a.date).days <= 60])
 
    return {
        "total_appointments": total,
        "completed_appointments": len(completed),
        "canceled_appointments": len(canceled),
        "cancellation_rate": cancel_rate,
        "days_since_last": days_since_last,
        "frequency_per_month": freq_month,
        "appointments_last_30": len(last_30),
        "appointments_last_60": len(last_60),
        "appointments_last_90": len(last_90),
        "recent_trend": recent_completed - previous_completed,
        "has_future_appointments": len(scheduled) > 0
    }
 
# ============================================================
# CALCULA SCORE FINAL DE RISCO (0–100)
# ============================================================
 
def _calculate_risk_score(metrics: Dict) -> int:
    """Calcula o score de risco baseado nas métricas coletadas."""
 
    score = 0
 
    # Quanto tempo sem consulta (peso maior)
    days_factor = min(metrics["days_since_last"] / 60, 1.0)
    score += days_factor * 30
 
    # Cancelamentos
    score += metrics["cancellation_rate"] * 25
 
    # Baixa frequência mensal
    if metrics["frequency_per_month"] < 1:
        score += 20
    elif metrics["frequency_per_month"] < 2:
        score += 10
 
    # Sem consultas no último mês
    if metrics["appointments_last_30"] == 0:
        score += 15
 
    # Nenhuma consulta nos últimos 60 dias
    elif metrics.get("appointments_last_60", 0) == 0:
        score += 10
 
    # Tendência de queda
    if metrics["recent_trend"] < -1:
        score += 10
    elif metrics["recent_trend"] < 0:
        score += 5
 
    # Sem consultas futuras
    if not metrics["has_future_appointments"]:
        score += 5
 
    return min(int(score), 100)
 
# ============================================================
# DETERMINA RISCO COMO BAIXO / MODERADO / ALTO
# ============================================================
 
def _determine_risk_level(risk_score: int) -> str:
    if risk_score >= 70:
        return RiskLevel.ALTO
    elif risk_score >= 40:
        return RiskLevel.MODERADO
    return RiskLevel.BAIXO
 
# ============================================================
# GERA MOTIVO PRINCIPAL DO RISCO
# ============================================================
 
def _identify_risk_reason(metrics: Dict) -> str:
    reasons = []
 
    if metrics["days_since_last"] > 45:
        reasons.append("Ausente há mais de 45 dias")
    elif metrics["days_since_last"] > 30:
        reasons.append("Ausente há mais de 30 dias")
 
    if metrics["cancellation_rate"] > 0.3:
        reasons.append("Alta taxa de cancelamentos")
    elif metrics["cancellation_rate"] > 0.2:
        reasons.append("Cancelamentos frequentes")
 
    if metrics["frequency_per_month"] < 1:
        reasons.append("Baixa frequência de consultas")
 
    if metrics["appointments_last_30"] == 0:
        reasons.append("Sem consultas no último mês")
 
    if metrics["recent_trend"] < -1:
        reasons.append("Diminuição na frequência")
 
    if not metrics["has_future_appointments"]:
        reasons.append("Sem consultas futuras")
 
    return ", ".join(reasons) if reasons else "Sem motivos críticos identificados"

 