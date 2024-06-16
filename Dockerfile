FROM python:alpine
# LABEL maintainer="maintainer.com"

# Make sure outputs are not buffered (set directly to stdout)
ENV PYTHONUNBUFFERED 1

# Copy requirements set working dir
COPY ./requirements.txt ./tmp/requirements.txt
COPY . /app/backend
WORKDIR /app

# Expose port 8000 in the docker container
EXPOSE 8000

# Create virtual env install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # download necessary packages using alpine pkg manager
    # don't cache and use virtual to stay lightweight
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    # Install dependencies to virtual env
    /py/bin/pip install -r /tmp/requirements.txt && \ 
    # CLEAN UP INSTALLS
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # add new user for security purposes 
    adduser \
        --disabled-password \ 
        --no-create-home \
        api-user

ENV PATH="/py/bin:$PATH"

USER api-user