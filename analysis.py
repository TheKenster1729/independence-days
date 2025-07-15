import pandas as pd
import numpy as np
import plotly.express as px
from scipy.special import comb

class BinomialDistribution:
    def __init__(self, n: int, p: float):
        self.n = n
        self.p = p

    def pmf(self, k: int) -> float:
        return comb(self.n, k) * self.p**k * (1 - self.p)**(self.n - k)
    
    def plot_distribution(self, k: np.array = np.arange(1, 5)):
        to_graph = [self.pmf(i)*365 for i in k]
        fig = px.bar(x=k, y=to_graph, title="Independence/National Day Overlaps", labels={"x": "Overlap Size", "y": "Expected Number of Overlapping Days"},
                     color_discrete_sequence=px.colors.qualitative.Set3)
        
        # Update layout for white background and emphasized axes
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': 'black'},
            margin=dict(l=60, r=30, t=60, b=60)
        )
        
        # Update x-axis to show only integers and emphasize it
        fig.update_xaxes(
            tickmode='linear',
            tick0=1,
            dtick=1,
            tickfont={'size': 12, 'color': 'black'},
            title_font={'size': 14, 'color': 'black'},
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=False
        )
        
        # Update y-axis to emphasize it
        fig.update_yaxes(
            tickfont={'size': 12, 'color': 'black'},
            title_font={'size': 14, 'color': 'black'},
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=False
        )
        
        # Add text annotations at the top of each bar
        for i, (x_val, y_val) in enumerate(zip(k, to_graph)):
            fig.add_annotation(
                x=x_val,
                y=y_val,
                text=f'{round(y_val)}',
                showarrow=False,
                yshift=10,
                font=dict(size=12, color='black')
            )
        
        return fig

class EmpiricalOverlaps:
    def __init__(self, path_to_data: str = "independence_and_national_days_updated.csv"):
        self.path_to_data = path_to_data
        self.data = None
        self.load_data()
        
    def load_data(self):
        """Load and parse the independence/national days data"""
        self.data = pd.read_csv(self.path_to_data)
        # Convert Display Date to datetime for analysis
        self.data['date'] = pd.to_datetime(self.data['Display Date'], format='%d.%b', errors='coerce')
        # Filter out rows where date parsing failed
        self.data = self.data.dropna(subset=['date'])
        
    def count_overlaps(self):
        """Count the actual number of overlaps in the data"""
        # Group by date and count occurrences
        date_counts = self.data['date'].value_counts()
        
        # Count overlaps of different sizes
        overlap_counts = {}
        for size in range(1, 6):  # Check overlaps of size 1-5
            count = len(date_counts[date_counts == size])
            overlap_counts[size] = count
            
        return overlap_counts
    
    def plot_combined_distribution(self, binomial_dist):
        """Create a combined plot showing both expected and empirical overlaps"""
        # Get empirical counts
        empirical_counts = self.count_overlaps()
        k_values = list(empirical_counts.keys())
        empirical_values = list(empirical_counts.values())
        
        # Get expected values from binomial distribution
        expected_values = [round(binomial_dist.pmf(i) * 365) for i in k_values]
        
        # Create the plot
        fig = px.bar(
            x=k_values,
            y=[empirical_values, expected_values],
            title="Independence/National Day Overlaps: Expected vs Empirical",
            labels={"x": "Overlap Size", "y": "Number of Overlapping Days", "variable": "Type"},
            barmode='group',
            color_discrete_sequence=[px.colors.qualitative.Set2[0], '#ff7f0e']  # Keep first Set2 color, use orange for second
        )
        
        # Update layout for white background and emphasized axes
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': 'black'},
            margin=dict(l=60, r=30, t=60, b=60),
            legend=dict(
                title="Data Type",
                x=0.98,
                y=0.98,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='black',
                borderwidth=1
            )
        )
        
        # Update x-axis
        fig.update_xaxes(
            tickmode='linear',
            tick0=1,
            dtick=1,
            tickfont={'size': 12, 'color': 'black'},
            title_font={'size': 14, 'color': 'black'},
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=False
        )
        
        # Update y-axis
        fig.update_yaxes(
            tickfont={'size': 12, 'color': 'black'},
            title_font={'size': 14, 'color': 'black'},
            zerolinecolor='black',
            zerolinewidth=2,
            showline=True,
            linewidth=2,
            linecolor='black',
            title = "Number of Overlapping Days",
            showgrid=False
        )
        
        # Update legend labels
        fig.data[0].name = "Empirical (Actual)"
        fig.data[1].name = "Expected (Binomial)"
        
        # Add value labels on bars with proper positioning for grouped bars
        for i, trace in enumerate(fig.data):
            for j, (x_val, y_val) in enumerate(zip(k_values, [empirical_values, expected_values][i])):
                # Calculate proper x offset for grouped bars
                x_offset = (i - 0.5) * 0.4  # Center each bar in its group
                fig.add_annotation(
                    x=x_val + x_offset,
                    y=y_val,
                    text=f'{y_val}',
                    showarrow=False,
                    yshift=10,
                    font=dict(size=10, color='black')
                )
        
        return fig

if __name__ == "__main__":
    # # Create theoretical binomial distribution
    # binomial = BinomialDistribution(n=201, p=1/365)
    # fig_theoretical = binomial.plot_distribution()
    # fig_theoretical.write_image("independence_national_day_overlaps_theoretical.png", scale = 2)
    
    # # Create empirical analysis and combined plot
    # empirical = EmpiricalOverlaps()
    # fig_combined = empirical.plot_combined_distribution(binomial)
    # fig_combined.write_image("independence_national_day_overlaps_with_empirical.png", scale = 2)
    fig = EmpiricalOverlaps().plot_combined_distribution(BinomialDistribution(n=201, p=1/365))
    fig.write_image("independence_national_day_overlaps_with_empirical.png", scale = 2)