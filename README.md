# ADF to TIFF Converter

A web-based geoprocessing tool that converts ESRI ArcInfo Binary Grid (.adf) files to GeoTIFF format. This tool runs entirely in the browser and can be hosted on GitHub Pages.

## 🚀 Live Demo

Access the tool at: `https://[your-username].github.io/adf-to-tiff-converter/`

## ✨ Features

- **Proper GeoTIFF output** - Creates fully compliant GeoTIFF files with spatial reference
- **GDAL-powered conversion** - Uses GDAL.js for accurate geospatial data processing
- **Preserves spatial metadata** - Maintains projection, geotransform, and NoData values
- **Client-side processing** - No server required, runs entirely in the browser
- **Drag and drop** interface for easy file upload
- **Multiple file support** - Upload entire ADF dataset (hdr.adf, w001001.adf, etc.)
- **Progress tracking** - Visual feedback during conversion
- **Instant download** - Download converted GeoTIFF files immediately
- **Fallback support** - Automatic fallback to simplified converter if GDAL fails
- **GitHub Pages compatible** - Free hosting with GitHub Pages

## 📁 Project Structure

```
adf-to-tiff-converter/
│
├── index.html          # Main HTML interface
├── app.js             # Core application logic
├── converter.js       # Advanced conversion module (optional)
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## 🛠️ Installation

### Option 1: Quick Setup

1. Fork this repository or download the files
2. Push to your GitHub repository
3. Enable GitHub Pages in repository settings
4. Access your tool at `https://[your-username].github.io/[repository-name]/`

### Option 2: Local Development

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/adf-to-tiff-converter.git
cd adf-to-tiff-converter
```

2. Serve locally using any HTTP server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server

# Using VS Code Live Server extension
# Right-click on index.html and select "Open with Live Server"
```

3. Open your browser and navigate to `http://localhost:8000`

## 📊 How It Works

### ADF File Format
ADF (Arc/Info Binary Grid) is a proprietary raster format used by ESRI. An ADF dataset consists of multiple files:
- `hdr.adf` - Header file containing metadata
- `w001001.adf` - Raster data file(s)
- `sta.adf` - Statistics (optional)
- `prj.adf` - Projection information (optional)
- Other supporting files

### Conversion Process
1. User uploads all ADF files from their dataset
2. GDAL.js library loads automatically from CDN
3. Files are written to GDAL's virtual file system
4. GDAL opens and parses the complete ADF dataset
5. Spatial reference (projection + geotransform) is extracted
6. Raster data is read band-by-band
7. A proper GeoTIFF is created with:
   - LZW compression for smaller file size
   - Tiled structure for better performance
   - Full spatial reference metadata
   - Preserved NoData values
8. The GeoTIFF is downloaded to the user's computer

## 🔧 Technical Implementation

### GDAL-Based Conversion (Primary Method)
The tool now uses **GDAL.js** (v2.5.0) for robust, production-ready conversion:
- ✅ **Complete ADF format support** - Reads all ADF variants
- ✅ **Preserves spatial reference** - Projection and geotransform metadata
- ✅ **Accurate georeferencing** - Creates spec-compliant GeoTIFF files
- ✅ **NoData preservation** - Maintains NoData values from source
- ✅ **Compression support** - LZW compression reduces file size
- ✅ **Tiled output** - Optimized for large dataset performance
- ✅ **ArcGIS Pro compatible** - Works seamlessly with ESRI software

### Fallback Converter (Backup Method)
If GDAL fails to load (e.g., network issues), a simplified JavaScript converter activates:
- Reads basic ADF structure
- Creates valid TIFF files
- ⚠️ May not preserve all spatial metadata
- Suitable for basic visualization

### Architecture
```
User Upload → GDAL.js Loader → Virtual File System → ADF Parser
                                                          ↓
ArcGIS Pro ← Download ← GeoTIFF Blob ← GDAL Writer ← Spatial Data
```

