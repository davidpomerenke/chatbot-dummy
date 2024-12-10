FROM --platform=linux/amd64 ghcr.io/astral-sh/uv:python3.12-bookworm
WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen
RUN mkdir chatbot
COPY chatbot/*.py chatbot/
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "chatbot/app.py"]
