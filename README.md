

# 大谷翔平的 Multi-Agent 教練：由 ADK 打造 AI 教練團

本專案展示如何使用 ADK (Agent Development Kit) 建立不同類型的 AI 代理，從基礎對話功能到複雜的多代理系統。專案包含四個漸進式的學習範例，幫助您掌握 AI 代理開發技術。

## 專案結構

```
adk-ohtani-coach-agents/
├── 1-quickstart/                # 基礎代理範例
│   ├── simple_agent/            
│   ├── function_tool_agent/     
│   └── built_in_tool_agent/     
├── 2-ohtani-rag/                # 多代理 RAG 系統
│   └── head_coach_agent/        
├── 3-deploy/                    # 應用部署範例
│   ├── duck_agent/              
│   ├── app.py                   # Streamlit 應用程式
│   ├── session_manager.py       # 會話管理
│   └── Dockerfile       
├── 4-ohtani-mcp/                # MCP 協議應用範例
│   └── head_coach_agent/   
└── requirements.txt             # 專案依賴套件
```

## 建立虛擬環境

| 步驟 | Linux / macOS  | Windows PowerShell  |
|------|-------------------------|------------------------------|
| 1. 建立環境 | `python3 -m venv .venv` | `python -m venv .venv` |
| 2. 啟用環境 | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| 3. 更新 pip | `pip install --upgrade pip` | `python.exe -m pip install --upgrade pip` |
| 4. 安裝套件 | `pip install -r requirements.txt` | `pip install -r requirements.txt` |

## 學習路徑

### 階段 1: 基礎代理 (1-quickstart)

📖 [詳細使用說明](./1-quickstart/README.md)

從最簡單的對話代理開始，逐步學習工具使用和外部服務整合：

- **Simple Agent**: 基礎對話功能
- **Function Tool Agent**: 自定義工具使用
- **Built-in Tool Agent**: 內建工具整合

```bash
cd 1-quickstart
adk web
```

### 階段 2: 多代理 RAG 系統 (2-ohtani-rag)

📖 [詳細使用說明](./2-ohtani-rag/README.md)

學習複雜的多代理協作和 RAG 技術：

- 階層式多代理架構
- 資料庫查詢與網路情報整合
- 智能錯誤處理和迭代改進

```bash
cd 2-ohtani-rag
adk web
```

### 階段 3: Web 應用部署 (3-deploy)

📖 [詳細使用說明](./3-deploy/README.md)

學習如何將 ADK 代理部署為可互動的網頁聊天機器人：

- 基於 Streamlit 的 Web 應用程式
- Docker 容器化部署
- 會話管理支援

#### 快速部署

```bash
cd 3-deploy
# 配置環境變數
cp .env.example .env
# 啟動容器化應用
docker-compose up --build
# 開啟瀏覽器訪問 http://localhost:8501
```

### 階段 4: MCP 協議應用 (4-ohtani-mcp)

📖 [詳細使用說明](./4-ohtani-mcp/README.md)

探索 Model Context Protocol 的進階應用。

```bash
cd 4-ohtani-mcp
adk web
```