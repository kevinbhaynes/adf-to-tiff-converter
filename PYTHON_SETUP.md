# Python ADF to GeoTIFF Converter - Setup Guide

This Python script provides a reliable, desktop-based solution for converting ESRI ArcInfo Binary Grid (.adf) files to GeoTIFF format.

## Quick Start

### For Windows Users

**Option 1: Use OSGeo4W (Recommended)**

1. **Download and Install OSGeo4W**
   - Go to: https://trac.osgeo.org/osgeo4w/
   - Download the OSGeo4W installer
   - Run the installer and select "Express Install"
   - Choose "GDAL" in the package list

2. **Open OSGeo4W Shell**
   - Search for "OSGeo4W Shell" in Start Menu
   - Right-click and "Run as Administrator"

3. **Navigate to your script location**
   ```bash
   cd C:\path\to\adf-to-tiff-converter
   ```

4. **Run the converter**
   ```bash
   python adf_to_geotiff.py C:\path\to\your\adf_folder
   ```

**Option 2: Use Anaconda/Miniconda**

1. **Install Miniconda**
   - Download from: https://docs.conda.io/en/latest/miniconda.html
   - Install for your system

2. **Create a GIS environment**
   ```bash
   conda create -n gis python=3.9
   conda activate gis
   conda install -c conda-forge gdal
   ```

3. **Run the converter**
   ```bash
   python adf_to_geotiff.py C:\path\to\your\adf_folder
   ```

### For Mac/Linux Users

**Option 1: Using Homebrew (Mac)**

```bash
# Install GDAL
brew install gdal

# Install Python GDAL bindings
pip3 install GDAL==$(gdal-config --version)

# Run the converter
python3 adf_to_geotiff.py /path/to/your/adf_folder
```

**Option 2: Using apt (Ubuntu/Debian)**

```bash
# Install GDAL
sudo apt-get update
sudo apt-get install gdal-bin python3-gdal

# Run the converter
python3 adf_to_geotiff.py /path/to/your/adf_folder
```

**Option 3: Using Anaconda (All platforms)**

```bash
# Create environment
conda create -n gis python=3.9
conda activate gis
conda install -c conda-forge gdal

# Run the converter
python adf_to_geotiff.py /path/to/your/adf_folder
```

## Usage

### Basic Usage

Convert an ADF folder to GeoTIFF (creates `output_converted.tif`):

```bash
python adf_to_geotiff.py /path/to/adf_folder
```

### Specify Output Name

```bash
python adf_to_geotiff.py /path/to/adf_folder my_output.tif
```

### Specify Compression

```bash
python adf_to_geotiff.py /path/to/adf_folder output.tif DEFLATE
```

**Compression Options:**
- `LZW` - Lossless, widely supported (default)
- `DEFLATE` - Lossless, better compression for some data
- `NONE` - No compression (larger files, faster processing)

## What the Script Does

1. ✅ Opens your ADF dataset
2. ✅ Reads all spatial metadata (projection, geotransform)
3. ✅ Preserves NoData values
4. ✅ Copies all raster bands
5. ✅ Creates a properly formatted GeoTIFF
6. ✅ Applies compression for smaller file size
7. ✅ Verifies the output is readable

## Output

The script will create a GeoTIFF file that:
- ✅ Opens in ArcGIS Pro without errors
- ✅ Maintains the correct coordinate system
- ✅ Preserves all spatial information
- ✅ Uses industry-standard compression
- ✅ Works in QGIS, GDAL, and all GIS software

## Example Output

```
============================================================
ADF to GeoTIFF Converter
============================================================

📁 Input directory: /data/my_grid

🔍 Opening ADF dataset...
✅ ADF dataset opened successfully

📊 Dataset Information:
   Size: 1024 x 768 pixels
   Bands: 1
   Projection: NAD_1983_UTM_Zone_17N
   Origin: (500000.00, 4500000.00)
   Pixel Size: (30.00, -30.00)
   NoData Value: -9999.0
   Data Type: Float32

🔄 Converting to GeoTIFF...
   Output: my_grid_converted.tif
   Compression: LZW
✅ Conversion successful!
   Output size: 2.45 MB

🔍 Verifying output...
✅ Output file verified successfully
   Size: 1024 x 768 pixels

============================================================
✅ CONVERSION COMPLETE!
============================================================

Your GeoTIFF is ready: my_grid_converted.tif
You can now open it in ArcGIS Pro, QGIS, or any GIS software.
```

## Troubleshooting

### "No module named 'osgeo'"

**Problem:** Python can't find GDAL

**Solution:**
- Make sure GDAL is installed: `pip install GDAL` or use conda
- On Windows, use OSGeo4W Shell
- Check installation: `python -c "from osgeo import gdal; print(gdal.__version__)"`

### "Failed to open ADF dataset"

**Problem:** ADF files are incomplete or corrupted

**Solution:**
- Make sure ALL ADF files are in the same folder (hdr.adf, w001001.adf, etc.)
- Verify the files open in ArcGIS Pro or QGIS first
- Check file permissions

### "Import Error: DLL load failed"

**Problem:** GDAL library dependencies missing (Windows)

**Solution:**
- Use OSGeo4W Shell instead of regular Command Prompt
- Or install via conda which handles dependencies automatically

## Batch Processing

To convert multiple ADF datasets, create a batch script:

**Windows (batch.bat):**
```batch
@echo off
python adf_to_geotiff.py "C:\data\grid1"
python adf_to_geotiff.py "C:\data\grid2"
python adf_to_geotiff.py "C:\data\grid3"
pause
```

**Mac/Linux (batch.sh):**
```bash
#!/bin/bash
python3 adf_to_geotiff.py /data/grid1
python3 adf_to_geotiff.py /data/grid2
python3 adf_to_geotiff.py /data/grid3
```

## Need Help?

If you encounter any issues:
1. Check that GDAL is properly installed
2. Verify your ADF files are complete and readable
3. Try opening the ADF in QGIS first to confirm it's valid
4. Check the error message for specific details

## Why This Works Better Than the Web Version

✅ **Uses native GDAL** - Direct access to the full GDAL library
✅ **No browser limitations** - Can handle any file size
✅ **Better error messages** - See exactly what went wrong
✅ **Proven and stable** - GDAL has been the industry standard for 20+ years
✅ **Works offline** - No internet connection needed
✅ **Faster processing** - Native code is much faster than WebAssembly
