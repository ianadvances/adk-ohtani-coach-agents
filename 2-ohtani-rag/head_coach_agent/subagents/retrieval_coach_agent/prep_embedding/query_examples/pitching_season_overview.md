# 投手賽季統計概覽

## 使用情境

評估各賽季投手表現和工作負荷。這個查詢適用於年度投手績效評估、先發輪值規劃、投手健康狀況監控，以及制定來季投球策略。對於投手教練而言，這些數據有助於分析投球效率和耐久性。對於醫療團隊，可以評估工作量對球員健康的影響。對於對手球隊，這是制定打擊策略的重要參考資料。

## SQL 查詢

```sql
-- 投手賽季統計
SELECT 
    season,
    team,
    games_started,
    wins,
    losses,
    era,
    strikeouts,
    innings_pitched
FROM pitching_season_stats 
ORDER BY season DESC;
```

## 說明

提供各賽季投手核心數據概覽，便於進行年度間比較。查詢從pitching_season_stats表格提取數據，聚焦於games_started（先發場次）、wins/losses（勝敗紀錄）、era（防禦率）、strikeouts（三振）和innings_pitched（投球局數）等核心數據。這些指標展現投手的工作量、勝負貢獻和投球效率。透過DESC排序，最新賽季的數據會優先顯示，便於追蹤最近的投手表現變化。