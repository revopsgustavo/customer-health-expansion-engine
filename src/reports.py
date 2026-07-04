from __future__ import annotations

from pathlib import Path

try:
    from src import metrics
    from src.utils import format_currency_br, format_integer_br, format_percent_br
except ModuleNotFoundError:  # pragma: no cover
    import metrics
    from utils import format_currency_br, format_integer_br, format_percent_br

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def metric_snapshot() -> dict[str, object]:
    return metrics.executive_summary_metrics(metrics.load_all())


def executive_analysis_text(snapshot: dict[str, object]) -> str:
    return f"""# Análise Executiva

## Veredito executivo
Os dados sugerem uma carteira SaaS B2B com {format_integer_br(snapshot['active_customers'])} clientes ativos, GRR de {format_percent_br(snapshot['grr'])}, NRR de {format_percent_br(snapshot['nrr'])}, {format_integer_br(snapshot['risk_customers'])} clientes em risco e {format_integer_br(snapshot['renewal_risk_customers'])} renovações próximas associadas a baixo health.

## Diagnóstico do período
A evidência disponível aponta para a necessidade de separar retenção bruta, expansão e risco de renovação. NRR pode esconder perda bruta quando expansão compensa churn ou contraction; por isso, a leitura executiva deve mostrar GRR, NRR e ponte de movimentos de receita no mesmo contexto.

## Resumo de métricas
- Clientes ativos: {format_integer_br(snapshot['active_customers'])}.
- MRR atual: {format_currency_br(snapshot['current_mrr'])}.
- GRR: {format_percent_br(snapshot['grr'])}.
- NRR: {format_percent_br(snapshot['nrr'])}.
- MRR perdido bruto: {format_currency_br(snapshot['gross_lost_mrr'])}.
- MRR de expansão realizado: {format_currency_br(snapshot['expansion_mrr'])}.
- Pipeline aberto de expansão: {format_currency_br(snapshot['expansion_pipeline_mrr'])}.
- Clientes em risco: {format_integer_br(snapshot['risk_customers'])}.
- Renovações em risco: {format_integer_br(snapshot['renewal_risk_customers'])}.
- Eventos de churn: {format_integer_br(snapshot['churn_events'])}.
- Health score médio: {snapshot['avg_health_score']:.1f}.
- NPS médio: {snapshot['avg_nps']:.1f}.
- Taxa de detratores: {format_percent_br(snapshot['detractor_rate'])}.
- Gaps de QBR: {format_integer_br(snapshot['qbr_quality_gaps'])}.
- Expansões sem next step: {format_integer_br(snapshot['expansion_without_next_step'])}.

## Principais achados
- Os dados sugerem que Customer Health precisa ser lido como governança de receita recorrente, não apenas como score operacional.
- Há indícios de risco em clientes com health baixo e renovações próximas, exigindo plano por conta.
- A evidência disponível aponta para risco de expansão mascarar perda bruta se GRR e NRR não forem reportados juntos.
- Oportunidades de upsell/cross-sell sem próximo passo precisam ser validadas antes de entrar como upside confiável.
- QBR e NPS devem alimentar priorização de carteira CSM e planos de retenção.

## Recomendações priorizadas
| Responsável | Ação | Métrica impactada | Acompanhamento | Prazo sugerido | Impacto esperado |
|---|---|---|---|---|---|
| Head de CS | Revisar renovações em risco com plano por conta | Renewal Risk | renewal_risk_customers | 5 dias úteis | Menor risco de churn evitável |
| CS Ops | Criar fila de intervenção por health, ARR e renovação | Customer Health | risk_customers | Semanal | Carteira CSM mais acionável |
| CRO | Reportar GRR, NRR e ponte de receita no mesmo painel | GRR/NRR | grr_nrr_bridge | Próximo business review | Menos leitura otimista de expansão |
| CSM Manager | Exigir next step datado em expansão qualificada | Expansion Pipeline | expansion_without_next_step | 48 horas | Upside mais confiável |
| CS Ops | Padronizar QBR com sponsor, plano e decisão | QBR Quality | qbr_quality_score | 30 dias | Melhor governança de valor |

## Limitações
Os dados são sintéticos e a análise é rule-based. As hipóteses precisam ser validadas com CSMs, Head de CS, Sales/CS Ops, clientes e dados reais de uso antes de qualquer conclusão causal.

## Conclusão executiva
A recomendação é priorizar uma rotina de Revenue Governance para Customer Success: proteger GRR, qualificar NRR, revisar renovações em risco e tratar expansão como hipótese operacional até existir evidência de avanço.
"""


