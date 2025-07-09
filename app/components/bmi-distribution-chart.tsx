"use client"

import { Pie, PieChart, Cell, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { name: "저체중", value: 87, color: "#3b82f6" },
  { name: "정상", value: 743, color: "#10b981" },
  { name: "과체중", value: 312, color: "#f59e0b" },
  { name: "비만", value: 105, color: "#ef4444" },
]

export function BMIDistributionChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>BMI 분포 현황</CardTitle>
        <CardDescription>체질량지수 범주별 인원 분포</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer
          config={{
            value: {
              label: "인원수",
            },
          }}
          className="h-[300px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <ChartTooltip content={<ChartTooltipContent />} formatter={(value) => [`${value}명`, "인원수"]} />
            </PieChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
