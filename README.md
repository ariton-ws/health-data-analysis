# 건강 데이터 분석 대시보드

COVID-19 팬데믹과 경제 회복에 대한 종합적인 건강 데이터 분석 결과를 웹 대시보드로 제공합니다.

## 📊 분석 내용

### 1. GDP 회복 분석
- GDP 수준과 COVID-19 이후 경제 회복률의 상관관계
- 개발도상국 vs 선진국의 회복 패턴 차이
- 지역별, 소득 그룹별 회복률 비교

### 2. COVID-19 건강 분석
- 건강 지출과 COVID-19 사망률의 관계
- 의료진 밀도와 건강 결과의 연관성
- 국가별 COVID-19 대응 효율성 평가

### 3. 고급 건강 분석
- 종합 건강 지수 개발
- 효율성 분석 및 차원 감소 효과
- GDP 대비 건강 시스템 성과 평가

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 웹 애플리케이션 실행
```bash
python app.py
```

### 3. 브라우저에서 접속
```
http://localhost:5000
```

## 📁 프로젝트 구조

```
health_data_analysis/
├── app.py                          # Flask 메인 애플리케이션
├── requirements.txt                # Python 의존성
├── README.md                      # 프로젝트 설명서
├── templates/                     # HTML 템플릿
│   ├── base.html                  # 기본 템플릿
│   ├── index.html                 # 메인 페이지
│   ├── gdp_recovery.html          # GDP 회복 분석 페이지
│   ├── covid_health.html          # COVID-19 건강 분석 페이지
│   ├── advanced_health.html       # 고급 건강 분석 페이지
│   └── original_data.html         # 원본 데이터 페이지
├── static/                        # 정적 파일
│   ├── css/
│   │   └── style.css              # 커스텀 CSS
│   └── js/
│       └── main.js                # 메인 JavaScript
├── data/                          # 원본 데이터
│   ├── gdp_per_capita/            # GDP per capita 데이터
│   ├── health_expenditure_financing.csv
│   ├── physicians_per_1000/       # 의료진 밀도 데이터
│   ├── hospital_beds_per_1000/    # 병상 수 데이터
│   ├── life_expectancy/           # 기대수명 데이터
│   ├── infant_mortality/          # 영아사망률 데이터
│   └── WHO-COVID-19-global-daily-data.csv
├── gdp_recovery_results/          # GDP 회복 분석 결과
├── covid_health_results/          # COVID-19 건강 분석 결과
└── advanced_analysis_results/     # 고급 건강 분석 결과
```

## 🎯 주요 기능

### 📈 인터랙티브 차트
- Plotly.js를 사용한 동적 차트
- 줌, 팬, 호버 기능 지원
- 반응형 디자인

### 🔍 필터링 기능
- 소득 그룹별 필터링
- 지역별 필터링
- 실시간 데이터 업데이트

### 📊 통계 요약
- 평균, 중앙값, 표준편차 등 기본 통계
- 데이터 분포 시각화
- 국가별 비교 분석

### 📋 데이터 테이블
- 정렬 가능한 데이터 테이블
- 검색 및 필터링
- CSV 내보내기 기능

## 🛠 기술 스택

### 백엔드
- **Flask**: Python 웹 프레임워크
- **Pandas**: 데이터 처리 및 분석
- **Plotly**: 차트 생성
- **NumPy**: 수치 계산

### 프론트엔드
- **Bootstrap 5**: UI 프레임워크
- **Plotly.js**: 인터랙티브 차트
- **Font Awesome**: 아이콘
- **Vanilla JavaScript**: 동적 기능

## 📊 데이터 소스

- **World Bank**: GDP, 건강 지출 데이터
- **WHO**: COVID-19 데이터, 의료 지표
- **Our World in Data**: 의료진 밀도, 병상 수

## 🔧 API 엔드포인트

### 데이터 API
- `GET /api/gdp-recovery-data` - GDP 회복 분석 데이터
- `GET /api/covid-health-data` - COVID-19 건강 분석 데이터
- `GET /api/advanced-health-data` - 고급 건강 분석 데이터
- `GET /api/original-data` - 원본 데이터

### 차트 API
- `GET /api/chart/gdp-recovery-scatter` - GDP 회복 산점도
- `GET /api/chart/covid-mortality-scatter` - COVID-19 사망률 산점도
- `GET /api/chart/health-index` - 종합 건강 지수 차트

## 🎨 UI/UX 특징

- **반응형 디자인**: 모바일, 태블릿, 데스크톱 지원
- **다크/라이트 모드**: 사용자 선호도에 따른 테마 변경
- **접근성**: WCAG 2.1 AA 준수
- **성능 최적화**: 지연 로딩, 캐싱 적용

## 📈 분석 결과 요약

### GDP 회복 분석
- **주요 발견**: 낮은 GDP 국가들이 더 높은 회복률을 보임
- **상관계수**: -0.42 (중간 정도의 음의 상관관계)
- **통계적 유의성**: p < 0.001

### COVID-19 건강 분석
- **주요 발견**: 건강 지출과 COVID-19 사망률 간 약한 상관관계
- **상관계수**: 0.31 (약한 양의 상관관계)
- **통계적 유의성**: p < 0.05

### 고급 건강 분석
- **종합 건강 지수**: 0.0 ~ 1.0 범위의 정규화된 지수
- **효율성 점수**: 투입 대비 산출의 효율성 측정
- **차원 감소**: PCA를 통한 주요 요인 추출

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

**건강 데이터 분석 대시보드** - COVID-19와 경제 회복에 대한 데이터 기반 인사이트 제공 