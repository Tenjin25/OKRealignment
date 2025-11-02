# OKRealignment

An interactive web mapping application visualizing Oklahoma's political realignment from 2008 to 2024 using Mapbox GL JS.

## Project Overview

This project analyzes county-level voting patterns across Oklahoma, showing how political preferences have shifted over presidential and state-level elections from 2008 through 2024.

**Status:** 🚧 In Development (Based on NCMap.html framework)

## Features (Planned)

- **Interactive County Map**: Click counties to see detailed election results
- **Historical Trends**: View voting patterns across multiple election cycles (2008-2024)
- **Contest Selector**: Analyze presidential, gubernatorial, and down-ballot races
- **Competitiveness Analysis**: Color-coded margins showing political lean intensity
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites
- A Mapbox access token (free tier available)
- A modern web browser
- Optional: A local web server for development

### Setup

1. **Get a Mapbox Access Token**
   - Visit [Mapbox Account](https://account.mapbox.com/access-tokens/)
   - Sign up or log in
   - Copy your default public token or create a new one

2. **Configure the Application**
   - Open `index.html` in your text editor
   - Find line ~948: `mapboxToken: 'pk.eyJ1...'`
   - Replace with your actual token (or use the existing one if it works)

3. **Run the Application**
   
   **Option A: Open directly in browser**
   ```powershell
   # Open with default browser
   start index.html
   ```
   
   **Option B: Use a local server (recommended for development)**
   ```powershell
   # Python 3
   python -m http.server 8000
   
   # Or use Python 2
   python -m SimpleHTTPServer 8000
   ```
   
   Then navigate to: `http://localhost:8000`

4. **Deploy to GitHub Pages**
   - Push repository to GitHub
   - Go to repository Settings → Pages
   - Select branch (usually `main`) and root directory
   - GitHub will automatically serve `index.html`
   - Your map will be live at: `https://[username].github.io/[repo-name]`

## Data Sources (Needed)

To complete this project, you'll need:

1. **Oklahoma County Boundaries** (GeoJSON format)
   - Source: [US Census TIGER/Line Shapefiles](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
   - Look for "tl_2020_40_county20.zip" (Oklahoma = FIPS code 40)

2. **Election Results Data** (JSON or CSV format)
   - County-level results for 2008, 2012, 2016, 2020, and 2024
   - Contests: President, Governor, US Senate, State races
   - Source: [Oklahoma State Election Board](https://www.ok.gov/elections/)

## Project Structure

```
OKRealignment/
├── index.html              # Main Oklahoma map application (GitHub Pages ready)
├── OKMap.html              # Backup/alternate version (same as index.html)
├── NCMap.html              # Reference NC implementation
├── README.md               # This file
├── data/                   # Election data (to be added)
│   ├── tl_2020_40_county20.geojson  # Oklahoma county boundaries (FIPS 40)
│   └── oklahoma_county_election_results_2008_2024.json
└── .github/
    └── copilot-instructions.md
```

## Technical Stack

- **Mapbox GL JS v3.0.1** - Interactive mapping
- **Turf.js v6.5.0** - Geospatial analysis
- **PapaParse v5.4.1** - CSV parsing
- **Vanilla JavaScript** - No framework dependencies

## Development Roadmap

- [x] Initialize project structure
- [x] Set up basic Mapbox map centered on Oklahoma
- [x] Retrofit complete NC UI framework for Oklahoma (OKMap.html)
- [x] Update all state-specific references (NC → OK)
- [x] Configure Oklahoma center coordinates and bounds
- [x] Adapt office names for Oklahoma state positions
- [x] Create Oklahoma-specific research findings placeholders
- [ ] **Data Collection Phase** (NEXT STEPS):
  - [ ] Download Oklahoma county boundaries (tl_2020_40_county20.zip)
  - [ ] Convert county shapefile to GeoJSON
  - [ ] Collect election results from OK State Election Board
  - [ ] Format data to match Tennessee/NC JSON structure
- [ ] Load and integrate Oklahoma data into OKMap.html
- [ ] Test and debug with real Oklahoma election data
- [ ] Mobile responsive optimizations
- [ ] Performance optimizations

## Customization

### Map Styles
Available Mapbox styles (change in line 90 of `index.html`):
- `mapbox://styles/mapbox/light-v11` (Current - best for data visualization)
- `mapbox://styles/mapbox/streets-v12`
- `mapbox://styles/mapbox/dark-v11`
- `mapbox://styles/mapbox/satellite-streets-v12`

### Color Schemes
Political competitiveness categories (from NC implementation):
- **Annihilation**: 40%+ margin
- **Dominant**: 30-40% margin
- **Stronghold**: 20-30% margin
- **Safe**: 10-20% margin
- **Likely**: 5.5-10% margin
- **Lean**: 1-5.5% margin
- **Tilt**: 0.5-1% margin
- **Tossup**: <0.5% margin

## References

- Base framework adapted from NC Political Realignment Map
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/guides/)
- [Turf.js Documentation](https://turfjs.org/)
- [Oklahoma State Election Board](https://www.ok.gov/elections/)

## GitHub Deployment

This project is ready for GitHub Pages deployment:

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Oklahoma Political Realignment Map"
   ```

2. **Create GitHub Repository**:
   - Go to GitHub and create a new repository
   - Name it `OKRealignment` or similar
   - Don't initialize with README (we already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/[your-username]/OKRealignment.git
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `(root)`
   - Click Save
   - Your site will be live at: `https://[your-username].github.io/OKRealignment`

5. **Update Mapbox Token** (Important for security):
   - Consider using environment variables for production
   - For GitHub Pages, you can use the token restriction features in your Mapbox account
   - Restrict token to specific URLs: `https://[your-username].github.io/OKRealignment/*`

## License

Educational project for CPT-236 course.

## Author

Created by Shamar Davis

## Acknowledgments

- Base framework adapted from NC Political Realignment Map
- Mapbox GL JS for mapping capabilities
- Election data from Oklahoma State Election Board
