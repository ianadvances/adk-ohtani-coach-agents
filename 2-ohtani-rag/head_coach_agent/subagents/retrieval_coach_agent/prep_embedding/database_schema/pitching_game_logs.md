# Table: pitching_game_logs (投手逐場記錄)

## Table 描述
儲存大谷翔平每場比賽的投手表現數據，包含投球局數、三振、防禦率等關鍵指標。

**適用情境：**
- 分析大谷翔平的投手表現趨勢和穩定性
- 評估特定對手或主客場對投球表現的影響
- 追蹤投手狀態變化（如防禦率、WHIP值的波動）
- 研究投球局數與表現品質的關聯性
- 比較不同時期的投手數據（如賽季初期vs後期）
- 分析勝負投與投手數據的相關性
- 製作投手表現報告或數據視覺化

## Schema 定義
```sql
CREATE TABLE pitching_game_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recent_game_rank INTEGER,
    opponent TEXT,
    score TEXT,
    game_type TEXT,
    decision TEXT,
    innings_pitched REAL,
    hits_allowed INTEGER,
    runs_allowed INTEGER,
    earned_runs INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    home_runs_allowed INTEGER,
    era REAL,
    whip REAL,
    baa REAL
);
```

## 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `recent_game_rank` | INTEGER | 最近第幾場比賽（1=最近第1場） | 1, 2, 3... |
| `opponent` | TEXT | 對戰球隊（'@'開頭表示在客場比賽） | "@落磯", "教士", "天使" |
| `score` | TEXT | 比賽比分 | "敗 3-8", "勝 11-4" |
| `game_type` | TEXT | 比賽類型 | "Reg"（例行賽） |
| `decision` | TEXT | 投手勝負記錄 | "L"（敗投）, "W"（勝投）, "-"（無關勝負） |
| `innings_pitched` | REAL | 投球局數 | 4.0, 5.1, 6.2 |
| `hits_allowed` | INTEGER | 被安打數 | 5, 3, 7 |
| `runs_allowed` | INTEGER | 失分 | 2, 0, 4 |
| `earned_runs` | INTEGER | 自責分 | 2, 0, 3 |
| `walks` | INTEGER | 四壞球 | 1, 3, 0 |
| `strikeouts` | INTEGER | 三振數 | 8, 12, 5 |
| `home_runs_allowed` | INTEGER | 被全壘打數 | 0, 1, 2 |
| `era` | REAL | 防禦率 | 2.50, 3.47, 4.61 |
| `whip` | REAL | WHIP值（每局被上壘率） | 1.20, 0.95, 1.45 |
| `baa` | REAL | 被打擊率 | 0.250, 0.180, 0.320 |

## 資料範例
```sql
INSERT INTO pitching_game_logs VALUES (
    1, 1, '@落磯', '敗 3-8', 'Reg', 'L', 
    4.0, 9, 5, 5, 0, 3, 0, 4.61, 1.28, 0.278
);
```

## 時間排序
- `recent_game_rank` 欄位表示最近第幾場比賽
- 數值 1 = 最近第 1 場（最新的比賽）
- 數值越大表示越早期的比賽
- 資料按時間倒序排列（最新在前）