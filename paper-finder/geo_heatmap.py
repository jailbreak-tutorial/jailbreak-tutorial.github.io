#!/usr/bin/env python3
"""
Generate a world heatmap of jailbreaking paper locations based on author affiliations.
Usage:
    python geo_heatmap.py --data-file outputs/jailbreaking_papers.csv

- Uses geopy for geocoding affiliations to lat/lon
- Uses folium for interactive mapping
- Double counts papers for each city if multiple authors from different places
- Caches geocoding results for speed
"""
import pandas as pd
import folium
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import argparse
import os
import pickle
from collections import Counter
import tqdm
import ast

CACHE_FILE = 'geo_cache.pkl'

def extract_affiliations(df):
    """Try to extract affiliations/cities from the data."""
    # Try to use 'affiliations' field if present, else fallback to parsing summary
    affiliations = []
    if 'affiliations' in df.columns:
        for aff_list in df['affiliations']:
            if isinstance(aff_list, str):
                try:
                    affs = ast.literal_eval(aff_list)
                except:
                    affs = [aff_list]
            else:
                affs = aff_list
            affiliations.extend(affs)
    else:
        # Fallback: try to extract university/city from summary (very rough)
        for summary in df['summary']:
            # Look for patterns like 'University of X', 'X University', 'Institute', 'Shanghai', etc.
            import re
            found = re.findall(r'(University of [A-Za-z ]+|[A-Za-z ]+ University|Institute of [A-Za-z ]+|Shanghai|Beijing|Toronto|Philadelphia|London|Paris|Tokyo|Zurich|Munich|Stanford|Berkeley|Cambridge|Oxford|MIT|Harvard|Princeton|Carnegie Mellon|ETH Zurich|Tsinghua|Peking|Seoul|Singapore|Sydney|Melbourne|Hong Kong|Edinburgh|Vancouver|Los Angeles|New York|Boston|Chicago|Austin|San Diego|San Francisco)', summary)
            affiliations.extend([f.strip() for f in found])
    return affiliations

def geocode_locations(locations, cache_file=CACHE_FILE):
    """Geocode a list of locations to lat/lon, using a cache."""
    # Load cache if exists
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            cache = pickle.load(f)
    else:
        cache = {}
    
    geolocator = Nominatim(user_agent="jailbreak-geo-heatmap")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, error_wait_seconds=5.0)
    
    coords = {}
    for loc in tqdm.tqdm(set(locations), desc="Geocoding locations"):
        if loc in cache:
            coords[loc] = cache[loc]
        else:
            try:
                location = geocode(loc)
                if location:
                    coords[loc] = (location.latitude, location.longitude)
                else:
                    coords[loc] = None
            except Exception as e:
                coords[loc] = None
        cache[loc] = coords[loc]
    # Save cache
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)
    return coords

def main():
    parser = argparse.ArgumentParser(description='Generate a world heatmap of jailbreaking paper locations.')
    parser.add_argument('--data-file', type=str, required=True, help='CSV or JSON file from arxiv_scraper')
    parser.add_argument('--output', type=str, default='geo_heatmap.html', help='Output HTML file for the map')
    args = parser.parse_args()

    # Load data
    if args.data_file.endswith('.csv'):
        df = pd.read_csv(args.data_file)
    elif args.data_file.endswith('.json'):
        df = pd.read_json(args.data_file)
    else:
        raise ValueError('Unsupported file type')

    # Extract affiliations/cities
    print('Extracting affiliations/cities...')
    affiliations = extract_affiliations(df)
    print(f'Found {len(affiliations)} affiliation/city mentions.')

    # Count occurrences
    aff_counter = Counter([a for a in affiliations if a and isinstance(a, str)])
    print(f'Unique locations: {len(aff_counter)}')

    # Geocode
    coords = geocode_locations(list(aff_counter.keys()))
    
    # Prepare heatmap data
    heat_data = []
    for loc, count in aff_counter.items():
        if coords.get(loc):
            lat, lon = coords[loc]
            heat_data.append([lat, lon, count])
    print(f'Plottable locations: {len(heat_data)}')

    # Create map
    m = folium.Map(location=[20,0], zoom_start=2, tiles='cartodbpositron')
    HeatMap(heat_data, radius=18, blur=15, min_opacity=0.3, max_zoom=6, gradient={0.2: 'blue', 0.4: 'lime', 0.7: 'orange', 1: 'red'}).add_to(m)
    folium.LayerControl().add_to(m)

    # Add city markers for top 10
    for loc, count in aff_counter.most_common(10):
        if coords.get(loc):
            lat, lon = coords[loc]
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                popup=f"{loc}: {count} papers",
                color='crimson',
                fill=True,
                fill_color='crimson',
                fill_opacity=0.7
            ).add_to(m)

    # Save
    m.save(args.output)
    print(f'✅ Heatmap saved to {args.output}')

if __name__ == '__main__':
    main() 