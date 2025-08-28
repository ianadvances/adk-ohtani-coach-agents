# 賽季投打綜合表現

## 使用情境

比較各賽季的投打平衡發展。這個查詢是分析大谷翔平獨特二刀流能力的核心工具，適用於評估他在投手和打擊兩個領域的平衡發展。對於棒球歷史學家而言，這類數據有助於將大谷翔平與貝比魯斯等歷史上的二刀流球員進行比較。對於球團管理層，這些綜合數據提供了評估大谷翔平整體價值的重要依據，特別是在考慮合約續約或交易時。媒體也經常使用這類數據來製作二刀流專題報導，展現大谷翔平在現代棒球中的獨特地位。

## SQL 查詢

```sql
-- 賽季投打綜合數據
SELECT 
    bs.season,
    bs.team,
    bs.games as batting_games,
    bs.home_runs,
    bs.rbis,
    bs.avg,
    bs.ops,
    ps.games_started as pitching_starts,
    ps.wins,
    ps.losses,
    ps.era,
    ps.strikeouts,
    ROUND(ps.strikeouts / ps.innings_pitched * 9, 1) as k_per_9
FROM batting_season_stats bs
JOIN pitching_season_stats ps ON bs.season = ps.season
ORDER BY bs.season DESC;
```

## 說明

整合各賽季的投打數據，提供完整的二刀流表現概覽，包含每9局三振率等進階指標。這個JOIN查詢以season為關聯鍵，確保投打數據來自同一賽季。batting_games和pitching_starts的對比顯示了大谷翔平在兩個角色間的時間分配。k_per_9（每9局三振率）是評估投手壓制力的標準化指標，便於跨賽季比較。透過這個查詢，可以觀察到大谷翔平是否在某些賽季更專注於投球或打擊，以及他的二刀流能力是否隨時間而進化。