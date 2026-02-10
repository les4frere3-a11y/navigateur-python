@echo off
echo ========================================
echo Installation des dependances PyQt5
echo ========================================
echo.

REM Verification de Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo Python detecte:
python --version
echo.

REM Mise a jour de pip
echo Mise a jour de pip...
python -m pip install --upgrade pip
echo.

REM Installation de PyQt5
echo Installation de PyQt5...
python -m pip install PyQt5
if %errorlevel% neq 0 (
    echo ERREUR: L'installation de PyQt5 a echoue
    pause
    exit /b 1
)
echo.

REM Installation de PyQtWebEngine
echo Installation de PyQtWebEngine...
python -m pip install PyQtWebEngine
if %errorlevel% neq 0 (
    echo ERREUR: L'installation de PyQtWebEngine a echoue
    pause
    exit /b 1
)
echo.

echo ========================================
echo Installation terminee avec succes!
echo ========================================
echo.
echo Vous pouvez maintenant lancer le navigateur avec:
echo python navigateur_web(2).py
echo.
pause
