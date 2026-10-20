"""Gera dados SINTÉTICOS de refeições e grava em SQLite + CSV.
Rode: python gerar_dados.py
"""
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
DIAS = 180
LIMITE_KCAL = {"cafe": 500, "almoco": 700, "lanche": 250, "jantar": 600}  # regra da dieta
HORA_BASE = {"cafe": 7, "almoco": 12, "lanche": 16, "jantar": 20}
KCAL_BASE = {"cafe": 380, "almoco": 620, "lanche": 220, "jantar": 520}

linhas = []
for d in pd.date_range("2025-01-01", periods=DIAS):
    sono = float(np.clip(rng.normal(7, 1.2), 4, 9.5))  # horas de sono na noite anterior
    fim_de_semana = d.dayofweek >= 5
    for tipo in LIMITE_KCAL:
        hora = int(np.clip(HORA_BASE[tipo] + rng.integers(-1, 3), 5, 23))
        comeu_fora = bool(rng.random() < (0.45 if fim_de_semana else 0.15))
        kcal = KCAL_BASE[tipo] * rng.normal(1.0, 0.12)
        kcal *= 1.25 if comeu_fora else 1.0          # comer fora pesa mais
        kcal *= 1.15 if fim_de_semana else 1.0
        kcal *= 1.0 + max(0, 6.5 - sono) * 0.08      # pouco sono -> come mais
        kcal *= 1.10 if hora >= 21 else 1.0          # tarde da noite
        kcal = round(kcal)
        proteina = round(kcal * rng.uniform(0.15, 0.30) / 4)
        linhas.append({
            "data": d.date().isoformat(), "dia_semana": d.dayofweek, "tipo_refeicao": tipo,
            "hora": hora, "comeu_fora": int(comeu_fora), "horas_sono": round(sono, 1),
            "calorias": kcal, "proteina_g": proteina,
            "dentro_da_dieta": int(kcal <= LIMITE_KCAL[tipo]),
        })

df = pd.DataFrame(linhas)
df.to_csv("refeicoes.csv", index=False)
with sqlite3.connect("dieta.db") as con:
    df.to_sql("refeicoes", con, if_exists="replace", index=False)
print(f"{len(df)} refeições geradas. Aderência geral: {df.dentro_da_dieta.mean():.1%}")
