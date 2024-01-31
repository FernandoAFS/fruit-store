# GLOBAL ARGS
ARG PYTHON_VERSION=3.11
ARG NODE_VERSION=16.20.2
ARG VERSION
ARG REVISION


# COMPILER
FROM python:${PYTHON_VERSION} AS builder

# install PDM
RUN pip install -U pip setuptools wheel pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY fruit_store/ /project/fruit_store

# install dependencies and project into the local packages directory
WORKDIR /project

# TODO: INCLUDE GRPC BOILERPLATE BUILD

# 2 step pdm-sync and
ENV VERSION=${VERSION}
RUN mkdir __pypackages__ && pdm sync -v --prod --no-editable


# RUNNER
FROM python:${PYTHON_VERSION} as runner-base
ARG PYTHON_VERSION=3.11

VOLUME /var/data

# INCLUDE GOSU AND TINI AND UNPRIVILEDGED USERS
RUN set -eux; \
	apt-get update; \
	apt-get install -y gosu tini; \
	rm -rf /var/lib/apt/lists/*; \
    groupadd --gid 999 fruit-store; \
    useradd --uid 999 -g fruit-store -b /project -M -s /bin/sh fruit-store;

WORKDIR /project

# retrieve packages from build stage
COPY --from=builder /project/__pypackages__/${PYTHON_VERSION}/lib /project/pkgs
COPY --from=builder /project/__pypackages__/${PYTHON_VERSION}/bin/* /bin/

COPY docker/entrypoint.sh /project/

ENV VERSION=${APP_VERSION}
ENV REVISION=${APP_REVISION}

ENV DATA_PATHS = "/var/data"
ENV PYTHONPATH=/project/pkgs
ENV USER="999:999"
 #ENV PATH="/project:$PATH"
ENV HOST_PORT="50051"
EXPOSE 50051


ENTRYPOINT ["./entrypoint.sh"]


# RUNNER
FROM runner-base as server
CMD [ "server" ]

FROM runner-base as client
CMD [ "client" ]
