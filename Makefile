PYTHON := ./venv/bin/python
PIP := ./venv/bin/pip
PYINSTALLER := ./venv/bin/pyinstaller

.PHONY: all run build install venv clean

all: run

venv:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

install:
	$(PIP) install -r requirements.txt

run:
	PYTHONPATH=src $(PYTHON) src/main.py

build:
	$(PYINSTALLER) \
		--name "EpicSevenX11ShopRefresher" \
		--onefile \
		--windowed \
		--paths src \
		--add-data "assets:assets" \
		--collect-all easyocr \
		--collect-all torch \
		--collect-all torchvision \
		--collect-all Xlib \
		--noconfirm \
		src/main.py

clean:
	rm -rf build dist *.spec src/__pycache__
