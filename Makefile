.PHONY: help
help:
	@echo "Available targets:"
	@echo "  help             : Show this help message"
	@echo "  lint             : Run Ruff linter"
	@echo "  test             : Run tests using pytest"
	@echo "  format           : Sort imports and format code with Ruff"

.PHONY: lint
lint:
	@echo "==> Running Ruff linter..."
	@poetry run ruff check elevator/ test/

.PHONY: test
test:
	@echo "==> Running tests..."
	@poetry run pytest test/

.PHONY: format
format:
	@echo "=====> Formatting code..."
	@poetry run ruff check --select I --fix elevator/ test/
	@poetry run ruff format elevator/ test/
