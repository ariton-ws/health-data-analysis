import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

export async function GET() {
  try {
    const filePath = path.join(process.cwd(), '..', 'gdp_recovery_results', 'gdp_recovery_report.md');
    const fileContent = await fs.readFile(filePath, 'utf-8');
    return new NextResponse(fileContent, { headers: { 'Content-Type': 'text/markdown' } });
  } catch (error) {
    return new NextResponse('Failed to load report', { status: 500 });
  }
} 