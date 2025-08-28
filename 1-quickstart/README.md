# 1-quickstart 使用說明書

本目錄包含三個漸進式的 AI 代理範例，從簡單的對話功能到具備工具使用能力的進階代理。這些範例將幫助您了解如何使用 ADK (Agent Development Kit) 建立不同類型的 AI 代理。

## 目錄結構

```
1-quickstart/
├── .env.example           # 環境變數配置範例
├── README.md              # 本說明文件
├── simple_agent/          # 基礎對話代理
│   ├── __init__.py
│   └── agent.py
├── function_tool_agent/   # 自定義工具代理
│   ├── __init__.py
│   └── agent.py
└── built_in_tool_agent/   # 內建工具代理
    ├── __init__.py
    └── agent.py
```

## 環境設定

### 1. 配置環境變數

首先，複製 `.env.example` 檔案並重新命名為 `.env`：

```bash
cp .env.example .env
```

然後根據您的需求選擇以下其中一種配置方式：

#### 選項 1: 使用 Vertex AI
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-east5
```

#### 選項 2: 使用 Google AI API
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-api-key
```

⚠️ **重要提醒**：請勿將真實的 API 金鑰提交到版本控制系統中。

### 2. 安裝依賴套件

確保您已安裝必要的 Python 套件

## 啟動和使用方式

### 1. 身份驗證設定（僅限 Vertex AI 使用者）

如果您在環境設定中選擇了「Vertex AI」，必須先進行 Google Cloud 身份驗證：

```bash
gcloud auth application-default login
```

**注意**：如果您使用的是「Google AI Studio」，請跳過此步驟。

### 2. 啟動 Dev UI

首先，使用終端機導航到 1-quickstart 目錄：

```bash
cd 1-quickstart
```

### 3. 啟動開發介面

執行以下命令啟動 Dev UI：

```bash
adk web
```

**Windows 使用者注意事項**：如果遇到 `_make_subprocess_transport NotImplementedError` 錯誤，請使用 `adk web --no-reload` 命令。

### 4. 開啟網頁介面

**步驟 1**：在瀏覽器中開啟提供的 URL（通常是 `http://localhost:8000` 或 `http://127.0.0.1:8000`）

**步驟 2**：在 UI 左上角的下拉選單中選擇您要測試的代理：
- `simple_agent` - 基礎對話代理
- `function_tool_agent` - 自定義工具代理  
- `built_in_tool_agent` - 內建工具代理

**疑難排解**：如果在下拉選單中看不到代理，請確認您是在 `1-quickstart` 目錄中執行 `adk web` 命令。

**步驟 3**：使用文字輸入框與您的代理對話

**步驟 4**：使用左側的「Events」標籤檢查個別函數呼叫、回應和模型回應：
- 點擊動作可查看詳細資訊
- 點擊「Trace」按鈕可查看每個事件的追蹤日誌，顯示每個函數呼叫的延遲時間

### 5. 其他互動方式

除了 Dev UI 外，還有其他方式與代理互動：

- **終端機模式**：`adk run`
- **API 伺服器模式**：`adk api_server`

## 代理介紹

### 1. Simple Agent - 基礎對話代理

**檔案位置**：`simple_agent/agent.py`

**功能描述**：
- 實現最基本的對話功能
- 採用「鸚鵡學舌」模式，會重複使用者的輸入
- 適合初學者了解代理的基本結構

**主要特色**：
- 簡潔的系統提示詞設定
- 基礎的對話處理邏輯

**預期輸出**：代理會以友善的方式回應並重複您的訊息。

### 2. Function Tool Agent - 自定義工具代理

**檔案位置**：`function_tool_agent/agent.py`

**功能描述**：
- 具備自定義工具使用能力
- 實現基本的數學運算功能
- 展示如何為代理添加特定功能

**主要特色**：
- 定義了兩個數學運算工具：`bad_add` 和 `bad_sub`
- 展示自定義工具的實作方式
- 支援基本的數學計算請求

**可用工具**：
- `bad_add(a, b)` - 加法運算
- `bad_sub(a, b)` - 減法運算
- 可試著詢問乘法或除法

**預期輸出**：代理會使用相應的數學工具進行計算並返回結果。

### 3. Built-in Tool Agent - 內建工具代理

**檔案位置**：`built_in_tool_agent/agent.py`

**功能描述**：
- 使用 ADK 提供的內建工具
- 具備 Google 搜尋功能
- 展示如何整合外部服務能力

**主要特色**：
- 使用 `google_search` 工具進行網路搜尋
- 能夠獲取即時資訊
- 適合需要外部資料來源的應用場景

**內建工具**：
- `google_search` - Google 搜尋工具，可搜尋網路上的最新資訊

**預期輸出**：代理會使用 Google 搜尋工具查找相關資訊並提供摘要。

## 學習路徑建議

### 階段 1：理解基礎概念
1. 從 `simple_agent` 開始，了解代理的基本結構
2. 觀察系統提示詞如何影響代理行為
3. 理解輸入輸出的處理流程

### 階段 2：掌握工具使用
1. 研究 `function_tool_agent` 的工具定義方式
2. 了解自定義工具的實作方法
3. 實作自己的自定義工具函數

### 階段 3：整合外部服務
1. 探索 `built_in_tool_agent` 的內建工具使用
2. 了解如何整合第三方 API 服務
3. 學習處理外部資料來源

## 常見問題

### Q: 如何選擇使用 Vertex AI 還是 Google AI API？
A: 
- **Vertex AI**：適合企業級應用，提供更好的安全性和管理功能
- **Google AI API**：適合個人開發和原型製作，設定較為簡單

### Q: 代理無法正常運作怎麼辦？
A: 
1. 檢查 `.env` 檔案是否正確配置
2. 確認 API 金鑰是否有效
3. 檢查網路連線是否正常
4. 查看錯誤訊息並對應處理

### Q: 如何擴展這些範例？
A: 
1. 在 `function_tool_agent` 基礎上添加更多自定義工具（如 `bad_add` 和 `bad_sub` 的擴展）
2. 結合多個內建工具創建更強大的代理
3. 修改系統提示詞以改變代理的行為模式

## 下一步

完成這些基礎範例後，您可以：

1. 前往 `2-ohtani-rag` 目錄學習 Multi-Agent 及 RAG（檢索增強生成）技術
2. 探索 `3-ohtani-mcp` 目錄了解 Multi-Agent 及 MCP（Model Context Protocol）應用
3. 開始開發您自己的 AI 代理專案
