VERSION = $(shell git log -1 --date=format:%Y-%m-%d --pretty=format:%cd-%h)

default:
	@echo "Scott-Arthur-CV-$(VERSION)" | tee /dev/tty | tr -d "\n" | pbcopy
