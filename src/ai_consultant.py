from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from src import metrics
    from src.utils import format_currency_br, format_percent_br
except ModuleNotFoundError:  # pragma: no cover
    import metrics
    from utils import format_currency_br, format_percent_br

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DOCS = ROOT / "docs"
OUTPUT = DOCS / "ai_consultant_analysis.md"


def severity_block(gaps: pd.DataFrame, severity: str) -> str:
    subset = gaps[gaps["severity"].eq(severity)] if "severity" in gaps else pd.DataFrame()
    if subset.empty:
        return "- Nenhum gap nesta severidade.\n"
    return "\n".join(f"- **{row.area} | {row.metric}**: {row.evidence} Ação recomendada: {row.recommended_action}" for row in subset.itertuples()) + "\n"


def build_analysis(gaps: pd.DataFrame, summary: dict[str, float]) -> str:
    critical = int(gaps.get("severity", pd.Series(dtype=str)).eq("critical").sum())
    high = int(gaps.get("severity", pd.Series(dtype=str)).eq("high").sum())
    return f"""# AI Consultant Analysis

## Veredito executivo
Os dados sugerem uma operação de Customer Success com sinais combinados de risco de retenção, oportunidade de expansão e necessidade de governança de carteira. O GRR está em {format_percent_br(summary['grr'])}, o NRR em {format_percent_br(summary['nrr'])}, há {summary['risk_customers']} clientes em risco e {summary['renewal_risk_customers']} renovações próximas associadas a baixo health. A análise é rule-based, usa dados sintéticos e gera hipóteses para validação humana.

## Leitura da operação
A evidência disponível aponta para um ponto central: expansão e NRR não devem ser lidos isoladamente. Quando existe perda bruta de MRR, expansão pode mascarar fragilidade de retenção. RevOps, CS Ops e liderança de Customer Success devem separar GRR, NRR, churn, contraction, expansion, QBR, NPS e risco de renovação antes de tomar decisões de carteira.

## Principais gaps
### Críticos
{severity_block(gaps, "critical")}
### Altos
{severity_block(gaps, "high")}
### Médios
{severity_block(gaps, "medium")}

## Hipóteses prováveis
- Os dados sugerem que parte do risco de churn pode estar ligada a adoção, tickets críticos, baixa cadência de QBR ou ausência de sponsor ativo.
- Há indícios de que oportunidades de expansão sem próximo passo podem inflar upside sem avanço operacional real.
- A evidência disponível aponta para necessidade de reportar GRR e NRR em ponte, para evitar leitura excessivamente positiva da expansão.
- Renovações próximas com health baixo precisam ser validadas com plano de sucesso, notas do CSM e contexto contratual.

## Evidências observadas
- Clientes ativos: {summary['active_customers']}.
- MRR atual: {format_currency_br(summary['current_mrr'])}.
- GRR: {format_percent_br(summary['grr'])}.
- NRR: {format_percent_br(summary['nrr'])}.
- MRR perdido bruto: {format_currency_br(summary['gross_lost_mrr'])}.
- MRR de expansão realizado: {format_currency_br(summary['expansion_mrr'])}.
- Pipeline aberto de expansão: {format_currency_br(summary['expansion_pipeline_mrr'])}.
- Clientes em risco: {summary['risk_customers']}.
- Renovações em risco: {summary['renewal_risk_customers']}.
- NPS médio: {summary['avg_nps']:.1f}.
- Taxa de detratores: {format_percent_br(summary['detractor_rate'])}.

## Evidências ausentes
- Motivos validados de churn e contraction por conta.
- Histórico real de uso por persona, módulo e valor contratado.
- Notas qualitativas dos CSMs e sponsors executivos.
- Critérios formais de health score e ponderação por ARR.
- Plano de sucesso atualizado por conta e data da próxima decisão de renovação.

## Recomendações priorizadas
- Responsável: Head de CS. Ação: revisar renovações em risco com plano por conta. Métrica: renewal_risk_customers.
- Responsável: CS Ops. Ação: criar fila de intervenção por health score, ARR e data de renovação. Métrica: risk_customers.
- Responsável: CRO. Ação: reportar GRR, NRR e ponte de revenue movements no mesmo painel. Métrica: grr_nrr_bridge.
- Responsável: CSM Manager. Ação: exigir next step datado em expansão qualificada. Métrica: expansion_without_next_step.

## Conclusão executiva
A recomendação é tratar Customer Health como governança de receita recorrente, não como painel isolado de satisfação. Os dados sugerem onde priorizar retenção, expansão e renovação, mas as hipóteses precisam ser validadas com contexto de conta antes de qualquer conclusão de causa raiz.
"""


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    gaps_path = PROCESSED / "consultant_gap_log.csv"
    gaps = pd.read_csv(gaps_path) if gaps_path.exists() else pd.DataFrame()
    OUTPUT.write_text(build_analysis(gaps, metrics.executive_summary_metrics(metrics.load_all())), encoding="utf-8")
    print(f"AI consultant analysis generated at {OUTPUT}")


if __name__ == "__main__":
    main()
