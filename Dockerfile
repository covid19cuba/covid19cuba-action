FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app jsonschema
RUN pip install --target=/app importlib_metadata
RUN pip install --target=/app python-telegram-bot
RUN pip install --target=/app feedparser
RUN pip install --target=/app requests
RUN pip install --target=/app bs4
RUN pip install --target=/app lxml
RUN pip install --target=/app parsel

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py", "--production"]
