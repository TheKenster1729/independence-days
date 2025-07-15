#!/usr/bin/env python3
"""
Test script for the Choropleth visualization
"""

from visualization import Choropleth

def main():
    # Create the choropleth visualization
    choropleth = Choropleth()
    
    # Display season statistics
    print("=== Independence and National Days by Season ===")
    choropleth.get_season_stats()
    
    # Create and display the map
    print("\nGenerating choropleth map...")
    fig = choropleth.plot()
    
    print("Choropleth map has been generated and displayed!")

if __name__ == "__main__":
    main() 