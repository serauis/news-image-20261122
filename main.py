#!/usr/bin/env python3
"""Entry program for news-image-20261122: copy the pre-drawn front page
to the grader's output path. Deterministic, standard library only."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(HERE, "entry.png")

if not os.path.isfile(SRC):
    sys.exit("entry.png missing from repository")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
