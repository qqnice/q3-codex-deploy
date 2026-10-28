#!/usr/bin/env bash
# Read-only: no sudo, installation, Docker mutation, or full environment dump.
set -u
export LC_ALL=C

if [ "$(uname -s)" != "Linux" ]; then
  printf '%s\n' '此工具應在目標 Linux VM 執行；目前主機不是 Linux。' >&2
  exit 2
fi

section() { printf '\n## %s\n' "$1"; }
run() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf '未安裝：%s\n' "$1"
    return 0
  fi
  "$@" || printf '檢查未完成（權限／版本／服務狀態需另確認）：%s\n' "$1"
}

section '主機'
run whoami
run hostname
run uname -m
if [ -r /etc/os-release ]; then
  sed -n '/^\(PRETTY_NAME\|VERSION_ID\|ID\)=/p' /etc/os-release
fi

section 'Docker 連線對象（先確認沒有指向其他主機）'
run docker context show
run docker context ls --format '{{.Name}} {{.DockerEndpoint}} {{.Current}}'
run docker version --format 'Client={{.Client.Version}} Server={{.Server.Version}}'
run docker compose version
run docker compose ls
run docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

section '入口程序與服務'
run ss -ltnp
run systemctl is-active apache2 nginx docker

section '資源'
run free -h
run nproc
run df -h
run docker stats --no-stream
run ip -br address

section 'q3 公開 DNS'
run dig +short A q3.qqnice.org
run dig +short AAAA q3.qqnice.org
run dig +short CAA qqnice.org

printf '\n%s\n' '盤點結束。未更動任何服務；結果不等於部署通過。'
