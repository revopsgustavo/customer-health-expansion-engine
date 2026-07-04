from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from src import metrics
except ModuleNotFoundError:  # pragma: no cover
    import metrics

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "processed" / "consultant_gap_log.csv"


def gap(gap_id: str, area: str, metric: str, actual, expected: str, severity: str, evidence: str, action: str, owner: str, follow: str) -> dict:
    return {
        "gap_id": gap_id,
        "area": area,
        "metric": metric,
        "actual_value": actual,
        "expected_value": expected,
        "severity": severity,
        "evidence": evidence,
        "probable_cause": "Hipótese provável: os dados sugerem fragilidade operacional ou de governança; precisa ser validado antes de confirmar causa raiz.",
        "missing_evidence": "Segmentação real da carteira, notas CSM, critérios de health score, motivo validado de churn, plano de sucesso e contexto de renovação.",
        "validation_questions": "O risco observado vem de adoção, valor percebido, suporte, sponsor, uso do produto, contrato, preço ou execução CSM?",
        "recommended_action": action,
        "owner": owner,
        "urgency": "immediate" if severity == "critical" else "this_week" if severity == "high" else "this_month",
        "expected_impact": "Proteger GRR, qualificar NRR, priorizar carteira CSM e separar expansão saudável de perda bruta mascarada.",
        "follow_up_metric": follow,
        "status": "open",
    }


def find_gaps(tables: dict[str, pd.DataFrame] | None = None) -> pd.DataFrame:
    tables = tables or metrics.load_all()
    summary = metrics.executive_summary_metrics(tables)
    rows = []
    if summary["grr"] < 0.9:
        rows.append(gap("gap_low_grr", "retention", "grr", round(summary["grr"], 3), ">= 0.90", "critical", f"Os dados sugerem GRR de {summary['grr']:.1%}.", "Priorizar plano de retenção para contas em risco antes de discutir expansão líquida.", "Head de CS", "grr"))
    if summary["nrr"] > 1 and summary["gross_lost_mrr"] > 0:
        rows.append(gap("gap_expansion_masking_loss", "revenue_governance", "expansion_masking_loss_ratio", round(summary["expansion_masking_loss_ratio"], 2), "< 1.00", "high", "Há indícios de que expansão pode estar compensando perda bruta de receita.", "Reportar GRR e NRR lado a lado e revisar contas com churn/contraction.", "CRO e Head de CS", "grr_nrr_bridge"))
    if summary["risk_customers"] > 0:
        rows.append(gap("gap_health_risk_customers", "customer_health", "risk_customers", summary["risk_customers"], "0", "high", f"A evidência disponível aponta para {summary['risk_customers']} clientes com health score baixo ou risco alto.", "Criar fila CSM de intervenção por risco, valor e data de renovação.", "CS Ops", "risk_customers"))
    if summary["renewal_risk_customers"] > 0:
        rows.append(gap("gap_renewal_risk", "renewal_governance", "renewal_risk_customers", summary["renewal_risk_customers"], "0", "critical", f"Há {summary['renewal_risk_customers']} renovações próximas associadas a baixo health.", "Rodar renewal review com plano de ação por conta e sponsor executivo.", "Head de CS", "renewal_risk_customers"))
    if summary["expansion_without_next_step"] > 0:
        rows.append(gap("gap_expansion_without_next_step", "expansion", "expansion_without_next_step", summary["expansion_without_next_step"], "0", "high", f"Há {summary['expansion_without_next_step']} oportunidades de expansão sem próximo passo.", "Exigir next step datado e critério de qualificação para upsell/cross-sell.", "CSM Manager", "expansion_without_next_step"))
    if summary["qbr_quality_gaps"] > 0:
        rows.append(gap("gap_qbr_quality", "qbr_governance", "qbr_quality_gaps", summary["qbr_quality_gaps"], "0", "medium", f"Os dados sugerem {summary['qbr_quality_gaps']} QBRs com baixa qualidade ou próximo passo frágil.", "Padronizar QBR com plano de sucesso, sponsor e decisões registradas.", "CS Ops", "qbr_quality_score"))
    if summary["detractor_rate"] > 0.15:
        rows.append(gap("gap_nps_detractors", "customer_voice", "detractor_rate", round(summary["detractor_rate"], 3), "<= 0.15", "high", f"A evidência disponível aponta para detratores em {summary['detractor_rate']:.1%} das respostas NPS.", "Validar temas de detratores e conectar plano de resposta a renovação.", "Head de CS", "detractor_rate"))
    if summary["critical_ticket_customers"] > 0:
        rows.append(gap("gap_critical_support_tickets", "support_risk", "critical_ticket_customers", summary["critical_ticket_customers"], "0", "high", f"Há indícios de {summary['critical_ticket_customers']} clientes com tickets críticos abertos.", "Escalar tickets críticos ligados a contas em renovação ou alto ARR.", "Support Manager", "critical_ticket_customers"))
    return pd.DataFrame(rows)


def main() -> None:
    gaps = find_gaps()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    gaps.to_csv(OUTPUT, index=False)
    print(f"Consultant gap log generated at {OUTPUT} with {len(gaps)} gaps")


if __name__ == "__main__":
    main()
