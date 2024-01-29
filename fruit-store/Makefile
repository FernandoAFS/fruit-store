include config.mk

help:
	@echo "$(PROJECT_NAME) python monorepo (version: $(VERSION))"
	@echo ""
	@echo "- $(BOLD)install$(BOLD_STOP): Installs all dependencies (dev-dependencies included)"
	@echo "- $(BOLD)up$(BOLD_STOP): Start application in development mode."
	@echo "- $(BOLD)grpc$(BOLD_STOP): Generate grpc boilerplate."
	@echo ""
	@echo "$(UNDERLINE)$(BOLD)Exporting$(UNDERLINE_STOP)$(BOLD_STOP)"
	@echo "- $(BOLD)docker-export$(BOLD_STOP): Generates docker images export at $(DIR_DOCKER_EXPORT)"
	@echo "- $(BOLD)tarball$(BOLD_STOP): Generates a tarball distribution of source: $(FILE_TARBALL)"
	@echo ""
	@echo "$(UNDERLINE)$(BOLD)Building$(UNDERLINE_STOP)$(BOLD_STOP)"
	@echo "- $(BOLD)docker$(BOLD_STOP): Generates all docker images"
	@echo "\t- $(BOLD)docker-server$(BOLD_STOP)"
	@echo "\t- $(BOLD)docker-client$(BOLD_STOP)"
	@echo ""
	@echo "$(UNDERLINE)$(BOLD)Tools:$(UNDERLINE_STOP)$(BOLD_STOP)"
	@echo "- $(BOLD)clean$(BOLD_STOP): Removes tarballs, caches and temp files"
	@echo "- $(BOLD)lynt$(BOLD_STOP): Runs linter on code"
	@echo "- $(BOLD)fmt$(BOLD_STOP): Runs formatter"
	@echo "- $(BOLD)type$(BOLD_STOP): Runs format checks"
	@echo "- $(BOLD)test$(BOLD_STOP): Runs all tests"

# MISC

install:
	$(CMD_INSTALL)

# RUN/DEVELOP

grpc:
	@mkdir -p $(GRPC_ANNOT)
	$(CMD_GRPC_BUILD) $(GRPC_OPT) $(GRPC_FILE)

up: grpc
	$(CMD_GRPC_SERVER)

# BUILD
docker: docker-server docker-client

docker-server:
	$(CMD_DOCKER_BUILD) $(DOCKER_OPT_SERVER) -f $(DOCKERFILE) .

docker-client:
	$(CMD_DOCKER_BUILD) $(DOCKER_OPT_CLIENT) -f $(DOCKERFILE) .


# EXPORT

docker-export: docker
	@mkdir -p $(DIR_DOCKER_EXPORT)
	$(CMD_DOCKER_EXPORT) \
		$(IMAGE_NAME_SERVER):latest $(IMAGE_NAME_SERVER):$(VERSION) \
		> $(FILE_DOCKER_EXPORT_SERVER)
	$(CMD_DOCKER_EXPORT) \
		$(IMAGE_NAME_CLIENT):latest $(IMAGE_NAME_CLIENT):$(VERSION) \
		> $(FILE_DOCKER_EXPORT_SERVER)

tarball:
	@mkdir -p $(DIR_TARBALL)
	git ls-files | xargs $(CMD_TAR) $(FILE_TARBALL)

# TOOLS
#
clean:
	$(CMD_CLEAN)

lynt:
	$(CMD_LYNT) $(PACKAGE)

fmt:
	$(CMD_FMT) $(PACKAGE)

type:
	$(CMD_TYPE) $(PACKAGE)

test:
	$(CMD_TEST) $(TEST_PACKAGE)
