#!/usr/bin/env python3
"""
Test script for all visualization features
"""

from visualization import Choropleth

def main():
    print("=== Independence and National Days Visualization Suite ===")
    
    # Create the choropleth visualization
    choropleth = Choropleth()
    
    # Display season statistics
    print("\n1. Season Distribution Statistics:")
    stats = choropleth.get_season_stats()
    
    # Create and save the histogram by month
    print("\n2. Creating histogram by month...")
    fig_hist = choropleth.histogram_by_month(save=True)
    
    # Create and save the bar graph of season counts
    print("\n3. Creating bar graph of season counts...")
    fig_bar = choropleth.bar_graph_season_counts(save=True)
    
    # Create and save the choropleth map
    print("\n4. Creating choropleth map...")
    fig_choropleth = choropleth.export_choropleth_to_png("choropleth_map.png")
    
    print("\n=== All visualizations completed! ===")
    print("Generated files:")
    print("- histogram_by_month.png")
    print("- bar_graph_season_counts.png") 
    print("- choropleth_map.png")
    
    print("\nVisualization features:")
    print("- Histogram: Shows distribution by month (12 bins)")
    print("- Bar graph: Shows count by season")
    print("- Choropleth: Interactive world map colored by season")

if __name__ == "__main__":
    main() 