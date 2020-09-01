ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}-buster AS build

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /usr/src/app

# Install python dependencies
COPY requirements.txt ./
RUN pip install wheel \
 && pip wheel --no-cache-dir -r requirements.txt --wheel-dir=/usr/src/wheels

COPY . .

RUN pip wheel . --wheel-dir=/usr/src/wheels

ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster AS runner

#Copy wheels from build stage
COPY --from=build /usr/src/wheels /usr/src/wheels


# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

RUN pip install --no-index --find-links /usr/src/wheels mypackage

CMD ["mypackage", "--version"]
