#!/bin/bash
for f in `find ima/*.seq`; do ./sequence.py $f; done
