@echo off
REM This batch file attempts to connect to an external domain using the ping command.
REM It is designed for simple network connectivity simulation.

REM Define the target external domain.
REM For simulation purposes, we are using mandiant.com.
SET TARGET_DOMAIN=mandiant.com

ECHO.
ECHO Attempting to ping %TARGET_DOMAIN%...
ECHO This will send a few network packets to the target domain.
ECHO.

REM The 'ping' command sends ICMP echo requests.
REM It can resolve domain names to IP addresses automatically.
REM -n 4: Sends 4 echo requests.
REM -w 1000: Waits 1000 milliseconds (1 second) for each reply.
ping %TARGET_DOMAIN% -n 4 -w 1000

REM Check the error level to determine if the ping was successful.
IF %ERRORLEVEL% EQU 0 (
    ECHO.
    ECHO Ping to %TARGET_DOMAIN% was successful. Network connectivity is likely established.
) ELSE (
    ECHO.
    ECHO Ping to %TARGET_DOMAIN% failed or timed out. There might be no network connectivity or the host is unreachable.
)

ECHO.
ECHO Script finished.
PAUSE
REM The PAUSE command keeps the command prompt window open until you press a key,
REM allowing you to review the ping results.
