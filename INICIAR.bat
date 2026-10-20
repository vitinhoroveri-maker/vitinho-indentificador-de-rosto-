@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Visio AI - Detector Facial
echo.
echo  ========================================
echo        VISIO AI - DETECTOR FACIAL
echo  ========================================
echo.
where py >nul 2>nul
if errorlevel 1 (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python nao foi encontrado.
    echo Instale em https://www.python.org/downloads/
    echo Marque "Add python.exe to PATH" durante a instalacao.
    pause
    exit /b 1
  )
  set "PY=python"
) else (
  set "PY=py"
)
if not exist ".venv\Scripts\python.exe" (
  echo Preparando ambiente...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo Nao foi possivel criar o ambiente.
    pause
    exit /b 1
  )
)
echo Instalando/verificando bibliotecas. O OpenCV sera fixado numa versao compativel...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo A instalacao falhou. Confira a conexao com a internet.
  pause
  exit /b 1
)
echo.
echo O painel vai abrir no navegador.
echo Se nao abrir automaticamente, acesse http://127.0.0.1:5000
start "" http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
echo.
echo Servidor encerrado.
pause
