from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.models import Appointment, User, Patient, AppointmentStatus, UserType
from schemas.schemas import AppointmentCreate, AppointmentUpdate, Appointment as AppointmentSchema
from services.auth_service import get_current_user
 
router = APIRouter(prefix="/appointments", tags=["appointments"])
 
# ============================
# GET /appointments
# ============================
@router.get("/", response_model=List[AppointmentSchema])
async def get_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type == UserType.PSICOLOGO:
        appointments = db.query(Appointment).filter(
            Appointment.psychologist_id == current_user.id
        ).all()
    else:
        patient = db.query(Patient).filter(
            Patient.email == current_user.email
        ).first()
 
        if not patient:
            return []
 
        appointments = db.query(Appointment).filter(
            Appointment.patient_id == patient.id
        ).all()
 
    return appointments
 
 
# ============================
# POST /appointments
# ============================
@router.post("/", response_model=AppointmentSchema)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Appointment).filter(
        Appointment.psychologist_id == appointment_data.psychologist_id,
        Appointment.date == appointment_data.date,
        Appointment.time == appointment_data.time,
        Appointment.status == AppointmentStatus.AGENDADO
    ).first()
 
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Horário não disponível"
        )
 
    db_appointment = Appointment(
        **appointment_data.dict(),
        status=AppointmentStatus.AGENDADO
    )
 
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
 
 
# ============================
# PUT /appointments/{id}
# ============================
@router.put("/{appointment_id}", response_model=AppointmentSchema)
async def update_appointment(
    appointment_id: int,
    update_data: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()
 
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
 
    if current_user.type == UserType.PSICOLOGO and appointment.psychologist_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão"
        )
 
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(appointment, field, value)
 
    db.commit()
    db.refresh(appointment)
    return appointment
 
 
# ============================
# DELETE /appointments/{id}
# ============================
@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()
 
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado"
        )
 
    appointment.status = AppointmentStatus.CANCELADO
    db.commit()
 
    return {"message": "Agendamento cancelado com sucesso"}
 
 