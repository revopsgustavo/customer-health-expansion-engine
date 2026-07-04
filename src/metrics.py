from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from src.utils import safe_divide
except ModuleNotFoundError:  # pragma: no cover
    from utils import safe_divide

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TODAY = pd.Timestamp("2026-07-04")


def load_table(name: str, base_path: Path = PROCESSED) -> pd.DataFrame:
    path = base_path / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def load_all(base_path: Path = PROCESSED) -> dict[str, pd.DataFrame]:
    names = [
        "customers",
        "subscriptions",
        "health_scores",
        "product_usage",
        "support_tickets",
        "nps_surveys",
        "qbr_events",
        "expansion_opportunities",
        "revenue_movements",
        "churn_events",
        "csms",
    ]
    return {name: load_table(name, base_path) for name in names}


def active_subscriptions(subscriptions: pd.DataFrame) -> pd.DataFrame:
    if subscriptions.empty or "status" not in subscriptions:
        return subscriptions.iloc[0:0].copy()
    return subscriptions[subscriptions["status"].astype(str).str.lower().eq("active")].copy()


def current_mrr(subscriptions: pd.DataFrame) -> float:
    if subscriptions.empty or "mrr" not in subscriptions:
        return 0.0
    return float(pd.to_numeric(active_subscriptions(subscriptions)["mrr"], errors="coerce").fillna(0).sum())


def movement_mrr(revenue_movements: pd.DataFrame, movement_type: str) -> float:
    if revenue_movements.empty or not {"movement_type", "mrr_amount"}.issubset(revenue_movements.columns):
        return 0.0
    rows = revenue_movements[revenue_movements["movement_type"].astype(str).str.lower().eq(movement_type)]
    return float(pd.to_numeric(rows["mrr_amount"], errors="coerce").fillna(0).sum())


def grr(tables: dict[str, pd.DataFrame]) -> float:
    start_mrr = current_mrr(tables["subscriptions"]) + movement_mrr(tables["revenue_movements"], "churn") + movement_mrr(tables["revenue_movements"], "contraction")
    lost = movement_mrr(tables["revenue_movements"], "churn") + movement_mrr(tables["revenue_movements"], "contraction")
    return max(0.0, safe_divide(start_mrr - lost, start_mrr))


def nrr(tables: dict[str, pd.DataFrame]) -> float:
    start_mrr = current_mrr(tables["subscriptions"]) + movement_mrr(tables["revenue_movements"], "churn") + movement_mrr(tables["revenue_movements"], "contraction")
    lost = movement_mrr(tables["revenue_movements"], "churn") + movement_mrr(tables["revenue_movements"], "contraction")
    expansion = movement_mrr(tables["revenue_movements"], "expansion")
    return max(0.0, safe_divide(start_mrr - lost + expansion, start_mrr))


def expansion_masking_loss(tables: dict[str, pd.DataFrame]) -> float:
    lost = movement_mrr(tables["revenue_movements"], "churn") + movement_mrr(tables["revenue_movements"], "contraction")
    expansion = movement_mrr(tables["revenue_movements"], "expansion")
    return safe_divide(expansion, lost)


def health_risk_customers(health_scores: pd.DataFrame) -> pd.DataFrame:
    if health_scores.empty:
        return pd.DataFrame()
    score = pd.to_numeric(health_scores.get("health_score"), errors="coerce")
    risk = health_scores.get("risk_level", pd.Series("", index=health_scores.index)).astype(str).str.lower()
    return health_scores[(score < 65) | risk.isin(["high", "critical"])].copy()


def renewal_risk(subscriptions: pd.DataFrame, health_scores: pd.DataFrame, days: int = 120) -> pd.DataFrame:
    if subscriptions.empty or health_scores.empty or not {"customer_id", "renewal_date"}.issubset(subscriptions.columns):
        return pd.DataFrame()
    subs = active_subscriptions(subscriptions)
    subs["renewal_date"] = pd.to_datetime(subs["renewal_date"], errors="coerce")
    upcoming = subs[(subs["renewal_date"] >= TODAY) & (subs["renewal_date"] <= TODAY + pd.Timedelta(days=days))]
    risky = health_risk_customers(health_scores)[["customer_id", "health_score", "risk_level"]]
    return upcoming.merge(risky, on="customer_id", how="inner")


def expansion_pipeline(expansion_opportunities: pd.DataFrame) -> pd.DataFrame:
    if expansion_opportunities.empty:
        return pd.DataFrame()
    open_stages = {"identified", "qualified", "proposal", "negotiation"}
    return expansion_opportunities[expansion_opportunities["stage"].astype(str).str.lower().isin(open_stages)].copy()


def expansion_pipeline_mrr(expansion_opportunities: pd.DataFrame) -> float:
    open_expansion = expansion_pipeline(expansion_opportunities)
    if open_expansion.empty or "estimated_expansion_mrr" not in open_expansion:
        return 0.0
    return float(pd.to_numeric(open_expansion["estimated_expansion_mrr"], errors="coerce").fillna(0).sum())


