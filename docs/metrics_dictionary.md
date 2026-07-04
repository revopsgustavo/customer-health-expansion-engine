# Metrics Dictionary

| Métrica | Definição | Interpretação | Decisão suportada | Limitação |
|---|---|---|---|---|
| GRR | Receita recorrente preservada antes de expansão | Mede retenção bruta | Priorizar contas e segmentos com perda bruta | Não explica causa de churn |
| NRR | Receita preservada mais expansão líquida | Mede crescimento líquido da base | Avaliar expansão e retenção juntas | Pode mascarar perda bruta |
| Expansion masking loss ratio | Expansão / perda bruta | Indica se expansão compensa churn/contraction | Separar leitura de expansão saudável e retenção | Precisa de bridge financeira validada |
| Risk customers | Clientes com health baixo ou risco alto | Mostra foco de intervenção CSM | Priorizar carteira por risco | Depende da regra de health score |
| Renewal risk customers | Renovações próximas com health baixo | Mostra risco temporal de contrato | Rodar renewal review | Não substitui contexto de negociação |
| Expansion pipeline MRR | MRR potencial em expansão aberta | Mostra upside de upsell/cross-sell | Qualificar pipeline de expansão | Não é receita realizada |
| QBR quality gaps | QBRs com baixa qualidade ou next step frágil | Mede governança de valor | Padronizar QBR e plano de sucesso | Qualidade é rule-based |
| Detractor rate | Respostas NPS até 6 / total | Sinaliza risco na voz do cliente | Acionar plano de resposta | Amostra sintética |