## 🎯 Usage Instructions

1. **Navigate to the tool** in your web browser
2. **Upload ADF files** by either:
   - Clicking the upload area and selecting files
   - Dragging and dropping files onto the upload area
3. **Select all files** from your ADF dataset (including hdr.adf and all data files)
4. **Click "Convert to TIFF"** to start the conversion
5. **Download** the converted TIFF file when complete

## ⚙️ Configuration

### Customization Options

Modify these settings in `app.js`:

```javascript
// Maximum file size (in bytes)
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB

// Output TIFF compression
const COMPRESSION = 'LZW'; // Options: 'NONE', 'LZW', 'JPEG'

// Tile size for large rasters
const TILE_SIZE = 256;
```

### Styling

Customize the appearance by modifying the CSS in `index.html`:
- Colors: Update the gradient colors in the CSS
- Layout: Adjust container widths and spacing
- Fonts: Change the font family

## 🚨 Limitations

### Current Limitations
- File size limited by browser memory (typically up to 2GB depending on browser)
- Requires internet connection for GDAL.js CDN (on first load)
- Processing large datasets may take time in the browser
- No server-side processing available

### Browser Compatibility
- Chrome 90+ ✅ (Recommended)
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

### Output Format
- **GeoTIFF** with proper spatial reference
- **Compression**: LZW (lossless)
- **Data Type**: Float32 (preserves precision)
- **Tiled**: Yes (optimized for performance)
- **Compatible with**: ArcGIS Pro, QGIS, GDAL tools, and all GeoTIFF-compliant software

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines
1. Keep the tool client-side only
2. Ensure GitHub Pages compatibility
3. Test with various ADF datasets
4. Update documentation for new features

## 📝 License

MIT License - feel free to use this tool for any purpose.

## 🆘 Troubleshooting

### Common Issues

**Issue: "Failed to add data, unsupported data type" in ArcGIS Pro**
- **Root Cause**: Old version created simple TIFF without geospatial metadata
- **Solution**: This is now FIXED! The tool creates proper GeoTIFF files with full spatial reference
- **Verification**: After conversion, the file should open directly in ArcGIS Pro without errors

**Issue: "Not recognized as being in a supported file format" error**
- **Root Cause**: Missing GeoTIFF tags (projection, geotransform)
- **Solution**: The new GDAL-based converter includes all required GeoTIFF tags
- **Check**: Look for "Created GeoTIFF: X bytes" in browser console to confirm proper creation

**Issue: "Missing hdr.adf file" error**
- **Solution**: Ensure you're uploading ALL files from the ADF dataset:
  - Required: `hdr.adf`, `w001001.adf` (or similar data files)
  - Optional but recommended: `sta.adf`, `prj.adf`, and other .adf files

**Issue: Large files fail to convert**
- **Solution**: Files may exceed browser memory limits (typically 2GB)
- **Workaround**: Try in Chrome with sufficient RAM, or process smaller tiles

**Issue: GDAL library fails to load**
- **Cause**: Network connectivity issues or CDN unavailable
- **Solution**: Check internet connection; tool will use fallback converter
- **Note**: Fallback converter may not preserve all spatial metadata

**Issue: Conversion takes a long time**
- **Explanation**: Large rasters are processed band-by-band in JavaScript
- **Expected**: Processing time varies with dataset size (e.g., 10-30 seconds for typical datasets)
- **Tip**: Check browser console for progress messages

## 📚 Resources

- [GDAL ADF Driver Documentation](https://gdal.org/drivers/raster/aig.html)
- [GeoTIFF Specification](http://geotiff.maptools.org/)
- [ESRI Grid Format](https://desktop.arcgis.com/en/arcmap/latest/manage-data/raster-and-images/esri-grid-format.htm)

## 🏷️ Tags

`geoprocessing` `adf` `tiff` `geotiff` `converter` `gis` `esri` `arcgis` `javascript` `client-side` `github-pages`

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ for the GIS community