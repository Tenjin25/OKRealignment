"""
Convert Oklahoma election CSV files to the JSON format required by the map.

This script processes election data from various CSV formats and creates
a standardized JSON file for the interactive map with competitiveness categorization.
"""

import csv
import json
import os
from collections import defaultdict
import re
from datetime import datetime

def clean_number(value):
    """Remove commas and quotes from number strings and convert to int."""
    if isinstance(value, str):
        value = value.replace(',', '').replace('"', '').strip()
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def normalize_county_name(county):
    """Normalize county name to UPPERCASE and handle special cases."""
    normalized = county.strip().upper()
    # Handle Le Flore County - ensure it matches GeoJSON spelling "LE FLORE" with space
    if 'LEFLORE' in normalized.replace(' ', ''):
        normalized = 'LE FLORE'
    return normalized

def get_competitiveness_category(margin_pct, winner):
    """
    Determine competitiveness category based on margin percentage.
    Returns dict with category, party, code, and color.
    """
    abs_margin = abs(margin_pct)
    
    # Define categories and colors
    if abs_margin < 0.5:
        return {
            "category": "Tossup",
            "party": "Tossup",
            "code": "TOSSUP",
            "color": "#f7f7f7"
        }
    
    # Republican categories
    if winner == "REP":
        if abs_margin >= 40:
            return {"category": "Annihilation", "party": "Republican", "code": "R_ANNIHILATION", "color": "#67000d"}
        elif abs_margin >= 30:
            return {"category": "Dominant", "party": "Republican", "code": "R_DOMINANT", "color": "#a50f15"}
        elif abs_margin >= 20:
            return {"category": "Stronghold", "party": "Republican", "code": "R_STRONGHOLD", "color": "#cb181d"}
        elif abs_margin >= 10:
            return {"category": "Safe", "party": "Republican", "code": "R_SAFE", "color": "#ef3b2c"}
        elif abs_margin >= 5.5:
            return {"category": "Likely", "party": "Republican", "code": "R_LIKELY", "color": "#fb6a4a"}
        elif abs_margin >= 1:
            return {"category": "Lean", "party": "Republican", "code": "R_LEAN", "color": "#fcae91"}
        else:
            return {"category": "Tilt", "party": "Republican", "code": "R_TILT", "color": "#fee8c8"}
    
    # Democratic categories
    elif winner == "DEM":
        if abs_margin >= 40:
            return {"category": "Annihilation", "party": "Democratic", "code": "D_ANNIHILATION", "color": "#08306b"}
        elif abs_margin >= 30:
            return {"category": "Dominant", "party": "Democratic", "code": "D_DOMINANT", "color": "#08519c"}
        elif abs_margin >= 20:
            return {"category": "Stronghold", "party": "Democratic", "code": "D_STRONGHOLD", "color": "#3182bd"}
        elif abs_margin >= 10:
            return {"category": "Safe", "party": "Democratic", "code": "D_SAFE", "color": "#6baed6"}
        elif abs_margin >= 5.5:
            return {"category": "Likely", "party": "Democratic", "code": "D_LIKELY", "color": "#9ecae1"}
        elif abs_margin >= 1:
            return {"category": "Lean", "party": "Democratic", "code": "D_LEAN", "color": "#c6dbef"}
        else:
            return {"category": "Tilt", "party": "Democratic", "code": "D_TILT", "color": "#e1f5fe"}
    
    # Default tossup
    return {
        "category": "Tossup",
        "party": "Tossup",
        "code": "TOSSUP",
        "color": "#f7f7f7"
    }

