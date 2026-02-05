.PHONY: help install extract transform run test docs clean

help:
	@echo "Pokemon ELT Pipeline - Available Commands:"
	@echo ""
	@echo "  make install     - Install Python dependencies"
	@echo "  make extract     - Run extraction phase only"
	@echo "  make transform   - Run transformation phase only"
	@echo "  make run         - Run complete pipeline"
	@echo "  make test        - Run dbt tests"
	@echo "  make docs        - Generate and serve dbt docs"
	@echo "  make clean       - Clean generated files"
	@echo ""

install:
	pip install -r requirements.txt

extract:
	python extract/extract_pokemon.py

transform:
	cd transform/pokemon_dbt && dbt run

run:
	python run_pipeline.py

test:
	cd transform/pokemon_dbt && dbt test

docs:
	cd transform/pokemon_dbt && dbt docs generate && dbt docs serve

clean:
	rm -rf transform/pokemon_dbt/target
	rm -rf transform/pokemon_dbt/logs
	rm -rf transform/pokemon_dbt/dbt_packages
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
