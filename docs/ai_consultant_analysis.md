# AI Consultant Analysis

## Veredito executivo
Os dados sugerem uma operação de Customer Success com sinais combinados de risco de retenção, oportunidade de expansão e necessidade de governança de carteira. O GRR está em 95,9%, o NRR em 100,6%, há 6 clientes em risco e 4 renovações próximas associadas a baixo health. A análise é rule-based, usa dados sintéticos e gera hipóteses para validação humana.

## Leitura da operação
A evidência disponível aponta para um ponto central: expansão e NRR não devem ser lidos isoladamente. Quando existe perda bruta de MRR, expansão pode mascarar fragilidade de retenção. RevOps, CS Ops e liderança de Customer Success devem separar GRR, NRR, churn, contraction, expansion, QBR, NPS e risco de renovação antes de tomar decisões de carteira.

## Principais gaps
### Críticos
- **renewal_governance | renewal_risk_customers**: Há 4 renovações próximas associadas a baixo health. Ação recomendada: Rodar renewal review com plano de ação por conta e sponsor executivo.

### Altos
- **revenue_governance | expansion_masking_loss_ratio**: Há indícios de que expansão pode estar compensando perda bruta de receita. Ação recomendada: Reportar GRR e NRR lado a lado e revisar contas com churn/contraction.
- **customer_health | risk_customers**: A evidência disponível aponta para 6 clientes com health score baixo ou risco alto. Ação recomendada: Criar fila CSM de intervenção por risco, valor e data de renovação.
- **expansion | expansion_without_next_step**: Há 3 oportunidades de expansão sem próximo passo. Ação recomendada: Exigir next step datado e critério de qualificação para upsell/cross-sell.
- **support_risk | critical_ticket_customers**: Há indícios de 3 clientes com tickets críticos abertos. Ação recomendada: Escalar tickets críticos ligados a contas em renovação ou alto ARR.

### Médios
- **qbr_governance | qbr_quality_gaps**: Os dados sugerem 6 QBRs com baixa qualidade ou próximo passo frágil. Ação recomendada: Padronizar QBR com plano de sucesso, sponsor e decisões registradas.


## Hipóteses prováveis
- Os dados sugerem que parte do risco de churn pode estar ligada a adoção, tickets críticos, baixa cadência de QBR ou ausência de sponsor ativo.
- Há indícios de que oportunidades de expansão sem próximo passo podem inflar upside sem avanço operacional real.
- A evidência disponível aponta para necessidade de reportar GRR e NRR em ponte, para evitar leitura excessivamente positiva da expansão.
- Renovações próximas com health baixo precisam ser validadas com plano de sucesso, notas do CSM e contexto contratual.

## Evidências observadas
- Clientes ativos: 48.
- MRR atual: R$ 1.563.140,00.
- GRR: 95,9%.
- NRR: 100,6%.
- MRR perdido bruto: R$ 66.300,00.
- MRR de expansão realizado: R$ 76.000,00.
- Pipeline aberto de expansão: R$ 204.000,00.
- Clientes em risco: 6.
- Renovações em risco: 4.
- NPS médio: 8.0.
- Taxa de detratores: 12,5%.

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
