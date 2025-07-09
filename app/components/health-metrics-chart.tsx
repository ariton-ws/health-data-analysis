"use client"

import { Line, LineChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { month: "1월", bloodPressure: 125, heartRate: 75, bmi: 24.2 },
  { month: "2월", bloodPressure: 123, heartRate: 73, bmi: 24.0 },
  { month: "3월", bloodPressure: 120, heartRate: 72, bmi: 23.8 },
  { month: "4월", bloodPressure: 118, heartRate: 71, bmi: 23.6 },
  { month: "5월", bloodPressure: 116, heartRate: 70, bmi: 23.4 },
  { month: "6월", bloodPressure: 115, heartRate: 69, bmi: 23.2 },
  { month: "7월", bloodPressure: 114, heartRate: 68, bmi: 23.0 },
  { month: "8월", bloodPressure: 115, heartRate: 69, bmi: 23.1 },
  { month: "9월", bloodPressure: 117, heartRate: 71, bmi: 23.3 },
  { month: "10월", bloodPressure: 119, heartRate: 72, bmi: 23.5 },
  { month: "11월", bloodPressure: 122, heartRate: 74, bmi: 23.7 },
  { month: "12월", bloodPressure: 124, heartRate: 75, bmi: 23.9 },
]

export function HealthMetricsChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>월별 건강 지표 추이</CardTitle>
        <CardDescription>혈압, 심박수, BMI의 연간 변화 패턴</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer
          config={{
            bloodPressure: {
              label: "수축기 혈압",
              color: "hsl(var(--chart-1))",
            },
            heartRate: {
              label: "심박수",
              color: "hsl(var(--chart-2))",
            },
            bmi: {
              label: "BMI",
              color: "hsl(var(--chart-3))",
            },
          }}
          className="h-[300px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Line
                type="monotone"
                dataKey="bloodPressure"
                stroke="var(--color-bloodPressure)"
                strokeWidth={2}
                name="수축기 혈압 (mmHg)"
              />
              <Line
                type="monotone"
                dataKey="heartRate"
                stroke="var(--color-heartRate)"
                strokeWidth={2}
                name="심박수 (BPM)"
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
