from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
import os
from datetime import datetime

app = Flask(__name__)

# 데이터 로드 함수들
def load_gdp_recovery_data():
    """GDP 회복 분석 데이터 로드"""
    try:
        df = pd.read_csv('gdp_recovery_results/gdp_recovery_data.csv')
        return df
    except:
        return pd.DataFrame()

def load_covid_health_data():
    """COVID-19 건강 분석 데이터 로드"""
    try:
        df = pd.read_csv('covid_health_results/covid_health_data.csv')
        return df
    except:
        return pd.DataFrame()

def load_advanced_health_data():
    """고급 건강 분석 데이터 로드"""
    try:
        df = pd.read_csv('advanced_analysis_results/enhanced_health_data.csv')
        return df
    except:
        return pd.DataFrame()

def load_original_data():
    """원본 데이터 로드"""
    data = {}
    
    # GDP per capita 데이터
    try:
        gdp_df = pd.read_csv('data/gdp_per_capita/gdp-per-capita-worldbank.csv')
        data['gdp_per_capita'] = gdp_df
    except:
        data['gdp_per_capita'] = pd.DataFrame()
    
    # Health expenditure 데이터
    try:
        health_df = pd.read_csv('data/health_expenditure_financing.csv')
        data['health_expenditure'] = health_df
    except:
        data['health_expenditure'] = pd.DataFrame()
    
    # Physicians per 1000 데이터
    try:
        physicians_df = pd.read_csv('data/physicians_per_1000/physicians-per-1000-people.csv')
        data['physicians'] = physicians_df
    except:
        data['physicians'] = pd.DataFrame()
    
    return data

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/gdp-recovery')
def gdp_recovery():
    """GDP 회복 분석 페이지"""
    return render_template('gdp_recovery.html')

@app.route('/covid-health')
def covid_health():
    """COVID-19 건강 분석 페이지"""
    return render_template('covid_health.html')

@app.route('/advanced-health')
def advanced_health():
    """고급 건강 분석 페이지"""
    return render_template('advanced_health.html')

@app.route('/original-data')
def original_data():
    """원본 데이터 페이지"""
    return render_template('original_data.html')

# API 엔드포인트들
@app.route('/api/gdp-recovery-data')
def api_gdp_recovery_data():
    """GDP 회복 분석 데이터 API"""
    df = load_gdp_recovery_data()
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    # 필터링 파라미터 처리
    income_group = request.args.get('income_group', '')
    region = request.args.get('region', '')
    
    if income_group:
        df = df[df['Income_Group'] == income_group]
    if region:
        df = df[df['Region'] == region]
    
    return jsonify({
        'data': df.to_dict('records'),
        'income_groups': df['Income_Group'].unique().tolist() if 'Income_Group' in df.columns else [],
        'regions': df['Region'].unique().tolist() if 'Region' in df.columns else []
    })

@app.route('/api/covid-health-data')
def api_covid_health_data():
    """COVID-19 건강 분석 데이터 API"""
    df = load_covid_health_data()
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    # 필터링 파라미터 처리
    income_group = request.args.get('income_group', '')
    region = request.args.get('region', '')
    
    if income_group:
        df = df[df['Income_Group'] == income_group]
    if region:
        df = df[df['Region'] == region]
    
    return jsonify({
        'data': df.to_dict('records'),
        'income_groups': df['Income_Group'].unique().tolist() if 'Income_Group' in df.columns else [],
        'regions': df['Region'].unique().tolist() if 'Region' in df.columns else []
    })

@app.route('/api/advanced-health-data')
def api_advanced_health_data():
    """고급 건강 분석 데이터 API"""
    df = load_advanced_health_data()
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    # 필터링 파라미터 처리
    income_group = request.args.get('income_group', '')
    region = request.args.get('region', '')
    
    if income_group:
        df = df[df['Income_Group'] == income_group]
    if region:
        df = df[df['Region'] == region]
    
    return jsonify({
        'data': df.to_dict('records'),
        'income_groups': df['Income_Group'].unique().tolist() if 'Income_Group' in df.columns else [],
        'regions': df['Region'].unique().tolist() if 'Region' in df.columns else []
    })

@app.route('/api/original-data')
def api_original_data():
    """원본 데이터 API"""
    data = load_original_data()
    
    dataset = request.args.get('dataset', 'gdp_per_capita')
    if dataset not in data:
        return jsonify({'error': '데이터셋을 찾을 수 없습니다.'})
    
    df = data[dataset]
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    return jsonify({
        'data': df.head(100).to_dict('records'),  # 처음 100개 행만
        'columns': df.columns.tolist(),
        'shape': df.shape
    })

@app.route('/api/chart/gdp-recovery-scatter')
def api_gdp_recovery_scatter():
    """GDP 회복 산점도 차트"""
    df = load_gdp_recovery_data()
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    fig = px.scatter(
        df, 
        x='GDP_Per_Capita_2019', 
        y='GDP_Recovery_Rate',
        color='Income_Group',
        hover_data=['Country', 'Region'],
        title='GDP per Capita vs Recovery Rate',
        labels={
            'GDP_Per_Capita_2019': 'GDP per Capita (2019)',
            'GDP_Recovery_Rate': 'GDP Recovery Rate (%)',
            'Income_Group': 'Income Group'
        }
    )
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/chart/covid-mortality-scatter')
def api_covid_mortality_scatter():
    """COVID-19 사망률 산점도 차트"""
    df = load_covid_health_data()
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    fig = px.scatter(
        df, 
        x='Health_Expenditure_Per_Capita', 
        y='COVID_Mortality_Rate',
        color='Income_Group',
        hover_data=['Country', 'Region'],
        title='Health Expenditure vs COVID-19 Mortality Rate',
        labels={
            'Health_Expenditure_Per_Capita': 'Health Expenditure per Capita ($)',
            'COVID_Mortality_Rate': 'COVID-19 Mortality Rate (per 100k)',
            'Income_Group': 'Income Group'
        }
    )
    
    return jsonify(json.loads(fig.to_json()))

@app.route('/api/chart/health-index')
def api_health_index():
    """종합 건강 지수 차트"""
    df = load_advanced_health_data()
    if df.empty:
        return jsonify({'error': '데이터를 로드할 수 없습니다.'})
    
    fig = px.scatter(
        df, 
        x='GDP_Per_Capita', 
        y='Comprehensive_Health_Index',
        color='Income_Group',
        size='Population',
        hover_data=['Country', 'Region'],
        title='GDP per Capita vs Comprehensive Health Index',
        labels={
            'GDP_Per_Capita': 'GDP per Capita ($)',
            'Comprehensive_Health_Index': 'Comprehensive Health Index',
            'Income_Group': 'Income Group',
            'Population': 'Population'
        }
    )
    
    return jsonify(json.loads(fig.to_json()))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 