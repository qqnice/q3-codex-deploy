# q3 地端 AI：交給 Ubuntu Codex 的部署任務

在已有兩個網站與 NAS 的 Linux VM 上，新增 **Ollama + Open WebUI + Gemma 3 1B**，透過 **https://q3.qqnas.org** 使用。Codex 先盤點，再依實際 Docker／Apache／Nginx／NAS 入口完成部署及驗收。

Git 保存任務、範本、檢查工具與架構圖。實際密碼、憑證、模型、聊天資料及主機紀錄保存在 VM，不回推 Git。

## 1. 在目標 Ubuntu 取得儲存庫

這是私人儲存庫，VM 必須先有此 GitHub 帳號的存取權。若 VM 已配置 Git 的 HTTPS 認證：

```bash
git clone https://github.com/qqnice/q3-codex-deploy.git
cd q3-codex-deploy
```

若 VM 已安裝 GitHub CLI、但尚未登入，可先在自己的終端機完成登入：

```bash
gh auth login --hostname github.com
gh auth setup-git
```

再執行上面的 clone。已有 SSH 金鑰者也可用 GitHub 顯示的 SSH clone 網址。不要將 GitHub token 寫入 clone 網址、提示詞或 .env。

如果資料夾已存在，先檢查內容與 Git 狀態，不重新 clone 覆蓋。

## 2. 啟動 Codex，貼這段話

在 `q3-codex-deploy` 資料夾啟動你已安裝的 Codex，把下面文字貼到 **Codex 對話**：

> 請讀取 CODEX_TASK.md、DEPLOYMENT_REFERENCE.md 及 templates/README.md，實際在這台 Ubuntu VM 部署 q3.qqnas.org 的 Ollama 與 Open WebUI，預設下載 gemma3:1b。先確認原有兩網站、NAS、Docker 和 80／443 入口，保留既有服務。依任務完成內部推論、HTTPS 憑證、自動續期、備份與驗收，將實際進度保存到 DEPLOYMENT_STATUS.md。一般部署步驟直接繼續，只有缺少必要資料或會中斷原有服務時才問我。現在開始唯讀盤點。

Codex 依相依關係持續執行。管理員信箱、憑證聯絡信箱、DNS 或 NAS 權限不足時，集中列出需要你提供的資料；不用預先填一大張主機規格表。

範本中的路徑、版本及資源上限要核對後才使用。正式部署在確認後的目錄，例如 `~/q3-llm`；不要在 Git 範本目錄直接啟動服務。

## 3. 為什麼先用 Gemma 3 1B

`gemma3:1b` 是文字模型；Ollama 頁面在核對時列出約 **806 MB** 的模型下載。它適合先測通安裝、登入與聊天，執行時另需推論快取、WebUI 及系統記憶體，不能把下載大小當 RAM 需求。[Ollama 模型頁](https://ollama.com/library/gemma3:1b)

先從單併發及小上下文開始，根據 VM 剩餘資源設定限制。1B 的中文回答、複雜推理與程式能力應以實測判斷；想改善品質時再評估較大模型。此版不能用來驗收圖片辨識。[Google Gemma 模型種類](https://ai.google.dev/gemma/docs/get_started)

Git 不放模型權重；部署時由 Ollama 下載到資料卷。模型使用依其原有授權條款，不因這個儲存庫而改變。

## 4. 檔案分工

| 檔案／目錄 | 用途 |
| --- | --- |
| AGENTS.md | Codex 在此儲存庫的工作邊界 |
| CODEX_TASK.md | 部署任務、分支判定、交付與驗收標準 |
| DEPLOYMENT_REFERENCE.md | 20 章操作參考，已改用 gemma3:1b |
| templates/ | AI Compose、loopback 增補、Docker Nginx 與環境欄位範本 |
| scripts/inspect-host.sh | 只讀 Linux 盤點工具，不安裝或變更服務 |
| scripts/check_repo.py | 文件語法、Git 排除規則及可選的 Compose 檢查 |
| diagrams/ | 簡圖與三項服務分區圖 |
| VALIDATION.md | 文件檢查與實機驗收邊界 |

部署時產生的 `DEPLOYMENT_STATUS.md`、`OPERATIONS.md` 已加入 Git 排除清單。前者記錄進度，後者記錄這台 VM 的維護方式，Codex 不應自動回推。

## 5. 先做檢查

在目標 Ubuntu 做唯讀盤點：

```bash
bash scripts/inspect-host.sh
```

檢查文件／範本，不啟動服務：

```bash
python3 scripts/check_repo.py
```

有 Docker Compose 時會額外解析範本；沒有時明列跳過。實際 Nginx／Apache 設定檢查、憑證與推論由部署任務在 VM 上執行。

## 6. 中斷與更新

若中斷，下次在同一份儲存庫的 Codex 對話貼：

> 請讀取 CODEX_TASK.md 和 DEPLOYMENT_STATUS.md，核對實際檔案、容器、模型與憑證狀態，接續未完成工作。保留資料與部署，不重做初始化，仍使用 gemma3:1b，繼續至驗收或明確列出缺少的外部條件。

需要取得日後文件更新時，先確認本機修改：

```bash
git status --short
git pull --ff-only
```

Git 更新只更新任務和範本。已部署的 VM 設定由 Codex 比對、備份、做最小修改，不能直接覆蓋正式 .env、Compose 或原有網站。

## 7. 來源與驗證範圍

原始 [Notion 手冊](https://app.notion.com/p/407efa09c19681ee8fb5d78abdd37a0f) 的模型範例為 Qwen；本儲存庫改用 Gemma 3 1B，其他架構原則一致。任務寫法參考 [OpenAI Codex 工作流程](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)，部署授權以 CODEX_TASK.md 為準。

製作儲存庫時未登入目標 VM。本機語法／設定檢查通過，不代表 Ubuntu 服務、正式憑證或自動續期已完成，必須以部署後實測證據驗收。
