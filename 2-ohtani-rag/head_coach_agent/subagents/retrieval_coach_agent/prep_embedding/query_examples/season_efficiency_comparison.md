# 賽季投打效率比較

## 使用情境

比較大谷翔平在不同賽季中投手和打擊效率的相對變化。這個分析有助於了解他的職業發展重心是否有所轉移，以及在哪些賽季他在投打兩方面達到了最佳平衡。對於長期追蹤大谷翔平職業生涯的分析師而言，這類數據可以揭示他的技能發展軌跡和適應策略。

## SQL 查詢

```sql
-- 賽季投打效率綜合比較
SELECT 
    bs.season,
    bs.team,
    -- 打擊效率指標
    ROUND(bs.home_runs * 1.0 / bs.games, 2) as hr_per_game,
    ROUND(bs.rbis * 1.0 / bs.games, 2) as rbi_per_game,
    bs.ops as batting_ops,
    -- 投手效率指標
    ROUND(ps.strikeouts * 1.0 / ps.games_started, 1) as k_per_start,
    ROUND(ps.innings_pitched * 1.0 / ps.games_started, 1) as ip_per_start,
    ps.era as pitching_era,
    -- 綜合效率評分
    ROUND(
        (bs.ops * 100 + (4.00 - LEAST(ps.era, 4.00)) * 25) / 2, 1
    ) as combined_efficiency_score
FROM batting_season_stats bs
JOIN pitching_season_stats ps ON bs.season = ps.season
ORDER BY combined_efficiency_score DESC;
```

## 說明

計算各賽季的投打效率指標並建立綜合評分系統。hr_per_game和rbi_per_game標準化了打擊貢獻，k_per_start和ip_per_start則標準化了投手工作量和效率。combined_efficiency_score是一個創新的綜合指標，將OPS和ERA轉換為可比較的數值並取平均，提供了評估二刀流整體表現的量化工具。這個評分系統可以幫助識別大谷翔平的巔峰賽季和相對低潮期。