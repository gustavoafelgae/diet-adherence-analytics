"""Prevê, ANTES de comer, se uma refeição vai ficar dentro da dieta.
Rode: python treinar_modelo.py
"""
import sqlite3
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

with sqlite3.connect("dieta.db") as con:
    df = pd.read_sql("SELECT * FROM refeicoes", con)

# 'calorias' e 'proteina_g' ficam FORA: a calorias define o rótulo (data leakage).
# O objetivo é prever pelo contexto, antes da refeição.
cat = ["tipo_refeicao", "dia_semana"]
num = ["hora", "comeu_fora", "horas_sono"]
X, y = df[cat + num], df["dentro_da_dieta"]

# Divisão por tempo (as últimas 20% das refeições viram teste), sem embaralhar
corte = int(len(df) * 0.8)
X_tr, X_te, y_tr, y_te = X.iloc[:corte], X.iloc[corte:], y.iloc[:corte], y.iloc[corte:]

prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), cat),
                          ("num", StandardScaler(), num)])
modelos = {
    "Baseline (classe mais comum)": DummyClassifier(strategy="most_frequent"),
    "Regressão Logística": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42),
}

relatorio = []
for nome, clf in modelos.items():
    pipe = Pipeline([("prep", prep), ("clf", clf)]).fit(X_tr, y_tr)
    prob = pipe.predict_proba(X_te)[:, 1]
    pred = pipe.predict(X_te)
    auc = roc_auc_score(y_te, prob)
    relatorio.append(f"=== {nome} | ROC AUC: {auc:.3f} ===\n{classification_report(y_te, pred, digits=3, zero_division=0)}")

texto = "\n".join(relatorio)
print(texto)
open("resultados_modelo.txt", "w", encoding="utf-8").write(texto)
