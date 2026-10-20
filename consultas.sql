-- 1) Aderência por tipo de refeição
SELECT tipo_refeicao,
       COUNT(*) AS refeicoes,
       ROUND(100.0 * AVG(dentro_da_dieta), 1) AS pct_dentro_da_dieta
FROM refeicoes
GROUP BY tipo_refeicao
ORDER BY pct_dentro_da_dieta;

-- 2) Aderência: comer fora x em casa
SELECT CASE comeu_fora WHEN 1 THEN 'fora' ELSE 'casa' END AS local,
       ROUND(100.0 * AVG(dentro_da_dieta), 1) AS pct_dentro_da_dieta,
       ROUND(AVG(calorias)) AS media_kcal
FROM refeicoes
GROUP BY comeu_fora;

-- 3) Aderência semanal com média móvel de 4 semanas (window function)
WITH semanal AS (
    SELECT strftime('%Y-%W', data) AS semana,
           100.0 * AVG(dentro_da_dieta) AS pct
    FROM refeicoes
    GROUP BY semana
)
SELECT semana,
       ROUND(pct, 1) AS pct_semana,
       ROUND(AVG(pct) OVER (ORDER BY semana ROWS BETWEEN 3 PRECEDING AND CURRENT ROW), 1) AS media_movel_4s
FROM semanal;

-- 4) Dias com todas as refeições dentro da dieta
SELECT COUNT(*) AS dias_perfeitos
FROM (SELECT data FROM refeicoes GROUP BY data HAVING MIN(dentro_da_dieta) = 1);