def process_county_results(county, candidates, year, contest_name):
    """
    Process county results and calculate all metrics including competitiveness.
    Returns a dict with all required fields.
    """
    if not candidates:
        return None
    
    # Sort by votes
    sorted_candidates = sorted(candidates, key=lambda x: x['votes'], reverse=True)
    
    # Find dem and rep candidates
    dem_candidate = next((c for c in candidates if c['party'] == 'DEM'), None)
    rep_candidate = next((c for c in candidates if c['party'] == 'REP'), None)
    
    # Calculate totals
    total_votes = sum(c['votes'] for c in candidates)
    dem_votes = dem_candidate['votes'] if dem_candidate else 0
    rep_votes = rep_candidate['votes'] if rep_candidate else 0
    two_party_total = dem_votes + rep_votes
    
    # Calculate other votes (non-DEM, non-REP)
    other_votes = total_votes - two_party_total
    
    # Calculate margin
    margin = abs(dem_votes - rep_votes)
    margin_pct = (margin / two_party_total * 100) if two_party_total > 0 else 0
    
    # Determine winner
    winner = "REP" if rep_votes > dem_votes else "DEM" if dem_votes > rep_votes else "TIE"
    
    # Get competitiveness
    competitiveness = get_competitiveness_category(margin_pct, winner)
    
    # Build all_parties dict
    all_parties = {}
    for c in candidates:
        party = c['party'] if c['party'] else 'OTHER'
        if party in all_parties:
            all_parties[party] += c['votes']
        else:
            all_parties[party] = c['votes']
    
    return {
        "county": county,
        "contest": contest_name,
        "year": str(year),
        "dem_candidate": dem_candidate['candidate'] if dem_candidate else "",
        "rep_candidate": rep_candidate['candidate'] if rep_candidate else "",
        "dem_votes": dem_votes,
        "rep_votes": rep_votes,
        "other_votes": other_votes,
        "total_votes": total_votes,
        "two_party_total": two_party_total,
        "margin": margin,
        "margin_pct": round(margin_pct, 2),
        "winner": winner,
        "competitiveness": competitiveness,
        "all_parties": all_parties
    }

