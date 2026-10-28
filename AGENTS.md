# Repository instructions

This repository is an Ubuntu deployment task kit for q3.qqnice.org, using Ollama, Open WebUI, and the small local model gemma3:1b.

- When the user asks to deploy on a Linux VM, read CODEX_TASK.md first, then DEPLOYMENT_REFERENCE.md and templates/README.md. Verify the actual host and existing services before modifying anything.
- When editing or reviewing this repository, work on the repository only. Do not interpret the deployment instructions as permission to deploy on the development computer.
- Preserve the two existing websites and NAS. Discover who owns ports 80/443, then extend the actual proxy. Never replace the host architecture merely to match a template.
- Keep runtime files outside Git: credentials, certificates, models, backups, chat databases, DEPLOYMENT_STATUS.md, and OPERATIONS.md. Use the existing .gitignore and check staged files before committing.
- Treat templates as examples until host discovery is complete. There is intentionally no universal install.sh.
- The default model is gemma3:1b, a text-only model. Do not substitute gemma3:latest or a larger model without the user's direction.
- For changes, run python3 scripts/check_repo.py. When Docker Compose is available, also validate templates with its config command; do not start containers during repository-only checks.
- Report only checks actually performed. Local syntax/config checks do not establish live deployment, DNS, TLS, renewal, or browser success.
- Use Traditional Chinese for user-facing explanations and documentation.
