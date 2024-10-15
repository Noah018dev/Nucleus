@echo off
cls
title Nucleus - CleanDisk
echo Cleaning up, the file %1 isn't deleting properly, so we're forcing it.
timeout /t 2 /nobreak > nul
del %1
exit