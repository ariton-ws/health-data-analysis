// 메인 JavaScript 파일

// 전역 변수
let isLoading = false;

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 앱 초기화
function initializeApp() {
    console.log('건강 데이터 분석 대시보드가 로드되었습니다.');
    
    // 네비게이션 활성화
    activateCurrentNav();
    
    // 툴팁 초기화
    initializeTooltips();
    
    // 로딩 상태 관리
    setupLoadingStates();
}

// 현재 네비게이션 활성화
function activateCurrentNav() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// 툴팁 초기화
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 로딩 상태 설정
function setupLoadingStates() {
    // 버튼 클릭 시 로딩 상태 표시
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn') && !e.target.classList.contains('btn-secondary')) {
            const btn = e.target;
            const originalText = btn.innerHTML;
            
            btn.innerHTML = '<span class="loading"></span> 로딩 중...';
            btn.disabled = true;
            
            // 3초 후 원래 상태로 복원
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 3000);
        }
    });
}

// 유틸리티 함수들
const utils = {
    // 숫자 포맷팅
    formatNumber: function(num, decimals = 0) {
        if (num === null || num === undefined || isNaN(num)) {
            return 'N/A';
        }
        return num.toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    },
    
    // 통화 포맷팅
    formatCurrency: function(amount, currency = 'USD') {
        if (amount === null || amount === undefined || isNaN(amount)) {
            return 'N/A';
        }
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    // 퍼센트 포맷팅
    formatPercent: function(value, decimals = 2) {
        if (value === null || value === undefined || isNaN(value)) {
            return 'N/A';
        }
        return value.toFixed(decimals) + '%';
    },
    
    // 날짜 포맷팅
    formatDate: function(date) {
        if (!date) return 'N/A';
        return new Date(date).toLocaleDateString('ko-KR');
    },
    
    // 배열에서 중복 제거
    unique: function(arr) {
        return [...new Set(arr)];
    },
    
    // 배열 정렬
    sortArray: function(arr, key = null, ascending = true) {
        if (!arr || arr.length === 0) return arr;
        
        const sorted = [...arr];
        if (key) {
            sorted.sort((a, b) => {
                const aVal = a[key];
                const bVal = b[key];
                
                if (aVal < bVal) return ascending ? -1 : 1;
                if (aVal > bVal) return ascending ? 1 : -1;
                return 0;
            });
        } else {
            sorted.sort((a, b) => {
                if (a < b) return ascending ? -1 : 1;
                if (a > b) return ascending ? 1 : -1;
                return 0;
            });
        }
        
        return sorted;
    },
    
    // 통계 계산
    calculateStats: function(data, key) {
        const values = data.map(d => d[key]).filter(v => !isNaN(v) && v !== null && v !== undefined);
        
        if (values.length === 0) {
            return {
                count: 0,
                mean: 0,
                median: 0,
                min: 0,
                max: 0,
                std: 0
            };
        }
        
        const sorted = values.sort((a, b) => a - b);
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const median = sorted.length % 2 === 0 
            ? (sorted[sorted.length/2 - 1] + sorted[sorted.length/2]) / 2
            : sorted[Math.floor(sorted.length/2)];
        
        const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
        const std = Math.sqrt(variance);
        
        return {
            count: values.length,
            mean: mean,
            median: median,
            min: sorted[0],
            max: sorted[sorted.length - 1],
            std: std
        };
    }
};

// 차트 관련 함수들
const chartUtils = {
    // 기본 차트 설정
    defaultConfig: {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    },
    
    // 색상 팔레트
    colors: [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ],
    
    // 산점도 차트 생성
    createScatterPlot: function(containerId, data, xKey, yKey, colorKey = null, sizeKey = null) {
        const trace = {
            x: data.map(d => d[xKey]),
            y: data.map(d => d[yKey]),
            mode: 'markers',
            type: 'scatter',
            text: data.map(d => d.Country || d.country || ''),
            hovertemplate: '<b>%{text}</b><br>' +
                          `${xKey}: %{x}<br>` +
                          `${yKey}: %{y}<extra></extra>`
        };
        
        if (colorKey) {
            trace.marker = {
                color: data.map(d => d[colorKey]),
                colorscale: 'Viridis',
                showscale: true,
                colorbar: {
                    title: colorKey
                }
            };
        }
        
        if (sizeKey) {
            trace.marker = trace.marker || {};
            trace.marker.size = data.map(d => d[sizeKey]);
        }
        
        const layout = {
            title: `${xKey} vs ${yKey}`,
            xaxis: { title: xKey },
            yaxis: { title: yKey },
            hovermode: 'closest'
        };
        
        Plotly.newPlot(containerId, [trace], layout, this.defaultConfig);
    },
    
    // 막대 차트 생성
    createBarChart: function(containerId, data, xKey, yKey, colorKey = null) {
        const trace = {
            x: data.map(d => d[xKey]),
            y: data.map(d => d[yKey]),
            type: 'bar',
            text: data.map(d => utils.formatNumber(d[yKey])),
            textposition: 'auto'
        };
        
        if (colorKey) {
            trace.marker = {
                color: data.map(d => d[colorKey]),
                colorscale: 'Viridis'
            };
        }
        
        const layout = {
            title: `${yKey} by ${xKey}`,
            xaxis: { title: xKey },
            yaxis: { title: yKey }
        };
        
        Plotly.newPlot(containerId, [trace], layout, this.defaultConfig);
    }
};

// 에러 처리
function handleError(error, context = '') {
    console.error(`Error in ${context}:`, error);
    
    // 사용자에게 에러 메시지 표시
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        <strong>오류가 발생했습니다!</strong> ${error.message || '알 수 없는 오류가 발생했습니다.'}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
    }
}

// 성공 메시지 표시
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show';
    successDiv.innerHTML = `
        <strong>성공!</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(successDiv, container.firstChild);
    }
}

// 전역 객체에 유틸리티 함수들 추가
window.utils = utils;
window.chartUtils = chartUtils;
window.handleError = handleError;
window.showSuccess = showSuccess; 