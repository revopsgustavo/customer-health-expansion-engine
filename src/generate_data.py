from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DATABASE = ROOT / "data" / "database"
TODAY = pd.Timestamp("2026-07-04")


def d(days: int) -> str:
    return (TODAY - pd.Timedelta(days=days)).strftime("%Y-%m-%d")


def f(days: int) -> str:
    return (TODAY + pd.Timedelta(days=days)).strftime("%Y-%m-%d")


def main() -> None:
    rng = np.random.default_rng(42)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    DATABASE.mkdir(parents=True, exist_ok=True)

    csms = pd.DataFrame(
        [
            ["csm_001", "Ana Martins", "Enterprise"],
            ["csm_002", "Bruno Rocha", "Enterprise"],
            ["csm_003", "Carla Lima", "Mid Market"],
            ["csm_004", "Diego Alves", "SMB"],
        ],
        columns=["csm_id", "csm_name", "primary_segment"],
    )

    customers = []
    subscriptions = []
    health_scores = []
    product_usage = []
    support_tickets = []
    nps_surveys = []
    qbr_events = []
    expansion_opportunities = []
    revenue_movements = []
    churn_events = []

    for i in range(1, 49):
        customer_id = f"cus_{i:03d}"
        csm_id = csms.iloc[i % len(csms)]["csm_id"]
        segment = ["Enterprise", "Mid Market", "SMB"][i % 3]
        base_mrr = float([59000, 28000, 9200][i % 3] + rng.integers(-2200, 2600))
        risk_level = "high" if i in {3, 8, 15, 22, 31, 40} else "medium" if i % 5 == 0 else "low"
        adoption = 46.0 if risk_level == "high" else 66.0 if risk_level == "medium" else 84.0
        nps = 4 if risk_level == "high" else 7 if risk_level == "medium" else int(rng.integers(8, 11))
        health = max(15.0, min(98.0, adoption * 0.65 + nps * 3.5 - (10 if risk_level == "high" else 0)))

        customers.append(
            {
                "customer_id": customer_id,
                "account_name": f"Customer {i:03d}",
                "segment": segment,
                "csm_id": csm_id,
                "acquisition_date": d(360 - i),
                "arr": base_mrr * 12,
                "gross_margin": 0.78,
            }
        )
        subscriptions.append(
            {
                "subscription_id": f"sub_{customer_id}",
                "customer_id": customer_id,
                "plan": segment,
                "mrr": base_mrr,
                "status": "active",
                "contract_start_date": d(365),
                "renewal_date": f(30 + (i * 7) % 210),
                "billing_cycle": "annual",
            }
        )
        health_scores.append(
            {
                "customer_id": customer_id,
                "health_date": d(4),
                "health_score": round(health, 1),
                "risk_level": risk_level,
                "adoption_score": adoption,
                "critical_tickets": 1 if risk_level == "high" and i % 2 == 0 else 0,
                "nps_score": nps,
                "days_since_last_qbr": 115 if risk_level == "high" else 48,
            }
        )
        for week in range(4):
            licensed = int(30 + i % 25)
            active = int(licensed * (adoption / 100))
            product_usage.append(
                {
                    "usage_id": f"use_{customer_id}_{week}",
                    "customer_id": customer_id,
                    "week_start_date": d(7 * (week + 1)),
                    "active_users": active,
                    "licensed_users": licensed,
                    "key_feature_events": int(active * 28),
                    "login_count": int(active * 12),
                    "adoption_score": adoption,
                }
            )
        support_tickets.append(
            {
                "ticket_id": f"tic_{customer_id}",
                "customer_id": customer_id,
                "created_date": d(18),
                "closed_date": "" if risk_level == "high" else d(8),
                "severity": "critical" if risk_level == "high" and i % 2 == 0 else "medium",
                "status": "open" if risk_level == "high" else "closed",
                "category": "bug",
                "first_response_hours": 18.0 if risk_level == "high" else 4.0,
            }
        )
        nps_surveys.append(
            {
                "survey_id": f"nps_{customer_id}",
                "customer_id": customer_id,
                "survey_date": d(19),
                "nps_score": nps,
                "respondent_role": "executive_sponsor",
                "comment_theme": "synthetic_theme",
            }
        )
        qbr_events.append(
            {
                "qbr_id": f"qbr_{customer_id}",
                "customer_id": customer_id,
                "qbr_date": d(120 if risk_level == "high" else 45),
                "executive_sponsor_present": risk_level != "high",
                "success_plan_updated": risk_level != "high",
                "next_steps_recorded": risk_level != "high",
                "qbr_quality_score": 52 if risk_level == "high" else 78,
            }
        )
        if i % 4 == 0:
            expansion_opportunities.append(
                {
                    "opportunity_id": f"exp_{i:03d}",
                    "customer_id": customer_id,
                    "created_date": d(25),
                    "expansion_type": "new_module" if i % 8 == 0 else "seat_growth",
                    "estimated_expansion_mrr": float(8000 + (i % 6) * 4500),
                    "stage": "qualified",
                    "probability": 0.55,
                    "next_step": "" if i in {8, 16, 32} else f(10),
                    "owner": csm_id,
                }
            )

    for movement_id, customer_id, movement_type, amount, reason in [
        ("mov_001", "cus_003", "churn", 54000.0, "lost_value"),
        ("mov_002", "cus_027", "churn", 3300.0, "lost_logo"),
        ("mov_003", "cus_015", "contraction", 9000.0, "seat_reduction"),
        ("mov_004", "cus_008", "expansion", 36000.0, "new_module"),
        ("mov_005", "cus_024", "expansion", 22000.0, "seat_growth"),
        ("mov_006", "cus_032", "expansion", 18000.0, "cross_sell"),
    ]:
        revenue_movements.append(
            {
                "movement_id": movement_id,
                "customer_id": customer_id,
                "movement_date": d(30),
                "movement_type": movement_type,
                "mrr_amount": amount,
                "reason": reason,
                "source": "synthetic",
            }
        )
        if movement_type == "churn":
            churn_events.append(
                {
                    "churn_event_id": movement_id.replace("mov", "chr"),
                    "customer_id": customer_id,
                    "churn_date": d(30),
                    "churn_mrr": amount,
                    "churn_reason": "not_validated",
                    "save_playbook_used": customer_id != "cus_003",
                }
            )

    tables = {
        "customers": pd.DataFrame(customers),
        "subscriptions": pd.DataFrame(subscriptions),
        "health_scores": pd.DataFrame(health_scores),
        "product_usage": pd.DataFrame(product_usage),
        "support_tickets": pd.DataFrame(support_tickets),
        "nps_surveys": pd.DataFrame(nps_surveys),
        "qbr_events": pd.DataFrame(qbr_events),
        "expansion_opportunities": pd.DataFrame(expansion_opportunities),
        "revenue_movements": pd.DataFrame(revenue_movements),
        "churn_events": pd.DataFrame(churn_events),
        "csms": csms,
    }
    for name, table in tables.items():
        table.to_csv(PROCESSED / f"{name}.csv", index=False)
    with sqlite3.connect(DATABASE / "customer_health_expansion_case.sqlite") as conn:
        for name, table in tables.items():
            table.to_sql(name, conn, if_exists="replace", index=False)
    print(f"Synthetic customer health and expansion data generated in {PROCESSED}")


if __name__ == "__main__":
    main()
