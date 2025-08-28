# Table: pitching_season_stats (賽季投球數據)

## Table 描述
儲存大谷翔平每個賽季的投手統計數據，包含勝負場次、防禦率、三振數等年度累計指標。

**適用情境：**
- 分析大谷翔平的投手生涯發展軌跡
- 比較不同賽季的投手表現變化
- 評估年度投手成績和獎項競爭力
- 研究球隊轉換對投手數據的影響
- 製作生涯投手統計報告
- 預測未來賽季投手表現
- 分析投手三大指標（防禦率、WHIP、被打擊率）的年度變化
- 追蹤勝場數和三振數的年度產出

## Schema 定義
```sql
CREATE TABLE pitching_season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER,
    team TEXT,
    games INTEGER,
    earned_runs INTEGER,
    holds INTEGER,
    blown_saves INTEGER,
    games_started INTEGER,
    home_runs_allowed INTEGER,
    complete_games INTEGER,
    shutouts INTEGER,
    innings_pitched REAL,
    saves INTEGER,
    walks INTEGER,
    era REAL,
    whip REAL,
    baa REAL,
    strikeouts INTEGER,
    hits_allowed INTEGER,
    wins INTEGER,
    losses INTEGER,
    runs_allowed INTEGER
);
```

## 欄位說明

| 欄位名稱 | 資料類型 | 說明 | 範例 |
|---------|---------|------|------|
| `id` | INTEGER | 主鍵，自動遞增 | 1, 2, 3... |
| `season` | INTEGER | 賽季年份 | 2021, 2022, 2023 |
| `team` | TEXT | 所屬球隊 | "天使", "道奇" |
| `games` | INTEGER | 出賽場次 | 28, 23, 20 |
| `earned_runs` | INTEGER | 自責分數 | 44, 29, 38 |
| `holds` | INTEGER | 中繼成功數 | 0, 0, 0 |
| `blown_saves` | INTEGER | 救援失敗數 | 0, 0, 0 |
| `games_started` | INTEGER | 先發場次 | 23, 28, 20 |
| `home_runs_allowed` | INTEGER | 被全壘打數 | 14, 11, 15 |
| `complete_games` | INTEGER | 完投場次 | 0, 1, 0 |
| `shutouts` | INTEGER | 完封場次 | 0, 1, 0 |
| `innings_pitched` | REAL | 投球局數 | 130.1, 166.0, 132.0 |
| `saves` | INTEGER | 救援成功數 | 0, 0, 0 |
| `walks` | INTEGER | 四壞球數 | 44, 44, 32 |
| `era` | REAL | 防禦率 | 3.18, 2.33, 3.14 |
| `whip` | REAL | WHIP值（每局被上壘率） | 1.09, 1.01, 1.05 |
| `baa` | REAL | 被打擊率 | 0.190, 0.205, 0.184 |
| `strikeouts` | INTEGER | 三振數 | 156, 219, 167 |
| `hits_allowed` | INTEGER | 被安打數 | 98, 127, 105 |
| `wins` | INTEGER | 勝場數 | 9, 15, 10 |
| `losses` | INTEGER | 敗場數 | 2, 9, 5 |
| `runs_allowed` | INTEGER | 失分數 | 51, 35, 43 |

## 資料範例
```sql
INSERT INTO pitching_season_stats VALUES (
    1, 2021, '天使', 23, 44, 0, 0, 23, 14, 0, 0, 
    130.1, 0, 44, 3.18, 1.09, 0.190, 156, 98, 9, 2, 51
);
```