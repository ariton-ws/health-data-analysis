"use client"

import { Bar, BarChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { category: "정상", count: 876, percentage: 70.2 },
  { category: "주의", count: 248, percentage: 19.9 },
  { category: "경계", count: 93, percentage: 7.5 },
  { category: "위험", count: 30, percentage: 2.4 },
]

export function BloodPressureChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>혈압 분포 현황</CardTitle>
        <CardDescription>전체 대상자의 혈압 범주별 분포</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer
          config={{
            count: {
              label: "인원수",
              color: "hsl(var(--chart-1))",
            },
          }}
          className="h-[300px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis />
              <ChartTooltip
                content={<ChartTooltipContent />}
                formatter={(value, name) => [`${value}명 (${data.find((d) => d.count === value)?.percentage}%)`, name]}
              />
              <Bar dataKey="count" fill="var(--color-count)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
