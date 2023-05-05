VERSION = $(shell git log -1 --date=format:%Y-%m-%d --pretty=format:%cd-%h)

build:
	mkdir -p public/.well-known
	jq --null-input --arg version $(VERSION) '{version: $$version}' \
	  > public/.well-known/build.json
	hugo

version:
	@echo "Scott-Arthur-CV-$(VERSION)" | tee /dev/tty | tr -d "\n" | pbcopy
