#!/usr/bin/env python3
"""Offline repository checks; optionally validate with an installed Compose CLI."""
from pathlib import Path
import json, os, re, shutil, subprocess, sys

root = Path(__file__).resolve().parents[1]
def check(command, **kwargs):
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, **kwargs)
    if result.returncode:
        # Never print expanded Compose config; it could contain real secrets.
        raise SystemExit(f"Check failed: {command[0]} (exit {result.returncode})")
    return result.stdout

bash_count = 0
for path in root.rglob("*.md"):
    if ".git" in path.parts:
        continue
    for lang, body in re.findall(r"^```(\w+)\n(.*?)^```[ \t]*$", path.read_text(), re.M | re.S):
        if lang == "bash":
            check(["bash", "-n"], input=body)
            bash_count += 1
for path in (root / "scripts").glob("*.sh"):
    check(["bash", "-n", str(path)])

task = (root / "CODEX_TASK.md").read_text()
guide = (root / "DEPLOYMENT_REFERENCE.md").read_text()
assert "gemma3:1b" in task and "gemma3:1b" in guide
assert "qwen3:1.7b" not in guide
assert "/no_think" not in guide
assert "file-upload://" not in guide
assert "notion-file-block://" not in guide
assert len(re.findall(r"^# \d+ ", guide, re.M)) == 20
assert len(re.findall(r"^```bash$", guide, re.M)) == 73
assert len(re.findall(r"^```mermaid$", guide, re.M)) == 2
for image in re.findall(r"!\[[^\]]*\]\((diagrams/[^)]+)\)", guide):
    assert (root / image).is_file(), image

secret_names = [
    ".env", "templates/.env", ".env.production", "certbot/private.pem",
    "runtime/credentials.json", "backups/test.tar.gz", "models/model.gguf",
    "DEPLOYMENT_STATUS.md", "OPERATIONS.md", "webui.db", "private.key"
]
git_ignore_checked = False
if (root / ".git").exists():
    for name in secret_names:
        check(["git", "check-ignore", "--no-index", "--quiet", name])
    example = subprocess.run(["git", "check-ignore", "--no-index", "--quiet",
                              "templates/.env.example"], cwd=root)
    assert example.returncode == 1, "Public example must not be ignored"
    git_ignore_checked = True

compose = os.environ.get("DOCKER_COMPOSE_BIN")
if compose:
    compose_cmd = [compose]
elif shutil.which("docker"):
    probe = subprocess.run(["docker", "compose", "version"], capture_output=True)
    compose_cmd = ["docker", "compose"] if probe.returncode == 0 else None
else:
    compose_cmd = None

compose_checked = False
if compose_cmd:
    base = compose_cmd + ["--env-file", "templates/.env.example",
                          "-f", "templates/compose.yml"]
    def resolve(extra=()):
        return json.loads(check(base + list(extra) + ["config", "--format", "json"]))
    config = resolve()
    assert config["name"] == "q3-llm"
    services = config["services"]
    assert set(services) == {"ollama", "open-webui"}
    assert not services["ollama"].get("ports")
    assert not services["open-webui"].get("ports")
    assert set(services["ollama"]["networks"]) == {"ai"}
    assert set(services["open-webui"]["networks"]) == {"ai", "proxy"}
    assert config["networks"]["proxy"]["external"]
    assert config["networks"]["proxy"]["name"] == "q3-proxy"
    assert "q3-open-webui" in services["open-webui"]["networks"]["proxy"]["aliases"]
    assert services["open-webui"]["environment"]["ENABLE_SIGNUP"] == "false"
    assert services["open-webui"]["environment"]["OLLAMA_BASE_URL"] == "http://ollama:11434"
    assert services["ollama"]["environment"]["OLLAMA_NO_CLOUD"] == "1"
    assert config["volumes"]["ollama-data"]["name"] == "q3-llm_ollama-data"
    assert config["volumes"]["openwebui-data"]["name"] == "q3-llm_openwebui-data"
    host = resolve(["-f", "templates/compose.host.yml"])
    ports = host["services"]["open-webui"]["ports"]
    assert len(ports) == 1 and ports[0]["host_ip"] == "127.0.0.1"
    assert str(ports[0]["published"]) == "3000" and ports[0]["target"] == 8080
    assert not host["services"]["ollama"].get("ports")
    compose_checked = True

print(json.dumps({
    "status": "passed", "bash_blocks": bash_count,
    "git_ignore_checked": git_ignore_checked,
    "compose_checked": compose_checked, "live_deployment_tested": False,
    "note": "Compose checks are skipped when no CLI is installed; no containers are started."
}, ensure_ascii=False, indent=2))
