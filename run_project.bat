@echo off
title IoT Honeypot Launcher
echo ==========================================
echo   Intelligent IoT Honeypot - DEMO START
echo ==========================================

echo.
echo [1/4] Starting Honeypot Server...
start "1. Honeypot Listener" cmd /k "python honeypot.py"

echo.
echo [2/4] Waiting for server to initialize...
timeout /t 3 >nul

echo.
echo [3/4] Launching Attack Simulation...
start "2. Attacker Botnet" cmd /c "python simulate_attack.py & echo. & echo Attack Complete! Closing in 5s... & timeout /t 5"

echo.
echo      Waiting for attack to generate logs...
timeout /t 5 >nul

echo.
echo [4/4] Running AI Analysis...
start "3. Analysis Engine" cmd /c "python analyzer.py & echo. & echo Analysis Done. You can close this window. & pause"

echo.
echo [Done] Launching Dashboard...
echo      Go to http://127.0.0.1:8080 in your browser.
start "4. Web Dashboard" cmd /k "python dashboard.py"

echo.
echo All systems go!
pause