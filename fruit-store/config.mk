# MISC

PROJECT_NAME:=Fruit Store
VERSION:=0 #$(shell git describe --tags --abbrev=0)
PACKAGE:=fruit_store
TEST_PACKAGE:=fruit_store_test/

# TERMINAL
BOLD:=$(shell tput bold)
BOLD_STOP:=$(shell tput sgr0)
UNDERLINE=$(shell tput smul)
UNDERLINE_STOP=$(shell tput rmul)
#
# DOCKER
DOCKERFILE:=docker/Dockerfile
IMAGE_NAME_SERVER:=fruit-store-server
IMAGE_NAME_CLIENT:=fruit-store-client

# GRPC
GRPC_DIR:=./proto
GRPC_ANNOT:=./$(PACKAGE)/annot/
GRPC_FILE:=./proto/fruit_store/grpc/*.proto

# https://github.com/grpc/grpc/issues/9575
GRPC_OPT:=-I$(GRPC_DIR) --python_out=. --pyi_out=$(GRPC_ANNOT) --grpc_python_out=.

# COMMANDS
CMD_DOCKER_BUILD:=docker build --build-arg APP_REVISION=$(REVISION) --build-arg APP_VERSION=$(VERSION)
CMD_DOCKER_EXPORT:=docker save
CMD_GZIP:=gzip
CMD_INSTALL:=pdm sync
CMD_RUN:=VERSION=$(VERSION) pdm run
CMD_TAR:=tar czf
CMD_GRPC_BUILD=$(CMD_RUN) python -m grpc_tools.protoc
CMD_GRPC_SERVER:=$(CMD_RUN) python -m fruit_store.cli.server

APP_CONFIG=DB_URI=$(DB_URI) DEBUG=True REVISION=$(REVISION) VERSION=$(VERSION)

CMD_SERVER:=$(APP_CONFIG) $(CMD_RUN) uvicorn --reload
CMD_LYNT:=$(CMD_RUN) ruff check
CMD_FMT:=$(CMD_RUN) ruff format
CMD_TYPE:=$(CMD_RUN) pyright
CMD_TEST:=$(CMD_RUN) coverage run -m pytest -v
CMD_CLEAN:=$(CMD_RUN) ruff clean # && rm -f $(FILES_CLEAN)

# STANDARD DOCKER OPTS
DOCKER_OPT_SERVER:= --target=server -t $(IMAGE_NAME_SERVER):latest -t $(IMAGE_NAME_SERVER):$(VERSION)
DOCKER_OPT_CLIENT:= --target=client -t $(IMAGE_NAME_CLIENT):latest -t $(IMAGE_NAME_CLIENT):$(VERSION)

# FILE OUTPUTS
DIR_TARBALL:=dist/tarball
FILE_TARBALL:=$(DIR_TARBALL)/fruit-store-$(VERSION).tar
DIR_DOCKER_EXPORT=dist/docker-export
FILE_DOCKER_EXPORT_SERVER:=$(DIR_DOCKER_EXPORT)/fruit-store-server-$(VERSION).tar
FILE_DOCKER_EXPORT_CLIENT:=$(DIR_DOCKER_EXPORT)/fruit-store-client-$(VERSION).tar
