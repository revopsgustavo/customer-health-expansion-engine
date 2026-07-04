from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import metrics
from src.utils import format_currency_br, format_integer_br, format_percent_br, has_columns, select_existing

PROCESSED = ROOT / "data" / "processed"
DOCS = ROOT / "docs"

st.set_page_config(page_title="Customer Health and Expansion", layout="wide")


@st.cache_data
def load_tables() -> dict[str, pd.DataFrame]:
    return metrics.load_all()


def read_table(name: str) -> pd.DataFrame:
    path = PROCESSED / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def markdown_doc(file_name: str) -> None:
    path = DOCS / file_name
    st.markdown(path.read_text(encoding="utf-8") if path.exists() else "Arquivo ainda não gerado. Rode a preparação do projeto.")


def safe_table(df: pd.DataFrame, columns: list[str] | None = None) -> None:
    if df.empty:
        st.warning("Dados insuficientes para exibir esta tabela.")
        return
    st.dataframe(select_existing(df, columns) if columns else df, use_container_width=True, hide_index=True)


def safe_bar(df: pd.DataFrame, x: str, y: str, title: str) -> None:
    if df.empty or not has_columns(df, [x, y]):
        st.warning("Dados insuficientes para exibir este gráfico.")
        return
    st.plotly_chart(px.bar(df, x=x, y=y, title=title), use_container_width=True)


def executive_reading(what: str, why: str, decision: str) -> None:
    st.info(f"**O que estamos vendo?** {what}\n\n**Por que importa?** {why}\n\n**Qual decisão isso suporta?** {decision}")


def overview(tables: dict[str, pd.DataFrame]) -> None:
    st.title("Customer Health and Expansion")
    st.caption("Case RevOps SaaS B2B: health score, churn risk, GRR, NRR, expansão, QBR, NPS e carteira CSM.")
    summary = metrics.executive_summary_metrics(tables)
    cols = st.columns(4)
    cols[0].metric("GRR", format_percent_br(summary["grr"]))
    cols[1].metric("NRR", format_percent_br(summary["nrr"]))
    cols[2].metric("Clientes em risco", format_integer_br(summary["risk_customers"]))
    cols[3].metric("Pipeline expansão", format_currency_br(summary["expansion_pipeline_mrr"]))
    executive_reading(
        "Retenção bruta, expansão e risco de renovação precisam ser lidos juntos.",
        "NRR pode parecer saudável enquanto perdas brutas continuam relevantes.",
        "Separar GRR, NRR e ponte de movimentos de receita antes de definir foco de CS.",
    )


def retention(tables: dict[str, pd.DataFrame]) -> None:
    st.title("GRR, NRR e Churn Risk")
    summary = metrics.executive_summary_metrics(tables)
    cols = st.columns(4)
    cols[0].metric("MRR atual", format_currency_br(summary["current_mrr"]))
    cols[1].metric("MRR perdido bruto", format_currency_br(summary["gross_lost_mrr"]))
    cols[2].metric("MRR expansão", format_currency_br(summary["expansion_mrr"]))
    cols[3].metric("Churn events", format_integer_br(summary["churn_events"]))
    executive_reading(
        "A ponte de receita mostra churn, contraction e expansion separadamente.",
        "Expansão pode mascarar perda bruta se GRR e NRR não forem reportados juntos.",
        "Priorizar contas com risco de renovação antes de celebrar expansão líquida.",
    )
    safe_table(tables["revenue_movements"])


def health(tables: dict[str, pd.DataFrame]) -> None:
    st.title("Customer Health")
    risk = metrics.health_risk_customers(tables["health_scores"])
    safe_bar(tables["health_scores"], "risk_level", "health_score", "Health score por nível de risco")
    safe_table(risk, ["customer_id", "health_score", "risk_level", "adoption_score", "critical_tickets", "nps_score", "days_since_last_qbr"])


def renewals(tables: dict[str, pd.DataFrame]) -> None:
    st.title("Renewal Risk")
    renewal_risk = metrics.renewal_risk(tables["subscriptions"], tables["health_scores"])
    executive_reading(
        "Renovações próximas com health score baixo exigem plano de conta.",
        "Risco de renovação conecta saúde, contrato e timing comercial.",
        "Rodar renewal review por conta com sponsor, plano de sucesso e próximo passo.",
    )
    safe_table(renewal_risk, ["customer_id", "plan", "mrr", "renewal_date", "health_score", "risk_level"])


def expansion(tables: dict[str, pd.DataFrame]) -> None:
    st.title("Expansion Pipeline")
    open_expansion = metrics.expansion_pipeline(tables["expansion_opportunities"])
    missing_next = metrics.expansion_without_next_step(tables["expansion_opportunities"])
    cols = st.columns(2)
    cols[0].metric("Pipeline aberto", format_currency_br(metrics.expansion_pipeline_mrr(tables["expansion_opportunities"])))
    cols[1].metric("Sem next step", format_integer_br(len(missing_next)))
    executive_reading(
        "Upsell e cross-sell precisam de next step datado e critério de qualificação.",
        "Pipeline de expansão sem avanço operacional pode inflar upside.",
        "Priorizar oportunidades por fit, health, sponsor e data de decisão.",
    )
    safe_table(open_expansion)


def qbr_nps(tables: dict[str, pd.DataFrame]) -> None:
    st.title("QBR e NPS")
    nps = metrics.nps_summary(tables["nps_surveys"])
    cols = st.columns(3)
    cols[0].metric("NPS médio", f"{nps['avg_nps']:.1f}")
    cols[1].metric("Detratores", format_percent_br(nps["detractor_rate"]))
    cols[2].metric("QBR gaps", format_integer_br(len(metrics.qbr_quality_gap(tables["qbr_events"]))))
    safe_table(metrics.qbr_quality_gap(tables["qbr_events"]))
    safe_table(tables["nps_surveys"])


def csm_portfolio(tables: dict[str, pd.DataFrame]) -> None:
    st.title("CSM Portfolio")
    portfolio = metrics.csm_portfolio(tables)
    executive_reading(
        "Carteira CSM deve ser lida por volume, risco e health médio.",
        "Balanceamento de carteira afeta retenção, expansão e qualidade de QBR.",
        "Rebalancear foco por risco e valor em vez de tratar contas como fila homogênea.",
    )
    safe_table(portfolio)
    safe_bar(portfolio, "owner", "risk_customers", "Clientes em risco por owner")


PAGES = {
    "Visão Executiva": overview,
    "GRR, NRR e Churn Risk": retention,
    "Customer Health": health,
    "Renewal Risk": renewals,
    "Expansion Pipeline": expansion,
    "QBR e NPS": qbr_nps,
    "CSM Portfolio": csm_portfolio,
    "Consultor de Gaps": lambda tables: (st.title("Consultor de Gaps"), safe_table(read_table("consultant_gap_log"))),
    "IA Consultora": lambda tables: (st.title("IA Consultora"), markdown_doc("ai_consultant_analysis.md")),
    "Análise Executiva": lambda tables: (st.title("Análise Executiva"), markdown_doc("executive_analysis.md")),
    "Executive Memo": lambda tables: (st.title("Executive Memo"), markdown_doc("executive_memo.md")),
}


def main() -> None:
    tables = load_tables()
    page = st.sidebar.radio("Menu", list(PAGES))
    PAGES[page](tables)


if __name__ == "__main__":
    main()
