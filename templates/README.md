# 範本用法

先完成 CODEX_TASK.md 的唯讀盤點，才選擇並複製範本到實際部署目錄。這裡沒有預設開放外部 Port，也不會自動改原有網站。

| 範本 | 適用 |
| --- | --- |
| compose.yml | 獨立 AI 專案：Ollama + Open WebUI，兩者均不發布主機 Port |
| .env.example | 管理員與固定密鑰欄位；必須在 VM 重新產生及填寫，不用示意值啟動 |
| compose.host.yml | 主機 Apache／Nginx 入口才加上 loopback 3000；部署時併入適用增補檔 |
| webstack.networks.example.yml | 既有 Nginx 使用 default 網路時的例子；已有自訂網路要合併保留 |
| nginx.http.conf | Docker Nginx 首次 HTTP-01 驗證入口 |
| nginx.https.conf | Docker Nginx 已取得正式憑證後的 HTTPS 與串流設定 |

主機 Apache／Nginx 的完整配置在 DEPLOYMENT_REFERENCE.md 第 12 章；第 13 章確認本次僅在 Ubuntu VM 部署，不使用 NAS 前置代理。不要把 Docker Nginx 的路徑和 resolver 套到主機 Nginx。

範本映像版本沿用教材核對值；實際部署前由 Codex 驗證架構相容性與版本。CPU／RAM 上限依實機調整。模型預設為 gemma3:1b，請在 AI 專案啟動後執行：

```bash
# 先 cd 到實際 AI 專案目錄；本例預設為 ~/q3-llm。
cd "$HOME/q3-llm"
docker compose exec -T ollama ollama pull gemma3:1b
docker compose exec -T ollama ollama run gemma3:1b \
  "請用繁體中文，以兩句話說明什麼是反向代理。"
```

上面會實際下載模型並推論，只在目標 VM 的正確專案執行。模型存在 Ollama 的 Volume，不加入 Git。

若需要先測範本解析，從儲存庫根目錄執行：

```bash
docker compose --env-file templates/.env.example \
  -f templates/compose.yml config --quiet
```

這只做設定解析，不建立容器。不要在這份示意 .env 上執行 up。
