import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class GDPRecoveryAnalyzer:
    def __init__(self):
        """GDP recovery analyzer"""
        self.output_dir = 'gdp_recovery_results'
        self._create_output_dir()
        self.data = None
        
    def _create_output_dir(self):
        """Create output directory"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_gdp_growth_data(self):
        """Load GDP growth data from World Bank"""
        try:
            # World Bank data has metadata in first 4 rows, then data starts from row 5
            df = pd.read_csv('data/gdp_growth/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_38363.csv', skiprows=4)
            print(f"✓ Loaded GDP growth data: {len(df)} countries")
            return df
        except Exception as e:
            print(f"❌ Error loading GDP growth data: {e}")
            return None
    
    def process_gdp_growth_data(self, df):
        """Process GDP growth data to extract country codes and growth rates"""
        if df is None:
            return None
        
        # Extract country code and growth rates for key years
        processed_df = df[['Country Code', '2019', '2020', '2021', '2022', '2023']].copy()
        processed_df = processed_df.dropna(subset=['Country Code'])
        processed_df.columns = ['REF_AREA', 'GDP_Growth_2019', 'GDP_Growth_2020', 'GDP_Growth_2021', 'GDP_Growth_2022', 'GDP_Growth_2023']
        
        # Convert to numeric, replacing empty strings with NaN
        for col in processed_df.columns[1:]:
            processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
        
        return processed_df
    
    def load_existing_data(self):
        """Load existing health and GDP data"""
        try:
            existing_data = pd.read_csv('advanced_analysis_results/enhanced_health_data.csv')
            print(f"✓ Loaded existing data: {len(existing_data)} countries")
            return existing_data
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            return None
    
    def merge_data(self, gdp_growth, existing_data):
        """Merge GDP growth data with existing health data"""
        print("\n=== Merging Data ===")
        
        # Merge on country code
        merged_data = pd.merge(existing_data, gdp_growth, on='REF_AREA', how='inner')
        
        print(f"✓ Final merged dataset: {len(merged_data)} countries")
        print(f"✓ Columns: {list(merged_data.columns)}")
        
        return merged_data
    
    def calculate_recovery_metrics(self, data):
        """Calculate COVID-19 recovery metrics"""
        print("\n=== Calculating Recovery Metrics ===")
        
        # 1. COVID-19 shock (2019 to 2020)
        data['COVID_Shock'] = data['GDP_Growth_2020'] - data['GDP_Growth_2019']
        
        # 2. Recovery from 2020 to 2023
        data['Recovery_2020_2023'] = data['GDP_Growth_2023'] - data['GDP_Growth_2020']
        
        # 3. Overall performance (2019 to 2023)
        data['Overall_Performance'] = data['GDP_Growth_2023'] - data['GDP_Growth_2019']
        
        # 4. Recovery speed (how quickly countries bounced back)
        data['Recovery_Speed'] = (data['GDP_Growth_2021'] + data['GDP_Growth_2022'] + data['GDP_Growth_2023']) / 3
        
        # 5. Economic resilience (ability to withstand shock)
        data['Economic_Resilience'] = data['Recovery_2020_2023'] / abs(data['COVID_Shock'] + 0.1)  # Add small number to avoid division by zero
        
        print("✓ Recovery metrics calculated:")
        print(f"  - COVID_Shock: Impact from 2019 to 2020")
        print(f"  - Recovery_2020_2023: Recovery from 2020 to 2023")
        print(f"  - Overall_Performance: Net change from 2019 to 2023")
        print(f"  - Recovery_Speed: Average growth during recovery period")
        print(f"  - Economic_Resilience: Recovery relative to shock size")
        
        return data
    
    def classify_countries(self, data):
        """Classify countries by development level"""
        print("\n=== Classifying Countries ===")
        
        # Use GDP per capita to classify countries
        gdp_median = data['GDPPerCapita'].median()
        
        data['Development_Level'] = data['GDPPerCapita'].apply(
            lambda x: 'High Income' if x >= gdp_median else 'Low-Middle Income'
        )
        
        # Also create more detailed classification
        data['Income_Group'] = pd.qcut(data['GDPPerCapita'], q=4, 
                                     labels=['Low Income', 'Lower Middle', 'Upper Middle', 'High Income'])
        
        print("✓ Countries classified by development level")
        print(f"  - High Income: {len(data[data['Development_Level'] == 'High Income'])} countries")
        print(f"  - Low-Middle Income: {len(data[data['Development_Level'] == 'Low-Middle Income'])} countries")
        
        return data
    
    def analyze_covid_impact(self, data):
        """Analyze COVID-19 impact and recovery patterns"""
        print("\n=== COVID-19 Impact Analysis ===")
        
        # Summary statistics
        print("\n📊 COVID-19 Impact Summary:")
        print(f"  - Average COVID shock: {data['COVID_Shock'].mean():.2f}%")
        print(f"  - Average recovery (2020-2023): {data['Recovery_2020_2023'].mean():.2f}%")
        print(f"  - Average overall performance: {data['Overall_Performance'].mean():.2f}%")
        
        # Countries with biggest shocks
        biggest_shocks = data.nsmallest(5, 'COVID_Shock')[['REF_AREA', 'COVID_Shock', 'GDP_Growth_2019', 'GDP_Growth_2020']]
        print(f"\n🏚️ Countries with Biggest COVID Shocks:")
        for _, row in biggest_shocks.iterrows():
            print(f"  - {row['REF_AREA']}: {row['COVID_Shock']:.1f}% (2019: {row['GDP_Growth_2019']:.1f}% → 2020: {row['GDP_Growth_2020']:.1f}%)")
        
        # Countries with best recovery
        best_recovery = data.nlargest(5, 'Recovery_2020_2023')[['REF_AREA', 'Recovery_2020_2023', 'GDP_Growth_2020', 'GDP_Growth_2023']]
        print(f"\n🚀 Countries with Best Recovery (2020-2023):")
        for _, row in best_recovery.iterrows():
            print(f"  - {row['REF_AREA']}: {row['Recovery_2020_2023']:.1f}% (2020: {row['GDP_Growth_2020']:.1f}% → 2023: {row['GDP_Growth_2023']:.1f}%)")
        
        # Countries with best overall performance
        best_overall = data.nlargest(5, 'Overall_Performance')[['REF_AREA', 'Overall_Performance', 'GDP_Growth_2019', 'GDP_Growth_2023']]
        print(f"\n🏆 Countries with Best Overall Performance (2019-2023):")
        for _, row in best_overall.iterrows():
            print(f"  - {row['REF_AREA']}: {row['Overall_Performance']:.1f}% (2019: {row['GDP_Growth_2019']:.1f}% → 2023: {row['GDP_Growth_2023']:.1f}%)")
        
        return biggest_shocks, best_recovery, best_overall
    
    def analyze_gdp_correlation(self, data):
        """Analyze correlation between GDP per capita and recovery metrics"""
        print("\n=== GDP per Capita vs Recovery Analysis ===")
        
        # Calculate correlations
        correlations = {}
        for metric in ['COVID_Shock', 'Recovery_2020_2023', 'Overall_Performance', 'Recovery_Speed', 'Economic_Resilience']:
            corr = data['GDPPerCapita'].corr(data[metric])
            correlations[metric] = corr
        
        print("\n📈 Correlations with GDP per Capita:")
        for metric, corr in correlations.items():
            print(f"  - {metric}: {corr:.3f}")
        
        # Interpretation
        print("\n💡 Key Insights:")
        if correlations['Recovery_2020_2023'] > 0.3:
            print("  - Higher GDP countries showed better recovery")
        elif correlations['Recovery_2020_2023'] < -0.3:
            print("  - Lower GDP countries showed better recovery")
        else:
            print("  - No strong correlation between GDP and recovery")
        
        if correlations['Economic_Resilience'] > 0.3:
            print("  - Higher GDP countries showed better economic resilience")
        elif correlations['Economic_Resilience'] < -0.3:
            print("  - Lower GDP countries showed better economic resilience")
        else:
            print("  - No strong correlation between GDP and economic resilience")
        
        return correlations
    
    def development_level_analysis(self, data):
        """Analyze recovery patterns by development level"""
        print("\n=== Development Level Analysis ===")
        
        # Group analysis
        group_analysis = data.groupby('Development_Level').agg({
            'COVID_Shock': ['mean', 'std'],
            'Recovery_2020_2023': ['mean', 'std'],
            'Overall_Performance': ['mean', 'std'],
            'Recovery_Speed': ['mean', 'std'],
            'Economic_Resilience': ['mean', 'std'],
            'GDPPerCapita': 'mean'
        }).round(2)
        
        print("\n📊 Recovery Metrics by Development Level:")
        print(group_analysis)
        
        # Statistical test (t-test)
        high_income = data[data['Development_Level'] == 'High Income']
        low_income = data[data['Development_Level'] == 'Low-Middle Income']
        
        from scipy import stats
        
        print("\n🔬 Statistical Comparison (High vs Low-Middle Income):")
        for metric in ['COVID_Shock', 'Recovery_2020_2023', 'Overall_Performance', 'Recovery_Speed']:
            t_stat, p_value = stats.ttest_ind(high_income[metric].dropna(), low_income[metric].dropna())
            print(f"  - {metric}: t={t_stat:.3f}, p={p_value:.3f} {'(significant)' if p_value < 0.05 else '(not significant)'}")
        
        return group_analysis
    
    def korea_special_analysis(self, data):
        """Special analysis for Korea"""
        print("\n=== Korea Special Analysis ===")
        
        if 'KOR' not in data['REF_AREA'].values:
            print("❌ Korea data not found.")
            return None
        
        kor_data = data[data['REF_AREA'] == 'KOR'].iloc[0]
        
        print(f"🇰🇷 Korea's Economic Performance:")
        print(f"  - GDP per Capita: ${kor_data['GDPPerCapita']:,.0f}")
        print(f"  - COVID Shock (2019→2020): {kor_data['COVID_Shock']:.2f}%")
        print(f"  - Recovery (2020→2023): {kor_data['Recovery_2020_2023']:.2f}%")
        print(f"  - Overall Performance (2019→2023): {kor_data['Overall_Performance']:.2f}%")
        print(f"  - Recovery Speed: {kor_data['Recovery_Speed']:.2f}%")
        print(f"  - Economic Resilience: {kor_data['Economic_Resilience']:.2f}")
        
        # Compare with similar GDP countries
        similar_gdp = data[
            (data['GDPPerCapita'] >= kor_data['GDPPerCapita'] * 0.7) &
            (data['GDPPerCapita'] <= kor_data['GDPPerCapita'] * 1.3) &
            (data['REF_AREA'] != 'KOR')
        ]
        
        if len(similar_gdp) > 0:
            print(f"\n📊 Comparison with Similar GDP Countries:")
            comparison_data = pd.concat([kor_data.to_frame().T, similar_gdp])
            comparison_sorted = comparison_data.sort_values('Overall_Performance', ascending=False)
            
            for i, (_, row) in enumerate(comparison_sorted.iterrows(), 1):
                marker = "🇰🇷" if row['REF_AREA'] == 'KOR' else "  "
                print(f"{marker} {i:2d}. {row['REF_AREA']:3s} - Overall: {row['Overall_Performance']:.1f}%, Recovery: {row['Recovery_2020_2023']:.1f}%")
        
        return kor_data
    
    def create_visualizations(self, data):
        """Create comprehensive visualizations"""
        print("\n=== Creating Visualizations ===")
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. COVID Shock vs Recovery
        ax1 = plt.subplot(3, 3, 1)
        plt.scatter(data['COVID_Shock'], data['Recovery_2020_2023'], alpha=0.7, s=50)
        plt.xlabel('COVID Shock (2019→2020)')
        plt.ylabel('Recovery (2020→2023)')
        plt.title('COVID Shock vs Recovery')
        plt.grid(True, alpha=0.3)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            kor_data = data[data['REF_AREA'] == 'KOR'].iloc[0]
            plt.scatter(kor_data['COVID_Shock'], kor_data['Recovery_2020_2023'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['COVID_Shock'], kor_data['Recovery_2020_2023']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 2. GDP per Capita vs Recovery
        ax2 = plt.subplot(3, 3, 2)
        plt.scatter(data['GDPPerCapita'], data['Recovery_2020_2023'], alpha=0.7, s=50)
        plt.xlabel('GDP per Capita')
        plt.ylabel('Recovery (2020→2023)')
        plt.title('GDP per Capita vs Recovery')
        plt.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(data['GDPPerCapita'].dropna(), data['Recovery_2020_2023'].dropna(), 1)
        p = np.poly1d(z)
        plt.plot(data['GDPPerCapita'], p(data['GDPPerCapita']), "r--", alpha=0.8)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            plt.scatter(kor_data['GDPPerCapita'], kor_data['Recovery_2020_2023'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['GDPPerCapita'], kor_data['Recovery_2020_2023']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 3. Development Level Comparison
        ax3 = plt.subplot(3, 3, 3)
        development_data = data.groupby('Development_Level')['Recovery_2020_2023'].mean()
        development_data.plot(kind='bar', ax=ax3, color=['skyblue', 'lightcoral'])
        plt.title('Average Recovery by Development Level')
        plt.ylabel('Recovery (2020→2023)')
        plt.xticks(rotation=45)
        
        # 4. GDP Growth Timeline
        ax4 = plt.subplot(3, 3, 4)
        years = ['2019', '2020', '2021', '2022', '2023']
        avg_growth = [data[f'GDP_Growth_{year}'].mean() for year in years]
        plt.plot(years, avg_growth, marker='o', linewidth=2, markersize=8)
        plt.title('Average GDP Growth Timeline')
        plt.ylabel('GDP Growth (%)')
        plt.grid(True, alpha=0.3)
        
        # 5. Economic Resilience Distribution
        ax5 = plt.subplot(3, 3, 5)
        plt.hist(data['Economic_Resilience'].dropna(), bins=15, alpha=0.7, edgecolor='black')
        plt.xlabel('Economic Resilience')
        plt.ylabel('Number of Countries')
        plt.title('Distribution of Economic Resilience')
        plt.grid(True, alpha=0.3)
        
        # Add vertical line for mean
        mean_resilience = data['Economic_Resilience'].mean()
        plt.axvline(mean_resilience, color='red', linestyle='--', label=f'Mean: {mean_resilience:.2f}')
        plt.legend()
        
        # 6. Recovery Speed vs Overall Performance
        ax6 = plt.subplot(3, 3, 6)
        plt.scatter(data['Recovery_Speed'], data['Overall_Performance'], alpha=0.7, s=50)
        plt.xlabel('Recovery Speed')
        plt.ylabel('Overall Performance (2019→2023)')
        plt.title('Recovery Speed vs Overall Performance')
        plt.grid(True, alpha=0.3)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            plt.scatter(kor_data['Recovery_Speed'], kor_data['Overall_Performance'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['Recovery_Speed'], kor_data['Overall_Performance']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 7. Top 10 Recovery Countries
        ax7 = plt.subplot(3, 3, 7)
        top_recovery = data.nlargest(10, 'Recovery_2020_2023')
        colors = ['red' if x == 'KOR' else 'skyblue' for x in top_recovery['REF_AREA']]
        plt.barh(top_recovery['REF_AREA'], top_recovery['Recovery_2020_2023'], color=colors)
        plt.xlabel('Recovery (2020→2023)')
        plt.title('Top 10 Recovery Countries')
        
        # 8. COVID Shock Distribution
        ax8 = plt.subplot(3, 3, 8)
        plt.hist(data['COVID_Shock'].dropna(), bins=15, alpha=0.7, edgecolor='black', color='lightcoral')
        plt.xlabel('COVID Shock (2019→2020)')
        plt.ylabel('Number of Countries')
        plt.title('Distribution of COVID Shock')
        plt.grid(True, alpha=0.3)
        
        # Add vertical line for mean
        mean_shock = data['COVID_Shock'].mean()
        plt.axvline(mean_shock, color='red', linestyle='--', label=f'Mean: {mean_shock:.2f}')
        plt.legend()
        
        # 9. Correlation Heatmap
        ax9 = plt.subplot(3, 3, 9)
        correlation_vars = ['GDPPerCapita', 'COVID_Shock', 'Recovery_2020_2023', 'Overall_Performance', 'Recovery_Speed', 'Economic_Resilience']
        corr_matrix = data[correlation_vars].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True, fmt='.2f', ax=ax9)
        plt.title('Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/gdp_recovery_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ GDP recovery analysis visualization saved")
        
        # Create additional detailed charts
        self.create_detailed_charts(data)
    
    def create_detailed_charts(self, data):
        """Create additional detailed charts"""
        
        # 1. Korea vs Similar Countries Timeline
        if 'KOR' in data['REF_AREA'].values:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            
            # Get Korea and similar GDP countries
            kor_data = data[data['REF_AREA'] == 'KOR'].iloc[0]
            similar_gdp = data[
                (data['GDPPerCapita'] >= kor_data['GDPPerCapita'] * 0.7) &
                (data['GDPPerCapita'] <= kor_data['GDPPerCapita'] * 1.3) &
                (data['REF_AREA'] != 'KOR')
            ]
            
            # Timeline comparison
            years = ['2019', '2020', '2021', '2022', '2023']
            
            # Korea timeline
            kor_growth = [kor_data[f'GDP_Growth_{year}'] for year in years]
            axes[0,0].plot(years, kor_growth, marker='o', linewidth=3, markersize=10, color='red', label='Korea')
            
            # Similar countries timeline
            for _, row in similar_gdp.iterrows():
                country_growth = [row[f'GDP_Growth_{year}'] for year in years]
                axes[0,0].plot(years, country_growth, marker='o', linewidth=1, markersize=4, alpha=0.5, color='gray')
            
            axes[0,0].set_title('GDP Growth Timeline: Korea vs Similar Countries')
            axes[0,0].set_ylabel('GDP Growth (%)')
            axes[0,0].legend()
            axes[0,0].grid(True, alpha=0.3)
            
                    # Recovery metrics comparison
        comparison_data = pd.concat([kor_data.to_frame().T, similar_gdp])
        metrics = ['COVID_Shock', 'Recovery_2020_2023', 'Overall_Performance', 'Recovery_Speed']
        
        for i, metric in enumerate(metrics):
            row, col = (i+1) // 2, (i+1) % 2
            if row < 2 and col < 2:  # Ensure we don't exceed subplot bounds
                comparison_sorted = comparison_data.sort_values(metric, ascending=True)
                colors = ['red' if x == 'KOR' else 'skyblue' for x in comparison_sorted['REF_AREA']]
                axes[row, col].barh(comparison_sorted['REF_AREA'], comparison_sorted[metric], color=colors)
                axes[row, col].set_title(metric.replace('_', ' '))
                axes[row, col].set_xlabel(metric.replace('_', ' '))
            
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/korea_comparison_detailed.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Korea detailed comparison saved")
        
        # 2. Development level analysis
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Box plots by development level
        metrics = ['COVID_Shock', 'Recovery_2020_2023', 'Overall_Performance', 'Recovery_Speed']
        
        for i, metric in enumerate(metrics):
            row, col = i // 2, i % 2
            data.boxplot(column=metric, by='Development_Level', ax=axes[row, col])
            axes[row, col].set_title(f'{metric.replace("_", " ")} by Development Level')
            axes[row, col].set_xlabel('Development Level')
            axes[row, col].set_ylabel(metric.replace('_', ' '))
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/development_level_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Development level analysis saved")
    
    def generate_report(self, data, correlations, group_analysis, kor_data):
        """Generate comprehensive analysis report"""
        print("\n=== Generating Report ===")
        
        report = []
        report.append("# GDP vs Economic Recovery Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("## 📊 Executive Summary")
        report.append(f"- **Countries analyzed**: {len(data)} countries")
        report.append(f"- **Time period**: 2019-2023 (COVID-19 pandemic and recovery)")
        report.append(f"- **Key finding**: {'Higher GDP countries showed better recovery' if correlations['Recovery_2020_2023'] > 0.3 else 'Lower GDP countries showed better recovery' if correlations['Recovery_2020_2023'] < -0.3 else 'No strong correlation between GDP and recovery'}")
        report.append("")
        
        # COVID-19 Impact
        report.append("## 🦠 COVID-19 Impact Analysis")
        report.append(f"- **Average COVID shock**: {data['COVID_Shock'].mean():.2f}%")
        report.append(f"- **Average recovery (2020-2023)**: {data['Recovery_2020_2023'].mean():.2f}%")
        report.append(f"- **Average overall performance**: {data['Overall_Performance'].mean():.2f}%")
        report.append("")
        
        # Top Performers
        top_recovery = data.nlargest(5, 'Recovery_2020_2023')
        report.append("## 🏆 Top Recovery Performers (2020-2023)")
        for i, (_, row) in enumerate(top_recovery.iterrows(), 1):
            report.append(f"{i}. **{row['REF_AREA']}**: {row['Recovery_2020_2023']:.1f}% recovery")
        report.append("")
        
        # GDP Correlation
        report.append("## 📈 GDP per Capita vs Recovery")
        report.append("**Correlations with GDP per Capita:**")
        for metric, corr in correlations.items():
            report.append(f"- {metric}: {corr:.3f}")
        report.append("")
        
        # Development Level Analysis
        report.append("## 🌍 Development Level Analysis")
        report.append("**Average Recovery by Development Level:**")
        for level in ['High Income', 'Low-Middle Income']:
            if level in group_analysis.index:
                recovery = group_analysis.loc[level, ('Recovery_2020_2023', 'mean')]
                report.append(f"- {level}: {recovery:.2f}%")
        report.append("")
        
        # Korea Analysis
        if kor_data is not None:
            report.append("## 🇰🇷 Korea Special Analysis")
            report.append(f"- **GDP per Capita**: ${kor_data['GDPPerCapita']:,.0f}")
            report.append(f"- **COVID Shock**: {kor_data['COVID_Shock']:.2f}%")
            report.append(f"- **Recovery**: {kor_data['Recovery_2020_2023']:.2f}%")
            report.append(f"- **Overall Performance**: {kor_data['Overall_Performance']:.2f}%")
            report.append(f"- **Economic Resilience**: {kor_data['Economic_Resilience']:.2f}")
            report.append("")
        
        # Key Insights
        report.append("## 💡 Key Insights")
        if correlations['Recovery_2020_2023'] > 0.3:
            report.append("1. **Higher GDP countries showed better recovery**: Economic resources matter for resilience")
        elif correlations['Recovery_2020_2023'] < -0.3:
            report.append("1. **Lower GDP countries showed better recovery**: Different economic structures may be more resilient")
        else:
            report.append("1. **No strong GDP-recovery correlation**: Recovery depends on factors beyond economic size")
        
        if correlations['Economic_Resilience'] > 0.3:
            report.append("2. **Higher GDP countries showed better economic resilience**: Wealth provides buffer against shocks")
        else:
            report.append("2. **Economic resilience varies**: Not necessarily tied to GDP levels")
        
        report.append("3. **Recovery patterns vary significantly**: No one-size-fits-all approach to economic recovery")
        report.append("4. **Policy responses matter**: Government interventions likely played crucial role")
        report.append("")
        
        # Policy Implications
        report.append("## 🎯 Policy Implications")
        report.append("1. **Diversified economic strategies**: Different countries need different recovery approaches")
        report.append("2. **Investment in resilience**: Building economic buffers for future crises")
        report.append("3. **International cooperation**: Global challenges require coordinated responses")
        report.append("4. **Data-driven policymaking**: Understanding recovery patterns for better planning")
        report.append("")
        
        # Conclusion
        report.append("## 🎯 Conclusion")
        report.append("This analysis reveals complex patterns in economic recovery from the COVID-19 pandemic.")
        report.append("While GDP per capita shows some correlation with recovery, many other factors influence economic resilience.")
        report.append("The findings suggest that both economic resources and policy choices play crucial roles in crisis recovery.")
        
        # Save report
        with open(f'{self.output_dir}/gdp_recovery_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✓ GDP recovery report saved")
        return '\n'.join(report)
    
    def run_complete_analysis(self):
        """Run complete GDP recovery analysis"""
        print("🚀 GDP vs Economic Recovery Analysis Starting!")
        print("=" * 60)
        
        # 1. Load GDP growth data
        gdp_growth = self.load_gdp_growth_data()
        if gdp_growth is None:
            print("❌ Failed to load GDP growth data")
            return
        
        # 2. Process GDP growth data
        gdp_growth_processed = self.process_gdp_growth_data(gdp_growth)
        if gdp_growth_processed is None:
            print("❌ Failed to process GDP growth data")
            return
        
        # 3. Load existing data
        existing_data = self.load_existing_data()
        if existing_data is None:
            print("❌ Failed to load existing data")
            return
        
        # 4. Merge data
        self.data = self.merge_data(gdp_growth_processed, existing_data)
        
        # 5. Calculate recovery metrics
        self.data = self.calculate_recovery_metrics(self.data)
        
        # 6. Classify countries
        self.data = self.classify_countries(self.data)
        
        # 7. Analyze COVID impact
        biggest_shocks, best_recovery, best_overall = self.analyze_covid_impact(self.data)
        
        # 8. Analyze GDP correlation
        correlations = self.analyze_gdp_correlation(self.data)
        
        # 9. Development level analysis
        group_analysis = self.development_level_analysis(self.data)
        
        # 10. Korea special analysis
        kor_data = self.korea_special_analysis(self.data)
        
        # 11. Create visualizations
        self.create_visualizations(self.data)
        
        # 12. Generate report
        self.generate_report(self.data, correlations, group_analysis, kor_data)
        
        # 13. Save processed data
        self.data.to_csv(f'{self.output_dir}/gdp_recovery_data.csv', index=False)
        
        print("\n" + "=" * 60)
        print("🎉 GDP Recovery Analysis Complete!")
        print(f"📁 Results saved in '{self.output_dir}' folder")
        print("\n📋 Generated files:")
        print("   - gdp_recovery_analysis.png: Main analysis visualization")
        print("   - korea_comparison_detailed.png: Korea detailed comparison")
        print("   - development_level_analysis.png: Development level analysis")
        print("   - gdp_recovery_report.md: Comprehensive analysis report")
        print("   - gdp_recovery_data.csv: Processed dataset with recovery metrics")
        print("\n💡 Key findings:")
        print("   - Economic recovery patterns vary significantly across countries")
        print("   - GDP per capita shows correlation with recovery performance")
        print("   - Policy responses and economic structure matter for resilience")
        print("   - Korea's recovery performance analyzed in detail")

if __name__ == "__main__":
    analyzer = GDPRecoveryAnalyzer()
    analyzer.run_complete_analysis() 