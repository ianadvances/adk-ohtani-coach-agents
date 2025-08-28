# 賽季間表現比較

## 使用情境

比較大谷翔平在不同賽季間的表現變化，評估他的職業發展軌跡和成長趨勢。這類分析對於了解球員的長期發展模式、適應能力和巔峰期具有重要價值。對於球團管理層，賽季間比較有助於評估球員的投資價值和未來潛力。對於球迷和分析師，這些數據提供了追蹤偶像成長歷程的完整視角，特別是在評估大谷翔平作為二刀流球員的獨特發展路徑。

## SQL 查詢

```sql
-- 賽季間投打綜合表現比較
WITH season_comparison AS (
    SELECT 
        bs.season,
        bs.team,
        -- 打擊表現指標
        bs.games as batting_games,
        bs.home_runs,
        bs.rbis,
        ROUND(bs.avg, 3) as batting_avg,
        ROUND(bs.ops, 3) as ops,
        -- 投手表現指標
        ps.games_started as pitching_starts,
        ps.wins,
        ps.losses,
        ROUND(ps.era, 2) as era,
        ps.strikeouts,
        ROUND(ps.innings_pitched, 1) as innings_pitched,
        -- 效率指標
        ROUND(bs.home_runs * 1.0 / bs.games, 2) as hr_per_game,
        ROUND(ps.strikeouts * 1.0 / ps.innings_pitched * 9, 1) as k_per_9,
        -- 綜合評分
        ROUND(
            (bs.ops * 100 + 
             ps.strikeouts / ps.innings_pitched * 50 + 
             (4.50 - LEAST(ps.era, 4.50)) * 25) / 3, 1
        ) as overall_rating
    FROM batting_season_stats bs
    JOIN pitching_season_stats ps ON bs.season = ps.season
),
season_rankings AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY overall_rating DESC) as overall_rank,
        RANK() OVER (ORDER BY ops DESC) as batting_rank,
        RANK() OVER (ORDER BY era ASC) as pitching_rank
    FROM season_comparison
)
SELECT 
    season,
    team,
    batting_games,
    home_runs,
    rbis,
    batting_avg,
    ops,
    pitching_starts,
    wins,
    losses,
    era,
    strikeouts,
    hr_per_game,
    k_per_9,
    overall_rating,
    overall_rank,
    batting_rank,
    pitching_rank,
    CASE 
        WHEN overall_rank = 1 THEN '巔峰賽季'
        WHEN overall_rank <= 3 THEN '優秀賽季'
        ELSE '發展賽季'
    END as season_classification
FROM season_rankings
ORDER BY season DESC;
```

## 說明

建立多維度的賽季比較框架，包含投打表現、效率指標和綜合排名。這個複雜查詢使用了兩個CTE：season_comparison計算各賽季的關鍵指標，season_rankings建立多個排名維度。overall_rating是一個綜合評分，結合了OPS、每9局三振率和ERA的標準化數值，提供了評估二刀流整體表現的量化工具。三個排名維度（overall_rank、batting_rank、pitching_rank）分別評估綜合表現、打擊表現和投球表現，有助於識別大谷翔平在不同方面的相對強弱。season_classification提供了直觀的賽季等級分類，幫助快速識別巔峰期和發展期。