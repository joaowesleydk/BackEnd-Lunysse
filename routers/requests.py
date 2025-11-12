from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime
from core.database import get_db
from models.models import Request, User, UserType, RequestStatus
from schemas.schemas import RequestCreate, RequestUpdate, Request as RequestSchema
from services.auth_service import get_current_user
 
router = APIRouter(prefix="/requests", tags=["requests"])
 
# ============================
# GET /requests
# ============================
@router.get("/", response_model=List[RequestSchema])
def get_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas psicólogos podem listar solicitações"
        )
 
    requests = db.query(Request).filter(
        Request.preferred_psychologist == current_user.id
    ).all()
 
    for req in requests:
        req.preferred_dates = json.loads(req.preferred_dates) if req.preferred_dates else []
        req.preferred_times = json.loads(req.preferred_times) if req.preferred_times else []
 
    return requests
 
 
# ============================
# POST /requests
# ============================
@router.post("/", response_model=RequestSchema)
def create_request(
    request_data: RequestCreate,
    db: Session = Depends(get_db),
):
    existing_request = db.query(Request).filter(
        Request.patient_email == request_data.patient_email,
        Request.preferred_psychologist == request_data.preferred_psychologist,
        Request.status == RequestStatus.PENDENTE
    ).first()
 
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já possui uma solicitação pendente para este psicólogo"
        )
 
    new_request = Request(
        patient_name=request_data.patient_name,
        patient_email=request_data.patient_email,
        patient_phone=request_data.patient_phone,
        preferred_psychologist=request_data.preferred_psychologist,
        description=request_data.description,
        preferred_dates=json.dumps(request_data.preferred_dates),
        preferred_times=json.dumps(request_data.preferred_times),
        status=RequestStatus.PENDENTE
    )
 
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
 
    new_request.preferred_dates = request_data.preferred_dates
    new_request.preferred_times = request_data.preferred_times
 
    return new_request
 
 
# ============================
# PUT /requests/{id}
# ============================
@router.put("/{request_id}", response_model=RequestSchema)
def update_request(
    request_id: int,
    update_data: RequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas psicólogos podem atualizar solicitações"
        )
 
    request = db.query(Request).filter(
        Request.id == request_id,
        Request.preferred_psychologist == current_user.id
    ).first()
 
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
 
    request.status = update_data.status
    request.notes = update_data.notes or ""
    request.updated_at = datetime.utcnow()
 
    db.commit()
    db.refresh(request)
 
    request.preferred_dates = json.loads(request.preferred_dates)
    request.preferred_times = json.loads(request.preferred_times)
 
    return request
 
 