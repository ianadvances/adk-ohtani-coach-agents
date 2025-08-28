# 打擊表現統計分析

## 使用情境

評估打擊能力的各項指標和一致性。這個全面的打擊統計分析對於評估大谷翔平作為指定打擊或野手的價值具有重要意義。適用於球團制定薪資策略、媒體撰寫深度分析報導、球迷了解偶像的攻擊威力，以及對手球隊制定投球策略。對於打擊教練而言，這些數據有助於識別大谷翔平的打擊優勢區域和改進空間。此外，這類統計也是評選年度最佳指定打擊、銀棒獎等獎項的重要參考依據，以及進行歷史比較和生涯里程碑追蹤的基礎數據。

## SQL 查詢

```sql
-- 打擊綜合統計分析
SELECT 
    COUNT(*) as total_games,
    SUM(at_bats) as total_at_bats,
    SUM(hits) as total_hits,
    ROUND(CAST(SUM(hits) AS FLOAT) / SUM(at_bats), 3) as overall_avg,
    SUM(home_runs) as total_home_runs,
    SUM(rbis) as total_rbis,
    ROUND(AVG(ops), 3) as avg_ops,
    COUNT(CASE WHEN home_runs > 0 THEN 1 END) as games_with_hr,
    COUNT(CASE WHEN hits >= 2 THEN 1 END) as multi_hit_games
FROM batting_game_logs;
```

## 說明

計算打擊的累計統計和平均表現，特別關注多安打場次和全壘打頻率。查詢透過SUM()函數累計at_bats（總打數）、hits（總安打）、home_runs（總全壘打）和rbis（總打點），提供整體攻擊貢獻的量化指標。overall_avg的計算使用CAST轉換確保精確的小數運算，反映真實的整體打擊率。AVG(ops)計算平均攻擊指數，這是評估打擊全面性的重要指標。特別值得注意的是games_with_hr和multi_hit_games的統計，前者反映長打爆發力的頻率，後者顯示穩定安打能力，這兩個指標對於評估打擊的威脅性和一致性具有重要意義。