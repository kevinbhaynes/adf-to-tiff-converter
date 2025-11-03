# ADF to TIFF Converter

A web-based geoprocessing tool that converts ESRI ArcInfo Binary Grid (.adf) files to GeoTIFF format. This tool runs entirely in the browser and can be hosted on GitHub Pages.

## 🚀 Live Demo

Access the tool at: `https://[your-username].github.io/adf-to-tiff-converter/`

## ✨ Features

- **Client-side processing** - No server required, runs entirely in the browser
- **Drag and drop** interface for easy file upload
- **Multiple file support** - Upload entire ADF dataset (hdr.adf, w001001.adf, etc.)
- **Progress tracking** - Visual feedback during conversion
- **Instant download** - Download converted TIFF files immediately
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
- `w001001.adf` - Raster data file
- `prj.adf` - Projection information (optional)
- Other supporting files

### Conversion Process
1. User uploads all ADF files from their dataset
2. The tool reads and parses the binary ADF format
3. Extracts raster data and georeferencing information
4. Creates a GeoTIFF file with preserved spatial reference
5. Provides download link for the converted file

## 🔧 Technical Implementation

### Current Implementation (Basic)
The basic version uses a simplified JavaScript-based conversion that:
- Reads ADF file headers
- Extracts basic raster data
- Creates a simple TIFF structure
- Suitable for basic visualization needs

### Advanced Implementation (Optional)
For full geospatial support, integrate GDAL.js:
- Complete ADF format support
- Preserves all spatial reference information
- Supports various compression options
- Handles large datasets efficiently

To enable GDAL.js support:
1. Include the converter.js module
2. Add GDAL.js CDN link to index.html:
```html
<script src="https://cdn.jsdelivr.net/npm/gdal3.js@2.5.0/dist/package/gdal3.js"></script>
```
3. Update app.js to use the advanced converter

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
- File size limited by browser memory
- Basic TIFF output (may not preserve all metadata)
- No server-side processing available
- Limited to ADF formats readable in JavaScript

### Browser Compatibility
- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

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

**Issue: "Missing hdr.adf file" error**
- Solution: Ensure you're uploading all files from the ADF dataset, including hdr.adf

**Issue: Large files fail to convert**
- Solution: Files may exceed browser memory limits. Try smaller datasets or use chunked processing

**Issue: TIFF file won't open in some software**
- Solution: Some GIS software may require specific TIFF tags. Try opening in QGIS or GDAL-compatible software

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