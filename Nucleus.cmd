@echo off
python compress.py
python nucleus_core.zip %*
del nucleus_core.zip /s /q > nul...