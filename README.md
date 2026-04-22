# 💰 Financial Priorities Nexus

> Sistema inteligente de identificação e priorização de tarefas financeiras lucrativas — Gerido pelo Cérebro Nexus.

## 📋 Descrição

Este projeto contém um motor de priorização financeira que analisa oportunidades de investimento e tarefas financeiras com base em múltiplos critérios:

- **Potencial de Lucro** — Retorno esperado em valor absoluto
- **Urgência** — Escala de 1 a 10 para criticidade temporal
- **Recursos Necessários** — Capital, tempo ou mão-de-obra requeridos
- **Dados de Mercado** — Tendência, volatilidade e taxa de crescimento do setor
- **Dependências** — Tarefas que precisam ser concluídas antes
- **Tolerância ao Risco** — Configurável de 0.0 (conservador) a 1.0 (agressivo)

## 🧠 Algoritmo

O sistema utiliza uma abordagem **Greedy ponderada** com as seguintes fórmulas:

1. **Ajuste de Mercado** = `trend_multiplier × (1 + sector_growth_rate) × (1 - volatility_penalty)`
2. **Fator de Urgência** = `1 + (urgency / 10)²`
3. **ROI Base** = `(profit × market_adj × urgency_factor) / resources`
4. **Score Final** = ROI ponderado por pesos estratégicos de urgência, mercado e eficiência de recursos

## 🚀 Utilização

```python
from financial_prioritizer import FinancialPrioritizer, FinancialTask, MarketData

# Definir dados de mercado
market = MarketData(trend_multiplier=1.2, volatility_index=0.3, sector_growth_rate=0.05)

# Criar tarefas
tasks = [
    FinancialTask(task_id="T1", name="Projeto Alpha", profit_potential=50000, urgency=8, resources_required=15000, market_data=market)
]

# Priorizar
prioritizer = FinancialPrioritizer(risk_tolerance=0.5)
plan = prioritizer.prioritize_tasks(tasks, available_resources=30000)
```

## 📁 Estrutura

```
financial_priorities_nexus/
├── financial_prioritizer.py   # Motor principal de priorização
└── README.md                  # Documentação
```

## 🔧 Requisitos

- Python 3.10+
- Sem dependências externas (usa apenas stdlib)

## 📊 Próximos Passos

- [ ] Integração com APIs de dados de mercado em tempo real
- [ ] Dashboard web para visualização de prioridades
- [ ] Persistência de histórico de decisões
- [ ] Integração com memória vetorial do Nexus para aprendizagem contínua

---

*Gerado automaticamente pelo Cérebro Nexus — Sistema de Gestão Financeira Autónoma*
