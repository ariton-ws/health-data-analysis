"use client"

import { Area, AreaChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { month: "1월", normal: 850, warning: 280, danger: 117 },
  { month: "2월", normal: 863, warning: 275, danger: 109 },
  { month: "3월", normal: 871, warning: 268, danger: 108 },
  { month: "4월", normal: 885, warning: 255, danger: 107 },
  { month: "5월", normal: 892, warning: 248, danger: 107 },
  { month: "6월", normal: 901, warning: 240, danger: 106 },
  { month: "7월", normal: 908, warning: 235, danger: 104 },
  { month: "8월", normal: 912, warning: 232, danger: 103 },
  { month: "9월", normal: 905, warning: 238, danger: 104 },
  { month: "10월", normal: 898, warning: 245, danger: 104 },
  { month: "11월", normal: 889, warning: 252, danger: 106 },
  { month: "12월", normal: 876, warning: 248, danger: 123 },
]

export function TrendAnalysisChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>건강 상태 추이 분석</CardTitle>
        <CardDescription>월별 건강 상태 분포 변화</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer
          config={{
            normal: {
              label: "정상",
              color: "hsl(var(--chart-2))",
            },
            warning: {
              label: "주의",
              color: "hsl(var(--chart-3))",
            },
            danger: {
              label: "위험",
              color: "hsl(var(--chart-1))",
            },
          }}
          className="h-[300px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Area
                type="monotone"
                dataKey="danger"
                stackId="1"
                stroke="var(--color-danger)"
                fill="var(--color-danger)"
                fillOpacity={0.8}
              />
              <Area
                type="monotone"
                dataKey="warning"
                stackId="1"
                stroke="var(--color-warning)"
                fill="var(--color-warning)"
                fillOpacity={0.8}
              />
              <Area
                type="monotone"
                dataKey="normal"
                stackId="1"
                stroke="var(--color-normal)"
                fill="var(--color-normal)"
                fillOpacity={0.8}
              />
            </AreaChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
