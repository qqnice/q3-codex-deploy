# 驗證紀錄與範圍

本儲存庫交給目標 Ubuntu 上的 Codex 執行。建立儲存庫時沒有連入目標 VM，也沒有啟動部署。

## 文件與範本

- 原始離線手冊曾與已發佈 Notion 手冊比對，76 個程式碼區塊內容一致。
- 本次將離線手冊與任務的預設模型改為 gemma3:1b，移除 Qwen 的 /no_think 範例；Notion 原文未改寫。
- 手冊保留 20 章、73 個 Bash 區塊、2 個 Mermaid 區塊及 1 個 YAML 區塊，兩張圖使用本機相對路徑。
- scripts/check_repo.py 檢查 Bash 語法、手冊完整性、模型設定、圖片連結與 Git 排除規則。
- 使用 Docker Compose v5.6.1 解析 AI 主範本與主機代理增補檔，檢查主線沒有公開 AI Port、Ollama 網路、WebUI 別名、Volume 名稱，以及主機分支只綁 loopback 3000。
- 原手冊的舊專案合併測試確認只增加 Nginx 網路，未改其他原服務；實機自訂配置仍需核對。
- Git 發布前檢查追蹤清單，排除密碼、私鑰、憑證、模型、聊天資料、備份與主機紀錄；templates/.env.example 只有明確示意值。

## 目標 VM 尚待驗證

- 實際 Docker／Compose、Nginx／Apache／NAS 入口與可用資源。
- 容器啟動、Gemma 3 下載和推論、登入與瀏覽器串流。
- 外部 DNS／Port、正式憑證申請及續期排程。
- 持久化、一致性備份，以及既有網站與 NAS 前後比較。

這些必須由 Ubuntu 上的 Codex 依 CODEX_TASK.md 執行，將證據記錄到本機 DEPLOYMENT_STATUS.md。文件檢查不能替代實機驗收。
