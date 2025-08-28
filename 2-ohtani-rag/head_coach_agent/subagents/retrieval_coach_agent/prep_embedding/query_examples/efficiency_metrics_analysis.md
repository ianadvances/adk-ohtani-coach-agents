# 效率指標分析

## 使用情境

深入分析大谷翔平的投打效率指標，評估他在資源利用和產出效率方面的表現。這類分析對於現代棒球的數據驅動決策具有重要意義，特別適用於球團管理層評估球員價值、制定薪資策略，以及球迷和分析師理解球員的真實貢獻度。效率指標能夠排除運氣因素，更準確地反映球員的實際能力和穩定性。

## SQL 查詢

```sql
-- 投打效率綜合指標分析
WITH efficiency_metrics AS (
    SELECT 
        bs.season,
        bs.team,
        -- 打擊效率指標
        ROUND(bs.home_runs * 1.0 / bs.at_bats * 100, 2) as hr_rate,
        ROUND(bs.rbis * 1.0 / bs.hits, 2) as rbi_per_hit,
        ROUND(bs.ops / (bs.games * 1.0) * 100, 2) as ops_efficiency,
        -- 投手效率指標
        ROUND(ps.strikeouts * 1.0 / ps.innings_pitched, 2) as k_per_inning,
        ROUND(ps.wins * 1.0 / ps.games_started * 100, 2) as win_rate,
        ROUND(ps.innings_pitched / ps.games_started, 2) as avg_game_length,
        -- 綜合效率評估
        ROUND(
            (bs.ops * 50 + 
             ps.strikeouts / ps.innings_pitched * 50 + 
             (4.50 - LEAST(ps.era, 4.50)) * 20) / 3, 2
        ) as overall_efficiency
    FROM batting_season_stats bs
    JOIN pitching_season_stats ps ON bs.season = ps.season
)
SELECT 
    season,
    team,
    hr_rate,
    rbi_per_hit,
    ops_efficiency,
    k_per_inning,
    win_rate,
    avg_game_length,
    overall_efficiency,
    RANK() OVER (ORDER BY overall_efficiency DESC) as efficiency_rank
FROM efficiency_metrics
ORDER BY overall_efficiency DESC;
```

## 說明

建立多維度效率指標體系，包含打擊效率、投球效率和綜合效率評分。hr_rate（全壘打率）衡量長打頻率，rbi_per_hit評估得分效率，k_per_inning反映投球壓制力。overall_efficiency是一個加權綜合指標，結合了OPS、每局三振率和ERA的標準化數值。RANK()函數提供了跨賽季的效率排名，有助於識別大谷翔平的巔峰效率期。這個分析框架可以擴展到更多進階指標，如WAR、wOBA等現代棒球統計學指標。