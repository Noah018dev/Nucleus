@echo off
title Nucleus - Workshop Cleaner
cls
echo Clearing __pycache__
rmdir /s /q __pycache__
echo Clearing workshop...
rmdir /s /q C:\Nucleus
exit