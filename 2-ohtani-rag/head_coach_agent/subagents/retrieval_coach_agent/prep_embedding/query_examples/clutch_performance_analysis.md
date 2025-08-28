# 關鍵情況表現

## 使用情境

分析大谷翔平在關鍵時刻和高壓情況下的表現能力。關鍵時刻表現是區分優秀球員和偉大球員的重要指標，這類分析對於評估球員的心理素質、抗壓能力和比賽影響力具有重要價值。對於球隊教練，了解球員的關鍵時刻表現有助於制定戰術安排和關鍵時刻的人員調度。對於球迷和媒體，關鍵時刻的精彩表現往往成為最難忘的經典時刻。

## SQL 查詢

```sql
-- 關鍵情況下的表現分析
WITH clutch_situations AS (
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
            WHEN home_runs >= 2 THEN '多轟場次'
            WHEN rbis >= 4 THEN '高打點場次'
            WHEN ops >= 1.200 THEN '爆發場次'
            WHEN hits >= 3 AND batting_avg >= 0.500 THEN '多安場次'
            ELSE '一般場次'
        END as performance_level,
        CASE 
            WHEN home_runs >= 2 OR rbis >= 4 OR ops >= 1.200 THEN 1
            ELSE 0
        END as is_clutch_game
    FROM batting_game_logs
)
SELECT 
    performance_level,
    COUNT(*) as game_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage,
    ROUND(AVG(at_bats), 1) as avg_ab,
    ROUND(AVG(hits), 1) as avg_hits,
    ROUND(AVG(home_runs), 1) as avg_hr,
    ROUND(AVG(rbis), 1) as avg_rbi,
    ROUND(AVG(ops), 3) as avg_ops
FROM clutch_situations
GROUP BY performance_level
ORDER BY 
    CASE performance_level
        WHEN '多轟場次' THEN 1
        WHEN '高打點場次' THEN 2
        WHEN '爆發場次' THEN 3
        WHEN '多安場次' THEN 4
        WHEN '一般場次' THEN 5
    END;
```

## 說明

定義不同等級的關鍵表現情況，統計各類型場次的頻率和平均表現。這個查詢建立了四個關鍵表現等級：多轟場次（2支以上全壘打）、高打點場次（4分以上打點）、爆發場次（OPS 1.200以上）和多安場次（3支以上安打且打擊率0.500以上）。percentage欄位顯示了各類型場次的出現頻率，這有助於評估大谷翔平製造關鍵時刻的能力。透過比較不同表現等級的平均數據，可以了解他在不同壓力情況下的穩定性和爆發力。