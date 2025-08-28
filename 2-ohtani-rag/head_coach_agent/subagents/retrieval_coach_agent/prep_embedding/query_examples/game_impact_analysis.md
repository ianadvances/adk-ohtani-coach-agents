# 單場比賽影響力分析

## 使用情境

分析大谷翔平在同一場比賽中的投打雙重貢獻。這是最能體現二刀流價值的分析角度，特別適用於尋找大谷翔平在投打兩方面都有出色表現的經典比賽。對於製作精彩回顧影片的媒體工作者，這類查詢能夠快速找到最具代表性的比賽片段。對於棒球戰術分析師，這些數據有助於研究二刀流球員對比賽節奏和戰術安排的影響。

## SQL 查詢

```sql
-- 投打雙重貢獻的比賽
SELECT 
    bg.recent_game_rank,
    bg.opponent,
    bg.at_bats,
    bg.hits,
    bg.home_runs,
    bg.rbis,
    bg.ops as batting_ops,
    pg.innings_pitched,
    pg.strikeouts,
    pg.era_game,
    pg.whip_game,
    CASE 
        WHEN bg.home_runs > 0 AND pg.strikeouts >= 5 THEN '投打雙響'
        WHEN bg.ops > 1.000 AND pg.era_game < 3.00 THEN '高效雙刀'
        WHEN bg.rbis >= 2 AND pg.innings_pitched >= 6 THEN '穩定貢獻'
        ELSE '一般表現'
    END as performance_type
FROM batting_game_logs bg
JOIN pitching_game_logs pg ON bg.recent_game_rank = pg.recent_game_rank
WHERE bg.home_runs > 0 OR bg.ops > 0.800 OR pg.strikeouts >= 5 OR pg.era_game < 4.00
ORDER BY 
    CASE 
        WHEN bg.home_runs > 0 AND pg.strikeouts >= 5 THEN 1
        WHEN bg.ops > 1.000 AND pg.era_game < 3.00 THEN 2
        WHEN bg.rbis >= 2 AND pg.innings_pitched >= 6 THEN 3
        ELSE 4
    END,
    bg.recent_game_rank ASC;
```

## 說明

找出投打都有貢獻的比賽，並根據表現水準分類排序。這個複雜的JOIN查詢以recent_game_rank為關聯鍵，確保投打數據來自同一場比賽。WHERE條件設定了多重篩選標準，確保至少在投球或打擊一方面有不錯表現。CASE語句建立了四個表現等級：'投打雙響'代表同場比賽有全壘打且至少5次三振的頂級表現；'高效雙刀'代表OPS超過1.000且ERA低於3.00的高效率表現；'穩定貢獻'代表有實質貢獻但未達頂級的穩定表現。ORDER BY子句優先顯示最精彩的投打雙重表現。