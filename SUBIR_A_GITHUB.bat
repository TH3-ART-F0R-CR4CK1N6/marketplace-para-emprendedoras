@echo off
echo ========================================
echo Subiendo Marketplace a GitHub
echo ========================================
echo.

cd "c:\All mio\Python projectos goood\Pagina marketplace"

echo [1/2] Verificando configuracion de Git...
git remote -v

echo.
echo [2/2] Subiendo a GitHub...
git push -u origin main

echo.
echo ========================================
echo LISTO! Tu proyecto esta en GitHub
echo URL: https://github.com/TH3-ART-F0R-CR4CK1N6/marketplace-emprendedoras
echo ========================================
echo.
pause
