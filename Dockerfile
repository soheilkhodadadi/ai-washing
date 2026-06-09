FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AIW_REPO_ROOT=/workspaces/ai-washing \
    AIW_DATA_ROOT=/workspaces/ai-washing-private-data \
    AIW_OUTPUT_ROOT=/workspaces/ai-washing/outputs/reproduced \
    AIW_PAPER_ROOT=/workspaces/ai-washing/outputs/paper_exports

RUN apt-get update \
    && apt-get install -y --no-install-recommends git make gcc g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/ai-washing
COPY requirements-lock.txt pyproject.toml ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements-lock.txt

CMD ["bash"]