def parse_old_format_csv(filepath, year, office_name):
    """
    Parse old format CSV files (00pres.csv, 02gov.csv, 02ltgov.csv, 02ussen.csv).
    These have candidates in column headers.
    """
    results = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        # Read all lines
        lines = f.readlines()
        
        # Find the header row with party names or candidate names with party abbreviations
        header_idx = 0
        has_separate_party_row = False
        
        for i, line in enumerate(lines):
            if 'Republican' in line or 'Democratic' in line:
                header_idx = i
                has_separate_party_row = True
                break
            elif '(R)' in line or '(D)' in line:  # Format like "JIM INHOFE (R)"
                header_idx = i
                has_separate_party_row = False
                break
        
        import csv
        candidates_info = []
        
        if has_separate_party_row:
            # 2000 format: candidate names above, parties below
            candidate_row_idx = header_idx - 1
            candidate_reader = csv.reader([lines[candidate_row_idx]], skipinitialspace=True)
            candidate_names = next(candidate_reader)
            
            party_reader = csv.reader([lines[header_idx]], skipinitialspace=True)
            parties = next(party_reader)
            
            # Build candidate-party mapping
            for i in range(1, len(candidate_names)):  # Skip first empty column
                if candidate_names[i] and parties[i] and 'TOTAL' not in candidate_names[i].upper():
                    # Map party abbreviations
                    party_name = parties[i].strip()
                    if 'Republican' in party_name:
                        party = 'REP'
                    elif 'Democratic' in party_name or 'Democrat' in party_name:
                        party = 'DEM'
                    elif 'Reform' in party_name or 'Independent' in party_name:
                        party = 'IND'
                    elif 'Libertarian' in party_name:
                        party = 'LIB'
                    else:
                        party = party_name[:3].upper()
                    
                    candidate_name = candidate_names[i].replace('\n', ' ').replace('\r', ' ').strip()
                    candidate_name = ' '.join(candidate_name.split())
                    
                    candidates_info.append({
                        'index': i,
                        'name': candidate_name,
                        'party': party
                    })
            
            data_start_idx = header_idx + 2
        else:
            # 2002 format: "CANDIDATE NAME (P)" all in one field (may span multiple lines in file)
            # Use csv.reader to properly handle multi-line quoted fields
            f_temp = open(filepath, 'r', encoding='utf-8')
            csv_reader = csv.reader(f_temp, skipinitialspace=True)
            
            # Skip to header row
            for _ in range(header_idx):
                next(csv_reader)
            
            candidate_names = next(csv_reader)
            f_temp.close()
            
            # For 2002 format, header row has NO county column, starts directly with candidates
            # Data rows have county in column 0, so candidates are offset by +1
            for i in range(len(candidate_names)):
                if candidate_names[i] and 'TOTAL' not in candidate_names[i].upper():
                    # Extract candidate name and party from format like "JIM INHOFE (R)"
                    text = candidate_names[i].replace('\n', ' ').replace('\r', ' ').strip()
                    text = ' '.join(text.split())
                    
                    match = re.search(r'([A-Za-z\s\.\']+)\(([A-Z])\)', text)
                    if match:
                        name = match.group(1).strip()
                        party_abbr = match.group(2)
                        
                        # Normalize party abbreviations
                        if party_abbr == 'R':
                            party = 'REP'
                        elif party_abbr == 'D':
                            party = 'DEM'
                        elif party_abbr == 'I':
                            party = 'IND'
                        elif party_abbr == 'L':
                            party = 'LIB'
                        else:
                            party = party_abbr
                        
                        candidates_info.append({
                            'index': i + 1,  # +1 because data rows have county in column 0
                            'name': name,
                            'party': party
                        })
            
            # Find where data rows start (after separator line)
            data_start_idx = header_idx + 1
            for i in range(header_idx, len(lines)):
                if lines[i].strip() and not lines[i].strip().startswith('='):
                    # Check if this looks like a data row (starts with a county name)
                    test_row = next(csv.reader([lines[i]], skipinitialspace=True))
                    if test_row and test_row[0] and test_row[0].strip() and not '=' in test_row[0]:
                        data_start_idx = i
                        break
        
        # Now parse data rows
        for line in lines[data_start_idx:]:
            if not line.strip():
                continue
            
            row_data = next(csv.reader([line], skipinitialspace=True))
            if not row_data or not row_data[0]:
                continue
            
            county = row_data[0].strip()
            
            # Skip state total row
            if 'STATE TOTAL' in county.upper() or 'TOTAL' in county.upper():
                continue
            
            county = normalize_county_name(county)
            
            # Extract votes for each candidate
            candidates_data = []
            for cand_info in candidates_info:
                idx = cand_info['index']
                if idx < len(row_data):
                    votes = clean_number(row_data[idx])
                    if votes > 0:
                        candidates_data.append({
                            'candidate': cand_info['name'],
                            'party': cand_info['party'],
                            'votes': votes
                        })
            
            if candidates_data:
                results[county] = candidates_data
    
    return results

def parse_2004_2008_format(filepath, year):
    """
    Parse 2004-2008 format files (20041102, 20081104).
    Format: county, office, district, candidate, party, votes
    """
    results_by_office = defaultdict(lambda: defaultdict(list))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            county = normalize_county_name(row.get('county', ''))
            office = row.get('office', '').strip()
            candidate = row.get('candidate', '').strip()
            party = row.get('party', '').strip()
            votes = clean_number(row.get('votes', 0))
            
            if county and candidate and votes > 0:
                results_by_office[office][county].append({
                    'candidate': candidate,
                    'party': party,
                    'votes': votes
                })
    
    return results_by_office

def parse_modern_format(filepath, year):
    """
    Parse modern format files (2012+).
    Format: county, office, candidate, party, votes (with various vote type columns)
    """
    results_by_office = defaultdict(lambda: defaultdict(list))
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            county = normalize_county_name(row.get('county', ''))
            office = row.get('office', '').strip()
            candidate = row.get('candidate', '').strip()
            party = row.get('party', '').strip()
            votes = clean_number(row.get('votes', 0))
            
            if county and candidate and office and votes > 0:
                results_by_office[office][county].append({
                    'candidate': candidate,
                    'party': party,
                    'votes': votes
                })
    
    return results_by_office