def readme_text(snapshot: dict[str, object]) -> str:
    return f"""# Customer Health and Expansion Engine

## Executive Summary
Este projeto analisa uma operação SaaS B2B sintética para demonstrar como RevOps, CS Ops e liderança de Customer Success podem conectar Customer Health, churn risk, expansion, GRR, NRR, QBR, NPS, renewal risk e carteira CSM.

Os dados sugerem GRR de {format_percent_br(snapshot['grr'])}, NRR de {format_percent_br(snapshot['nrr'])}, {format_integer_br(snapshot['risk_customers'])} clientes em risco, {format_integer_br(snapshot['renewal_risk_customers'])} renovações em risco e {format_currency_br(snapshot['expansion_pipeline_mrr'])} em pipeline aberto de expansão.

## Business Problem
Times de Customer Success podem parecer saudáveis quando olham apenas NRR ou expansão, mas ainda assim perder receita bruta, contas estratégicas ou renovações relevantes. O problema de negócio é separar retenção, expansão, saúde da carteira, QBR, NPS e risco de renovação para orientar decisões de liderança.

## Why It Matters for RevOps
Customer Health é uma disciplina de Revenue Governance. GRR protege a base, NRR mede expansão líquida, QBR valida valor percebido, NPS indica voz do cliente e renewal risk mostra onde a liderança precisa agir antes do contrato vencer.

## Recommended Decisions
- Priorizar renovações próximas com baixo health score.
- Separar GRR e NRR para evitar expansão mascarando perda bruta.
- Exigir next step datado em upsell/cross-sell qualificado.
- Usar QBR e NPS como evidência de risco, não como métricas isoladas.
- Rebalancear foco CSM por risco, MRR e data de renovação.

## What This Project Includes
- Dados sintéticos de clientes, assinaturas, health scores, uso de produto, tickets, NPS, QBRs, expansão, churn e movimentos de receita.
- Métricas de GRR, NRR, churn risk, renewal risk, expansion pipeline e CSM portfolio.
- Consultor de gaps rule-based com evidência, hipótese, validação, owner e métrica de acompanhamento.
- IA consultora rule-based para análise executiva.
- Dashboard Streamlit em português do Brasil.

## Dashboard Preview
O dashboard fica em `app/streamlit_app.py` e cobre visão executiva, GRR/NRR, customer health, renewal risk, expansion pipeline, QBR/NPS, CSM portfolio e consultor de gaps.

Para registrar prova visual, use `docs/screenshots/`.

## How to Run
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/consultant_gap_finder.py
python src/ai_consultant.py
python src/data_quality.py
python src/reports.py
python -m compileall src app
python -m pytest
streamlit run app/streamlit_app.py
```

## Data Disclaimer
Nenhum dado real é usado. Todos os dados são sintéticos, determinísticos e criados para demonstrar raciocínio de RevOps/CS Ops.

## Limitations
A análise é rule-based, não usa ML nem APIs externas. Os achados são hipóteses para validação e não devem ser tratados como causa raiz confirmada.

## Tech Stack
Python, pandas, numpy, SQLite, Streamlit, Plotly e pytest.

## Consulting Use Case
Este projeto simula um diagnóstico consultivo para empresas SaaS B2B que precisam entender churn risk, renewal risk, expansão, GRR/NRR e governança de carteira CSM.

## Contact
LinkedIn: https://www.linkedin.com/in/gustavo-worliczek-lazzarotto/  
E-mail: gustavo.lazzaro77o@gmail.com
"""


