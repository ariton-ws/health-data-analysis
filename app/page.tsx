"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Progress } from "@/components/ui/progress"
import {
  Activity,
  Heart,
  TrendingUp,
  TrendingDown,
  Users,
  Calendar,
  Download,
  Share2,
  AlertTriangle,
  CheckCircle,
} from "lucide-react"
import { HealthMetricsChart } from "./components/health-metrics-chart"
import { BloodPressureChart } from "./components/blood-pressure-chart"
import { BMIDistributionChart } from "./components/bmi-distribution-chart"
import { CorrelationChart } from "./components/correlation-chart"
import { TrendAnalysisChart } from "./components/trend-analysis-chart"

export default function HealthDataAnalysis() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Activity className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">건강 데이터 분석 리포트</h1>
                <p className="text-sm text-gray-500">종합적인 건강 지표 분석 결과</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                리포트 다운로드
              </Button>
              <Button variant="outline" size="sm">
                <Share2 className="h-4 w-4 mr-2" />
                공유
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Executive Summary */}
        <div className="mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <span>분석 요약</span>
              </CardTitle>
              <CardDescription>2024년 건강 데이터 분석 결과 주요 인사이트</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">1,247</div>
                  <div className="text-sm text-gray-600">총 분석 대상자</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">78.3%</div>
                  <div className="text-sm text-gray-600">정상 범위 비율</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600 mb-2">12개월</div>
                  <div className="text-sm text-gray-600">분석 기간</div>
                </div>
              </div>
              <Separator className="my-6" />
              <div className="prose max-w-none">
                <p className="text-gray-700 leading-relaxed">
                  본 분석은 2024년 1월부터 12월까지 수집된 건강 데이터를 바탕으로 수행되었습니다. 전체 대상자 중 78.3%가
                  정상 건강 범위에 속하며, 혈압과 BMI 지표에서 계절적 변화 패턴이 관찰되었습니다. 특히 겨울철 혈압
                  상승과 여름철 체중 감소 경향이 통계적으로 유의미한 결과를 보였습니다.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">평균 혈압</CardTitle>
              <Heart className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">118/76</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-600 flex items-center">
                  <TrendingDown className="h-3 w-3 mr-1" />
                  2.3% 개선
                </span>
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">평균 BMI</CardTitle>
              <Activity className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">23.4</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-600 flex items-center">
                  <TrendingDown className="h-3 w-3 mr-1" />
                  1.2% 감소
                </span>
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">평균 심박수</CardTitle>
              <Heart className="h-4 w-4 text-pink-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">72 BPM</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-orange-600 flex items-center">
                  <TrendingUp className="h-3 w-3 mr-1" />
                  0.8% 증가
                </span>
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">위험군 비율</CardTitle>
              <AlertTriangle className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">21.7%</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-600 flex items-center">
                  <TrendingDown className="h-3 w-3 mr-1" />
                  3.1% 감소
                </span>
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <HealthMetricsChart />
          <BloodPressureChart />
          <BMIDistributionChart />
          <TrendAnalysisChart />
        </div>

        {/* Correlation Analysis */}
        <div className="mb-8">
          <CorrelationChart />
        </div>

        {/* Detailed Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>주요 발견사항</CardTitle>
              <CardDescription>데이터 분석을 통해 도출된 핵심 인사이트</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start space-x-3">
                <Badge variant="secondary" className="mt-1">
                  1
                </Badge>
                <div>
                  <h4 className="font-semibold text-sm">계절적 혈압 변화</h4>
                  <p className="text-sm text-gray-600">겨울철 평균 혈압이 여름철 대비 8-12mmHg 높게 측정되었습니다.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Badge variant="secondary" className="mt-1">
                  2
                </Badge>
                <div>
                  <h4 className="font-semibold text-sm">연령별 BMI 분포</h4>
                  <p className="text-sm text-gray-600">40-50대 연령층에서 과체중 비율이 가장 높게 나타났습니다.</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Badge variant="secondary" className="mt-1">
                  3
                </Badge>
                <div>
                  <h4 className="font-semibold text-sm">운동과 건강지표 상관관계</h4>
                  <p className="text-sm text-gray-600">
                    주 3회 이상 운동군에서 모든 건강지표가 유의미하게 개선되었습니다.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>권장사항</CardTitle>
              <CardDescription>분석 결과를 바탕으로 한 건강 관리 제안</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">겨울철 혈압 관리</span>
                  <Badge variant="outline">높은 우선순위</Badge>
                </div>
                <Progress value={85} className="h-2" />
                <p className="text-xs text-gray-600">실내 온도 유지 및 정기적인 혈압 측정 권장</p>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">체중 관리 프로그램</span>
                  <Badge variant="outline">중간 우선순위</Badge>
                </div>
                <Progress value={65} className="h-2" />
                <p className="text-xs text-gray-600">40-50대 대상 맞춤형 체중 관리 프로그램 도입</p>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">운동 프로그램 확대</span>
                  <Badge variant="outline">높은 우선순위</Badge>
                </div>
                <Progress value={90} className="h-2" />
                <p className="text-xs text-gray-600">주 3회 이상 규칙적인 운동 참여 독려</p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Footer */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Calendar className="h-4 w-4" />
                <span>마지막 업데이트: 2024년 12월 31일</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Users className="h-4 w-4" />
                <span>분석 대상: 1,247명</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
