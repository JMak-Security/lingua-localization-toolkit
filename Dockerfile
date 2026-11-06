FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2,<27" \
    && python -m pip install --no-cache-dir . \
    && mkdir -p /output \
    && chown 10001:10001 /output
COPY examples/ examples/

VOLUME ["/output"]
USER 10001:10001
ENTRYPOINT ["lingua"]
CMD ["check", "examples/en.json", "examples/qps-ploc.json", "--report", "/output/check.json"]
