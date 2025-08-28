# 投手表現統計分析

## 使用情境

深入分析投手整體表現水準和穩定性。這個綜合統計查詢適用於季末總結、年度獎項評選參考、球員交易評估，以及深度棒球分析報告的撰寫。對於投手教練而言，這些統計數據有助於識別大谷翔平的投球優勢和需要改進的領域。對於對手球隊的打擊教練，這些數據提供了制定對戰策略的重要參考。此外，這類統計分析也是棒球研究學者進行比較研究和歷史分析的重要工具，可以將大谷翔平的表現與其他頂級投手進行客觀比較。

## SQL 查詢

```sql
-- 投手綜合統計分析
SELECT 
    COUNT(*) as total_games,
    ROUND(AVG(era), 2) as avg_era,
    ROUND(MIN(era), 2) as best_era,
    ROUND(MAX(era), 2) as worst_era,
    SUM(strikeouts) as total_strikeouts,
    ROUND(AVG(strikeouts), 1) as avg_strikeouts_per_game,
    ROUND(SUM(innings_pitched), 1) as total_innings,
    ROUND(AVG(innings_pitched), 1) as avg_innings_per_start,
    COUNT(CASE WHEN decision = 'W' THEN 1 END) as wins,
    COUNT(CASE WHEN decision = 'L' THEN 1 END) as losses
FROM pitching_game_logs;
```

## 說明

提供投手表現的全面統計分析，包含平均值、極值、累計數據等，有助於評估整體投手能力。查詢使用多種聚合函數來計算不同層面的統計指標：COUNT(*)統計總出賽場次，AVG()、MIN()、MAX()函數分別計算防禦率的平均值、最佳值和最差值，展現表現的穩定性和變化範圍。SUM()函數累計三振數和投球局數，反映整體工作量和壓制力。透過CASE WHEN條件統計勝負場次，提供勝率相關資訊。這些多維度的統計數據組合，能夠建構出大谷翔平投手能力的完整輪廓，包括他的平均水準、最佳表現潛力、穩定性以及對球隊勝利的貢獻度。