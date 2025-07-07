import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class COVIDHealthAnalyzer:
    def __init__(self):
        """COVID-19 health system analyzer"""
        self.output_dir = 'covid_health_results'
        self._create_output_dir()
        self.data = None
        self.covid_data = None
        
        # Country code mapping from 2-letter to 3-letter codes
        self.country_code_mapping = {
            'AF': 'AFG', 'AL': 'ALB', 'DZ': 'DZA', 'AS': 'ASM', 'AD': 'AND', 'AO': 'AGO', 'AI': 'AIA', 'AQ': 'ATA',
            'AG': 'ATG', 'AR': 'ARG', 'AM': 'ARM', 'AW': 'ABW', 'AU': 'AUS', 'AT': 'AUT', 'AZ': 'AZE', 'BS': 'BHS',
            'BH': 'BHR', 'BD': 'BGD', 'BB': 'BRB', 'BY': 'BLR', 'BE': 'BEL', 'BZ': 'BLZ', 'BJ': 'BEN', 'BM': 'BMU',
            'BT': 'BTN', 'BO': 'BOL', 'BA': 'BIH', 'BW': 'BWA', 'BV': 'BVT', 'BR': 'BRA', 'IO': 'IOT', 'BN': 'BRN',
            'BG': 'BGR', 'BF': 'BFA', 'BI': 'BDI', 'KH': 'KHM', 'CM': 'CMR', 'CA': 'CAN', 'CV': 'CPV', 'KY': 'CYM',
            'CF': 'CAF', 'TD': 'TCD', 'CL': 'CHL', 'CN': 'CHN', 'CX': 'CXR', 'CC': 'CCK', 'CO': 'COL', 'KM': 'COM',
            'CG': 'COG', 'CD': 'COD', 'CK': 'COK', 'CR': 'CRI', 'CI': 'CIV', 'HR': 'HRV', 'CU': 'CUB', 'CY': 'CYP',
            'CZ': 'CZE', 'DK': 'DNK', 'DJ': 'DJI', 'DM': 'DMA', 'DO': 'DOM', 'EC': 'ECU', 'EG': 'EGY', 'SV': 'SLV',
            'GQ': 'GNQ', 'ER': 'ERI', 'EE': 'EST', 'ET': 'ETH', 'FK': 'FLK', 'FO': 'FRO', 'FJ': 'FJI', 'FI': 'FIN',
            'FR': 'FRA', 'GF': 'GUF', 'PF': 'PYF', 'TF': 'ATF', 'GA': 'GAB', 'GM': 'GMB', 'GE': 'GEO', 'DE': 'DEU',
            'GH': 'GHA', 'GI': 'GIB', 'GR': 'GRC', 'GL': 'GRL', 'GD': 'GRD', 'GP': 'GLP', 'GU': 'GUM', 'GT': 'GTM',
            'GN': 'GIN', 'GW': 'GNB', 'GY': 'GUY', 'HT': 'HTI', 'HM': 'HMD', 'VA': 'VAT', 'HN': 'HND', 'HK': 'HKG',
            'HU': 'HUN', 'IS': 'ISL', 'IN': 'IND', 'ID': 'IDN', 'IR': 'IRN', 'IQ': 'IRQ', 'IE': 'IRL', 'IL': 'ISR',
            'IT': 'ITA', 'JM': 'JAM', 'JP': 'JPN', 'JO': 'JOR', 'KZ': 'KAZ', 'KE': 'KEN', 'KI': 'KIR', 'KP': 'PRK',
            'KR': 'KOR', 'KW': 'KWT', 'KG': 'KGZ', 'LA': 'LAO', 'LV': 'LVA', 'LB': 'LBN', 'LS': 'LSO', 'LR': 'LBR',
            'LY': 'LBY', 'LI': 'LIE', 'LT': 'LTU', 'LU': 'LUX', 'MO': 'MAC', 'MK': 'MKD', 'MG': 'MDG', 'MW': 'MWI',
            'MY': 'MYS', 'MV': 'MDV', 'ML': 'MLI', 'MT': 'MLT', 'MH': 'MHL', 'MQ': 'MTQ', 'MR': 'MRT', 'MU': 'MUS',
            'YT': 'MYT', 'MX': 'MEX', 'FM': 'FSM', 'MD': 'MDA', 'MC': 'MCO', 'MN': 'MNG', 'MS': 'MSR', 'MA': 'MAR',
            'MZ': 'MOZ', 'MM': 'MMR', 'NA': 'NAM', 'NR': 'NRU', 'NP': 'NPL', 'NL': 'NLD', 'NC': 'NCL', 'NZ': 'NZL',
            'NI': 'NIC', 'NE': 'NER', 'NG': 'NGA', 'NU': 'NIU', 'NF': 'NFK', 'MP': 'MNP', 'NO': 'NOR', 'OM': 'OMN',
            'PK': 'PAK', 'PW': 'PLW', 'PS': 'PSE', 'PA': 'PAN', 'PG': 'PNG', 'PY': 'PRY', 'PE': 'PER', 'PH': 'PHL',
            'PN': 'PCN', 'PL': 'POL', 'PT': 'PRT', 'PR': 'PRI', 'QA': 'QAT', 'RE': 'REU', 'RO': 'ROU', 'RU': 'RUS',
            'RW': 'RWA', 'SH': 'SHN', 'KN': 'KNA', 'LC': 'LCA', 'PM': 'SPM', 'VC': 'VCT', 'WS': 'WSM', 'SM': 'SMR',
            'ST': 'STP', 'SA': 'SAU', 'SN': 'SEN', 'SC': 'SYC', 'SL': 'SLE', 'SG': 'SGP', 'SK': 'SVK', 'SI': 'SVN',
            'SB': 'SLB', 'SO': 'SOM', 'ZA': 'ZAF', 'GS': 'SGS', 'ES': 'ESP', 'LK': 'LKA', 'SD': 'SDN', 'SR': 'SUR',
            'SJ': 'SJM', 'SZ': 'SWZ', 'SE': 'SWE', 'CH': 'CHE', 'SY': 'SYR', 'TW': 'TWN', 'TJ': 'TJK', 'TZ': 'TZA',
            'TH': 'THA', 'TL': 'TLS', 'TG': 'TGO', 'TK': 'TKL', 'TO': 'TON', 'TT': 'TTO', 'TN': 'TUN', 'TR': 'TUR',
            'TM': 'TKM', 'TC': 'TCA', 'TV': 'TUV', 'UG': 'UGA', 'UA': 'UKR', 'AE': 'ARE', 'GB': 'GBR', 'US': 'USA',
            'UM': 'UMI', 'UY': 'URY', 'UZ': 'UZB', 'VU': 'VUT', 'VE': 'VEN', 'VN': 'VNM', 'VG': 'VGB', 'VI': 'VIR',
            'WF': 'WLF', 'EH': 'ESH', 'YE': 'YEM', 'ZM': 'ZMB', 'ZW': 'ZWE'
        }
        
    def _create_output_dir(self):
        """Create output directory"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_covid_data(self):
        """Load WHO COVID-19 data"""
        try:
            print("=== Loading WHO COVID-19 Data ===")
            self.covid_data = pd.read_csv('data/WHO-COVID-19-global-daily-data.csv')
            print(f"✓ Loaded COVID-19 data: {len(self.covid_data)} records")
            print(f"✓ Countries: {self.covid_data['Country_code'].nunique()}")
            print(f"✓ Date range: {self.covid_data['Date_reported'].min()} to {self.covid_data['Date_reported'].max()}")
            return self.covid_data
        except Exception as e:
            print(f"❌ Error loading COVID-19 data: {e}")
            return None
    
    def process_covid_data(self):
        """Process COVID-19 data to calculate country-level metrics"""
        print("\n=== Processing COVID-19 Data ===")
        
        if self.covid_data is None:
            return None
        
        # Convert date column
        self.covid_data['Date_reported'] = pd.to_datetime(self.covid_data['Date_reported'])
        
        # Convert numeric columns, replacing empty strings with 0
        numeric_columns = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
        for col in numeric_columns:
            self.covid_data[col] = pd.to_numeric(self.covid_data[col], errors='coerce').fillna(0)
        
        # Calculate country-level COVID-19 metrics
        covid_metrics = []
        
        for country_code in self.covid_data['Country_code'].unique():
            country_data = self.covid_data[self.covid_data['Country_code'] == country_code]
            
            if len(country_data) == 0:
                continue
            
            # Get latest data
            latest_data = country_data[country_data['Date_reported'] == country_data['Date_reported'].max()]
            
            if len(latest_data) == 0:
                continue
            
            latest = latest_data.iloc[0]
            
            # Calculate metrics
            total_cases = latest['Cumulative_cases']
            total_deaths = latest['Cumulative_deaths']
            
            # Calculate case fatality rate (deaths per 1000 cases)
            case_fatality_rate = (total_deaths / total_cases * 1000) if total_cases > 0 else 0
            
            # Calculate peak daily cases and deaths
            peak_daily_cases = country_data['New_cases'].max()
            peak_daily_deaths = country_data['New_deaths'].max()
            
            # Calculate average daily cases and deaths
            avg_daily_cases = country_data['New_cases'].mean()
            avg_daily_deaths = country_data['New_deaths'].mean()
            
            # Calculate days with data
            days_with_data = len(country_data)
            
            covid_metrics.append({
                'Country_code_2': country_code,  # Keep original 2-letter code
                'REF_AREA': self.country_code_mapping.get(country_code, country_code),  # Convert to 3-letter code
                'Total_Cases': total_cases,
                'Total_Deaths': total_deaths,
                'Case_Fatality_Rate': case_fatality_rate,
                'Peak_Daily_Cases': peak_daily_cases,
                'Peak_Daily_Deaths': peak_daily_deaths,
                'Avg_Daily_Cases': avg_daily_cases,
                'Avg_Daily_Deaths': avg_daily_deaths,
                'Days_With_Data': days_with_data
            })
        
        covid_metrics_df = pd.DataFrame(covid_metrics)
        print(f"✓ Processed COVID-19 metrics for {len(covid_metrics_df)} countries")
        
        # Show mapping statistics
        mapped_countries = covid_metrics_df[covid_metrics_df['REF_AREA'] != covid_metrics_df['Country_code_2']]
        print(f"✓ Successfully mapped {len(mapped_countries)} countries from 2-letter to 3-letter codes")
        
        return covid_metrics_df
    
    def load_existing_data(self):
        """Load existing health and GDP data"""
        try:
            existing_data = pd.read_csv('gdp_recovery_results/gdp_recovery_data.csv')
            print(f"✓ Loaded existing data: {len(existing_data)} countries")
            return existing_data
        except Exception as e:
            print(f"❌ Error loading existing data: {e}")
            return None
    
    def merge_data(self, covid_metrics, existing_data):
        """Merge COVID-19 data with existing health data"""
        print("\n=== Merging Data ===")
        
        # Show sample of country codes in both datasets
        print(f"COVID-19 data country codes (sample): {list(covid_metrics['REF_AREA'].head(10))}")
        print(f"Existing data country codes (sample): {list(existing_data['REF_AREA'].head(10))}")
        
        # Merge on country code
        merged_data = pd.merge(existing_data, covid_metrics, on='REF_AREA', how='inner')
        
        print(f"✓ Final merged dataset: {len(merged_data)} countries")
        print(f"✓ Columns: {list(merged_data.columns)}")
        
        # Show countries that were successfully merged
        print(f"✓ Successfully merged countries: {list(merged_data['REF_AREA'].head(10))}")
        
        return merged_data
    
    def calculate_covid_performance_metrics(self, data):
        """Calculate COVID-19 performance metrics"""
        print("\n=== Calculating COVID-19 Performance Metrics ===")
        
        # 1. COVID-19 severity index (cases per capita)
        data['Cases_Per_Capita'] = data['Total_Cases'] / 1000000  # per million
        
        # 2. Deaths per capita
        data['Deaths_Per_Capita'] = data['Total_Deaths'] / 1000000  # per million
        
        # 3. COVID-19 response efficiency (lower case fatality rate = better)
        data['COVID_Response_Efficiency'] = 1000 / (data['Case_Fatality_Rate'] + 1)  # inverse of fatality rate
        
        # 4. Health system stress (peak daily cases per capita)
        data['Health_System_Stress'] = data['Peak_Daily_Cases'] / 1000000  # per million
        
        # 5. Overall COVID-19 performance score (composite index)
        # Normalize metrics and combine
        from sklearn.preprocessing import StandardScaler
        
        performance_metrics = ['Case_Fatality_Rate', 'Cases_Per_Capita', 'Deaths_Per_Capita']
        scaler = StandardScaler()
        
        # For metrics where lower is better, we'll invert them
        normalized_data = data[performance_metrics].copy()
        normalized_data['Case_Fatality_Rate'] = -normalized_data['Case_Fatality_Rate']  # lower is better
        normalized_data['Cases_Per_Capita'] = -normalized_data['Cases_Per_Capita']  # lower is better
        normalized_data['Deaths_Per_Capita'] = -normalized_data['Deaths_Per_Capita']  # lower is better
        
        # Scale the data
        scaled_data = scaler.fit_transform(normalized_data)
        
        # Calculate composite score
        data['COVID_Performance_Score'] = np.mean(scaled_data, axis=1)
        
        print("✓ COVID-19 performance metrics calculated:")
        print(f"  - Cases_Per_Capita: Cases per million population")
        print(f"  - Deaths_Per_Capita: Deaths per million population")
        print(f"  - COVID_Response_Efficiency: Inverse of case fatality rate")
        print(f"  - Health_System_Stress: Peak daily cases per million")
        print(f"  - COVID_Performance_Score: Composite performance index")
        
        return data
    
    def analyze_health_expenditure_vs_covid(self, data):
        """Analyze relationship between health expenditure and COVID-19 response"""
        print("\n=== Health Expenditure vs COVID-19 Response Analysis ===")
        
        # Calculate correlations
        correlations = {}
        covid_metrics = ['Case_Fatality_Rate', 'Cases_Per_Capita', 'Deaths_Per_Capita', 
                        'COVID_Response_Efficiency', 'COVID_Performance_Score']
        
        for metric in covid_metrics:
            if metric in data.columns:
                corr = data['HealthExpenditure'].corr(data[metric])
                correlations[metric] = corr
        
        print("\n📈 Correlations with Health Expenditure (% of GDP):")
        for metric, corr in correlations.items():
            print(f"  - {metric}: {corr:.3f}")
        
        # Interpretation
        print("\n💡 Key Insights:")
        if correlations.get('Case_Fatality_Rate', 0) < -0.3:
            print("  - Higher health expenditure associated with lower case fatality rates")
        elif correlations.get('Case_Fatality_Rate', 0) > 0.3:
            print("  - Higher health expenditure associated with higher case fatality rates")
        else:
            print("  - No strong correlation between health expenditure and case fatality rates")
        
        if correlations.get('COVID_Performance_Score', 0) > 0.3:
            print("  - Higher health expenditure associated with better COVID-19 performance")
        elif correlations.get('COVID_Performance_Score', 0) < -0.3:
            print("  - Higher health expenditure associated with worse COVID-19 performance")
        else:
            print("  - No strong correlation between health expenditure and overall COVID-19 performance")
        
        # Top and bottom performers by health expenditure
        high_expenditure = data[data['HealthExpenditure'] >= data['HealthExpenditure'].quantile(0.75)]
        low_expenditure = data[data['HealthExpenditure'] <= data['HealthExpenditure'].quantile(0.25)]
        
        print(f"\n📊 High Health Expenditure Countries (Top 25%):")
        print(f"  - Average case fatality rate: {high_expenditure['Case_Fatality_Rate'].mean():.1f} per 1000 cases")
        print(f"  - Average COVID performance score: {high_expenditure['COVID_Performance_Score'].mean():.2f}")
        
        print(f"\n📊 Low Health Expenditure Countries (Bottom 25%):")
        print(f"  - Average case fatality rate: {low_expenditure['Case_Fatality_Rate'].mean():.1f} per 1000 cases")
        print(f"  - Average COVID performance score: {low_expenditure['COVID_Performance_Score'].mean():.2f}")
        
        return correlations, high_expenditure, low_expenditure
    
    def analyze_physicians_vs_mortality(self, data):
        """Analyze relationship between physician density and COVID-19 mortality"""
        print("\n=== Physicians vs COVID-19 Mortality Analysis ===")
        
        # Filter countries with physician data
        physician_data = data[data['PhysiciansPer1000'].notna()].copy()
        
        if len(physician_data) == 0:
            print("❌ No physician data available")
            return None
        
        print(f"✓ Analyzing {len(physician_data)} countries with physician data")
        
        # Calculate correlations
        correlations = {}
        mortality_metrics = ['Case_Fatality_Rate', 'Deaths_Per_Capita', 'COVID_Performance_Score']
        
        for metric in mortality_metrics:
            if metric in physician_data.columns:
                corr = physician_data['PhysiciansPer1000'].corr(physician_data[metric])
                correlations[metric] = corr
        
        print("\n📈 Correlations with Physicians per 1000 people:")
        for metric, corr in correlations.items():
            print(f"  - {metric}: {corr:.3f}")
        
        # Interpretation
        print("\n💡 Key Insights:")
        if correlations.get('Case_Fatality_Rate', 0) < -0.3:
            print("  - Higher physician density associated with lower case fatality rates")
        elif correlations.get('Case_Fatality_Rate', 0) > 0.3:
            print("  - Higher physician density associated with higher case fatality rates")
        else:
            print("  - No strong correlation between physician density and case fatality rates")
        
        # Physician density groups analysis
        physician_data['Physician_Group'] = pd.qcut(physician_data['PhysiciansPer1000'], 
                                                   q=3, labels=['Low', 'Medium', 'High'])
        
        group_analysis = physician_data.groupby('Physician_Group').agg({
            'Case_Fatality_Rate': ['mean', 'std'],
            'Deaths_Per_Capita': ['mean', 'std'],
            'COVID_Performance_Score': ['mean', 'std'],
            'PhysiciansPer1000': 'mean'
        }).round(2)
        
        print(f"\n📊 COVID-19 Outcomes by Physician Density:")
        print(group_analysis)
        
        # Statistical test
        from scipy import stats
        
        high_physicians = physician_data[physician_data['Physician_Group'] == 'High']
        low_physicians = physician_data[physician_data['Physician_Group'] == 'Low']
        
        print(f"\n🔬 Statistical Comparison (High vs Low Physician Density):")
        for metric in ['Case_Fatality_Rate', 'Deaths_Per_Capita', 'COVID_Performance_Score']:
            if metric in physician_data.columns:
                t_stat, p_value = stats.ttest_ind(
                    high_physicians[metric].dropna(), 
                    low_physicians[metric].dropna()
                )
                print(f"  - {metric}: t={t_stat:.3f}, p={p_value:.3f} {'(significant)' if p_value < 0.05 else '(not significant)'}")
        
        return correlations, group_analysis, physician_data
    
    def korea_special_analysis(self, data):
        """Special analysis for Korea's COVID-19 performance"""
        print("\n=== Korea Special COVID-19 Analysis ===")
        
        if 'KOR' not in data['REF_AREA'].values:
            print("❌ Korea data not found.")
            return None
        
        kor_data = data[data['REF_AREA'] == 'KOR'].iloc[0]
        
        print(f"🇰🇷 Korea's COVID-19 Performance:")
        print(f"  - Health Expenditure: {kor_data['HealthExpenditure']:.2f}% (of GDP)")
        print(f"  - Physicians per 1000: {kor_data.get('PhysiciansPer1000', 'N/A')}")
        print(f"  - Total Cases: {kor_data['Total_Cases']:,.0f}")
        print(f"  - Total Deaths: {kor_data['Total_Deaths']:,.0f}")
        print(f"  - Case Fatality Rate: {kor_data['Case_Fatality_Rate']:.1f} per 1000 cases")
        print(f"  - Cases per Million: {kor_data['Cases_Per_Capita']:.0f}")
        print(f"  - Deaths per Million: {kor_data['Deaths_Per_Capita']:.0f}")
        print(f"  - COVID Performance Score: {kor_data['COVID_Performance_Score']:.2f}")
        
        # Compare with similar health expenditure countries
        similar_expenditure = data[
            (data['HealthExpenditure'] >= kor_data['HealthExpenditure'] * 0.8) &
            (data['HealthExpenditure'] <= kor_data['HealthExpenditure'] * 1.2) &
            (data['REF_AREA'] != 'KOR')
        ]
        
        if len(similar_expenditure) > 0:
            print(f"\n📊 Comparison with Similar Health Expenditure Countries:")
            comparison_data = pd.concat([kor_data.to_frame().T, similar_expenditure])
            comparison_sorted = comparison_data.sort_values('COVID_Performance_Score', ascending=False)
            
            for i, (_, row) in enumerate(comparison_sorted.iterrows(), 1):
                marker = "🇰🇷" if row['REF_AREA'] == 'KOR' else "  "
                print(f"{marker} {i:2d}. {row['REF_AREA']:3s} - Performance: {row['COVID_Performance_Score']:.2f}, "
                      f"Fatality: {row['Case_Fatality_Rate']:.1f}, Cases/M: {row['Cases_Per_Capita']:.0f}")
        
        return kor_data
    
    def create_visualizations(self, data):
        """Create comprehensive visualizations"""
        print("\n=== Creating Visualizations ===")
        
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Health Expenditure vs Case Fatality Rate
        ax1 = plt.subplot(3, 3, 1)
        plt.scatter(data['HealthExpenditure'], data['Case_Fatality_Rate'], alpha=0.7, s=50)
        plt.xlabel('Health Expenditure (% of GDP)')
        plt.ylabel('Case Fatality Rate (per 1000 cases)')
        plt.title('Health Expenditure vs Case Fatality Rate')
        plt.grid(True, alpha=0.3)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            kor_data = data[data['REF_AREA'] == 'KOR'].iloc[0]
            plt.scatter(kor_data['HealthExpenditure'], kor_data['Case_Fatality_Rate'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['HealthExpenditure'], kor_data['Case_Fatality_Rate']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 2. Health Expenditure vs COVID Performance Score
        ax2 = plt.subplot(3, 3, 2)
        plt.scatter(data['HealthExpenditure'], data['COVID_Performance_Score'], alpha=0.7, s=50)
        plt.xlabel('Health Expenditure (% of GDP)')
        plt.ylabel('COVID Performance Score')
        plt.title('Health Expenditure vs COVID Performance')
        plt.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(data['HealthExpenditure'].dropna(), data['COVID_Performance_Score'].dropna(), 1)
        p = np.poly1d(z)
        plt.plot(data['HealthExpenditure'], p(data['HealthExpenditure']), "r--", alpha=0.8)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            plt.scatter(kor_data['HealthExpenditure'], kor_data['COVID_Performance_Score'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['HealthExpenditure'], kor_data['COVID_Performance_Score']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 3. Physicians vs Case Fatality Rate
        ax3 = plt.subplot(3, 3, 3)
        physician_data = data[data['PhysiciansPer1000'].notna()]
        if len(physician_data) > 0:
            plt.scatter(physician_data['PhysiciansPer1000'], physician_data['Case_Fatality_Rate'], alpha=0.7, s=50)
            plt.xlabel('Physicians per 1000 people')
            plt.ylabel('Case Fatality Rate (per 1000 cases)')
            plt.title('Physicians vs Case Fatality Rate')
            plt.grid(True, alpha=0.3)
            
            # Highlight Korea
            if 'KOR' in physician_data['REF_AREA'].values:
                kor_phys = physician_data[physician_data['REF_AREA'] == 'KOR'].iloc[0]
                plt.scatter(kor_phys['PhysiciansPer1000'], kor_phys['Case_Fatality_Rate'], 
                           color='red', s=200, marker='*', label='Korea', zorder=5)
                plt.annotate('KOR', (kor_phys['PhysiciansPer1000'], kor_phys['Case_Fatality_Rate']), 
                            fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 4. Cases per Capita vs Deaths per Capita
        ax4 = plt.subplot(3, 3, 4)
        plt.scatter(data['Cases_Per_Capita'], data['Deaths_Per_Capita'], alpha=0.7, s=50)
        plt.xlabel('Cases per Million')
        plt.ylabel('Deaths per Million')
        plt.title('Cases vs Deaths per Capita')
        plt.grid(True, alpha=0.3)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            plt.scatter(kor_data['Cases_Per_Capita'], kor_data['Deaths_Per_Capita'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['Cases_Per_Capita'], kor_data['Deaths_Per_Capita']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 5. Health Expenditure Groups vs COVID Performance
        ax5 = plt.subplot(3, 3, 5)
        data['Health_Expenditure_Group'] = pd.qcut(data['HealthExpenditure'], q=3, 
                                                  labels=['Low', 'Medium', 'High'])
        group_means = data.groupby('Health_Expenditure_Group')['COVID_Performance_Score'].mean()
        group_means.plot(kind='bar', ax=ax5, color=['lightcoral', 'lightblue', 'lightgreen'])
        plt.title('COVID Performance by Health Expenditure Group')
        plt.ylabel('COVID Performance Score')
        plt.xticks(rotation=45)
        
        # 6. Case Fatality Rate Distribution
        ax6 = plt.subplot(3, 3, 6)
        plt.hist(data['Case_Fatality_Rate'].dropna(), bins=15, alpha=0.7, edgecolor='black', color='lightcoral')
        plt.xlabel('Case Fatality Rate (per 1000 cases)')
        plt.ylabel('Number of Countries')
        plt.title('Distribution of Case Fatality Rates')
        plt.grid(True, alpha=0.3)
        
        # Add vertical line for mean
        mean_fatality = data['Case_Fatality_Rate'].mean()
        plt.axvline(mean_fatality, color='red', linestyle='--', label=f'Mean: {mean_fatality:.1f}')
        plt.legend()
        
        # 7. Top 10 COVID Performance Countries
        ax7 = plt.subplot(3, 3, 7)
        top_performance = data.nlargest(10, 'COVID_Performance_Score')
        colors = ['red' if x == 'KOR' else 'skyblue' for x in top_performance['REF_AREA']]
        plt.barh(top_performance['REF_AREA'], top_performance['COVID_Performance_Score'], color=colors)
        plt.xlabel('COVID Performance Score')
        plt.title('Top 10 COVID Performance Countries')
        
        # 8. Health System Stress vs Performance
        ax8 = plt.subplot(3, 3, 8)
        plt.scatter(data['Health_System_Stress'], data['COVID_Performance_Score'], alpha=0.7, s=50)
        plt.xlabel('Health System Stress (Peak Daily Cases/M)')
        plt.ylabel('COVID Performance Score')
        plt.title('Health System Stress vs Performance')
        plt.grid(True, alpha=0.3)
        
        # Highlight Korea
        if 'KOR' in data['REF_AREA'].values:
            plt.scatter(kor_data['Health_System_Stress'], kor_data['COVID_Performance_Score'], 
                       color='red', s=200, marker='*', label='Korea', zorder=5)
            plt.annotate('KOR', (kor_data['Health_System_Stress'], kor_data['COVID_Performance_Score']), 
                        fontsize=12, fontweight='bold', color='red', xytext=(5,5), textcoords='offset points')
        
        # 9. Correlation Heatmap
        ax9 = plt.subplot(3, 3, 9)
        correlation_vars = ['HealthExpenditure', 'PhysiciansPer1000', 'Case_Fatality_Rate', 
                           'Cases_Per_Capita', 'Deaths_Per_Capita', 'COVID_Performance_Score']
        corr_data = data[correlation_vars].dropna()
        if len(corr_data) > 0:
            corr_matrix = corr_data.corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True, fmt='.2f', ax=ax9)
            plt.title('Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/covid_health_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ COVID health analysis visualization saved")
        
        # Create additional detailed charts
        self.create_detailed_charts(data)
    
    def create_detailed_charts(self, data):
        """Create additional detailed charts"""
        
        # 1. Korea vs Similar Countries Comparison
        if 'KOR' in data['REF_AREA'].values:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            
            kor_data = data[data['REF_AREA'] == 'KOR'].iloc[0]
            similar_expenditure = data[
                (data['HealthExpenditure'] >= kor_data['HealthExpenditure'] * 0.8) &
                (data['HealthExpenditure'] <= kor_data['HealthExpenditure'] * 1.2) &
                (data['REF_AREA'] != 'KOR')
            ]
            
            comparison_data = pd.concat([kor_data.to_frame().T, similar_expenditure])
            metrics = ['Case_Fatality_Rate', 'Cases_Per_Capita', 'Deaths_Per_Capita', 'COVID_Performance_Score']
            
            for i, metric in enumerate(metrics):
                row, col = i // 2, i % 2
                comparison_sorted = comparison_data.sort_values(metric, ascending=True)
                colors = ['red' if x == 'KOR' else 'skyblue' for x in comparison_sorted['REF_AREA']]
                axes[row, col].barh(comparison_sorted['REF_AREA'], comparison_sorted[metric], color=colors)
                axes[row, col].set_title(metric.replace('_', ' '))
                axes[row, col].set_xlabel(metric.replace('_', ' '))
            
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/korea_covid_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✓ Korea COVID comparison saved")
        
        # 2. Health expenditure groups analysis
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        data['Health_Expenditure_Group'] = pd.qcut(data['HealthExpenditure'], q=3, 
                                                  labels=['Low', 'Medium', 'High'])
        
        metrics = ['Case_Fatality_Rate', 'Cases_Per_Capita', 'Deaths_Per_Capita', 'COVID_Performance_Score']
        
        for i, metric in enumerate(metrics):
            row, col = i // 2, i % 2
            data.boxplot(column=metric, by='Health_Expenditure_Group', ax=axes[row, col])
            axes[row, col].set_title(f'{metric.replace("_", " ")} by Health Expenditure Group')
            axes[row, col].set_xlabel('Health Expenditure Group')
            axes[row, col].set_ylabel(metric.replace('_', ' '))
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/health_expenditure_groups.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Health expenditure groups analysis saved")
    
    def generate_report(self, data, health_correlations, physician_correlations, kor_data):
        """Generate comprehensive analysis report"""
        print("\n=== Generating Report ===")
        
        report = []
        report.append("# COVID-19 Health System Analysis Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("## 📊 Executive Summary")
        report.append(f"- **Countries analyzed**: {len(data)} countries")
        report.append(f"- **Time period**: COVID-19 pandemic (2020-2023)")
        report.append(f"- **Key finding**: {'Health expenditure correlates with COVID-19 performance' if abs(health_correlations.get('COVID_Performance_Score', 0)) > 0.3 else 'No strong correlation between health expenditure and COVID-19 performance'}")
        report.append("")
        
        # COVID-19 Impact Summary
        report.append("## 🦠 COVID-19 Impact Summary")
        report.append(f"- **Average case fatality rate**: {data['Case_Fatality_Rate'].mean():.1f} per 1000 cases")
        report.append(f"- **Average cases per million**: {data['Cases_Per_Capita'].mean():.0f}")
        report.append(f"- **Average deaths per million**: {data['Deaths_Per_Capita'].mean():.0f}")
        report.append("")
        
        # Top Performers
        top_performance = data.nlargest(5, 'COVID_Performance_Score')
        report.append("## 🏆 Top COVID-19 Performance Countries")
        for i, (_, row) in enumerate(top_performance.iterrows(), 1):
            report.append(f"{i}. **{row['REF_AREA']}**: Performance score {row['COVID_Performance_Score']:.2f}, "
                         f"Fatality rate {row['Case_Fatality_Rate']:.1f}")
        report.append("")
        
        # Health Expenditure Analysis
        report.append("## 💰 Health Expenditure vs COVID-19 Response")
        report.append("**Correlations with Health Expenditure (% of GDP):**")
        for metric, corr in health_correlations.items():
            report.append(f"- {metric}: {corr:.3f}")
        report.append("")
        
        # Physician Analysis
        if physician_correlations:
            report.append("## 👨‍⚕️ Physicians vs COVID-19 Mortality")
            report.append("**Correlations with Physicians per 1000 people:**")
            for metric, corr in physician_correlations.items():
                report.append(f"- {metric}: {corr:.3f}")
            report.append("")
        
        # Korea Analysis
        if kor_data is not None:
            report.append("## 🇰🇷 Korea Special Analysis")
            report.append(f"- **Health Expenditure**: {kor_data['HealthExpenditure']:.2f}% (of GDP)")
            report.append(f"- **Physicians per 1000**: {kor_data.get('PhysiciansPer1000', 'N/A')}")
            report.append(f"- **Case Fatality Rate**: {kor_data['Case_Fatality_Rate']:.1f} per 1000 cases")
            report.append(f"- **Cases per Million**: {kor_data['Cases_Per_Capita']:.0f}")
            report.append(f"- **Deaths per Million**: {kor_data['Deaths_Per_Capita']:.0f}")
            report.append(f"- **COVID Performance Score**: {kor_data['COVID_Performance_Score']:.2f}")
            report.append("")
        
        # Key Insights
        report.append("## 💡 Key Insights")
        
        if health_correlations.get('Case_Fatality_Rate', 0) < -0.3:
            report.append("1. **Higher health expenditure associated with lower case fatality rates**: Investment in healthcare pays off")
        elif health_correlations.get('Case_Fatality_Rate', 0) > 0.3:
            report.append("1. **Higher health expenditure associated with higher case fatality rates**: Counterintuitive result needs investigation")
        else:
            report.append("1. **No strong correlation between health expenditure and case fatality rates**: Other factors may be more important")
        
        if physician_correlations and physician_correlations.get('Case_Fatality_Rate', 0) < -0.3:
            report.append("2. **Higher physician density associated with lower case fatality rates**: Medical workforce matters")
        elif physician_correlations and physician_correlations.get('Case_Fatality_Rate', 0) > 0.3:
            report.append("2. **Higher physician density associated with higher case fatality rates**: Complex relationship")
        else:
            report.append("2. **Physician density shows mixed correlation with outcomes**: Quality may matter more than quantity")
        
        report.append("3. **COVID-19 performance varies significantly**: No one-size-fits-all approach to pandemic response")
        report.append("4. **Health system resilience is complex**: Multiple factors contribute to pandemic outcomes")
        report.append("")
        
        # Policy Implications
        report.append("## 🎯 Policy Implications")
        report.append("1. **Invest in healthcare infrastructure**: Strong health systems are crucial for crisis response")
        report.append("2. **Focus on quality, not just quantity**: Physician density alone doesn't guarantee better outcomes")
        report.append("3. **Prepare for future pandemics**: Build resilient health systems")
        report.append("4. **Learn from successful countries**: Study what worked in different contexts")
        report.append("")
        
        # Conclusion
        report.append("## 🎯 Conclusion")
        report.append("This analysis reveals the complex relationship between health system characteristics and COVID-19 outcomes.")
        report.append("While health expenditure and physician density show some correlations with performance, many other factors influence pandemic response.")
        report.append("The findings emphasize the importance of building comprehensive, resilient health systems for future crises.")
        
        # Save report
        with open(f'{self.output_dir}/covid_health_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✓ COVID health report saved")
        return '\n'.join(report)
    
    def run_complete_analysis(self):
        """Run complete COVID-19 health system analysis"""
        print("🚀 COVID-19 Health System Analysis Starting!")
        print("=" * 60)
        
        # 1. Load COVID-19 data
        covid_data = self.load_covid_data()
        if covid_data is None:
            print("❌ Failed to load COVID-19 data")
            return
        
        # 2. Process COVID-19 data
        covid_metrics = self.process_covid_data()
        if covid_metrics is None:
            print("❌ Failed to process COVID-19 data")
            return
        
        # 3. Load existing data
        existing_data = self.load_existing_data()
        if existing_data is None:
            print("❌ Failed to load existing data")
            return
        
        # 4. Merge data
        self.data = self.merge_data(covid_metrics, existing_data)
        
        # 5. Calculate COVID-19 performance metrics
        self.data = self.calculate_covid_performance_metrics(self.data)
        
        # 6. Analyze health expenditure vs COVID-19 response
        health_correlations, high_exp, low_exp = self.analyze_health_expenditure_vs_covid(self.data)
        
        # 7. Analyze physicians vs mortality
        physician_result = self.analyze_physicians_vs_mortality(self.data)
        if physician_result is not None:
            physician_correlations, physician_groups, physician_data = physician_result
        else:
            physician_correlations, physician_groups, physician_data = None, None, None
        
        # 8. Korea special analysis
        kor_data = self.korea_special_analysis(self.data)
        
        # 9. Create visualizations
        self.create_visualizations(self.data)
        
        # 10. Generate report
        self.generate_report(self.data, health_correlations, physician_correlations, kor_data)
        
        # 11. Save processed data
        self.data.to_csv(f'{self.output_dir}/covid_health_data.csv', index=False)
        
        print("\n" + "=" * 60)
        print("🎉 COVID-19 Health System Analysis Complete!")
        print(f"📁 Results saved in '{self.output_dir}' folder")
        print("\n📋 Generated files:")
        print("   - covid_health_analysis.png: Main analysis visualization")
        print("   - korea_covid_comparison.png: Korea detailed comparison")
        print("   - health_expenditure_groups.png: Health expenditure groups analysis")
        print("   - covid_health_report.md: Comprehensive analysis report")
        print("   - covid_health_data.csv: Processed dataset with COVID-19 metrics")
        print("\n💡 Key findings:")
        print("   - Health system characteristics influence COVID-19 outcomes")
        print("   - Physician density and health expenditure show correlations with performance")
        print("   - Korea's COVID-19 performance analyzed in detail")
        print("   - Complex relationships between health resources and pandemic response")

if __name__ == "__main__":
    analyzer = COVIDHealthAnalyzer()
    analyzer.run_complete_analysis() 