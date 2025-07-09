"use client"

import { Scatter, ScatterChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const data = [
  { bmi: 18.5, bloodPressure: 110, age: 25 },
  { bmi: 19.2, bloodPressure: 112, age: 28 },
  { bmi: 20.1, bloodPressure: 115, age: 32 },
  { bmi: 21.3, bloodPressure: 118, age: 35 },
  { bmi: 22.5, bloodPressure: 120, age: 38 },
  { bmi: 23.8, bloodPressure: 125, age: 42 },
  { bmi: 25.2, bloodPressure: 130, age: 45 },
  { bmi: 26.7, bloodPressure: 135, age: 48 },
  { bmi: 28.1, bloodPressure: 140, age: 52 },
  { bmi: 29.5, bloodPressure: 145, age: 55 },
  { bmi: 30.8, bloodPressure: 150, age: 58 },
  { bmi: 32.2, bloodPressure: 155, age: 62 },
]

export function CorrelationChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>BMI와 혈압 상관관계 분석</CardTitle>
        <CardDescription>체질량지수와 수축기 혈압 간의 상관관계 (r = 0.847, p {"<"} 0.001)</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer
          config={{
            bloodPressure: {
              label: "수축기 혈압",
              color: "hsl(var(--chart-1))",
            },
          }}
          className="h-[400px]"
        >
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="bmi" type="number" domain={["dataMin - 1", "dataMax + 1"]} name="BMI" />
              <YAxis dataKey="bloodPressure" type="number" domain={["dataMin - 5", "dataMax + 5"]} name="수축기 혈압" />
              <ChartTooltip
                content={<ChartTooltipContent />}
                formatter={(value, name, props) => [
                  name === "bloodPressure" ? `${value} mmHg` : value,
                  name === "bloodPressure" ? "수축기 혈압" : "BMI",
                ]}
              />
              <Scatter dataKey="bloodPressure" fill="var(--color-bloodPressure)" />
            </ScatterChart>
          </ResponsiveContainer>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
