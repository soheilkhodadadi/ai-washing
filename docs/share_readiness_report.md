# Share Readiness Report

This report checks whether the AI Washing workstation can be used through the low-friction Docker path.

## Environment Boundary

- Docker image: `ai-washing:local`
- Private data root provided: `yes`
- Private data are mounted read-only at `/workspaces/ai-washing-private-data` when provided.
- Private data are not copied into the image.

## Severity Counts

- `ok`: 7

## Check Results

- `docker_cli_available`: `ok` / `pass` / return `0`
- `docker_engine_available`: `ok` / `pass` / return `0`
- `docker_compose_available`: `ok` / `pass` / return `0`
- `docker_image_build`: `ok` / `pass` / return `0`
- `docker_code_only_preflight`: `ok` / `pass` / return `0`
- `docker_private_data_absent_fails_cleanly`: `ok` / `pass` / return `2`
- `docker_private_data_mount_check`: `ok` / `pass` / return `0`
