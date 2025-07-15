#!/usr/bin/env python3
"""
Example usage of the Choropleth visualization class
"""

from visualization import Choropleth

def main():
    print("=== Independence and National Days Choropleth Map ===")
    print("This visualization shows countries colored by the season of their")
    print("independence or national day celebrations.\n")
    
    # Create the choropleth visualization
    choropleth = Choropleth()
    
    # Show statistics
    print("Season Distribution:")
    stats = choropleth.get_season_stats()
    
    print(f"\nColor Legend:")
    for season, color in choropleth.season_colors.items():
        print(f"  {season}: {color}")
    
    # Generate the map
    print("\nGenerating interactive choropleth map...")
    fig = choropleth.plot()
    
    print("\nMap features:")
    print("- Hover over countries to see country name and date")
    print("- Zoom and pan to explore different regions")
    print("- Click legend items to show/hide seasons")
    print("- Countries are colored by season of their independence/national day")

if __name__ == "__main__":
    main() 