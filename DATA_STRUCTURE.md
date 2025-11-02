# Oklahoma Election Data Structure Guide

This document explains the expected data format for the Oklahoma Political Realignment Map.

## Required Files

### 1. County Boundaries: `data/tl_2020_40_county20.geojson`

**Source**: US Census Bureau TIGER/Line Shapefiles
- Download: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- Search for: "2020 County" and select Oklahoma (FIPS 40)
- Convert shapefile to GeoJSON using: https://mapshaper.org/ or QGIS

**Required Properties**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "NAME20": "Oklahoma",        // County name (required)
        "NAMELSAD20": "Oklahoma County",
        "GEOID": "40109",
        "STATEFP": "40",
        "COUNTYFP": "109"
      },
      "geometry": { ... }
    }
  ]
}
```

### 2. Election Results: `data/oklahoma_county_election_results_2008_2024.json`

**Structure** (matches NC/Tennessee format):

```json
{
  "results_by_year": {
    "2024": {
      "presidential": {
        "president_2024": {
          "contest_name": "PRESIDENT AND VICE PRESIDENT OF THE UNITED STATES",
          "dem_candidate": "Kamala Harris",
          "rep_candidate": "Donald Trump",
          "results": {
            "OKLAHOMA": {
              "dem_votes": 123456,
              "rep_votes": 234567,
              "other_votes": 5000,
              "total_votes": 363023,
              "margin": -111111,
              "margin_pct": 30.6,
              "competitiveness": {
                "category": "Dominant",
                "party": "Republican",
                "description": "Dominant Republican (30-40%)",
                "color": "#a50f15"
              }
            },
            "TULSA": { ... },
            // ... all 77 Oklahoma counties
          }
        }
      },
      "us_senate": {
        "us_senate_2024": { ... }
      },
      "governor": {
        "governor_2024": { ... }
      }
    },
    "2020": { ... },
    "2016": { ... },
    "2012": { ... },
    "2008": { ... }
  }
}
```

## Competitiveness Categories

Based on margin percentage:

| Margin | Category | Republican Color | Democratic Color |
|--------|----------|-----------------|------------------|
| 40%+   | Annihilation | `#67000d` | `#08306b` |
| 30-40% | Dominant | `#a50f15` | `#08519c` |
| 20-30% | Stronghold | `#cb181d` | `#3182bd` |
| 10-20% | Safe | `#ef3b2c` | `#6baed6` |
| 5.5-10% | Likely | `#fb6a4a` | `#9ecae1` |
| 1-5.5% | Lean | `#fcae91` | `#c6dbef` |
| 0.5-1% | Tilt | `#fee8c8` | `#e1f5fe` |
| <0.5% | Tossup | `#f7f7f7` | `#f7f7f7` |

## Data Collection Sources

### Oklahoma State Election Board
- Website: https://www.ok.gov/elections/
- Results by year: https://www.ok.gov/elections/Election_Info/
- Historical results available from 2000-present

### County-Level Data
All 77 Oklahoma counties (alphabetically):
- Adair, Alfalfa, Atoka, Beaver, Beckham, Blaine, Bryan, Caddo, Canadian, Carter, Cherokee, Choctaw, Cimarron, Cleveland, Coal, Comanche, Cotton, Craig, Creek, Custer, Delaware, Dewey, Ellis, Garfield, Garvin, Grady, Grant, Greer, Harmon, Harper, Haskell, Hughes, Jackson, Jefferson, Johnston, Kay, Kingfisher, Kiowa, Latimer, Le Flore, Lincoln, Logan, Love, Major, Marshall, Mayes, McClain, McCurtain, McIntosh, Murray, Muskogee, Noble, Nowata, Okfuskee, Oklahoma, Okmulgee, Osage, Ottawa, Pawnee, Payne, Pittsburg, Pontotoc, Pottawatomie, Pushmataha, Roger Mills, Rogers, Seminole, Sequoyah, Stephens, Texas, Tillman, Tulsa, Wagoner, Washington, Washita, Woods, Woodward

## Contest Types

### Statewide Races
- President (2008, 2012, 2016, 2020, 2024)
- US Senate (varies by cycle)
- Governor (2010, 2014, 2018, 2022)
- Lieutenant Governor
- Attorney General
- State Treasurer
- State Auditor
- Labor Commissioner
- Insurance Commissioner
- Superintendent of Public Instruction
- Corporation Commissioner

## Example Python Script for Data Collection

```python
import json
import csv

def calculate_competitiveness(margin_pct, winner):
    """Calculate competitiveness category and color"""
    if margin_pct >= 40:
        category, color = "Annihilation", "#67000d" if winner == "R" else "#08306b"
    elif margin_pct >= 30:
        category, color = "Dominant", "#a50f15" if winner == "R" else "#08519c"
    elif margin_pct >= 20:
        category, color = "Stronghold", "#cb181d" if winner == "R" else "#3182bd"
    elif margin_pct >= 10:
        category, color = "Safe", "#ef3b2c" if winner == "R" else "#6baed6"
    elif margin_pct >= 5.5:
        category, color = "Likely", "#fb6a4a" if winner == "R" else "#9ecae1"
    elif margin_pct >= 1:
        category, color = "Lean", "#fcae91" if winner == "R" else "#c6dbef"
    elif margin_pct >= 0.5:
        category, color = "Tilt", "#fee8c8" if winner == "R" else "#e1f5fe"
    else:
        category, color = "Tossup", "#f7f7f7"
    
    party = "Republican" if winner == "R" else "Democratic"
    return {
        "category": category,
        "party": party,
        "description": f"{category} {party} ({margin_pct:.1f}%)" if category != "Tossup" else f"Tossup ({party} win)",
        "color": color
    }

# Use this function when processing your CSV/Excel election data
```

## Validation Checklist

Before deploying:
- [ ] GeoJSON has all 77 Oklahoma counties
- [ ] County names match between GeoJSON and election data (uppercase in data)
- [ ] All years have complete county coverage
- [ ] Candidate names are consistent
- [ ] Vote totals add up correctly
- [ ] Competitiveness colors are calculated
- [ ] Test with one year first, then add others
