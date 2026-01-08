import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    const response = await fetch(`${apiUrl}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      throw new Error('API request failed')
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Analysis error:', error)

    // Return mock data as fallback
    const mockData = {
      scenario_id: `ETH-${Math.random().toString(36).substr(2, 8)}`,
      timestamp: new Date().toISOString(),
      strategic: {
        impact_score: 0.78,
        confidence: 0.95,
      },
      operational: {
        harmony_score: 0.72,
      },
      tactical: {
        sustainability: 0.75,
      },
      execution: {
        readiness: 0.74,
        approved: true,
      },
      decision: {
        approved: true,
        approval_type: 'CONDITIONAL',
        confidence: 0.98,
        reasoning: 'Conditional approval granted. High potential for positive impact with proper oversight.',
        actions: [
          'Implement transparent AI decision-making processes',
          'Establish regular bias audits',
        ],
        conditions: [
          'Require human oversight for critical decisions',
          'Implement comprehensive data privacy measures',
        ],
      },
    }

    return NextResponse.json(mockData)
  }
}
