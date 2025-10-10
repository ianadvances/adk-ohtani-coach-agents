
# 3-deploy 使用說明書

本目錄包含一個基於 Streamlit 的 Web 應用程式部署範例，展示如何將 ADK (Agent Development Kit) 代理部署為可互動的網頁聊天機器人。系統採用容器化部署方式，包含會話管理功能和 Agent，提供完整的聊天機器人體驗。

## 目錄結構

```
3-deploy/
├── .dockerignore          # Docker 忽略檔案
├── .env.example           # 環境變數配置範例
├── Dockerfile             # Docker 映像定義
├── README.md              # 本說明文件
├── app.py                 # Streamlit 應用程式
├── docker-compose.yml     # Docker Compose 配置
├── duck_agent/            # 小鴨代理模組
│   ├── __init__.py
│   └── agent.py
├── requirements.txt       # Python 依賴
└── session_manager.py     # 會話管理器
```

## 環境設定

### 1. 配置環境變數

首先，複製 `.env.example` 檔案並重新命名為 `.env`：

```bash
cp .env.example .env
```

### 2. 安裝依賴套件

確保您已安裝必要的 Python 套件

## 啟動和使用方式

### 1. 部署方式

#### 方式一：Docker Compose 部署（推薦）

使用終端機導航到 3-deploy 目錄：

```bash
cd 3-deploy
```

啟動容器化應用程式：

```bash
docker-compose up --build
```

#### 方式二：開發模式執行

直接執行 Streamlit 應用程式：

```bash
streamlit run app.py
```

### 2. 開啟網頁介面

在瀏覽器中開啟以下 URL：

```
http://localhost:8501
```

## 系統功能介紹

### 主要應用程式

**Streamlit App** 是整個系統的前端介面，提供完整的聊天機器人體驗。

### 核心組件詳細說明

#### 1. Duck Agent

**檔案位置**：`duck_agent/agent.py`

**功能描述**：
- 搞笑小鴨代理，使用 `gemini-2.5-flash-lite` 模型
- 以幽默可愛的方式回應使用者
- 具備獨特的小鴨個性和語言風格

**主要特色**：
- 在回應前後加上小鴨叫聲「呱呱」
- 偶爾加入小鴨評論，如「(小鴨覺得很有道理)」
- 保持輕鬆幽默的語調

**回應範例**：
- 使用者：「你好」
- 小鴨：「你好～呱呱 (小鴨很開心見到你！)"

#### 2. Session Manager

**檔案位置**：`session_manager.py`

**功能描述**：
- 會話管理器，負責處理多個聊天會話
- 使用 ADK 的 `InMemorySessionService` 進行會話管理
- 支援會話創建、刪除和訊息記錄

**主要特色**：
- **會話管理**：創建、刪除和切換多個聊天會話
- **訊息記錄**：保存每個會話的完整對話歷史 (應用重啟時會重置)
- **錯誤處理**：完善的異常處理機制

**核心功能**：
- `create_session()` - 創建新的聊天會話
- `delete_session()` - 刪除指定會話
- `send_message()` - 發送訊息並獲取回應
- `get_session_messages()` - 獲取會話的訊息記錄

#### 3. Streamlit 應用程式

**檔案位置**：`app.py`

**功能描述**：
- 基於 Streamlit 的 Web 前端介面
- 提供直觀的聊天機器人使用體驗
- 支援多會話管理和即時對話

**主要特色**：
- **側邊欄會話管理**：創建、選擇和刪除會話
- **即時聊天介面**：類似現代聊天應用的對話體驗
- **串流顯示**：支援打字效果的即時回應
- **響應式設計**：適配不同螢幕尺寸

**使用者介面組件**：
- 會話列表和管理按鈕
- 聊天記錄顯示區域
- 訊息輸入和發送表單
- 狀態提示和錯誤處理

## 部署架構說明

### Docker 容器化

#### Dockerfile 配置
- **基礎映像**：`python:3.11-slim`
- **工作目錄**：`/app`
- **暴露端口**：`8501`（Streamlit 預設端口）
- **啟動命令**：`streamlit run app.py`

#### Docker Compose 服務
- **服務名稱**：`duck-chat-app`
- **端口映射**：`8501:8501`
- **環境配置**：從 `.env` 檔案載入
- **重啟策略**：`unless-stopped`

### 依賴管理

**核心依賴**：
- `streamlit==1.49.1` - Web 應用程式框架
- `google-adk==1.10.0` - Google Agent Development Kit
- `google-genai==1.31.0` - Google Generative AI SDK

## 使用範例

### 基本對話流程

1. **創建會話**：在側邊欄點擊「創建新會話」
2. **開始對話**：在輸入框中輸入訊息
3. **查看回應**：小鴨會以可愛的方式回應
4. **管理會話**：可以切換或刪除不同的會話

**對話範例**：

**使用者**：「今天天氣真好」

**小鴨**：「呱呱～今天天氣真好～ (小鴨也想去池塘游泳)」

### 會話管理功能

- **多會話支援**：可以同時維護多個獨立的對話
- **會話命名**：為每個會話設定自訂名稱
- **歷史記錄**：每個會話保留完整的對話歷史
- **會話切換**：快速在不同會話間切換

## 技術架構說明

### 前端架構
- **Streamlit**：Web 應用程式框架
- **會話狀態管理**：使用 Streamlit 的 session_state
- **響應式佈局**：側邊欄 + 主內容區域

### 後端架構
- **ADK Runner**：代理執行引擎
- **InMemorySessionService**：記憶體會話服務
- **Duck Agent**：基於 Gemini 的聊天代理

### 部署架構
- **Docker 容器**：應用程式容器化
- **環境變數**：配置管理
- **端口映射**：網路訪問配置

## 常見問題

### Q: 如何自訂小鴨的回應風格？
A: 
- 修改 `duck_agent/agent.py` 中的 `instruction` 欄位
- 調整回應規則和語言風格
- 可以加入更多個性化的回應模式

### Q: 如何部署到生產環境？
A: 
- 使用 Docker Compose 進行容器化部署
- 配置適當的環境變數和安全設定
- 考慮使用反向代理（如 Nginx）進行負載均衡

### Q: 如何監控應用程式狀態？
A: 
- 查看 Docker 容器日誌：`docker-compose logs -f`
- 監控容器狀態：`docker-compose ps`
- 設定健康檢查和監控告警

### Q: 如何更換其他 AI 模型？
A: 
- 修改 `duck_agent/agent.py` 中的 `model` 參數
- 支援其他 Gemini 模型或透過 LiteLLM 整合其他模型
- 調整相應的環境變數配置

## 技術擴展建議

1. **資料庫整合**：使用 PostgreSQL 或 Firestore 進行會話持久化
2. **快取機制**：實現 Redis 快取提升回應速度
3. **API 介面**：提供 RESTful API 供其他應用整合
4. **監控系統**：整合 Prometheus 和 Grafana 進行監控

## 下一步

完成 3-deploy 的學習後，您可以：

1. 探索 `4-ohtani-mcp` 目錄了解 MCP（Model Context Protocol）應用
2. 嘗試自訂小鴨代理的個性和回應風格
3. 探索如何將其他目錄的複雜代理系統部署為 Web 應用
4. 研究如何整合多個代理到同一個 Web 介面中
5. 學習如何將 ADK 應用部署到雲端平台（如 Google Cloud Run、AWS ECS 等）
6. 開發自己的 AI 聊天機器人產品