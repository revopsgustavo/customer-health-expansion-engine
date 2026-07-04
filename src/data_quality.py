from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = PROCESSED / "data_quality_report.csv"

REQUIRED = {
    "customers": ["customer_id", "arr"],
    "subscriptions": ["subscription_id", "customer_id", "mrr", "status", "renewal_date"],
    "health_scores": ["customer_id", "health_score", "risk_level"],
    "product_usage": ["usage_id", "customer_id", "active_users", "licensed_users"],
    "support_tickets": ["ticket_id", "customer_id", "severity", "status"],
    "nps_surveys": ["survey_id", "customer_id", "nps_score"],
    "qbr_events": ["qbr_id", "customer_id", "qbr_date", "qbr_quality_score"],
    "expansion_opportunities": ["opportunity_id", "customer_id", "estimated_expansion_mrr", "stage"],
    "revenue_movements": ["movement_id", "customer_id", "movement_type", "mrr_amount"],
    "churn_events": ["churn_event_id", "customer_id", "churn_mrr"],
    "csms": ["csm_id", "csm_name"],
}


def blank(series: pd.Series) -> pd.Series:
    return series.isna() | series.astype(str).str.strip().eq("")


def read(name: str) -> pd.DataFrame:
    path = PROCESSED / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def validate() -> pd.DataFrame:
    rows = []
    tables = {name: read(name) for name in REQUIRED}
    customer_ids = set(tables["customers"].get("customer_id", pd.Series(dtype=str)).dropna())
    for name, columns in REQUIRED.items():
        path = PROCESSED / f"{name}.csv"
        df = tables[name]
        rows.append({"table": name, "check_name": "file_exists", "status": "pass" if path.exists() else "fail", "details": str(path)})
        for column in columns:
            exists = column in df.columns
            rows.append({"table": name, "check_name": f"column_exists:{column}", "status": "pass" if exists else "fail", "details": column})
            if exists and column.endswith("_id"):
                missing = int(blank(df[column]).sum())
                rows.append({"table": name, "check_name": f"id_not_null:{column}", "status": "pass" if missing == 0 else "fail", "details": f"missing={missing}"})
        if name != "customers" and "customer_id" in df.columns:
            invalid = sorted((set(df["customer_id"].dropna()) - customer_ids))
            rows.append({"table": name, "check_name": "valid_customer_id", "status": "pass" if not invalid else "fail", "details": ",".join(invalid[:10])})
    if "health_score" in tables["health_scores"]:
        score = pd.to_numeric(tables["health_scores"]["health_score"], errors="coerce")
        rows.append({"table": "health_scores", "check_name": "health_score_between_0_and_100", "status": "pass" if score.dropna().between(0, 100).all() else "fail", "details": "0-100"})
    if "nps_score" in tables["nps_surveys"]:
        nps = pd.to_numeric(tables["nps_surveys"]["nps_score"], errors="coerce")
        rows.append({"table": "nps_surveys", "check_name": "nps_between_0_and_10", "status": "pass" if nps.dropna().between(0, 10).all() else "fail", "details": "0-10"})
    return pd.DataFrame(rows)


def main() -> None:
    report = validate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT, index=False)
    print(f"Data quality report generated at {OUTPUT}. failed_checks={int(report.status.eq('fail').sum())}")


if __name__ == "__main__":
    main()
