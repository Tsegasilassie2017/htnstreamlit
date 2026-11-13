.PHONY: install data train evaluate all app test synthetic

install:
	pip install -r requirements.txt

synthetic:           ## smoke-test data (NOT real)
	python scripts/make_synthetic_data.py

data:                ## validate, clean, split
	PYTHONPATH=src python -m htn.pipeline --stage data

train:               ## compare models, tune best, save artifact
	PYTHONPATH=src python -m htn.pipeline --stage train

evaluate:            ## one-time test-set evaluation
	PYTHONPATH=src python -m htn.pipeline --stage evaluate

all:
	PYTHONPATH=src python -m htn.pipeline --stage all

app:
	streamlit run htnstreamlit.py

test:
	pytest -q
