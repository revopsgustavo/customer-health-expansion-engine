from __future__ import annotations

from src import metrics


def test_customer_health_metrics_do_not_error_and_stay_in_range():
    tables = metrics.load_all()
    summary = metrics.executive_summary_metrics(tables)
    assert summary["active_customers"] >= 1
    assert 0 <= summary["grr"] <= 2
    assert 0 <= summary["nrr"] <= 2
    assert summary["current_mrr"] >= 0
    assert summary["gross_lost_mrr"] >= 0
    assert summary["expansion_pipeline_mrr"] >= 0
    assert summary["risk_customers"] >= 0
    assert 0 <= summary["detractor_rate"] <= 1
