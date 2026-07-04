# Customer Health and Expansion Engine

## Executive Summary
Este projeto analisa uma operação SaaS B2B sintética para demonstrar como RevOps, CS Ops e liderança de Customer Success podem conectar Customer Health, churn risk, expansion, GRR, NRR, QBR, NPS, renewal risk e carteira CSM.

Os dados sugerem GRR de 95,9%, NRR de 100,6%, 6 clientes em risco, 4 renovações em risco e R$ 204.000,00 em pipeline aberto de expansão.

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
