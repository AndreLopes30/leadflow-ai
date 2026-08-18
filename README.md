# LeadFlow AI

Automação de triagem e qualificação de leads utilizando **n8n, Python/FastAPI e PostgreSQL**.

O LeadFlow AI recebe um lead por webhook, normaliza os dados, aplica regras de
qualificação, persiste o resultado e direciona automaticamente o atendimento de
acordo com a prioridade identificada.

![Fluxo LeadFlow AI](docs/leadflow-workflow.png)

## O problema

Em processos comerciais, leads podem chegar por diferentes canais e exigir uma
triagem manual antes de serem direcionados para atendimento.

Esse processo pode gerar demora, inconsistência na classificação e trabalho
repetitivo para a equipe.

## A solução

O LeadFlow AI automatiza esse processo, conectando n8n, uma API em Python/FastAPI
e PostgreSQL para transformar dados recebidos por webhook em uma classificação
acionável para o atendimento comercial.

## Arquitetura

```mermaid
flowchart LR
    W[Webhook] --> N[n8n: valida e normaliza]
    N --> A[FastAPI: classifica]
    A --> P[(PostgreSQL)]
    A --> S{n8n Switch}
    S --> H[HIGH]
    S --> M[MEDIUM]
    S --> L[LOW]
