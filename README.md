# Aderência à dieta: SQL, dashboard e modelo preditivo

> Projeto de portfólio com **dados sintéticos** (gerados por `gerar_dados.py`). Os números abaixo refletem o comportamento simulado, não dados reais de pessoas.

## Pergunta de negócio
Em quais situações (tipo de refeição, comer fora, sono, horário) uma pessoa tende a sair da dieta, e dá para **prever antes da refeição** se ela ficará dentro do plano?

## Dados
- 720 refeições (180 dias × 4 refeições), tabela `refeicoes` em SQLite (`dieta.db`) e `refeicoes.csv`.
- Colunas: data, dia da semana, tipo de refeição, hora, comeu fora, horas de sono, calorias, proteína e `dentro_da_dieta` (1 se as calorias ≤ limite da refeição).
- **[Troque por: como você pretende usar os dados reais do seu app, com anonimização.]**

## Método
1. **SQL** (`consultas.sql`): aderência por tipo de refeição, comer fora x casa, média móvel semanal (window function) e dias perfeitos.
2. **Dashboard** (`app.py`, Streamlit): KPIs e gráficos alimentados pelas consultas SQL.
3. **Modelo** (`treinar_modelo.py`): Regressão Logística e Random Forest comparados a um baseline. As calorias foram **excluídas das variáveis** para evitar *data leakage*, já que definem o rótulo. A divisão treino/teste é **temporal** (80% iniciais para treino, 20% finais para teste).

## Resultados
- Aderência geral: **61,8%**. Café da manhã é a refeição mais aderente (**81%**); almoço e jantar ficam perto de **54%**.
- Comer fora: **17%** de aderência contra **77%** em casa.
- Modelo (ROC AUC no teste): baseline **0,50**, Regressão Logística **0,87**, Random Forest **0,86**. Acurácia de ~80% contra 64% do baseline.
- Leitura honesta: como os dados são simulados com regras que eu mesmo defini, o modelo "redescobre" essas regras. O valor do projeto está no **pipeline** (dados → SQL → dashboard → modelo → avaliação), não no número em si.

## Como rodar
```bash
pip install -r requirements.txt
python gerar_dados.py
python treinar_modelo.py
streamlit run app.py
```

## Próximos passos
- Trocar SQLite por **PostgreSQL** e orquestrar a carga com um script de ETL.
- Alimentar o pipeline com os dados reais do app (anonimizados).
- Testar validação cruzada temporal e ajustar o limiar de decisão.