def parse_precinct_format(filepath, year):
    """
    Parse precinct-level files and aggregate by county (2010, 2014).
    Format: county, office, candidate, party, precinct, votes/total_votes
    """
    results_by_office = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    candidate_party_map = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            county = normalize_county_name(row.get('county', ''))
            office = row.get('office', '').strip()
            candidate = row.get('candidate', '').strip()
            party = row.get('party', '').strip()
            
            # Handle different vote column names
            if 'total_votes' in row:
                votes = clean_number(row.get('total_votes', 0))
            else:
                votes = clean_number(row.get('votes', 0))
            
            if county and candidate and office and votes > 0:
                # Skip over/under votes and straight party votes
                if 'over votes' in candidate.lower() or 'under votes' in candidate.lower():
                    continue
                if 'straight party' in office.lower():
                    continue
                
                # Aggregate votes by county
                key = (county, office, candidate)
                results_by_office[office][county][candidate] += votes
                # Store party affiliation
                if candidate not in candidate_party_map:
                    candidate_party_map[candidate] = party
    
    # Convert to the expected format
    formatted_results = defaultdict(lambda: defaultdict(list))
    for office, counties in results_by_office.items():
        for county, candidates in counties.items():
            for candidate, votes in candidates.items():
                formatted_results[office][county].append({
                    'candidate': candidate,
                    'party': candidate_party_map.get(candidate, ''),
                    'votes': votes
                })
    
    return formatted_results

def create_contest_id(office_name, year):
    """Create a standardized contest ID."""
    # Simplify office name for ID
    office_clean = office_name.lower().replace(' ', '_').replace('.', '').replace(',', '')
    office_clean = re.sub(r'[^a-z0-9_]', '', office_clean)
    return f"{office_clean}_{year}"

