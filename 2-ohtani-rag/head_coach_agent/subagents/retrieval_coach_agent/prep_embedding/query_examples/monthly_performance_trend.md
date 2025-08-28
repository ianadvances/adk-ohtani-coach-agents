# 月份表現趨勢分析

## 使用情境

分析大谷翔平在不同月份的表現模式，識別季節性變化和適應週期。MLB賽季從春季延續到秋季，不同月份的氣候條件、比賽密度和身體狀況都可能影響球員表現。這個分析對於制定訓練計畫、安排休息時間和預測未來表現具有重要參考價值。對於幻想棒球玩家，月份趨勢分析有助於制定選手使用策略。

## SQL 查詢

```sql
-- 按月份統計表現趨勢
WITH monthly_stats AS (
    SELECT 
        CASE 
            WHEN recent_game_rank BETWEEN 1 AND 30 THEN '4月'
            WHEN recent_game_rank BETWEEN 31 AND 60 THEN '5月'
            WHEN recent_game_rank BETWEEN 61 AND 90 THEN '6月'
            WHEN recent_game_rank BETWEEN 91 AND 120 THEN '7月'
            WHEN recent_game_rank BETWEEN 121 AND 150 THEN '8月'
            WHEN recent_game_rank BETWEEN 151 AND 162 THEN '9月'
            ELSE '其他'
        END as month_period,
        at_bats,
        hits,
        home_runs,
        rbis,
        batting_avg,
        ops
    FROM batting_game_logs
    WHERE recent_game_rank <= 162
)
SELECT 
    month_period,
    COUNT(*) as games,
    SUM(at_bats) as total_ab,
    SUM(hits) as total_hits,
    SUM(home_runs) as total_hr,
    SUM(rbis) as total_rbi,
    ROUND(SUM(hits) * 1.0 / NULLIF(SUM(at_bats), 0), 3) as monthly_avg,
    ROUND(AVG(ops), 3) as avg_ops,
    ROUND(SUM(home_runs) * 1.0 / COUNT(*), 2) as hr_per_game,
    ROUND(SUM(rbis) * 1.0 / COUNT(*), 2) as rbi_per_game
FROM monthly_stats
WHERE month_period != '其他'
GROUP BY month_period
ORDER BY 
    CASE month_period
        WHEN '4月' THEN 1
        WHEN '5月' THEN 2
        WHEN '6月' THEN 3
        WHEN '7月' THEN 4
        WHEN '8月' THEN 5
        WHEN '9月' THEN 6
    END;
```

## 說明

將賽季按月份分組，分析各月份的打擊表現趨勢和變化模式。這個查詢使用CASE語句將比賽場次轉換為對應的月份期間，每個月份大約對應30場比賽。NULLIF函數防止除零錯誤，確保查詢的穩定性。透過hr_per_game和rbi_per_game的月份比較，可以觀察到大谷翔平是否在特定月份有更好的長打表現或得分貢獻。ORDER BY子句確保月份按正確的時間順序排列，便於觀察季節性趨勢。