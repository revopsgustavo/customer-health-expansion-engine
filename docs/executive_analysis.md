# Análise Executiva

## Veredito executivo
Os dados sugerem uma carteira SaaS B2B com 48 clientes ativos, GRR de 95,9%, NRR de 100,6%, 6 clientes em risco e 4 renovações próximas associadas a baixo health.

## Diagnóstico do período
A evidência disponível aponta para a necessidade de separar retenção bruta, expansão e risco de renovação. NRR pode esconder perda bruta quando expansão compensa churn ou contraction; por isso, a leitura executiva deve mostrar GRR, NRR e ponte de movimentos de receita no mesmo contexto.

## Resumo de métricas
- Clientes ativos: 48.
- MRR atual: R$ 1.563.140,00.
- GRR: 95,9%.
- NRR: 100,6%.
- MRR perdido bruto: R$ 66.300,00.
- MRR de expansão realizado: R$ 76.000,00.
- Pipeline aberto de expansão: R$ 204.000,00.
- Clientes em risco: 6.
- Renovações em risco: 4.
- Eventos de churn: 2.
- Health score médio: 76.7.
- NPS médio: 8.0.
- Taxa de detratores: 12,5%.
- Gaps de QBR: 6.
- Expansões sem next step: 3.

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
