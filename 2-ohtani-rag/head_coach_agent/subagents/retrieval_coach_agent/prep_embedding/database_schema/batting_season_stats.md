# Table: batting_season_stats (賽季打擊數據)

## Table 描述
儲存大谷翔平每個賽季的打擊統計數據，包含全壘打、打點、打擊率等年度累計指標。

**適用情境：**
- 分析大谷翔平的打擊生涯發展軌跡
- 比較不同賽季的打擊表現變化
- 評估年度打擊成績和里程碑達成
- 研究球隊轉換對打擊數據的影響
- 製作生涯打擊統計報告
- 預測未來賽季打擊表現
- 分析打擊三圍（打擊率、上壘率、長打率）的年度變化
- 追蹤全壘打和打點的年度產出

## Schema 定義
```sql
CREATE TABLE batting_season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER,
    team TEXT,
    games INTEGER,
    doubles INTEGER,
    triples INTEGER,
    home_runs INTEGER,
    rbis INTEGER,
    stolen_bases INTEGER,
    avg REAL,
    caught_stealing INTEGER,
    obp REAL,
    walks INTEGER,
    slg REAL,
    ops REAL,
    strikeouts INTEGER,
    grounded_into_dp INTEGER,
    at_bats INTEGER,
    runs INTEGER
);
```

## 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `season` | INTEGER | 賽季年份 | 2021, 2022, 2023 |
| `team` | TEXT | 所屬球隊 | "天使", "道奇" |
| `games` | INTEGER | 出賽場次 | 155, 157, 135 |
| `doubles` | INTEGER | 二壘安打數 | 26, 34, 38 |
| `triples` | INTEGER | 三壘安打數 | 8, 5, 3 |
| `home_runs` | INTEGER | 全壘打數 | 46, 34, 44 |
| `rbis` | INTEGER | 打點數 | 100, 95, 96 |
| `stolen_bases` | INTEGER | 盜壘成功數 | 26, 11, 20 |
| `avg` | REAL | 打擊率 | 0.273, 0.283, 0.304 |
| `caught_stealing` | INTEGER | 盗壘失敗數 | 8, 4, 6 |
| `obp` | REAL | 上壘率 | 0.372, 0.343, 0.412 |
| `walks` | INTEGER | 四壞球數 | 96, 64, 81 |
| `slg` | REAL | 長打率 | 0.592, 0.519, 0.654 |
| `ops` | REAL | OPS值（上壘率+長打率） | 0.965, 0.875, 1.066 |
| `strikeouts` | INTEGER | 三振數 | 189, 219, 215 |
| `grounded_into_dp` | INTEGER | 雙殺打數 | 21, 15, 18 |
| `at_bats` | INTEGER | 打數 | 537, 520, 497 |
| `runs` | INTEGER | 得分數 | 103, 90, 96 |

## 資料範例
```sql
INSERT INTO batting_season_stats VALUES (
    1, 2021, '天使', 158, 26, 8, 46, 100, 26, 
    0.273, 8, 0.372, 96, 0.592, 0.965, 189, 21, 537, 103
);
```