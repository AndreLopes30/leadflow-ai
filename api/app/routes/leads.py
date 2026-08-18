from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Lead
from ..schemas import LeadCreate, LeadResponse
from ..services.lead_classifier import classify_lead


router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.post(
    "/classify",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
)
def classify_and_store_lead(
    payload: LeadCreate,
    db: Session = Depends(get_db),
) -> Lead:
    classification = classify_lead(payload)
    lead = Lead(
        **payload.model_dump(),
        category=classification.category,
        score=classification.score,
        priority=classification.priority,
        summary=classification.summary,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