def metrics_dictionary_text() -> str:
    return """# Metrics Dictionary

| Métrica | Definição | Interpretação | Decisão suportada | Limitação |
|---|---|---|---|---|
| GRR | Receita recorrente preservada antes de expansão | Mede retenção bruta | Priorizar contas e segmentos com perda bruta | Não explica causa de churn |
| NRR | Receita preservada mais expansão líquida | Mede crescimento líquido da base | Avaliar expansão e retenção juntas | Pode mascarar perda bruta |
| Expansion masking loss ratio | Expansão / perda bruta | Indica se expansão compensa churn/contraction | Separar leitura de expansão saudável e retenção | Precisa de bridge financeira validada |
| Risk customers | Clientes com health baixo ou risco alto | Mostra foco de intervenção CSM | Priorizar carteira por risco | Depende da regra de health score |
| Renewal risk customers | Renovações próximas com health baixo | Mostra risco temporal de contrato | Rodar renewal review | Não substitui contexto de negociação |
| Expansion pipeline MRR | MRR potencial em expansão aberta | Mostra upside de upsell/cross-sell | Qualificar pipeline de expansão | Não é receita realizada |
| QBR quality gaps | QBRs com baixa qualidade ou next step frágil | Mede governança de valor | Padronizar QBR e plano de sucesso | Qualidade é rule-based |
| Detractor rate | Respostas NPS até 6 / total | Sinaliza risco na voz do cliente | Acionar plano de resposta | Amostra sintética |
"""


def executive_memo_text(snapshot: dict[str, object]) -> str:
    return f"""# Executive Memo

## Problem
Os dados sugerem que a liderança precisa separar retenção bruta, expansão e risco de renovação para evitar decisões baseadas apenas em NRR.

## Evidence
- GRR: {format_percent_br(snapshot['grr'])}.
- NRR: {format_percent_br(snapshot['nrr'])}.
- Clientes em risco: {format_integer_br(snapshot['risk_customers'])}.
- Renovações em risco: {format_integer_br(snapshot['renewal_risk_customers'])}.
- Pipeline aberto de expansão: {format_currency_br(snapshot['expansion_pipeline_mrr'])}.
- MRR perdido bruto: {format_currency_br(snapshot['gross_lost_mrr'])}.

## Business Risk
Há indícios de que expansão pode mascarar perda bruta. Isso pode levar liderança a subpriorizar churn risk, renewal risk e planos de recuperação de valor.

## Recommended Decision
Reportar GRR, NRR e ponte de revenue movements juntos; priorizar renovações em risco e exigir next step datado para expansão qualificada.

## Owner
Head de CS, CS Ops, CSM Managers e CRO.

## Follow-up Metric
GRR, NRR, renewal_risk_customers, risk_customers, expansion_without_next_step e qbr_quality_score.

## What Is Missing
Motivos validados de churn, notas CSM, critérios reais de health score, plano de sucesso por conta e feedback qualitativo dos clientes.

## Final Recommendation
A evidência disponível aponta para uma rotina de Customer Revenue Governance com foco em retenção bruta, expansão qualificada e validação humana das hipóteses.
"""


def final_handoff_text() -> str:
    return """# Final Handoff Report

## Status
Projeto Customer Health and Expansion revisado para vitrine GitHub, com dados sintéticos, dashboard, métricas, consultor de gaps, IA consultora rule-based, documentação e testes.

## Specialist GitHub Readiness Review
- conteúdo alinhado a Customer Health, Churn Risk, Expansion, GRR, NRR, QBR, NPS e CSM portfolio: sim
- README revisado: sim
- análise executiva revisada: sim
- IA consultora revisada: sim
- consultor de gaps revisado: sim
- metrics dictionary revisado: sim
- executive memo criado: sim
- dashboard em português: sim
- dados reais, APIs externas ou ML: não
"""


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    snapshot = metric_snapshot()
    (DOCS / "executive_analysis.md").write_text(executive_analysis_text(snapshot), encoding="utf-8")
    (ROOT / "README.md").write_text(readme_text(snapshot), encoding="utf-8")
    (DOCS / "metrics_dictionary.md").write_text(metrics_dictionary_text(), encoding="utf-8")
    (DOCS / "executive_memo.md").write_text(executive_memo_text(snapshot), encoding="utf-8")
    (DOCS / "final_handoff_report.md").write_text(final_handoff_text(), encoding="utf-8")
    print("Customer Health reports generated.")


if __name__ == "__main__":
    main()
