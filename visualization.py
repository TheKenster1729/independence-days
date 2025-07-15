import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import geopandas as gpd
import numpy as np

class Choropleth:
    def __init__(self, path_to_data: str = "independence_and_national_days_updated.csv"):
        self.df = pd.read_csv(path_to_data)
        self._create_iso_mapping()
        self._create_hemisphere_mapping()
        self._process_data()
    
    def _create_iso_mapping(self):
        """Create mapping from numerical ISO codes to three-letter ISO codes"""
        self.iso_mapping = {
            4: 'AFG', 8: 'ALB', 12: 'DZA', 20: 'AND', 24: 'AGO',
            28: 'ATG', 32: 'ARG', 51: 'ARM', 36: 'AUS', 40: 'AUT',
            31: 'AZE', 44: 'BHS', 48: 'BHR', 50: 'BGD', 52: 'BRB',
            112: 'BLR', 56: 'BEL', 84: 'BLZ', 204: 'BEN', 64: 'BTN',
            68: 'BOL', 70: 'BIH', 72: 'BWA', 76: 'BRA', 96: 'BRN',
            100: 'BGR', 854: 'BFA', 108: 'BDI', 116: 'KHM', 120: 'CMR',
            124: 'CAN', 132: 'CPV', 140: 'CAF', 148: 'TCD', 152: 'CHL',
            156: 'CHN', 158: 'TWN', 170: 'COL', 174: 'COM', 184: 'COK', 188: 'CRI',
            191: 'HRV', 192: 'CUB', 196: 'CYP', 203: 'CZE', 384: 'CIV',
            180: 'COD', 208: 'DNK', 262: 'DJI', 212: 'DMA', 214: 'DOM',
            218: 'ECU', 818: 'EGY', 222: 'SLV', 226: 'GNQ', 232: 'ERI',
            233: 'EST', 748: 'SWZ', 231: 'ETH', 242: 'FJI', 246: 'FIN',
            250: 'FRA', 266: 'GAB', 270: 'GMB', 268: 'GEO', 276: 'DEU',
            288: 'GHA', 300: 'GRC', 308: 'GRD', 320: 'GTM', 324: 'GIN',
            624: 'GNB', 328: 'GUY', 332: 'HTI', 340: 'HND', 348: 'HUN',
            352: 'ISL', 356: 'IND', 360: 'IDN', 364: 'IRN', 368: 'IRQ',
            372: 'IRL', 376: 'ISR', 380: 'ITA', 388: 'JAM', 392: 'JPN',
            400: 'JOR', 398: 'KAZ', 404: 'KEN', 528: 'NLD', 296: 'KIR',
            688: 'SRB', 414: 'KWT', 417: 'KGZ', 418: 'LAO', 428: 'LVA',
            422: 'LBN', 426: 'LSO', 430: 'LBR', 434: 'LBY', 438: 'LIE',
            440: 'LTU', 442: 'LUX', 450: 'MDG', 454: 'MWI', 458: 'MYS',
            462: 'MDV', 466: 'MLI', 470: 'MLT', 584: 'MHL', 478: 'MRT',
            480: 'MUS', 484: 'MEX', 583: 'FSM', 498: 'MDA', 492: 'MCO',
            496: 'MNG', 499: 'MNE', 504: 'MAR', 508: 'MOZ', 104: 'MMR',
            516: 'NAM', 520: 'NRU', 524: 'NPL', 554: 'NZL', 558: 'NIC',
            562: 'NER', 566: 'NGA', 570: 'NIU', 408: 'PRK', 807: 'MKD',
            578: 'NOR', 512: 'OMN', 586: 'PAK', 585: 'PLW', 275: 'PSE',
            591: 'PAN', 598: 'PNG', 600: 'PRY', 604: 'PER', 608: 'PHL',
            616: 'POL', 620: 'PRT', 634: 'QAT', 178: 'COG', 642: 'ROU',
            643: 'RUS', 646: 'RWA', 659: 'KNA', 662: 'LCA', 670: 'VCT',
            882: 'WSM', 674: 'SMR', 682: 'SAU', 686: 'SEN', 690: 'SYC',
            694: 'SLE', 702: 'SGP', 703: 'SVK', 705: 'SVN', 90: 'SLB',
            706: 'SOM', 710: 'ZAF', 410: 'KOR', 728: 'SSD', 724: 'ESP',
            144: 'LKA', 729: 'SDN', 740: 'SUR', 752: 'SWE', 756: 'CHE',
            760: 'SYR', 678: 'STP', 762: 'TJK', 834: 'TZA', 764: 'THA',
            626: 'TLS', 768: 'TGO', 776: 'TON', 780: 'TTO', 788: 'TUN',
            792: 'TUR', 795: 'TKM', 798: 'TUV', 800: 'UGA', 804: 'UKR',
            784: 'ARE', 840: 'USA', 858: 'URY', 860: 'UZB', 548: 'VUT',
            336: 'VAT', 862: 'VEN', 704: 'VNM', 887: 'YEM', 894: 'ZMB',
            716: 'ZWE'
        }
    
    def _create_hemisphere_mapping(self):
        """Create mapping from country to hemisphere"""
        self.hemisphere_mapping = {
            # Northern Hemisphere countries
            'AFG': 'Northern', 'ALB': 'Northern', 'DZA': 'Northern', 'AND': 'Northern', 
            'ARM': 'Northern', 'AUT': 'Northern', 'AZE': 'Northern', 'BHR': 'Northern',
            'BGD': 'Northern', 'BLR': 'Northern', 'BEL': 'Northern', 'BTN': 'Northern',
            'BIH': 'Northern', 'BGR': 'Northern', 'BFA': 'Northern', 'KHM': 'Northern',
            'CMR': 'Northern', 'CAN': 'Northern', 'CPV': 'Northern', 'CAF': 'Northern',
            'TCD': 'Northern', 'CHN': 'Northern', 'COL': 'Northern', 'COM': 'Northern',
            'COK': 'Southern', 'CRI': 'Northern', 'HRV': 'Northern', 'CUB': 'Northern',
            'CYP': 'Northern', 'CZE': 'Northern', 'CIV': 'Northern', 'COD': 'Southern',
            'DNK': 'Northern', 'DJI': 'Northern', 'DMA': 'Northern', 'DOM': 'Northern',
            'ECU': 'Southern', 'EGY': 'Northern', 'SLV': 'Northern', 'GNQ': 'Northern',
            'ERI': 'Northern', 'EST': 'Northern', 'SWZ': 'Southern', 'ETH': 'Northern',
            'FIN': 'Northern', 'FRA': 'Northern', 'GAB': 'Southern', 'GMB': 'Northern',
            'GEO': 'Northern', 'DEU': 'Northern', 'GHA': 'Northern', 'GRC': 'Northern',
            'GRD': 'Northern', 'GTM': 'Northern', 'GIN': 'Northern', 'GNB': 'Northern',
            'GUY': 'Southern', 'HTI': 'Northern', 'HND': 'Northern', 'HUN': 'Northern',
            'ISL': 'Northern', 'IND': 'Northern', 'IDN': 'Southern', 'IRN': 'Northern',
            'IRQ': 'Northern', 'IRL': 'Northern', 'ISR': 'Northern', 'ITA': 'Northern',
            'JAM': 'Northern', 'JPN': 'Northern', 'JOR': 'Northern', 'KAZ': 'Northern',
            'KEN': 'Southern', 'KIR': 'Southern', 'SRB': 'Northern', 'KWT': 'Northern',
            'KGZ': 'Northern', 'LAO': 'Northern', 'LVA': 'Northern', 'LBN': 'Northern',
            'LSO': 'Southern', 'LBR': 'Northern', 'LBY': 'Northern', 'LIE': 'Northern',
            'LTU': 'Northern', 'LUX': 'Northern', 'MDG': 'Southern', 'MWI': 'Southern',
            'MYS': 'Northern', 'MDV': 'Northern', 'MLI': 'Northern', 'MLT': 'Northern',
            'MHL': 'Northern', 'MRT': 'Northern', 'MUS': 'Southern', 'MEX': 'Northern',
            'FSM': 'Northern', 'MDA': 'Northern', 'MCO': 'Northern', 'MNG': 'Northern',
            'MNE': 'Northern', 'MAR': 'Northern', 'MOZ': 'Southern', 'MMR': 'Northern',
            'NAM': 'Southern', 'NRU': 'Southern', 'NPL': 'Northern', 'NZL': 'Southern',
            'NIC': 'Northern', 'NER': 'Northern', 'NGA': 'Northern', 'NIU': 'Southern',
            'PRK': 'Northern', 'MKD': 'Northern', 'NOR': 'Northern', 'OMN': 'Northern',
            'PAK': 'Northern', 'PLW': 'Northern', 'PSE': 'Northern', 'PAN': 'Northern',
            'PNG': 'Southern', 'PRY': 'Southern', 'PER': 'Southern', 'PHL': 'Northern',
            'POL': 'Northern', 'PRT': 'Northern', 'QAT': 'Northern', 'COG': 'Southern',
            'ROU': 'Northern', 'RUS': 'Northern', 'RWA': 'Southern', 'KNA': 'Northern',
            'LCA': 'Northern', 'VCT': 'Northern', 'WSM': 'Southern', 'SMR': 'Northern',
            'SAU': 'Northern', 'SEN': 'Northern', 'SYC': 'Southern', 'SLE': 'Northern',
            'SGP': 'Northern', 'SVK': 'Northern', 'SVN': 'Northern', 'SLB': 'Southern',
            'SOM': 'Northern', 'ZAF': 'Southern', 'KOR': 'Northern', 'SSD': 'Northern',
            'ESP': 'Northern', 'LKA': 'Northern', 'SDN': 'Northern', 'SUR': 'Southern',
            'SWE': 'Northern', 'CHE': 'Northern', 'SYR': 'Northern', 'STP': 'Southern',
            'TJK': 'Northern', 'TZA': 'Southern', 'THA': 'Northern', 'TLS': 'Southern',
            'TGO': 'Northern', 'TON': 'Southern', 'TTO': 'Northern', 'TUN': 'Northern',
            'TUR': 'Northern', 'TKM': 'Northern', 'TUV': 'Southern', 'UGA': 'Southern',
            'UKR': 'Northern', 'ARE': 'Northern', 'USA': 'Northern', 'URY': 'Southern',
            'UZB': 'Northern', 'VUT': 'Southern', 'VAT': 'Northern', 'VEN': 'Northern',
            'VNM': 'Northern', 'YEM': 'Northern', 'ZMB': 'Southern', 'ZWE': 'Southern',
            'ARG': 'Southern', 'AUS': 'Southern', 'BRA': 'Southern', 'CHL': 'Southern',
            'TWN': 'Northern'
        }
    
    def _process_data(self):
        """Process the data to extract seasons from display dates and convert ISO codes"""
        # Ensure ISO Code is integer (handle missing values)
        self.df['ISO Code'] = pd.to_numeric(self.df['ISO Code'], errors='coerce').astype('Int64')
        # Convert numerical ISO codes to three-letter codes
        self.df['ISO_3'] = self.df['ISO Code'].map(self.iso_mapping)
        # Add hemisphere information
        self.df['hemisphere'] = self.df['ISO_3'].map(self.hemisphere_mapping)
        # Convert display dates to seasons
        self.df['season'] = self.df['Display Date'].apply(self._get_season)
        # Create a mapping for season colors
        self.season_colors = {
            'Winter': '#4C72B0',  # Blue
            'Spring': '#55A868',  # Green  
            'Summer': '#E69F00',  # Orange
            'Fall': '#C44E52'     # Red
        }
    
    def _get_season(self, date_str):
        """Convert date string to season"""
        try:
            # Parse the date string (format: DD.MMM)
            date_obj = datetime.strptime(date_str, "%d.%b")
            month = date_obj.month
            
            # Define seasons (Northern Hemisphere)
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            elif month in [9, 10, 11]:
                return 'Fall'
            else:
                return 'Unknown'
        except:
            return 'Unknown'
    
    def plot(self):
        """Create and display the choropleth map"""
        print(self.df)
        # Create the choropleth map
        fig = px.choropleth(
            self.df,
            locations='ISO_3',
            color='season',
            color_discrete_map=self.season_colors,
            title='Independence and National Days by Season',
            labels={'season': 'Season'},
            hover_data=['Country', 'Display Date']
        )
        
        # Update layout for better appearance
        fig.update_layout(
            title_x=0.5,
            title_font_size=20,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor='lightgray',
                showland=True,
                landcolor='lightgray',
                showocean=True,
                oceancolor='lightblue',
                projection_type='natural earth'
            ),
            legend=dict(
                title="Season",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Show the plot
        fig.show()
        
        return fig
    
    def get_season_stats(self):
        """Get statistics about the distribution of seasons"""
        season_counts = self.df['season'].value_counts()
        print("Distribution of Independence/National Days by Season:")
        print(season_counts)
        return season_counts

    def histogram_by_month(self, save=False):
        """Create a histogram that bins the data by month (12 bins total)"""
        # Convert display dates to month numbers (1-12)
        def date_to_month(date_str):
            try:
                date_obj = datetime.strptime(date_str, "%d.%b")
                return date_obj.month
            except:
                return None
        
        # Add month column
        self.df['month'] = self.df['Display Date'].apply(date_to_month)
        
        # Create histogram with exactly 12 bins (one for each month)
        fig = px.histogram(
            self.df,
            x='month',
            nbins=12,
            title='Distribution of Independence/National Days by Month',
            labels={'month': 'Month', 'count': 'Number of Countries'},
            color_discrete_sequence=['#4C72B0']
        )
        
        # Update layout to show month names on x-axis
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Set exact bin boundaries and labels
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),  # 1 through 12
                ticktext=month_names,
                title='Month',
                range=[0.5, 12.5]  # Center the bars properly
            ),
            yaxis=dict(title='Number of Countries'),
            title_x=0.5,
            title_font_size=16
        )
        
        if save:
            fig.write_image("histogram_by_month.png", scale=2)
            print("✓ Exported histogram to 'histogram_by_month.png'")
        
        return fig

    def bar_graph_season_counts(self, save = False):
        """Create a bar graph of the distribution of seasons"""
        season_counts = self.df['season'].value_counts()
        fig = px.bar(season_counts, x=season_counts.index, y=season_counts.values,
                     title="Distribution of Independence/National Days by Season")
        if save:
            fig.write_image("bar_graph_season_counts.png", scale = 2)
        else:
            fig.show()
        return fig
    
    def export_choropleth_to_png(self, filename: str = "choropleth.png"):
        """Export the choropleth map to a PNG file"""
        fig = self.plot()
        fig.write_image(filename, scale = 2)
        print(f"✓ Exported choropleth to {filename!r}")
        
    def hemisphere_season_analysis(self, save=False):
        """Create a graph showing season distribution by hemisphere"""
        # Create a cross-tabulation of hemisphere vs season
        hemisphere_season = pd.crosstab(self.df['hemisphere'], self.df['season'])
        
        # Create a stacked bar chart
        fig = px.bar(
            hemisphere_season,
            title='Season Distribution by Hemisphere',
            labels={'value': 'Number of Countries', 'index': 'Hemisphere'},
            color_discrete_map=self.season_colors
        )
        
        # Update layout
        fig.update_layout(
            title_x=0.5,
            title_font_size=16,
            xaxis_title='Hemisphere',
            yaxis_title='Number of Countries',
            legend_title='Season'
        )
        
        if save:
            fig.write_image("hemisphere_season_analysis.png", scale=2)
            print("✓ Exported hemisphere-season analysis to 'hemisphere_season_analysis.png'")
        
        return fig
    
    def get_hemisphere_stats(self):
        """Get statistics about hemisphere and season distribution"""
        # Hemisphere counts
        hemisphere_counts = self.df['hemisphere'].value_counts()
        print("Countries by Hemisphere:")
        print(hemisphere_counts)
        
        # Season distribution by hemisphere
        hemisphere_season = pd.crosstab(self.df['hemisphere'], self.df['season'])
        print("\nSeason Distribution by Hemisphere:")
        print(hemisphere_season)
        
        # Most common season for each hemisphere
        print("\nMost Common Season by Hemisphere:")
        for hemisphere in ['Northern', 'Southern']:
            if hemisphere in hemisphere_season.index:
                most_common = hemisphere_season.loc[hemisphere].idxmax()
                count = hemisphere_season.loc[hemisphere, most_common]
                print(f"{hemisphere}: {most_common} ({count} countries)")
        
        return hemisphere_counts, hemisphere_season

if __name__ == "__main__":
    # hem_counts, hem_season = Choropleth().get_hemisphere_stats()
    # print(hem_counts)
    # print(hem_season)
    hist = Choropleth().histogram_by_month(save=True)
    hist.show()