def main():
    data_dir = 'data/Election_Data'
    output_file = 'data/oklahoma_county_election_results_2008_2024.json'
    
    # Initialize result structure
    result = {
        "metadata": {
            "state": "Oklahoma",
            "state_fips": "40",
            "counties_count": 77,
            "years_covered": "2000-2020",
            "data_source": "Oklahoma State Election Board",
            "focus": "Clean geographic political patterns",
            "processed_date": datetime.now().strftime("%Y-%m-%d"),
            "categorization_system": {
                "competitiveness_scale": {
                    "Republican": [
                        {"category": "Annihilation", "range": "R+40%+", "color": "#67000d"},
                        {"category": "Dominant", "range": "R+30-40%", "color": "#a50f15"},
                        {"category": "Stronghold", "range": "R+20-30%", "color": "#cb181d"},
                        {"category": "Safe", "range": "R+10-20%", "color": "#ef3b2c"},
                        {"category": "Likely", "range": "R+5.5-10%", "color": "#fb6a4a"},
                        {"category": "Lean", "range": "R+1-5.5%", "color": "#fcae91"},
                        {"category": "Tilt", "range": "R+0.5-1%", "color": "#fee8c8"}
                    ],
                    "Tossup": [
                        {"category": "Tossup", "range": "±0.5%", "color": "#f7f7f7"}
                    ],
                    "Democratic": [
                        {"category": "Tilt", "range": "D+0.5-1%", "color": "#e1f5fe"},
                        {"category": "Lean", "range": "D+1-5.5%", "color": "#c6dbef"},
                        {"category": "Likely", "range": "D+5.5-10%", "color": "#9ecae1"},
                        {"category": "Safe", "range": "D+10-20%", "color": "#6baed6"},
                        {"category": "Stronghold", "range": "D+20-30%", "color": "#3182bd"},
                        {"category": "Dominant", "range": "D+30-40%", "color": "#08519c"},
                        {"category": "Annihilation", "range": "D+40%+", "color": "#08306b"}
                    ]
                },
                "office_types": ["Federal", "State", "Judicial", "Other"],
                "enhanced_features": [
                    "Competitiveness categorization for each county",
                    "Contest type classification (Federal/State/Judicial)",
                    "Office ranking system for analysis prioritization",
                    "Color coding compatible with political geography visualization"
                ]
            }
        },
        "results_by_year": {}
    }
    
    print("Processing Oklahoma election data...")
    print("=" * 60)
    
    # Define file mappings
    files_to_process = [
        # Old format
        ('00pres-aligned.csv', 2000, 'President', 'old'),
        ('02gov-aligned.csv', 2002, 'Governor', 'old'),
        ('02ltgov-aligned.csv', 2002, 'Lieutenant Governor', 'old'),
        ('02ussen-aligned.csv', 2002, 'U.S. Senate', 'old'),
        
        # 2004-2008 format
        ('20041102__ok__general__president.csv', 2004, None, '2004'),
        ('20041102__ok__general__corp__commissioner__county.csv', 2004, None, '2004'),
        ('20081104__ok__general__president__county.csv', 2008, None, '2008'),
        ('20081104__ok__general__us_senate__county.csv', 2008, None, '2008'),
        ('20081104__ok__general__corp_commissioner__county.csv', 2008, None, '2008'),
        
        # Precinct format (needs aggregation)
        ('20101102__ok__general__precinct.csv', 2010, None, 'precinct'),
        ('20141104__ok__general__precinct.csv', 2014, None, 'precinct'),
        
        # Modern format (2012+)
        ('20121106__ok__general__county.csv', 2012, None, 'modern'),
        ('20161108__ok__general__county.csv', 2016, None, 'modern'),
        ('20181106__ok__general__county.csv', 2018, None, 'modern'),
        ('20201103__ok__general__county.csv', 2020, None, 'modern'),
    ]
    
    for file_info in files_to_process:
        filename = file_info[0]
        year = file_info[1]
        office_override = file_info[2] if len(file_info) > 2 else None
        format_type = file_info[3] if len(file_info) > 3 else 'modern'
        
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ Skipping {filename} - file not found")
            continue
        
        print(f"\n📄 Processing {filename} ({year})...")
        
        try:
            # Initialize year if needed
            if str(year) not in result['results_by_year']:
                result['results_by_year'][str(year)] = {}
            
            if format_type == 'old':
                # Old format - single office per file
                county_results = parse_old_format_csv(filepath, year, office_override)
                
                contest_id = create_contest_id(office_override, year)
                
                # Create contest structure
                if 'presidential' not in result['results_by_year'][str(year)] and 'president' in office_override.lower():
                    result['results_by_year'][str(year)]['presidential'] = {}
                elif 'governor' in office_override.lower():
                    if 'gubernatorial' not in result['results_by_year'][str(year)]:
                        result['results_by_year'][str(year)]['gubernatorial'] = {}
                elif 'senate' in office_override.lower():
                    if 'us_senate' not in result['results_by_year'][str(year)]:
                        result['results_by_year'][str(year)]['us_senate'] = {}
                
                # Determine category
                office_lower = office_override.lower()
                if 'president' in office_lower:
                    category = 'presidential'
                elif 'lieutenant governor' in office_lower:
                    category = 'lieutenant_governor'
                elif 'governor' in office_lower:
                    category = 'gubernatorial'
                elif 'senate' in office_lower:
                    category = 'us_senate'
                else:
                    category = 'other'
                
                if category not in result['results_by_year'][str(year)]:
                    result['results_by_year'][str(year)][category] = {}
                
                # Process each county
                contest_results = {}
                for county, candidates in county_results.items():
                    county_result = process_county_results(county, candidates, year, office_override)
                    if county_result:
                        contest_results[county] = county_result
                
                result['results_by_year'][str(year)][category][contest_id] = {
                    "contest_name": office_override.upper(),
                    "results": contest_results
                }
                
                print(f"   ✓ {office_override}: {len(contest_results)} counties")
                
            else:
                # Modern format (2004+)
                if format_type in ['2004', '2008']:
                    results_by_office = parse_2004_2008_format(filepath, year)
                elif format_type == 'precinct':
                    results_by_office = parse_precinct_format(filepath, year)
                else:
                    results_by_office = parse_modern_format(filepath, year)
                
                # Define partisan offices we want to keep
                partisan_offices = [
                    'president',
                    'u.s. senate', 'us senate',
                    'governor',
                    'lieutenant governor', 'lt governor', 'ltgov',
                    'attorney general',
                    'state auditor', 'auditor',
                    'state treasurer', 'treasurer',
                    'superintendent of public instruction', 'superintendent',
                    'commissioner of labor', 'labor commissioner',
                    'insurance commissioner',
                    'corporation commissioner', 'corp commissioner'
                ]
                
                for office, county_results in results_by_office.items():
                    office_lower = office.lower()
                    
                    # Skip non-partisan races
                    is_partisan = any(partisan_term in office_lower for partisan_term in partisan_offices)
                    
                    # Skip judicial, local, and proposition races
                    if any(term in office_lower for term in ['supreme court', 'court of', 'judge', 'justice', 
                                                               'proposition', 'state question', 'for county', 
                                                               'for mayor', 'for council', 'city of', 'town of',
                                                               'for board member', 'fire', 'ward', 'district no.']):
                        continue
                    
                    if not is_partisan:
                        continue
                    
                    contest_id = create_contest_id(office, year)
                    
                    # Determine category
                    if 'president' in office_lower:
                        category = 'presidential'
                    elif 'lieutenant' in office_lower or 'ltgov' in office_lower or 'lt gov' in office_lower:
                        category = 'lieutenant_governor'
                    elif 'governor' in office_lower and 'lieutenant' not in office_lower:
                        category = 'gubernatorial'
                    elif 'senate' in office_lower and ('u.s' in office_lower or 'us' in office_lower):
                        category = 'us_senate'
                    elif 'attorney general' in office_lower:
                        category = 'attorney_general'
                    elif 'auditor' in office_lower:
                        category = 'state_auditor'
                    elif 'treasurer' in office_lower:
                        category = 'state_treasurer'
                    elif 'superintendent' in office_lower:
                        category = 'superintendent'
                    elif 'labor' in office_lower:
                        category = 'labor_commissioner'
                    elif 'insurance' in office_lower:
                        category = 'insurance_commissioner'
                    elif 'corporation' in office_lower or 'corp' in office_lower:
                        category = 'corporation_commissioner'
                    else:
                        continue  # Skip if we can't categorize it
                    
                    if category not in result['results_by_year'][str(year)]:
                        result['results_by_year'][str(year)][category] = {}
                    
                    # Process each county
                    contest_results = {}
                    for county, candidates in county_results.items():
                        county_result = process_county_results(county, candidates, year, office)
                        if county_result:
                            contest_results[county] = county_result
                    
                    result['results_by_year'][str(year)][category][contest_id] = {
                        "contest_name": office.upper(),
                        "results": contest_results
                    }
                    
                    print(f"   ✓ {office}: {len(contest_results)} counties")
        
        except Exception as e:
            print(f"   ✗ Error processing {filename}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save to JSON
    print(f"\n💾 Saving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("✅ Conversion complete!")
    print(f"\nYears processed: {', '.join(sorted(result['results_by_year'].keys()))}")
    
    for year in sorted(result['results_by_year'].keys()):
        print(f"\n{year}:")
        for category in result['results_by_year'][year]:
            contests = result['results_by_year'][year][category]
            for contest_id, contest_data in contests.items():
                county_count = len(contest_data['results'])
                print(f"  - {contest_data['contest_name']}: {county_count} counties")
    
    file_size = os.path.getsize(output_file) / 1024
    print(f"\n📊 Output file size: {file_size:.2f} KB")
    print(f"📁 Location: {output_file}")

if __name__ == '__main__':
    main()
