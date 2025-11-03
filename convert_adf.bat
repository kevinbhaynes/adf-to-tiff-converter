@echo off
REM ADF to GeoTIFF Converter - Windows Batch Script
REM Drag and drop your ADF folder onto this file to convert

echo ============================================================
echo ADF to GeoTIFF Converter
echo ============================================================
echo.

if "%~1"=="" (
    echo No folder provided!
    echo.
    echo How to use:
    echo 1. Drag and drop your ADF folder onto this batch file
    echo 2. Or run: convert_adf.bat "C:\path\to\adf_folder"
    echo.
    pause
    exit /b 1
)

echo Input: %~1
echo.

REM Run the Python script
python adf_to_geotiff.py "%~1"

echo.
pause
