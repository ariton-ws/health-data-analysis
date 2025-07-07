import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

export async function GET() {
  try {
    const filePath = path.join(process.cwd(), '..', 'gdp_recovery_results', 'gdp_recovery_data.csv');
    const fileContent = await fs.readFile(filePath, 'utf-8');
    
    const lines = fileContent.split('\n');
    const headers = lines[0].split(',');
    
    const data = lines.slice(1)
      .filter(line => line.trim())
      .map(line => {
        const values = line.split(',');
        const row: any = {};
        headers.forEach((header, index) => {
          const value = values[index]?.trim() || '';
          if (value === '') {
            row[header.trim()] = null;
          } else {
            row[header.trim()] = isNaN(Number(value)) ? value : Number(value);
          }
        });
        return row;
      });
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error reading GDP recovery data:', error);
    return NextResponse.json({ error: 'Failed to load data' }, { status: 500 });
  }
} 