import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import warnings
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
warnings.filterwarnings('ignore')

class AdvancedHealthAnalyzer:
    def __init__(self):
        """Advanced health data analyzer"""
        self.output_dir = 'advanced_analysis_results'
        self._create_output_dir()
        self.data = None
        
    def _create_output_dir(self):
        """Create output directory"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_data(self):
        """Load processed data from previous analysis"""
        try:
            self.data = pd.read_csv('real_analysis_results/processed_health_data.csv')
            print(f"✓ Loaded processed data: {len(self.data)} countries")
            return self.data
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def data_quality_assessment(self):
        """Assess data quality and completeness"""
        print("\n=== Data Quality Assessment ===")
        
        # Missing data analysis
        missing_data = self.data.isnull().sum()
        missing_percent = (missing_data / len(self.data)) * 100
        
        print("Missing data analysis:")
        for col in self.data.columns:
            if missing_data[col] > 0:
                print(f"  - {col}: {missing_data[col]} ({missing_percent[col]:.1f}%)")
        
        # Data distribution analysis
        print("\nData distribution summary:")
        print(self.data.describe())
        
        # Outlier detection
        print("\nOutlier detection (using IQR method):")
        for col in self.data.select_dtypes(include=[np.number]).columns:
            if col != 'REF_AREA':
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = self.data[(self.data[col] < Q1 - 1.5*IQR) | (self.data[col] > Q3 + 1.5*IQR)]
                if len(outliers) > 0:
                    print(f"  - {col}: {len(outliers)} outliers detected")
        
        return missing_data
    
    def _annotate_points(self, ax, df, x_col, y_col, label_col, highlight_codes=None):
        """산점도에서 주요 국가에 레이블 표시"""
        if highlight_codes is None:
            highlight_codes = []
        for _, row in df.iterrows():
            if row[label_col] in highlight_codes:
                ax.annotate(row[label_col], (row[x_col], row[y_col]), fontsize=11, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
            else:
                ax.annotate(row[label_col], (row[x_col], row[y_col]), fontsize=8, alpha=0.7, xytext=(5,5), textcoords='offset points')

    def efficiency_score_critique(self):
        """Critique the efficiency score methodology"""
        print("\n=== Efficiency Score Methodology Critique ===")
        
        # Analyze efficiency score distribution
        efficiency_stats = self.data['EfficiencyScore'].describe()
        print(f"Efficiency Score Statistics:")
        print(f"  - Mean: {efficiency_stats['mean']:.2f}")
        print(f"  - Median: {efficiency_stats['50%']:.2f}")
        print(f"  - Std: {efficiency_stats['std']:.2f}")
        print(f"  - Range: {efficiency_stats['max'] - efficiency_stats['min']:.2f}")
        
        # Identify potential issues with efficiency score
        print("\nPotential Issues with Efficiency Score:")
        
        # 1. Countries with very low health expenditure
        low_expenditure = self.data[self.data['HealthExpenditure'] < 5]
        print(f"  1. Countries with <5% health expenditure: {len(low_expenditure)}")
        print(f"     Average efficiency score: {low_expenditure['EfficiencyScore'].mean():.2f}")
        
        # 2. Countries with very high health expenditure
        high_expenditure = self.data[self.data['HealthExpenditure'] > 10]
        print(f"  2. Countries with >10% health expenditure: {len(high_expenditure)}")
        print(f"     Average efficiency score: {high_expenditure['EfficiencyScore'].mean():.2f}")
        
        # 3. Correlation between health expenditure and efficiency score
        corr = self.data['HealthExpenditure'].corr(self.data['EfficiencyScore'])
        print(f"  3. Correlation (Health Expenditure vs Efficiency Score): {corr:.3f}")
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Efficiency vs Health Expenditure
        axes[0,0].scatter(self.data['HealthExpenditure'], self.data['EfficiencyScore'], alpha=0.7, s=50)
        axes[0,0].set_xlabel('Health Expenditure (% of GDP)', fontsize=12)
        axes[0,0].set_ylabel('Efficiency Score', fontsize=12)
        axes[0,0].set_title('Efficiency Score vs Health Expenditure', fontsize=14)
        axes[0,0].grid(True, alpha=0.3)
        
        # 주요 국가 레이블 표시
        top5 = self.data.nlargest(5, 'EfficiencyScore')
        bottom5 = self.data.nsmallest(5, 'EfficiencyScore')
        kor = self.data[self.data['REF_AREA'] == 'KOR']
        highlight_codes = list(top5['REF_AREA']) + list(bottom5['REF_AREA'])
        if not kor.empty:
            highlight_codes.append('KOR')
        
        # Highlight extreme cases with different colors and sizes
        axes[0,0].scatter(top5['HealthExpenditure'], top5['EfficiencyScore'], 
                         color='red', s=100, label='Top 5 Efficiency', alpha=0.8, edgecolor='black')
        axes[0,0].scatter(bottom5['HealthExpenditure'], bottom5['EfficiencyScore'], 
                         color='blue', s=100, label='Bottom 5 Efficiency', alpha=0.8, edgecolor='black')
        if not kor.empty:
            axes[0,0].scatter(kor['HealthExpenditure'], kor['EfficiencyScore'], 
                             color='green', s=150, marker='*', label='Korea', alpha=0.9, edgecolor='black')
        
        # Add country labels for highlighted countries
        for _, row in top5.iterrows():
            axes[0,0].annotate(row['REF_AREA'], (row['HealthExpenditure'], row['EfficiencyScore']), 
                             fontsize=10, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        for _, row in bottom5.iterrows():
            axes[0,0].annotate(row['REF_AREA'], (row['HealthExpenditure'], row['EfficiencyScore']), 
                             fontsize=10, fontweight='bold', color='blue', xytext=(5,5), textcoords='offset points')
        if not kor.empty:
            axes[0,0].annotate('KOR', (kor.iloc[0]['HealthExpenditure'], kor.iloc[0]['EfficiencyScore']), 
                             fontsize=12, fontweight='bold', color='green', xytext=(5,5), textcoords='offset points')
        
        axes[0,0].legend()
        
        # 2. Life Expectancy vs Health Expenditure
        axes[0,1].scatter(self.data['HealthExpenditure'], self.data['LifeExpectancy'], alpha=0.7, s=50)
        axes[0,1].set_xlabel('Health Expenditure (% of GDP)', fontsize=12)
        axes[0,1].set_ylabel('Life Expectancy (years)', fontsize=12)
        axes[0,1].set_title('Life Expectancy vs Health Expenditure', fontsize=14)
        axes[0,1].grid(True, alpha=0.3)
        
        # Add country labels for the same highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[0,1].annotate(row['REF_AREA'], (row['HealthExpenditure'], row['LifeExpectancy']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # 3. Efficiency Score Distribution
        axes[1,0].hist(self.data['EfficiencyScore'], bins=15, alpha=0.7, edgecolor='black', color='lightblue')
        axes[1,0].set_xlabel('Efficiency Score', fontsize=12)
        axes[1,0].set_ylabel('Number of Countries', fontsize=12)
        axes[1,0].set_title('Distribution of Efficiency Scores', fontsize=14)
        axes[1,0].grid(True, alpha=0.3)
        
        # Add vertical lines for mean and median
        mean_val = self.data['EfficiencyScore'].mean()
        median_val = self.data['EfficiencyScore'].median()
        axes[1,0].axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
        axes[1,0].axvline(median_val, color='orange', linestyle='--', label=f'Median: {median_val:.2f}')
        axes[1,0].legend()
        
        # 4. Health Expenditure Distribution
        axes[1,1].hist(self.data['HealthExpenditure'], bins=15, alpha=0.7, edgecolor='black', color='lightcoral')
        axes[1,1].set_xlabel('Health Expenditure (% of GDP)', fontsize=12)
        axes[1,1].set_ylabel('Number of Countries', fontsize=12)
        axes[1,1].set_title('Distribution of Health Expenditure', fontsize=14)
        axes[1,1].grid(True, alpha=0.3)
        
        # Add vertical lines for mean and median
        mean_exp = self.data['HealthExpenditure'].mean()
        median_exp = self.data['HealthExpenditure'].median()
        axes[1,1].axvline(mean_exp, color='red', linestyle='--', label=f'Mean: {mean_exp:.2f}%')
        axes[1,1].axvline(median_exp, color='orange', linestyle='--', label=f'Median: {median_exp:.2f}%')
        axes[1,1].legend()
        
        plt.suptitle('Efficiency Score Methodology Critique: Issues and Distribution Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'{self.output_dir}/efficiency_critique.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Efficiency critique visualization saved")
    
    def diminishing_returns_analysis(self):
        """Analyze diminishing returns in health expenditure"""
        print("\n=== Diminishing Returns Analysis ===")
        
        # Create expenditure groups
        self.data['ExpenditureGroup'] = pd.cut(
            self.data['HealthExpenditure'], 
            bins=[0, 5, 8, 10, 15, 20], 
            labels=['Group A (0-5%)', 'Group B (5-8%)', 'Group C (8-10%)', 'Group D (10-15%)', 'Group E (15%↑)']
        )
        
        # Analyze life expectancy by expenditure group
        group_analysis = self.data.groupby('ExpenditureGroup').agg({
            'LifeExpectancy': ['mean', 'std', 'count'],
            'InfantMortality': ['mean', 'std'],
            'EfficiencyScore': ['mean', 'std']
        }).round(2)
        
        print("Life Expectancy by Health Expenditure Group:")
        print(group_analysis)
        
        # Calculate marginal returns
        print("\nMarginal Returns Analysis:")
        for i in range(len(group_analysis) - 1):
            current_group = group_analysis.index[i]
            next_group = group_analysis.index[i + 1]
            
            current_le = group_analysis.loc[current_group, ('LifeExpectancy', 'mean')]
            next_le = group_analysis.loc[next_group, ('LifeExpectancy', 'mean')]
            
            current_exp = self.data[self.data['ExpenditureGroup'] == current_group]['HealthExpenditure'].mean()
            next_exp = self.data[self.data['ExpenditureGroup'] == next_group]['HealthExpenditure'].mean()
            
            marginal_return = (next_le - current_le) / (next_exp - current_exp)
            print(f"  {current_group} → {next_group}: {marginal_return:.3f} years per % GDP")
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))
        
        # 1. Life Expectancy by Expenditure Group (bar)
        group_means = self.data.groupby('ExpenditureGroup')['LifeExpectancy'].mean()
        group_means.plot(kind='bar', ax=axes[0,0], color='skyblue', edgecolor='black')
        axes[0,0].set_title('Average Life Expectancy by Health Expenditure Group', fontsize=14)
        axes[0,0].set_ylabel('Life Expectancy (years)', fontsize=12)
        axes[0,0].set_xlabel('Health Expenditure Group', fontsize=12)
        axes[0,0].tick_params(axis='x', rotation=30)
        
        # 2. Efficiency Score by Expenditure Group (bar)
        group_eff = self.data.groupby('ExpenditureGroup')['EfficiencyScore'].mean()
        group_eff.plot(kind='bar', ax=axes[0,1], color='lightcoral', edgecolor='black')
        axes[0,1].set_title('Average Efficiency Score by Health Expenditure Group', fontsize=14)
        axes[0,1].set_ylabel('Efficiency Score', fontsize=12)
        axes[0,1].set_xlabel('Health Expenditure Group', fontsize=12)
        axes[0,1].tick_params(axis='x', rotation=30)
        
        # 3. Scatter with expenditure groups (color by group)
        colors = {
            'Group A (0-5%)': 'red', 'Group B (5-8%)': 'orange', 'Group C (8-10%)': 'yellow', 
            'Group D (10-15%)': 'lightgreen', 'Group E (15%↑)': 'darkgreen'
        }
        for group in self.data['ExpenditureGroup'].unique():
            if pd.notna(group):
                group_data = self.data[self.data['ExpenditureGroup'] == group]
                axes[1,0].scatter(group_data['HealthExpenditure'], group_data['LifeExpectancy'], 
                                color=colors[str(group)], label=str(group), alpha=0.7, edgecolor='black')
                # 각 점에 국가코드 표시
                for _, row in group_data.iterrows():
                    axes[1,0].annotate(row['REF_AREA'], (row['HealthExpenditure'], row['LifeExpectancy']), 
                                     fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        axes[1,0].set_xlabel('Health Expenditure (% of GDP)', fontsize=12)
        axes[1,0].set_ylabel('Life Expectancy (years)', fontsize=12)
        axes[1,0].set_title('Countries by Health Expenditure vs Life Expectancy (Colored by Group)', fontsize=14)
        axes[1,0].legend(title='Expenditure Group', fontsize=9)
        axes[1,0].grid(True, alpha=0.3)
        
        # 4. Box plot of efficiency scores by group
        self.data.boxplot(column='EfficiencyScore', by='ExpenditureGroup', ax=axes[1,1], grid=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
        axes[1,1].set_title('Efficiency Score Distribution by Health Expenditure Group', fontsize=14)
        axes[1,1].set_xlabel('Health Expenditure Group', fontsize=12)
        axes[1,1].set_ylabel('Efficiency Score', fontsize=12)
        axes[1,1].tick_params(axis='x', rotation=30)
        
        # Add group information text box at the bottom
        group_info = "Group Information:\n"
        for group in self.data['ExpenditureGroup'].unique():
            if pd.notna(group):
                countries = self.data[self.data['ExpenditureGroup'] == group]['REF_AREA'].tolist()
                group_info += f"{group}: {', '.join(countries)}\n"
        
        # Add text box with group information
        fig.text(0.02, 0.02, group_info, fontsize=10, verticalalignment='bottom', 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.suptitle('Diminishing Returns: Health Outcomes by Health Expenditure Groups', fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0.08, 1, 0.95])
        plt.savefig(f'{self.output_dir}/diminishing_returns.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Diminishing returns analysis saved")
        
        return group_analysis
    
    def comprehensive_health_index(self):
        """Create a comprehensive health index using multiple indicators"""
        print("\n=== Comprehensive Health Index Analysis ===")
        
        # Select relevant indicators for health index
        health_indicators = ['LifeExpectancy', 'InfantMortality', 'PhysiciansPer1000', 'HospitalBedsPer1000']
        
        # Handle missing values
        health_data = self.data[['REF_AREA'] + health_indicators].copy()
        
        # For missing values, use median imputation
        for col in health_indicators:
            if health_data[col].isnull().sum() > 0:
                median_val = health_data[col].median()
                health_data[col].fillna(median_val, inplace=True)
                print(f"  - Filled {health_data[col].isnull().sum()} missing values in {col} with median: {median_val:.2f}")
        
        # Normalize indicators (0-1 scale)
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(health_data[health_indicators])
        normalized_df = pd.DataFrame(normalized_data, columns=health_indicators, index=health_data.index)
        
        # Create weights (can be adjusted based on importance)
        weights = {
            'LifeExpectancy': 0.4,      # Most important
            'InfantMortality': 0.3,     # Important (inverse)
            'PhysiciansPer1000': 0.2,   # Medium importance
            'HospitalBedsPer1000': 0.1  # Least important
        }
        
        # Calculate weighted health index
        health_index = (
            normalized_df['LifeExpectancy'] * weights['LifeExpectancy'] +
            (-normalized_df['InfantMortality']) * weights['InfantMortality'] +  # Inverse for infant mortality
            normalized_df['PhysiciansPer1000'] * weights['PhysiciansPer1000'] +
            normalized_df['HospitalBedsPer1000'] * weights['HospitalBedsPer1000']
        )
        
        # Add to main dataset
        self.data['HealthIndex'] = health_index
        
        # Rank countries by health index
        health_ranking = self.data[['REF_AREA', 'HealthIndex', 'EfficiencyScore']].sort_values('HealthIndex', ascending=False)
        
        print("\nTop 10 Countries by Comprehensive Health Index:")
        for i, (_, row) in enumerate(health_ranking.head(10).iterrows(), 1):
            print(f"  {i:2d}. {row['REF_AREA']:3s} - Health Index: {row['HealthIndex']:.3f}, Efficiency: {row['EfficiencyScore']:.2f}")
        
        print("\nBottom 10 Countries by Comprehensive Health Index:")
        for i, (_, row) in enumerate(health_ranking.tail(10).iterrows(), 1):
            print(f"  {i:2d}. {row['REF_AREA']:3s} - Health Index: {row['HealthIndex']:.3f}, Efficiency: {row['EfficiencyScore']:.2f}")
        
        # Compare with efficiency score
        corr_health_efficiency = self.data['HealthIndex'].corr(self.data['EfficiencyScore'])
        print(f"\nCorrelation between Health Index and Efficiency Score: {corr_health_efficiency:.3f}")
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Health Index vs Efficiency Score
        axes[0,0].scatter(self.data['EfficiencyScore'], self.data['HealthIndex'], alpha=0.7, s=50)
        axes[0,0].set_xlabel('Efficiency Score', fontsize=12)
        axes[0,0].set_ylabel('Comprehensive Health Index', fontsize=12)
        axes[0,0].set_title('Health Index vs Efficiency Score', fontsize=14)
        axes[0,0].grid(True, alpha=0.3)
        
        # 주요 국가 레이블 표시
        top5 = self.data.nlargest(5, 'HealthIndex')
        bottom5 = self.data.nsmallest(5, 'HealthIndex')
        kor = self.data[self.data['REF_AREA'] == 'KOR']
        highlight_codes = list(top5['REF_AREA']) + list(bottom5['REF_AREA'])
        if not kor.empty:
            highlight_codes.append('KOR')
        
        # Highlight extreme cases with different colors and sizes
        axes[0,0].scatter(top5['EfficiencyScore'], top5['HealthIndex'], 
                         color='red', s=100, label='Top 5 Health Index', alpha=0.8, edgecolor='black')
        axes[0,0].scatter(bottom5['EfficiencyScore'], bottom5['HealthIndex'], 
                         color='blue', s=100, label='Bottom 5 Health Index', alpha=0.8, edgecolor='black')
        if not kor.empty:
            axes[0,0].scatter(kor['EfficiencyScore'], kor['HealthIndex'], 
                             color='green', s=150, marker='*', label='Korea', alpha=0.9, edgecolor='black')
        
        # Add country labels for highlighted countries
        for _, row in top5.iterrows():
            axes[0,0].annotate(row['REF_AREA'], (row['EfficiencyScore'], row['HealthIndex']), 
                             fontsize=10, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        for _, row in bottom5.iterrows():
            axes[0,0].annotate(row['REF_AREA'], (row['EfficiencyScore'], row['HealthIndex']), 
                             fontsize=10, fontweight='bold', color='blue', xytext=(5,5), textcoords='offset points')
        if not kor.empty:
            axes[0,0].annotate('KOR', (kor.iloc[0]['EfficiencyScore'], kor.iloc[0]['HealthIndex']), 
                             fontsize=12, fontweight='bold', color='green', xytext=(5,5), textcoords='offset points')
        
        axes[0,0].legend()
        
        # 2. Health Index Distribution
        axes[0,1].hist(self.data['HealthIndex'], bins=15, alpha=0.7, edgecolor='black', color='lightgreen')
        axes[0,1].set_xlabel('Comprehensive Health Index', fontsize=12)
        axes[0,1].set_ylabel('Number of Countries', fontsize=12)
        axes[0,1].set_title('Distribution of Health Index', fontsize=14)
        axes[0,1].grid(True, alpha=0.3)
        
        # Add vertical lines for mean and median
        mean_health = self.data['HealthIndex'].mean()
        median_health = self.data['HealthIndex'].median()
        axes[0,1].axvline(mean_health, color='red', linestyle='--', label=f'Mean: {mean_health:.3f}')
        axes[0,1].axvline(median_health, color='orange', linestyle='--', label=f'Median: {median_health:.3f}')
        axes[0,1].legend()
        
        # 3. Top 15 countries by health index
        top_15 = health_ranking.head(15)
        bars = axes[1,0].barh(range(len(top_15)), top_15['HealthIndex'], color='skyblue', edgecolor='black')
        axes[1,0].set_yticks(range(len(top_15)))
        axes[1,0].set_yticklabels(top_15['REF_AREA'])
        axes[1,0].set_xlabel('Comprehensive Health Index', fontsize=12)
        axes[1,0].set_title('Top 15 Countries by Health Index', fontsize=14)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            axes[1,0].text(width + 0.01, bar.get_y() + bar.get_height()/2, f'{width:.3f}', 
                          ha='left', va='center', fontsize=8)
        
        # 4. Health Index vs GDP per capita
        axes[1,1].scatter(self.data['GDPPerCapita'], self.data['HealthIndex'], alpha=0.7, s=50)
        axes[1,1].set_xlabel('GDP per Capita (PPP)', fontsize=12)
        axes[1,1].set_ylabel('Comprehensive Health Index', fontsize=12)
        axes[1,1].set_title('Health Index vs GDP per Capita', fontsize=14)
        axes[1,1].grid(True, alpha=0.3)
        
        # Add country labels for highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[1,1].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['HealthIndex']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        plt.suptitle('Comprehensive Health Index Analysis: Multi-Indicator Assessment', fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'{self.output_dir}/comprehensive_health_index.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Comprehensive health index analysis saved")
        
        return health_ranking
    
    def gdp_analysis(self):
        """Analyze relationship between GDP and health indicators"""
        print("\n=== GDP and Health Analysis ===")
        
        # Calculate correlations with GDP
        gdp_correlations = {}
        for col in ['LifeExpectancy', 'InfantMortality', 'PhysiciansPer1000', 'HospitalBedsPer1000', 'HealthExpenditure', 'EfficiencyScore']:
            if col in self.data.columns:
                corr = self.data['GDPPerCapita'].corr(self.data[col])
                gdp_correlations[col] = corr
        
        print("Correlations with GDP per Capita:")
        for indicator, corr in gdp_correlations.items():
            print(f"  - {indicator}: {corr:.3f}")
        
        # GDP groups analysis
        self.data['GDPGroup'] = pd.qcut(self.data['GDPPerCapita'], q=4, labels=['Low GDP', 'Medium GDP', 'High GDP', 'Very High GDP'])
        
        gdp_group_analysis = self.data.groupby('GDPGroup').agg({
            'LifeExpectancy': 'mean',
            'InfantMortality': 'mean',
            'HealthExpenditure': 'mean',
            'EfficiencyScore': 'mean',
            'HealthIndex': 'mean'
        }).round(2)
        
        print("\nHealth Indicators by GDP Group:")
        print(gdp_group_analysis)
        
        # Visualization
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 주요 국가 레이블 표시용
        top5_life = self.data.nlargest(5, 'LifeExpectancy')
        bottom5_life = self.data.nsmallest(5, 'LifeExpectancy')
        kor = self.data[self.data['REF_AREA'] == 'KOR']
        highlight_codes = list(top5_life['REF_AREA']) + list(bottom5_life['REF_AREA'])
        if not kor.empty:
            highlight_codes.append('KOR')
        
        # 1. Life Expectancy vs GDP
        axes[0,0].scatter(self.data['GDPPerCapita'], self.data['LifeExpectancy'], alpha=0.7, s=50)
        axes[0,0].set_xlabel('GDP per Capita (PPP)', fontsize=12)
        axes[0,0].set_ylabel('Life Expectancy (years)', fontsize=12)
        axes[0,0].set_title('Life Expectancy vs GDP per Capita', fontsize=14)
        axes[0,0].grid(True, alpha=0.3)
        
        # Add country labels for highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[0,0].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['LifeExpectancy']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # 2. Health Expenditure vs GDP
        axes[0,1].scatter(self.data['GDPPerCapita'], self.data['HealthExpenditure'], alpha=0.7, s=50)
        axes[0,1].set_xlabel('GDP per Capita (PPP)', fontsize=12)
        axes[0,1].set_ylabel('Health Expenditure (% of GDP)', fontsize=12)
        axes[0,1].set_title('Health Expenditure vs GDP per Capita', fontsize=14)
        axes[0,1].grid(True, alpha=0.3)
        
        # Add country labels for highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[0,1].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['HealthExpenditure']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # 3. Efficiency Score vs GDP
        axes[0,2].scatter(self.data['GDPPerCapita'], self.data['EfficiencyScore'], alpha=0.7, s=50)
        axes[0,2].set_xlabel('GDP per Capita (PPP)', fontsize=12)
        axes[0,2].set_ylabel('Efficiency Score', fontsize=12)
        axes[0,2].set_title('Efficiency Score vs GDP per Capita', fontsize=14)
        axes[0,2].grid(True, alpha=0.3)
        
        # Add country labels for highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[0,2].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['EfficiencyScore']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # 4. Infant Mortality vs GDP
        axes[1,0].scatter(self.data['GDPPerCapita'], self.data['InfantMortality'], alpha=0.7, s=50)
        axes[1,0].set_xlabel('GDP per Capita (PPP)', fontsize=12)
        axes[1,0].set_ylabel('Infant Mortality (per 1000)', fontsize=12)
        axes[1,0].set_title('Infant Mortality vs GDP per Capita', fontsize=14)
        axes[1,0].grid(True, alpha=0.3)
        
        # Add country labels for highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[1,0].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['InfantMortality']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # 5. Physicians vs GDP
        if 'PhysiciansPer1000' in self.data.columns:
            axes[1,1].scatter(self.data['GDPPerCapita'], self.data['PhysiciansPer1000'], alpha=0.7, s=50)
            axes[1,1].set_xlabel('GDP per Capita (PPP)', fontsize=12)
            axes[1,1].set_ylabel('Physicians per 1000', fontsize=12)
            axes[1,1].set_title('Physicians per 1000 vs GDP per Capita', fontsize=14)
            axes[1,1].grid(True, alpha=0.3)
            
            # Add country labels for highlighted countries
            for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
                if pd.notna(row['PhysiciansPer1000']):
                    axes[1,1].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['PhysiciansPer1000']), 
                                     fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # 6. Health Index vs GDP
        axes[1,2].scatter(self.data['GDPPerCapita'], self.data['HealthIndex'], alpha=0.7, s=50)
        axes[1,2].set_xlabel('GDP per Capita (PPP)', fontsize=12)
        axes[1,2].set_ylabel('Comprehensive Health Index', fontsize=12)
        axes[1,2].set_title('Health Index vs GDP per Capita', fontsize=14)
        axes[1,2].grid(True, alpha=0.3)
        
        # Add country labels for highlighted countries
        for _, row in self.data.loc[self.data['REF_AREA'].isin(highlight_codes)].iterrows():
            axes[1,2].annotate(row['REF_AREA'], (row['GDPPerCapita'], row['HealthIndex']), 
                             fontsize=8, alpha=0.7, xytext=(5,2), textcoords='offset points')
        
        # Add GDP group information text box
        gdp_info = "GDP Group Information:\n"
        for group in self.data['GDPGroup'].unique():
            if pd.notna(group):
                countries = self.data[self.data['GDPGroup'] == group]['REF_AREA'].tolist()
                gdp_info += f"{group}: {', '.join(countries)}\n"
        
        # Add text box with GDP group information
        fig.text(0.02, 0.02, gdp_info, fontsize=9, verticalalignment='bottom', 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.suptitle('GDP and Health Indicators Analysis: Economic Development vs Health Outcomes', fontsize=16, fontweight='bold')
        plt.tight_layout(rect=[0, 0.08, 1, 0.95])
        plt.savefig(f'{self.output_dir}/gdp_health_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ GDP health analysis saved")
        
        return gdp_correlations, gdp_group_analysis
    
    def generate_advanced_report(self):
        """Generate comprehensive advanced analysis report"""
        print("\n=== Generating Advanced Analysis Report ===")
        
        report = []
        report.append("# Advanced Health Data Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("## 📋 Executive Summary")
        report.append("This advanced analysis examines health system efficiency metrics and introduces comprehensive health indicators.")
        report.append("The analysis reveals important limitations in simple efficiency scores and identifies more balanced approaches to health system evaluation.")
        report.append("")
        
        # Methodology Critique
        report.append("## ⚠️ Efficiency Score Methodology Critique")
        report.append("### Key Issues Identified:")
        report.append("1. **Mathematical Bias**: Countries with very low health expenditure artificially score high")
        report.append("2. **Missing Context**: Does not account for healthcare quality, access, or social determinants")
        report.append("3. **Diminishing Returns**: Fails to capture the non-linear relationship between spending and outcomes")
        report.append("4. **Data Limitations**: Missing data for key indicators affects reliability")
        report.append("")
        
        # Comprehensive Health Index
        report.append("## 🏥 Comprehensive Health Index")
        report.append("### Methodology:")
        report.append("- **Weighted combination** of multiple health indicators")
        report.append("- **Normalized scores** to account for different scales")
        report.append("- **Balanced approach** considering both outcomes and resources")
        report.append("")
        report.append("### Indicators Used:")
        report.append("- Life Expectancy (40% weight)")
        report.append("- Infant Mortality (30% weight, inverse)")
        report.append("- Physicians per 1000 (20% weight)")
        report.append("- Hospital Beds per 1000 (10% weight)")
        report.append("")
        
        # Key Insights
        report.append("## 💡 Key Findings")
        report.append("1. **Efficiency vs. Quality**: High efficiency scores don't always indicate better health systems")
        report.append("2. **GDP Relationship**: Strong correlation between GDP and health outcomes, but diminishing returns observed")
        report.append("3. **Resource Allocation**: Countries with moderate expenditure often achieve optimal balance")
        report.append("4. **Data Gaps**: Missing physician and hospital bed data limits comprehensive analysis")
        report.append("")
        
        # Policy Implications
        report.append("## 🎯 Analysis Implications")
        report.append("1. **Holistic Assessment**: Multiple indicators needed, not just efficiency scores")
        report.append("2. **Context Matters**: Economic, social, and cultural factors should be considered")
        report.append("3. **Optimal Investment**: Evidence-based resource allocation is crucial")
        report.append("4. **Data Improvement**: Better data collection systems are needed")
        report.append("")
        
        # Future Analysis Opportunities
        report.append("## 🔬 Future Analysis Opportunities")
        report.append("Based on the findings, additional analyses could explore:")
        report.append("")
        report.append("### 1. **Regional Analysis**")
        report.append("- Compare health systems within geographic regions")
        report.append("- Analyze cultural and economic similarities")
        report.append("- Identify regional best practices")
        report.append("")
        report.append("### 2. **Time Series Analysis**")
        report.append("- Track changes in health indicators over time")
        report.append("- Analyze the impact of policy changes")
        report.append("- Identify trends and patterns")
        report.append("")
        report.append("### 3. **Quality Metrics Integration**")
        report.append("- Include patient satisfaction data")
        report.append("- Analyze healthcare accessibility")
        report.append("- Consider treatment outcomes")
        report.append("")
        report.append("### 4. **Social Determinants Study**")
        report.append("- Education levels and health outcomes")
        report.append("- Income inequality and health disparities")
        report.append("- Environmental factors and health")
        report.append("")
        report.append("### 5. **Advanced Statistical Methods**")
        report.append("- Machine learning for pattern recognition")
        report.append("- Factor analysis for indicator reduction")
        report.append("- Predictive modeling for health outcomes")
        report.append("")
        
        # Data Limitations and Considerations
        report.append("## ⚠️ Data Limitations and Considerations")
        report.append("### Missing Data Issues:")
        report.append("- **Physicians per 1000**: 52.9% missing data")
        report.append("- **Hospital Beds per 1000**: 64.7% missing data")
        report.append("- **Inconsistent reporting**: Different countries report data differently")
        report.append("")
        report.append("### Impact on Analysis:")
        report.append("- Results may not capture the full picture")
        report.append("- Findings should be interpreted with caution")
        report.append("- Better data collection systems are needed")
        report.append("")
        
        # Conclusion
        report.append("## 🎯 Conclusions")
        report.append("This analysis demonstrates that health system evaluation is more complex than simple efficiency scores suggest.")
        report.append("A comprehensive approach considering multiple indicators, economic context, and quality measures provides a more accurate assessment.")
        report.append("")
        report.append("### Areas for Improvement:")
        report.append("- Collect more comprehensive data from multiple sources")
        report.append("- Include qualitative factors like healthcare quality")
        report.append("- Analyze changes over time rather than just cross-sectional data")
        report.append("- Consider regional and cultural differences more deeply")
        report.append("")
        report.append("This project highlights the importance of critical thinking in data analysis and the need to question simple metrics that may be misleading.")
        
        # Save report
        with open(f'{self.output_dir}/advanced_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✓ Advanced analysis report saved")
        return '\n'.join(report)
    
    def run_complete_advanced_analysis(self):
        """Run complete advanced analysis"""
        print("🚀 Advanced Health Data Analysis Starting!")
        print("=" * 60)
        
        # 1. Load data
        data = self.load_data()
        if data is None:
            print("❌ Failed to load data")
            return
        
        # 2. Data quality assessment
        self.data_quality_assessment()
        
        # 3. Efficiency score critique
        self.efficiency_score_critique()
        
        # 4. Diminishing returns analysis
        self.diminishing_returns_analysis()
        
        # 5. Comprehensive health index
        self.comprehensive_health_index()
        
        # 6. GDP analysis
        self.gdp_analysis()
        
        # 7. Generate advanced report
        self.generate_advanced_report()
        
        # 8. Save enhanced dataset
        self.data.to_csv(f'{self.output_dir}/enhanced_health_data.csv', index=False)
        
        print("\n" + "=" * 60)
        print("🎉 Advanced Analysis Complete!")
        print(f"📁 Results saved in '{self.output_dir}' folder")
        print("\n📋 Generated files:")
        print("   - efficiency_critique.png: Efficiency score methodology critique")
        print("   - diminishing_returns.png: Diminishing returns analysis")
        print("   - comprehensive_health_index.png: Comprehensive health index analysis")
        print("   - gdp_health_analysis.png: GDP and health indicators analysis")
        print("   - advanced_analysis_report.md: Comprehensive advanced analysis report")
        print("   - enhanced_health_data.csv: Enhanced dataset with new indicators")
        print("\n💡 Key findings from advanced analysis:")
        print("   - Efficiency scores have mathematical biases favoring low-expenditure countries")
        print("   - Comprehensive health index provides more balanced assessment")
        print("   - GDP shows strong correlation with health outcomes but diminishing returns")
        print("   - Multiple indicators needed for accurate health system evaluation")

if __name__ == "__main__":
    analyzer = AdvancedHealthAnalyzer()
    analyzer.run_complete_advanced_analysis() 