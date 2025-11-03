#!/usr/bin/env python3
"""
ADF to GeoTIFF Converter
Converts ESRI ArcInfo Binary Grid (.adf) files to GeoTIFF format
"""

import os
import sys
from pathlib import Path
from osgeo import gdal, osr

# Enable GDAL exceptions for better error messages
gdal.UseExceptions()


def convert_adf_to_geotiff(adf_path, output_path, compression='LZW'):
    """
    Convert an ADF (ESRI Grid) to GeoTIFF format.

    Args:
        adf_path (str): Path to the ADF directory or hdr.adf file
        output_path (str): Path for the output GeoTIFF file
        compression (str): Compression method (LZW, DEFLATE, or NONE)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"\n{'='*60}")
        print("ADF to GeoTIFF Converter")
        print(f"{'='*60}\n")

        # Validate input path
        adf_path = Path(adf_path)
        if not adf_path.exists():
            print(f"❌ Error: Input path does not exist: {adf_path}")
            return False

        # If a directory is provided, look for hdr.adf
        if adf_path.is_dir():
            hdr_file = adf_path / 'hdr.adf'
            if not hdr_file.exists():
                print(f"❌ Error: No hdr.adf found in directory: {adf_path}")
                return False
            input_dataset_path = str(adf_path)
            print(f"📁 Input directory: {adf_path}")
        else:
            # If a file is provided, use its parent directory
            input_dataset_path = str(adf_path.parent)
            print(f"📁 Input file: {adf_path}")
            print(f"📁 Using directory: {input_dataset_path}")

        # Open the ADF dataset
        print(f"\n🔍 Opening ADF dataset...")
        src_ds = gdal.Open(input_dataset_path, gdal.GA_ReadOnly)

        if src_ds is None:
            print(f"❌ Error: Failed to open ADF dataset")
            print(f"   Make sure all ADF files are present (hdr.adf, w001001.adf, etc.)")
            return False

        # Get dataset information
        print(f"✅ ADF dataset opened successfully")
        print(f"\n📊 Dataset Information:")
        print(f"   Size: {src_ds.RasterXSize} x {src_ds.RasterYSize} pixels")
        print(f"   Bands: {src_ds.RasterCount}")

        # Get projection
        projection = src_ds.GetProjection()
        if projection:
            srs = osr.SpatialReference(wkt=projection)
            print(f"   Projection: {srs.GetName() if srs.GetName() else 'Custom'}")
        else:
            print(f"   Projection: None (will be preserved)")

        # Get geotransform
        geotransform = src_ds.GetGeoTransform()
        if geotransform:
            print(f"   Origin: ({geotransform[0]:.2f}, {geotransform[3]:.2f})")
            print(f"   Pixel Size: ({geotransform[1]:.2f}, {geotransform[5]:.2f})")

        # Get band information
        band = src_ds.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        if nodata is not None:
            print(f"   NoData Value: {nodata}")

        data_type = gdal.GetDataTypeName(band.DataType)
        print(f"   Data Type: {data_type}")

        # Prepare output path
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Set up GeoTIFF creation options
        print(f"\n🔄 Converting to GeoTIFF...")
        print(f"   Output: {output_path}")
        print(f"   Compression: {compression}")

        creation_options = [
            f'COMPRESS={compression}',
            'TILED=YES',
            'BIGTIFF=IF_NEEDED',
        ]

        # Create the GeoTIFF
        driver = gdal.GetDriverByName('GTiff')
        dst_ds = driver.CreateCopy(
            str(output_path),
            src_ds,
            strict=0,
            options=creation_options
        )

        if dst_ds is None:
            print(f"❌ Error: Failed to create output GeoTIFF")
            return False

        # Flush to disk
        dst_ds.FlushCache()

        # Get output file size
        output_size_mb = output_path.stat().st_size / (1024 * 1024)

        print(f"✅ Conversion successful!")
        print(f"   Output size: {output_size_mb:.2f} MB")

        # Close datasets
        src_ds = None
        dst_ds = None

        # Verify the output
        print(f"\n🔍 Verifying output...")
        verify_ds = gdal.Open(str(output_path), gdal.GA_ReadOnly)
        if verify_ds is None:
            print(f"⚠️  Warning: Could not verify output file")
        else:
            print(f"✅ Output file verified successfully")
            print(f"   Size: {verify_ds.RasterXSize} x {verify_ds.RasterYSize} pixels")
            verify_ds = None

        print(f"\n{'='*60}")
        print("✅ CONVERSION COMPLETE!")
        print(f"{'='*60}\n")
        print(f"Your GeoTIFF is ready: {output_path}")
        print(f"You can now open it in ArcGIS Pro, QGIS, or any GIS software.\n")

        return True

    except Exception as e:
        print(f"\n❌ Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to handle command-line arguments"""

    # Check for command-line arguments
    if len(sys.argv) < 2:
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║         ADF to GeoTIFF Converter - Usage Guide           ║")
        print("╚═══════════════════════════════════════════════════════════╝\n")
        print("Usage:")
        print("  python adf_to_geotiff.py <input_adf> [output_geotiff] [compression]\n")
        print("Arguments:")
        print("  input_adf      : Path to ADF directory or hdr.adf file (required)")
        print("  output_geotiff : Path for output .tif file (optional)")
        print("                   Default: input_name_converted.tif")
        print("  compression    : Compression method (optional)")
        print("                   Options: LZW, DEFLATE, NONE")
        print("                   Default: LZW\n")
        print("Examples:")
        print("  python adf_to_geotiff.py /path/to/adf_folder")
        print("  python adf_to_geotiff.py /path/to/adf_folder output.tif")
        print("  python adf_to_geotiff.py /path/to/adf_folder output.tif DEFLATE\n")
        print("Note: Make sure all ADF files are in the same directory:")
        print("      hdr.adf, w001001.adf, sta.adf, etc.\n")
        sys.exit(1)

    # Parse arguments
    input_path = sys.argv[1]

    # Generate output path if not provided
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        input_name = Path(input_path).stem if Path(input_path).is_file() else Path(input_path).name
        output_path = f"{input_name}_converted.tif"

    # Get compression method
    compression = sys.argv[3] if len(sys.argv) > 3 else 'LZW'
    compression = compression.upper()

    if compression not in ['LZW', 'DEFLATE', 'NONE']:
        print(f"⚠️  Warning: Invalid compression '{compression}', using LZW")
        compression = 'LZW'

    # Perform conversion
    success = convert_adf_to_geotiff(input_path, output_path, compression)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
