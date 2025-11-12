# routers/reports.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import User, UserType
from schemas.schemas import ReportsData
from services.report_service import generate_reports_data
from services.auth_service import get_current_user
 
router = APIRouter(prefix="/reports", tags=["reports"])
 
@router.get("/{psychologist_id}", response_model=ReportsData)
def get_reports(
    psychologist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.type != UserType.PSICOLOGO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas psicólogos podem acessar relatórios"
        )
 
    if current_user.id != psychologist_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode acessar seus próprios relatórios"
        )
 
    data = generate_reports_data(db, psychologist_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
 
    return data
 
 