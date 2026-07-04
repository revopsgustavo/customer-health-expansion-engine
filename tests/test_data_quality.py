from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def test_main_customer_success_files_exist():
    for name in [
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
    ]:
        assert (PROCESSED / f"{name}.csv").exists()


def test_required_customer_success_columns_and_ids_not_null():
    required = {
        "customers": ["customer_id", "arr"],
        "subscriptions": ["subscription_id", "customer_id", "mrr", "status", "renewal_date"],
        "health_scores": ["customer_id", "health_score", "risk_level"],
        "expansion_opportunities": ["opportunity_id", "customer_id", "estimated_expansion_mrr", "stage", "next_step"],
        "revenue_movements": ["movement_id", "customer_id", "movement_type", "mrr_amount"],
        "qbr_events": ["qbr_id", "customer_id", "qbr_date", "qbr_quality_score"],
        "nps_surveys": ["survey_id", "customer_id", "nps_score"],
    }
    for table, columns in required.items():
        df = pd.read_csv(PROCESSED / f"{table}.csv")
        for column in columns:
            assert column in df.columns
        assert df[columns[0]].notna().all()
