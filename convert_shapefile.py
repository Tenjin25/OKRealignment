"""
Convert Oklahoma County Shapefile to GeoJSON
Converts tl_2020_40_county20.shp to tl_2020_40_county20.geojson
"""

import json
import sys

try:
    import geopandas as gpd
    print("✓ geopandas is installed")
except ImportError:
    print("✗ geopandas is not installed")
    print("\nInstalling geopandas...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "geopandas"])
    import geopandas as gpd
    print("✓ geopandas installed successfully")

# Paths
shapefile_path = "data/tl_2020_40_county20/tl_2020_40_county20.shp"
geojson_path = "data/tl_2020_40_county20.geojson"

print(f"\n📂 Reading shapefile: {shapefile_path}")

try:
    # Read the shapefile
    gdf = gpd.read_file(shapefile_path)
    
    print(f"✓ Shapefile loaded successfully")
    print(f"  - Counties found: {len(gdf)}")
    print(f"  - Columns: {', '.join(gdf.columns.tolist())}")
    print(f"  - CRS: {gdf.crs}")
    
    # Display sample counties
    print(f"\n📋 Sample counties:")
    for idx, row in gdf.head(5).iterrows():
        county_name = row.get('NAME20', row.get('NAME', 'Unknown'))
        print(f"  - {county_name}")
    
    # Convert to WGS84 (EPSG:4326) if needed for web mapping
    if gdf.crs and gdf.crs != 'EPSG:4326':
        print(f"\n🔄 Converting CRS to EPSG:4326 (WGS84)...")
        gdf = gdf.to_crs('EPSG:4326')
        print(f"✓ CRS converted")
    
    # Save as GeoJSON
    print(f"\n💾 Saving GeoJSON: {geojson_path}")
    gdf.to_file(geojson_path, driver='GeoJSON')
    
    # Verify the output
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    print(f"✓ GeoJSON saved successfully")
    print(f"  - Features: {len(geojson_data['features'])}")
    print(f"  - File size: {len(json.dumps(geojson_data)) / 1024:.2f} KB")
    
    # List all county names
    print(f"\n📍 All Oklahoma Counties ({len(geojson_data['features'])}):")
    counties = sorted([f['properties'].get('NAME20', f['properties'].get('NAME', 'Unknown')) 
                      for f in geojson_data['features']])
    
    for i in range(0, len(counties), 4):
        row_counties = counties[i:i+4]
        print(f"  {', '.join(row_counties)}")
    
    print(f"\n✅ Conversion complete!")
    print(f"   Output: {geojson_path}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
