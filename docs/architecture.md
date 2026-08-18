# Arquitetura

O LeadFlow AI utiliza três serviços pequenos, executados pelo Docker Compose:

```mermaid
flowchart LR
    C[Cliente] -->|POST webhook| N[n8n]
    N -->|normaliza e valida| A[FastAPI]
    A -->|persiste| P[(PostgreSQL)]
    A -->|score e prioridade| N
    N --> S{Switch}
    S --> H[HIGH]
    S --> M[MEDIUM]
    S --> L[LOW]
    H --> C
    M --> C
    L --> C
```

## Responsabilidades

- **n8n:** recebe o webhook, normaliza os campos, chama a API e escolhe a ação comercial.
- **FastAPI:** valida o contrato, aplica regras determinísticas e grava o resultado.
- **PostgreSQL:** mantém os leads e suas classificações.

As regras ficam isoladas em `api/app/services/lead_classifier.py`. Essa separação permite
adicionar futuramente outro classificador (por exemplo, um provedor LLM) sem alterar o
contrato HTTP nem o workflow.
