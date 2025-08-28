# 單場最佳表現排名

## 使用情境

排名大谷翔平的單場最佳表現，找出他職業生涯中最精彩的比賽。這類分析對於製作精彩回顧、評選年度最佳表現、以及為球迷提供經典比賽回憶具有重要價值。對於體育媒體工作者，這些排名數據是製作專題報導和紀錄片的重要素材。對於棒球歷史研究者，單場最佳表現有助於評估球員在特定時刻的巔峰能力。

## SQL 查詢

```sql
-- 單場打擊最佳表現排名
WITH game_performance_score AS (
    SELECT 
        recent_game_rank,
        opponent,
        at_bats,
        hits,
        doubles,
        home_runs,
        rbis,
        batting_avg,
        ops,
        -- 綜合表現評分公式
        (
            home_runs * 10 +           -- 全壘打權重最高
            doubles * 5 +              -- 二壘安打中等權重
            (hits - doubles - home_runs) * 2 +  -- 一壘安打基礎權重
            rbis * 3 +                 -- 打點重要權重
            CASE 
                WHEN ops >= 2.000 THEN 15
                WHEN ops >= 1.500 THEN 10
                WHEN ops >= 1.000 THEN 5
                ELSE 0
            END                        -- OPS獎勵分數
        ) as performance_score
    FROM batting_game_logs
    WHERE at_bats > 0  -- 確保有實際打擊機會
)
SELECT 
    recent_game_rank,
    opponent,
    at_bats,
    hits,
    doubles,
    home_runs,
    rbis,
    ROUND(batting_avg, 3) as avg,
    ROUND(ops, 3) as ops,
    performance_score,
    RANK() OVER (ORDER BY performance_score DESC) as performance_rank,
    CASE 
        WHEN performance_score >= 40 THEN '傳奇級表現'
        WHEN performance_score >= 30 THEN '優異表現'
        WHEN performance_score >= 20 THEN '良好表現'
        ELSE '一般表現'
    END as performance_level
FROM game_performance_score
ORDER BY performance_score DESC
LIMIT 20;
```

## 說明

建立綜合評分系統對單場表現進行排名，結合多項打擊指標的加權計算。這個評分公式考慮了不同打擊成果的相對價值：全壘打獲得最高的10分權重，反映其對比賽的決定性影響；打點獲得3分權重，體現得分貢獻的重要性；OPS達到特定門檻時給予額外獎勵分數，鼓勵整體攻擊效率。performance_level分類提供了直觀的表現等級評估，40分以上被定義為'傳奇級表現'。LIMIT 20確保只顯示前20場最佳表現，便於重點關注最精彩的比賽。