def expansion_without_next_step(expansion_opportunities: pd.DataFrame) -> pd.DataFrame:
    open_expansion = expansion_pipeline(expansion_opportunities)
    if open_expansion.empty or "next_step" not in open_expansion:
        return pd.DataFrame()
    return open_expansion[open_expansion["next_step"].isna() | open_expansion["next_step"].astype(str).str.strip().eq("")].copy()


def stale_qbrs(qbr_events: pd.DataFrame, days: int = 90) -> pd.DataFrame:
    if qbr_events.empty or not {"customer_id", "qbr_date"}.issubset(qbr_events.columns):
        return pd.DataFrame()
    latest = qbr_events.copy()
    latest["qbr_date"] = pd.to_datetime(latest["qbr_date"], errors="coerce")
    latest = latest.sort_values("qbr_date").groupby("customer_id", as_index=False).tail(1)
    return latest[(TODAY - latest["qbr_date"]).dt.days > days].copy()


def qbr_quality_gap(qbr_events: pd.DataFrame) -> pd.DataFrame:
    if qbr_events.empty or "qbr_quality_score" not in qbr_events:
        return pd.DataFrame()
    score = pd.to_numeric(qbr_events["qbr_quality_score"], errors="coerce")
    missing_next = qbr_events.get("next_steps_recorded", pd.Series(True, index=qbr_events.index)).astype(str).str.lower().isin(["false", "0", ""])
    return qbr_events[(score < 70) | missing_next].copy()


def nps_summary(nps_surveys: pd.DataFrame) -> dict[str, float]:
    if nps_surveys.empty or "nps_score" not in nps_surveys:
        return {"avg_nps": 0.0, "detractor_rate": 0.0}
    score = pd.to_numeric(nps_surveys["nps_score"], errors="coerce")
    return {"avg_nps": float(score.mean()), "detractor_rate": safe_divide(int((score <= 6).sum()), len(score))}


def critical_ticket_customers(support_tickets: pd.DataFrame) -> pd.DataFrame:
    if support_tickets.empty or not {"customer_id", "severity", "status"}.issubset(support_tickets.columns):
        return pd.DataFrame()
    open_status = ~support_tickets["status"].astype(str).str.lower().isin(["closed", "resolved"])
    critical = support_tickets["severity"].astype(str).str.lower().isin(["critical", "high"])
    return support_tickets[open_status & critical].copy()


def csm_portfolio(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    health = tables["health_scores"].copy()
    expansion = tables["expansion_opportunities"].copy()
    if health.empty:
        return pd.DataFrame()
    if "owner" in expansion:
        owner_map = expansion.groupby("customer_id", as_index=False).agg(owner=("owner", "first"))
        health = health.merge(owner_map, on="customer_id", how="left")
    if "owner" not in health:
        health["owner"] = "unassigned"
    risk = health_risk_customers(health)
    rows = []
    for owner, group in health.fillna({"owner": "unassigned"}).groupby("owner"):
        rows.append(
            {
                "owner": owner,
                "customers": len(group),
                "risk_customers": int(group["customer_id"].isin(risk["customer_id"]).sum()),
                "avg_health_score": float(pd.to_numeric(group["health_score"], errors="coerce").mean()),
            }
        )
    return pd.DataFrame(rows)


def executive_summary_metrics(tables: dict[str, pd.DataFrame]) -> dict[str, float]:
    health = tables["health_scores"]
    churn = tables["churn_events"]
    expansion = tables["expansion_opportunities"]
    subscriptions = tables["subscriptions"]
    nps = nps_summary(tables["nps_surveys"])
    revenue_movements = tables["revenue_movements"]
    gross_lost = movement_mrr(revenue_movements, "churn") + movement_mrr(revenue_movements, "contraction")
    return {
        "active_customers": int(active_subscriptions(subscriptions)["customer_id"].nunique()) if not subscriptions.empty else 0,
        "current_mrr": current_mrr(subscriptions),
        "grr": grr(tables),
        "nrr": nrr(tables),
        "gross_lost_mrr": gross_lost,
        "expansion_mrr": movement_mrr(revenue_movements, "expansion"),
        "expansion_pipeline_mrr": expansion_pipeline_mrr(expansion),
        "expansion_masking_loss_ratio": expansion_masking_loss(tables),
        "risk_customers": len(health_risk_customers(health)),
        "renewal_risk_customers": len(renewal_risk(subscriptions, health)),
        "churn_events": len(churn),
        "avg_health_score": float(pd.to_numeric(health["health_score"], errors="coerce").mean()) if not health.empty else 0.0,
        "avg_nps": nps["avg_nps"],
        "detractor_rate": nps["detractor_rate"],
        "qbr_quality_gaps": len(qbr_quality_gap(tables["qbr_events"])),
        "expansion_without_next_step": len(expansion_without_next_step(expansion)),
        "critical_ticket_customers": critical_ticket_customers(tables["support_tickets"])["customer_id"].nunique()
        if not tables["support_tickets"].empty
        else 0,
    }
