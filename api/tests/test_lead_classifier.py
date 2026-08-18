from types import SimpleNamespace

from app.services.lead_classifier import classify_lead


def make_lead(**overrides: object) -> SimpleNamespace:
    values = {
        "name": "Lead Teste",
        "email": "lead@example.com",
        "phone": None,
        "insurance_type": None,
        "message": "Quero informações sobre seguros.",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_classifies_high_priority_lead() -> None:
    lead = make_lead(
        phone="11999999999",
        insurance_type="saude_empresarial",
        message=(
            "Preciso de uma cotação urgente para minha empresa com 25 funcionários "
            "ainda hoje."
        ),
    )

    result = classify_lead(lead)

    assert result.category == "saude_empresarial"
    assert result.score == 100
    assert result.priority == "HIGH"
    assert "25 vidas" in result.summary


def test_classifies_medium_priority_lead() -> None:
    lead = make_lead(
        phone="11988887777",
        insurance_type="seguro_auto",
        message="Quero fazer uma cotação de seguro para meu carro.",
    )

    result = classify_lead(lead)

    assert result.score == 50
    assert result.priority == "MEDIUM"


def test_classifies_low_priority_lead() -> None:
    lead = make_lead(message="Gostaria de receber informações gerais sobre seguros.")

    result = classify_lead(lead)

    assert result.score == 10
    assert result.priority == "LOW"
