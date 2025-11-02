# Oklahoma Political Realignment Map# OKRealignment



An interactive web mapping application visualizing Oklahoma's political realignment from 2000 to 2020 using Mapbox GL JS. This project analyzes county-level voting patterns across all 77 Oklahoma counties, showing how political preferences have shifted over two decades of presidential and state-level elections.An interactive web mapping application visualizing Oklahoma's political realignment from 2008 to 2024 using Mapbox GL JS.



[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://tenjin25.github.io/OKRealignment/)## Project Overview

[![Data Coverage](https://img.shields.io/badge/data-2000--2020-blue)]()

[![Counties](https://img.shields.io/badge/counties-77-orange)]()This project analyzes county-level voting patterns across Oklahoma, showing how political preferences have shifted over presidential and state-level elections from 2008 through 2024.



## 🎯 Features**Status:** 🚧 In Development (Based on NCMap.html framework)



- **Interactive County Map**: Click any of Oklahoma's 77 counties to see detailed election results## Features (Planned)

- **Historical Analysis**: View voting patterns across 20+ years (2000-2020) of elections

- **Multi-Contest Support**: Analyze presidential, gubernatorial, US Senate, and statewide executive races- **Interactive County Map**: Click counties to see detailed election results

- **Competitiveness Analysis**: 15-level color-coded system showing political lean intensity- **Historical Trends**: View voting patterns across multiple election cycles (2008-2024)

- **Comprehensive Data**: 50+ partisan statewide contests across 11 election years- **Contest Selector**: Analyze presidential, gubernatorial, and down-ballot races

- **Responsive Design**: Works seamlessly on desktop and mobile devices- **Competitiveness Analysis**: Color-coded margins showing political lean intensity

- **Responsive Design**: Works on desktop and mobile devices

## 📊 Data Coverage

## Getting Started

### Election Years

**2000** • **2002** • **2004** • **2008** • **2010** • **2012** • **2014** • **2016** • **2018** • **2020**### Prerequisites

- A Mapbox access token (free tier available)

### Contest Types- A modern web browser

- **Presidential Elections**: 2000, 2008, 2012, 2016, 2020- Optional: A local web server for development

- **Gubernatorial**: 2002, 2010, 2014, 2018

- **US Senate**: 2002, 2008, 2010, 2014, 2016, 2020### Setup

- **Lieutenant Governor**: 2002, 2010, 2014, 2018

- **State Executive Offices**: Attorney General, State Auditor, State Treasurer, Superintendent of Public Instruction, Labor Commissioner, Insurance Commissioner, Corporation Commissioner1. **Get a Mapbox Access Token**

   - Visit [Mapbox Account](https://account.mapbox.com/access-tokens/)

### Data Quality   - Sign up or log in

- ✅ **77/77 counties** for all contests   - Copy your default public token or create a new one

- ✅ **Precinct-level aggregation** for 2010 and 2014 (128,911 and 42,849 records)

- ✅ **Multi-candidate support** including third-party and independent candidates2. **Configure the Application**

- ✅ **Complete vote totals** with margin calculations and competitiveness categorization   - Open `index.html` in your text editor

   - Find line ~948: `mapboxToken: 'pk.eyJ1...'`

## 🚀 Quick Start   - Replace with your actual token (or use the existing one if it works)



### View Live Demo3. **Run the Application**

Visit **[https://tenjin25.github.io/OKRealignment/](https://tenjin25.github.io/OKRealignment/)** to see the map in action.   

   **Option A: Open directly in browser**

### Run Locally   ```powershell

   # Open with default browser

1. **Clone the repository**   start index.html

   ```bash   ```

   git clone https://github.com/Tenjin25/OKRealignment.git   

   cd OKRealignment   **Option B: Use a local server (recommended for development)**

   ```   ```powershell

   # Python 3

2. **Start a local server**   python -m http.server 8000

   ```bash   

   # Python 3   # Or use Python 2

   python -m http.server 8000   python -m SimpleHTTPServer 8000

      ```

   # Or Python 2   

   python -m SimpleHTTPServer 8000   Then navigate to: `http://localhost:8000`

   ```

4. **Deploy to GitHub Pages**

3. **Open in browser**   - Push repository to GitHub

   Navigate to: `http://localhost:8000`   - Go to repository Settings → Pages

   - Select branch (usually `main`) and root directory

### Prerequisites   - GitHub will automatically serve `index.html`

- A modern web browser (Chrome, Firefox, Safari, Edge)   - Your map will be live at: `https://[username].github.io/[repo-name]`

- Optional: Mapbox access token (a demo token is included but has usage limits)

## Data Sources (Needed)

## 📁 Project Structure

To complete this project, you'll need:

```

OKRealignment/1. **Oklahoma County Boundaries** (GeoJSON format)

├── index.html                      # Main application (GitHub Pages ready)   - Source: [US Census TIGER/Line Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)

├── create_county_results_json.py   # Python script to generate election JSON   - Look for "tl_2020_40_county20.zip" (Oklahoma = FIPS code 40)

├── convert_shapefile.py            # Script to convert shapefiles to GeoJSON

├── data/2. **Election Results Data** (JSON or CSV format)

│   ├── tl_2020_40_county20.geojson              # Oklahoma county boundaries (3.86 MB)   - County-level results for 2008, 2012, 2016, 2020, and 2024

│   ├── oklahoma_county_election_results_2008_2024.json  # Election data (2.4 MB)   - Contests: President, Governor, US Senate, State races

│   ├── tl_2020_40_county20/                     # Original shapefiles   - Source: [Oklahoma State Election Board](https://www.ok.gov/elections/)

│   └── Election_Data/                           # Source CSV files

│       ├── 00pres-aligned.csv                   # 2000 Presidential## Project Structure

│       ├── 02gov-aligned.csv                    # 2002 Governor

│       ├── 02ltgov-aligned.csv                  # 2002 Lt. Governor```

│       ├── 02ussen-aligned.csv                  # 2002 US SenateOKRealignment/

│       ├── 20041102__ok__general__corp__commissioner__county.csv├── index.html              # Main Oklahoma map application (GitHub Pages ready)

│       ├── 20081104__ok__general__president__county.csv├── OKMap.html              # Backup/alternate version (same as index.html)

│       ├── 20081104__ok__general__us_senate__county.csv├── NCMap.html              # Reference NC implementation

│       ├── 20101102__ok__general__precinct.csv  # Precinct data (aggregated)├── README.md               # This file

│       ├── 20121106__ok__general__county.csv├── data/                   # Election data (to be added)

│       ├── 20141104__ok__general__precinct.csv  # Precinct data (aggregated)│   ├── tl_2020_40_county20.geojson  # Oklahoma county boundaries (FIPS 40)

│       ├── 20161108__ok__general__county.csv│   └── oklahoma_county_election_results_2008_2024.json

│       ├── 20181106__ok__general__county.csv└── .github/

│       └── 20201103__ok__general__county.csv    └── copilot-instructions.md

├── scripts/```

│   ├── map.js                      # Core mapping functionality

│   └── common.js                   # Shared utilities## Technical Stack

├── styles/

│   ├── main.css                    # Application styles- **Mapbox GL JS v3.0.1** - Interactive mapping

│   └── common.css                  # Shared styles- **Turf.js v6.5.0** - Geospatial analysis

└── .github/- **PapaParse v5.4.1** - CSV parsing

    └── copilot-instructions.md     # Development guidelines- **Vanilla JavaScript** - No framework dependencies

```

## Development Roadmap

## 🎨 Competitiveness Scale

- [x] Initialize project structure

The map uses a 15-level competitiveness categorization system with distinct colors:- [x] Set up basic Mapbox map centered on Oklahoma

- [x] Retrofit complete NC UI framework for Oklahoma (OKMap.html)

### Republican Lean (Red Spectrum)- [x] Update all state-specific references (NC → OK)

| Category | Margin | Color |- [x] Configure Oklahoma center coordinates and bounds

|----------|--------|-------|- [x] Adapt office names for Oklahoma state positions

| **Annihilation** | R+40%+ | #67000d (Deep Red) |- [x] Create Oklahoma-specific research findings placeholders

| **Dominant** | R+30-40% | #a50f15 |- [ ] **Data Collection Phase** (NEXT STEPS):

| **Stronghold** | R+20-30% | #cb181d |  - [ ] Download Oklahoma county boundaries (tl_2020_40_county20.zip)

| **Safe** | R+10-20% | #ef3b2c |  - [ ] Convert county shapefile to GeoJSON

| **Likely** | R+5.5-10% | #fb6a4a |  - [ ] Collect election results from OK State Election Board

| **Lean** | R+1-5.5% | #fcae91 |  - [ ] Format data to match Tennessee/NC JSON structure

| **Tilt** | R+0.5-1% | #fee8c8 (Light Red) |- [ ] Load and integrate Oklahoma data into OKMap.html

- [ ] Test and debug with real Oklahoma election data

### Tossup- [ ] Mobile responsive optimizations

| Category | Margin | Color |- [ ] Performance optimizations

|----------|--------|-------|

| **Tossup** | ±0.5% | #f7f7f7 (Light Gray) |## Customization



### Democratic Lean (Blue Spectrum)### Map Styles

| Category | Margin | Color |Available Mapbox styles (change in line 90 of `index.html`):

|----------|--------|-------|- `mapbox://styles/mapbox/light-v11` (Current - best for data visualization)

| **Tilt** | D+0.5-1% | #e1f5fe (Light Blue) |- `mapbox://styles/mapbox/streets-v12`

| **Lean** | D+1-5.5% | #c6dbef |- `mapbox://styles/mapbox/dark-v11`

| **Likely** | D+5.5-10% | #9ecae1 |- `mapbox://styles/mapbox/satellite-streets-v12`

| **Safe** | D+10-20% | #6baed6 |

| **Stronghold** | D+20-30% | #3182bd |### Color Schemes

| **Dominant** | D+30-40% | #08519c |Political competitiveness categories (from NC implementation):

| **Annihilation** | D+40%+ | #08306b (Deep Blue) |- **Annihilation**: 40%+ margin

- **Dominant**: 30-40% margin

## 🔧 Data Processing- **Stronghold**: 20-30% margin

- **Safe**: 10-20% margin

The election data is processed through a sophisticated Python pipeline:- **Likely**: 5.5-10% margin

- **Lean**: 1-5.5% margin

### Input Formats Supported- **Tilt**: 0.5-1% margin

- **Old Format (2000-2002)**: Multi-row headers with complex CSV quoting- **Tossup**: <0.5% margin

- **2004-2008 Format**: Standard county-level CSV with office columns

- **Precinct Format (2010-2014)**: Precinct-level data aggregated to county totals## References

- **Modern Format (2012+)**: Standardized county-level format

- Base framework adapted from NC Political Realignment Map

### Processing Features- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/guides/)

- ✅ Party label normalization (R→REP, D→DEM, I→IND, L→LIB)- [Turf.js Documentation](https://turfjs.org/)

- ✅ Special handling for Le Flore County naming- [Oklahoma State Election Board](https://www.ok.gov/elections/)

- ✅ Multi-line CSV field parsing with `skipinitialspace=True`

- ✅ Partisan race filtering (excludes judicial, local, legislative)## GitHub Deployment

- ✅ Automatic competitiveness categorization

- ✅ Margin calculation with percentage precisionThis project is ready for GitHub Pages deployment:



### Regenerate Data1. **Initialize Git** (if not already done):

To regenerate the election JSON from source CSVs:   ```bash

   git init

```bash   git add .

python create_county_results_json.py   git commit -m "Initial commit: Oklahoma Political Realignment Map"

```   ```



This will:2. **Create GitHub Repository**:

1. Parse all CSV files in `data/Election_Data/`   - Go to GitHub and create a new repository

2. Aggregate precinct data by county where applicable   - Name it `OKRealignment` or similar

3. Calculate competitiveness for each county-contest pair   - Don't initialize with README (we already have one)

4. Generate `data/oklahoma_county_election_results_2008_2024.json`

3. **Push to GitHub**:

## 🛠️ Technical Stack   ```bash

   git remote add origin https://github.com/[your-username]/OKRealignment.git

- **[Mapbox GL JS v3.0.1](https://docs.mapbox.com/mapbox-gl-js/)** - Interactive mapping and vector tiles   git branch -M main

- **[Turf.js v6.5.0](https://turfjs.org/)** - Geospatial analysis utilities   git push -u origin main

- **[PapaParse v5.4.1](https://www.papaparse.com/)** - CSV parsing for data import   ```

- **Python 3.13** - Data processing and conversion scripts

- **Vanilla JavaScript** - No framework dependencies for core functionality4. **Enable GitHub Pages**:

   - Go to repository Settings → Pages

### Key Libraries Used   - Source: Deploy from a branch

```javascript   - Branch: `main` / `(root)`

// Mapping   - Click Save

mapboxgl.accessToken = 'your-token-here';   - Your site will be live at: `https://[your-username].github.io/OKRealignment`

const map = new mapboxgl.Map({ ... });

5. **Update Mapbox Token** (Important for security):

// Geospatial calculations   - Consider using environment variables for production

turf.centroid(county);   - For GitHub Pages, you can use the token restriction features in your Mapbox account

turf.booleanPointInPolygon(point, polygon);   - Restrict token to specific URLs: `https://[your-username].github.io/OKRealignment/*`



// Data parsing## License

Papa.parse(csvData, { ... });

```Educational project for CPT-236 course.



## 📚 Data Sources## Author



### Geographic DataCreated by Shamar Davis

- **County Boundaries**: US Census Bureau TIGER/Line Shapefiles

  - File: `tl_2020_40_county20.zip`## Acknowledgments

  - FIPS Code: 40 (Oklahoma)

  - Format: Converted from SHP to GeoJSON- Base framework adapted from NC Political Realignment Map

  - Contains: 77 counties with accurate boundaries- Mapbox GL JS for mapping capabilities

- Election data from Oklahoma State Election Board

### Election Data
- **Oklahoma State Election Board**: Historical election results
- **OpenElections Project**: Standardized CSV formats for older elections
- **County Clerks**: Precinct-level data for 2010 and 2014

### Processing Steps
1. Download shapefiles from Census Bureau
2. Convert to GeoJSON using `convert_shapefile.py`
3. Collect election CSVs from State Election Board
4. Standardize formats and align data
5. Run `create_county_results_json.py` to generate final JSON
6. Validate data completeness (all 77 counties present)

## 🔐 Configuration

### Mapbox Token
The included token has rate limits. For production use:

1. **Get your own token**: [Mapbox Account](https://account.mapbox.com/access-tokens/)
2. **Update `index.html`**:
   ```javascript
   mapboxgl.accessToken = 'YOUR_TOKEN_HERE';
   ```
3. **Restrict token usage**:
   - Add URL restrictions: `https://yourdomain.com/*`
   - Limit to specific scopes: `styles:tiles`, `fonts:read`

### Map Styles
Change the base map style in `index.html`:
```javascript
style: 'mapbox://styles/mapbox/light-v11'  // Current (best for choropleth)
// Other options:
// 'mapbox://styles/mapbox/streets-v12'
// 'mapbox://styles/mapbox/dark-v11'
// 'mapbox://styles/mapbox/satellite-streets-v12'
```

## 🚢 Deployment

### GitHub Pages (Recommended)

1. **Enable GitHub Pages**:
   - Go to repository **Settings** → **Pages**
   - Source: **Deploy from a branch**
   - Branch: **`master`** / **`(root)`**
   - Click **Save**

2. **Your site will be live at**:
   ```
   https://tenjin25.github.io/OKRealignment/
   ```

3. **Update token restrictions** in Mapbox to allow your GitHub Pages URL

### Other Hosting Options
- **Netlify**: Drag and drop the folder
- **Vercel**: Connect GitHub repository
- **Apache/Nginx**: Serve as static files

## 🤝 Contributing

This is an educational project, but contributions are welcome!

### Areas for Enhancement
- [ ] Add 2004 Presidential data (if source file available)
- [ ] Include 2022 and 2024 election results
- [ ] Add congressional district boundaries
- [ ] Create animated time-lapse visualization
- [ ] Export feature for maps and data
- [ ] Mobile app version

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of CPT-236 coursework.

**Data Usage**:
- Election data: Public domain (Oklahoma State Election Board)
- Geographic data: Public domain (US Census Bureau)
- Map tiles: Mapbox (requires attribution)

## 👨‍💻 Author

**Shamar Davis**
- GitHub: [@Tenjin25](https://github.com/Tenjin25)
- Course: CPT-236 - Web Mapping and GIS

## 🙏 Acknowledgments

- **NC Political Realignment Map** - Base framework and UI inspiration
- **Mapbox** - Mapping platform and vector tiles
- **Oklahoma State Election Board** - Historical election data
- **US Census Bureau** - County boundary shapefiles
- **OpenElections Project** - Standardized election data formats
- **GitHub Copilot** - Development assistance and data processing

## 📖 Additional Documentation

- **[DATA_STRUCTURE.md](DATA_STRUCTURE.md)** - Detailed JSON structure and schema
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Development guidelines

## 📊 Project Statistics

- **Total Contests**: 50+ partisan statewide races
- **Election Years**: 11 years (2000-2020)
- **Counties**: 77 (100% coverage)
- **Data Points**: 3,850+ county-contest combinations
- **File Size**: ~2.4 MB compressed JSON
- **Code Lines**: 2,500+ lines across HTML, JS, Python
- **CSV Files Processed**: 29 source files
- **Precinct Records Aggregated**: 171,760 records

---

**⭐ Star this repository if you find it useful!**

**🐛 Found a bug?** [Open an issue](https://github.com/Tenjin25/OKRealignment/issues)

**❓ Have questions?** Check the [documentation](DATA_STRUCTURE.md) or open a discussion
