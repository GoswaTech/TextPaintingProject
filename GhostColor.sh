#!/bin/bash

if [ "$1" == "-c" ]; then
	python src/TextPaintingProjectConsole.py
else
	python src/TextPaintingProjectGraphic.py
fi
