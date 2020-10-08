FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip3 install --target=/app Cython
RUN pip3 install --target=/app jsonschema
RUN pip3 install --target=/app importlib_metadata
RUN pip3 install --target=/app python-telegram-bot
RUN pip3 install --target=/app feedparser
RUN pip3 install --target=/app requests
RUN pip3 install --target=/app bs4

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py", "--production"]
