VENV := .venv
PY := $(VENV)/bin/python
PIP := $(PY) -m pip

.PHONY: venv install run trends clean

venv:
	python3 -m venv $(VENV)
	$(PIP) install -U pip

install: venv
	$(PIP) install -e .

run: install
	$(VENV)/bin/mirrorwalk run \
		--grammar sefer --dim 6 --steps 256 --seed 42 \
		--walker adaptive --objective "novelty+structure+avoid-loops" \
		--memory $$HOME/.mirrorwalk/memory.sqlite \
		--style mythic

trends: install
	$(VENV)/bin/mirrorwalk trends --memory $$HOME/.mirrorwalk/memory.sqlite --limit 20

clean:
	rm -rf $(VENV) runs
