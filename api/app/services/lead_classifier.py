import re
import unicodedata
from dataclasses import dataclass
from typing import Protocol


class LeadLike(Protocol):
    name: str
    email: str
    phone: str | None
    insurance_type: str | None
    message: str


@dataclass(frozen=True)
class Classification:
    category: str
    score: int
    priority: str
    summary: str


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _infer_category(insurance_type: str | None, message: str) -> str:
    if insurance_type:
        return _normalize(insurance_type).replace(" ", "_")

    categories = {
        "saude_empresarial": ("saude", "plano empresarial", "plano de saude"),
        "seguro_auto": ("automovel", "carro", "seguro auto"),
        "seguro_residencial": ("residencia", "residencial", "casa"),
        "seguro_vida": ("seguro de vida", "protecao familiar"),
    }
    return next(
        (category for category, terms in categories.items() if _contains_any(message, terms)),
        "outros",
    )


def _priority(score: int) -> str:
    if score >= 75:
        return "HIGH"
    if score >= 45:
        return "MEDIUM"
    return "LOW"


def _build_summary(category: str, message: str, has_business_context: bool) -> str:
    volume = re.search(r"\b(\d{1,4})\s*(?:funcionarios|colaboradores|vidas)\b", message)
    readable_category = category.replace("_", " ")
    if has_business_context and volume:
        return (
            f"Empresa interessada em {readable_category} para aproximadamente "
            f"{volume.group(1)} vidas."
        )
    if has_business_context:
        return f"Empresa interessada em informações sobre {readable_category}."
    return f"Lead interessado em informações sobre {readable_category}."


def classify_lead(lead: LeadLike) -> Classification:
    """Classify a lead with transparent, deterministic business rules."""
    message = _normalize(lead.message)
    score = 10

    explicit_intent = _contains_any(
        message,
        ("cotacao", "cotar", "contratar", "fechar", "proposta", "orcamento"),
    )
    business_context = _contains_any(
        message,
        ("empresa", "funcionarios", "colaboradores", "cnpj", "vidas"),
    )
    volume_informed = bool(
        re.search(r"\b\d{1,4}\s*(?:funcionarios|colaboradores|vidas)\b", message)
    )
    urgency = _contains_any(
        message,
        ("urgente", "urgencia", "imediato", "ainda hoje", "esta semana"),
    )

    score += 30 if explicit_intent else 0
    score += 20 if business_context else 0
    score += 15 if volume_informed else 0
    score += 15 if urgency else 0
    score += 5 if lead.phone else 0
    score += 5 if lead.insurance_type else 0
    score = min(score, 100)

    category = _infer_category(lead.insurance_type, message)
    return Classification(
        category=category,
        score=score,
        priority=_priority(score),
        summary=_build_summary(category, message, business_context),
    )
