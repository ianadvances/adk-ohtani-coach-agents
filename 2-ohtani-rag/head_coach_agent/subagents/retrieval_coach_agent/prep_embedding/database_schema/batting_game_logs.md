# Table: batting_game_logs (打擊逐場記錄)

## Table 描述
儲存大谷翔平每場比賽的打擊表現數據，包含打數、安打、全壘打、打點等關鍵指標。

**適用情境：**
- 追蹤打擊手感和狀態起伏
- 分析對特定球隊的打擊表現
- 評估主客場對打擊成績的影響
- 研究打擊率、上壘率、長打率的變化趨勢
- 分析全壘打產出的週期性和爆發力
- 評估關鍵時刻的打點貢獻
- 製作打擊成績報告和績效分析
- 預測未來打擊表現或設定目標

## Schema 定義
```sql
CREATE TABLE batting_game_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recent_game_rank INTEGER,
    opponent TEXT,
    score TEXT,
    game_type TEXT,
    at_bats INTEGER,
    runs INTEGER,
    hits INTEGER,
    doubles INTEGER,
    triples INTEGER,
    home_runs INTEGER,
    rbis INTEGER,
    walks INTEGER,
    strikeouts INTEGER,
    stolen_bases INTEGER,
    caught_stealing INTEGER,
    batting_avg REAL,
    obp REAL,
    slg REAL,
    ops REAL
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
| `at_bats` | INTEGER | 打數 | 4, 5, 3 |
| `runs` | INTEGER | 得分 | 1, 0, 2 |
| `hits` | INTEGER | 安打數 | 2, 1, 3 |
| `doubles` | INTEGER | 二壘安打 | 0, 1, 2 |
| `triples` | INTEGER | 三壘安打 | 0, 0, 1 |
| `home_runs` | INTEGER | 全壘打 | 1, 0, 2 |
| `rbis` | INTEGER | 打點 | 2, 0, 3 |
| `walks` | INTEGER | 四壞球 | 1, 0, 2 |
| `strikeouts` | INTEGER | 三振 | 1, 2, 0 |
| `stolen_bases` | INTEGER | 盜壘成功 | 0, 1, 0 |
| `caught_stealing` | INTEGER | 盜壘失敗 | 0, 0, 1 |
| `batting_avg` | REAL | 打擊率 | 0.285, 0.300, 0.275 |
| `obp` | REAL | 上壘率 | 0.393, 0.420, 0.350 |
| `slg` | REAL | 長打率 | 0.625, 0.580, 0.700 |
| `ops` | REAL | OPS值（上壘率+長打率） | 1.018, 1.000, 1.050 |

## 資料範例
```sql
INSERT INTO batting_game_logs VALUES (
    1, 1, '@落磯', '敗 3-8', 'Reg', 
    2, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 
    0.285, 0.393, 0.625, 1.018
);
```

## 時間排序
- `recent_game_rank` 欄位表示最近第幾場比賽
- 數值 1 = 最近第 1 場（最新的比賽）
- 數值越大表示越早期的比賽
- 資料按時間倒序排列（最新在前）