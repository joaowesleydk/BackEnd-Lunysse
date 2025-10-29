from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from core.database import datetime, timezone
import enum
 
class userType (str, enum.Enum):
    PSICOLOGO = "psicologo"
    PACIENTE = "paciente"
   
class AppointmentStatus (str, enum.Enum):
    AGENDADO = "agendado"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    REAGENDADO = "reagendado"
   
class RequestStatus(str, enum.Enum):
    PENDENTE = "pendente"
    ACEITO = "aceito"
    REJEITADO = "rejeitado"
 
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    type = Column(Enum(userType))
    name = Column(String)
    Specialty = Column(String, nullable=True)
    crp = Column(String, unique=True, nullable=True)
    Phone = Column(String, unique=True, nullable=True)
    Created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
 
class Patient(Base):
    __tablename__ = "patient"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    Phone = Column(String, unique=True)
    email = Column(String, unique=True)
    birth_date = Column(String)
    age = Column(Integer)
    status = Column(String)
    psychologist_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
   
    psychologist = relationship("User", foreign_keys=[psychologist_id])
 
class Appointment(Base):
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    psychologist_id = Column(Integer, ForeignKey("user.id"))
    date = Column(Date)
    time = Column(String)
    status = Column(Enum(AppointmentStatus))
    description = Column(String)
    duration = Column(Integer, default=50)
    notes = Column(Text, default="")
    full_notes = Column(Text, default="")
    Created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
 
    psychologist = relationship("User", foreign_keys=[psychologist_id])
    patient = relationship("Patient", foreign_keys=[patient_id])
 
class Request(Base):
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    patient_email = Column(String)
    patient_phone = Column(String)
    preferred_psychologist = Column(Integer, ForeignKey("user.id"))
    description = Column(Text)
    urgency = Column(String)
    preferred_date = Column(Text, nullable=True)
    preferred_time = Column(Text, nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDENTE)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
   
    psychologist = relationship("User")
 
 