FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/workspaces/ai-washing/src \
    AIW_REPO_ROOT=/workspaces/ai-washing \
    AIW_DATA_ROOT=/workspaces/ai-washing-private-data \
    AIW_OUTPUT_ROOT=/workspaces/ai-washing/outputs/reproduced \
    AIW_PAPER_ROOT=/workspaces/ai-washing/outputs/paper_exports \
    HOME=/tmp \
    MPLCONFIGDIR=/tmp/aiw-matplotlib \
    XDG_CACHE_HOME=/tmp/aiw-cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash git make gcc g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/ai-washing
COPY requirements-lock.txt requirements-dashboard.txt pyproject.toml ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements-lock.txt \
    && python -m pip install -r requirements-dashboard.txt \
    && python -m pip check

COPY . .
RUN mkdir -p outputs/reproduced outputs/paper_exports /workspaces/ai-washing-private-data /tmp/aiw-matplotlib /tmp/aiw-cache \
    && chmod 1777 /tmp/aiw-matplotlib /tmp/aiw-cache \
    && python -m pip install -e . \
    && make validate path-leak-scan import-smoke

CMD ["bash"]
