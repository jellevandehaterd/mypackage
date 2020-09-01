ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}-buster AS build

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install wheel \
 && pip wheel --no-cache-dir -r requirements.txt --wheel-dir=/usr/src/wheels

COPY . .

RUN pip wheel . --wheel-dir=/usr/src/wheels

ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster AS runner

WORKDIR /usr/src/app

COPY --from=build /usr/src/wheels /usr/src/wheels
COPY --from=build /usr/src/app .

RUN pip install --no-index --find-links /usr/src/wheels mypackage

CMD ["python", "-m", "mypackage", "--version"]
