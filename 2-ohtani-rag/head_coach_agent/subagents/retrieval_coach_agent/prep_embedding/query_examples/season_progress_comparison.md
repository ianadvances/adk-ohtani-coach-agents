# 賽季進展表現比較

## 使用情境

追蹤大谷翔平在賽季中的表現變化趨勢。這個分析對於了解球員的適應能力、體能管理和技術調整具有重要價值。對於球隊醫療和體能訓練團隊，這類數據有助於評估訓練計畫的效果和調整休息安排。對於球迷和媒體，賽季進展分析提供了追蹤偶像成長軌跡的有趣視角，特別是在觀察大谷翔平如何在漫長的MLB賽季中保持高水準表現。

## SQL 查詢

```sql
-- 賽季前半段 vs 後半段表現比較
WITH season_halves AS (
    SELECT 
        recent_game_rank,
        opponent,
        at_bats,
        hits,
        home_runs,
        rbis,
        batting_avg,
        ops,
        CASE 
            WHEN recent_game_rank <= 81 THEN '前半季'
            ELSE '後半季'
        END as season_half
    FROM batting_game_logs
    WHERE recent_game_rank <= 162  -- 正規賽季場次
)
SELECT 
    season_half,
    COUNT(*) as games_played,
    SUM(at_bats) as total_ab,
    SUM(hits) as total_hits,
    SUM(home_runs) as total_hr,
    SUM(rbis) as total_rbi,
    ROUND(SUM(hits) * 1.0 / SUM(at_bats), 3) as avg,
    ROUND(AVG(ops), 3) as avg_ops,
    ROUND(SUM(home_runs) * 1.0 / COUNT(*), 2) as hr_per_game
FROM season_halves
GROUP BY season_half
ORDER BY season_half;
```

## 說明

使用CTE將賽季分為前後半段，比較各階段的累積統計和平均表現。這個查詢採用了81場比賽作為分界點，這是MLB正規賽季162場的一半。透過GROUP BY season_half，可以清楚看出大谷翔平在賽季不同階段的表現差異。hr_per_game指標特別有助於觀察長打頻率的變化，這通常反映了球員的體能狀態和適應程度。這種時間序列分析方法也可以進一步細分為月份或更小的時間單位。