ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}-buster AS build

# Setup env
ENV LANG C.UTF-8 \
    LC_ALL C.UTF-8 \
    PYTHONDONTWRITEBYTECODE 1 \
    PYTHONFAULTHANDLER 1

WORKDIR /usr/src/app

# Install python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install wheel pep517 twine\
 && pip wheel --no-cache-dir -r requirements.txt --wheel-dir=/usr/src/wheels

COPY . .

RUN  python -m pep517.build --out-dir=/usr/src/wheels --binary .

# Run tests
FROM build AS test
#Copy wheels from build stage
COPY --from=build /usr/src/wheels /usr/src/wheels

ARG coverage_limit=95

WORKDIR /usr/src/app
# Separate commands to enable build cache
RUN pip install -r tests/requirements.txt --find-links /usr/src/wheels \
 && git config --global user.email "test@example.com" \
 && git config --global user.name "test" \
 && tox -e py

ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster AS runner

#Copy wheels from build stage
COPY --from=build /usr/src/wheels /usr/src/wheels

RUN pip install --no-index --find-links /usr/src/wheels mypackage
# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

CMD ["mypackage", "--version"]
