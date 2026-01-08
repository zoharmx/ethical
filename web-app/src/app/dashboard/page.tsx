"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import {
  Sparkles, ArrowLeft, Play, Loader2, CheckCircle2, XCircle, AlertCircle,
  Brain, Shield, TrendingUp, Target, Zap, Users, Globe, FileText
} from "lucide-react"
import Link from "next/link"
import { cn, formatScore, getApprovalColor } from "@/lib/utils"

interface AnalysisResult {
  scenario_id: string
  timestamp: string
  strategic: {
    impact_score: number
    confidence: number
  }
  operational: {
    harmony_score: number
  }
  tactical: {
    sustainability: number
  }
  execution: {
    readiness: number
    approved: boolean
  }
  decision: {
    approved: boolean
    approval_type: "APPROVED" | "CONDITIONAL" | "REJECTED"
    confidence: number
    reasoning: string
    actions: string[]
    conditions: string[]
  }
}

const sampleScenarios = [
  {
    name: "AI Healthcare Diagnostics",
    action: "Deploy AI-powered diagnostic system in regional hospitals",
    context: "Healthcare provider wants to use AI to assist doctors in diagnosing diseases from medical imaging",
    stakeholders: ["Patients", "Doctors", "Hospital administrators", "Insurance companies"]
  },
  {
    name: "Educational AI Tutor",
    action: "Implement personalized AI tutoring system for students",
    context: "Educational institution proposes AI system to provide personalized learning experiences",
    stakeholders: ["Students", "Teachers", "Parents", "Educational administrators"]
  },
  {
    name: "Workplace Surveillance",
    action: "Deploy AI surveillance system to monitor employee productivity",
    context: "Company proposes AI system to track employee activities and productivity metrics",
    stakeholders: ["Employees", "Management", "HR department", "Labor unions"]
  }
]

export default function DashboardPage() {
  const [selectedScenario, setSelectedScenario] = useState(0)
  const [scenario, setScenario] = useState(sampleScenarios[0])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [currentModule, setCurrentModule] = useState(0)
  const [result, setResult] = useState<AnalysisResult | null>(null)

  const modules = [
    { name: "Purpose Validator", icon: Target, description: "Validating alignment with positive impact" },
    { name: "Insight Generator", icon: Brain, description: "Generating deep insights with Mistral AI" },
    { name: "Context Analyzer", icon: Globe, description: "Multi-perspective analysis (Gemini + DeepSeek)" },
    { name: "Opportunity Identifier", icon: TrendingUp, description: "Identifying value creation opportunities" },
    { name: "Risk Assessor", icon: Shield, description: "Evaluating risks and limitations" },
    { name: "Conflict Resolver", icon: Users, description: "Balancing opportunities and risks" },
    { name: "Sustainability Evaluator", icon: Zap, description: "Assessing long-term viability" },
    { name: "Implementation Planner", icon: FileText, description: "Creating implementation roadmap" },
    { name: "Integration Engine", icon: Brain, description: "Synthesizing all modules" },
    { name: "Decision Orchestrator", icon: CheckCircle2, description: "Making final decision" }
  ]

  const handleAnalyze = async () => {
    setIsAnalyzing(true)
    setCurrentModule(0)
    setResult(null)

    // Simulate analysis progress
    for (let i = 0; i < modules.length; i++) {
      setCurrentModule(i)
      await new Promise(resolve => setTimeout(resolve, 800))
    }

    // Simulate API call
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(scenario)
      })

      if (response.ok) {
        const data = await response.json()
        setResult(data)
      } else {
        // Fallback to mock data if API not available
        const mockResult: AnalysisResult = {
          scenario_id: `ETH-${Math.random().toString(36).substr(2, 8)}`,
          timestamp: new Date().toISOString(),
          strategic: {
            impact_score: selectedScenario === 2 ? 0.43 : selectedScenario === 0 ? 0.78 : 0.85,
            confidence: 0.95
          },
          operational: {
            harmony_score: selectedScenario === 2 ? 0.35 : selectedScenario === 0 ? 0.72 : 0.82
          },
          tactical: {
            sustainability: selectedScenario === 2 ? 0.40 : selectedScenario === 0 ? 0.75 : 0.88
          },
          execution: {
            readiness: selectedScenario === 2 ? 0.38 : selectedScenario === 0 ? 0.74 : 0.85,
            approved: selectedScenario !== 2
          },
          decision: {
            approved: selectedScenario !== 2,
            approval_type: selectedScenario === 2 ? "REJECTED" : selectedScenario === 0 ? "CONDITIONAL" : "APPROVED",
            confidence: 0.98,
            reasoning: selectedScenario === 2
              ? "Failed purpose validation. Impact score: 43%. Critical concerns: Privacy Violation, Authoritarianism, Employee Autonomy Violation."
              : selectedScenario === 0
              ? "Conditional approval granted. High potential for positive impact (78%) with proper oversight and safeguards in place."
              : "Approved with high confidence. Strong alignment with ethical standards (85%). Excellent sustainability and positive societal impact.",
            actions: selectedScenario === 2 ? [] : [
              "Implement transparent AI decision-making processes",
              "Establish regular bias audits",
              "Create stakeholder feedback mechanisms"
            ],
            conditions: selectedScenario === 2 ? [] : selectedScenario === 0 ? [
              "Require human doctor oversight for all diagnoses",
              "Implement comprehensive data privacy measures",
              "Establish clear liability frameworks"
            ] : []
          }
        }
        setResult(mockResult)
      }
    } catch (error) {
      console.error('Analysis error:', error)
    }

    setIsAnalyzing(false)
  }

  const handleScenarioChange = (index: number) => {
    setSelectedScenario(index)
    setScenario(sampleScenarios[index])
    setResult(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-effect">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </Button>
              </Link>
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 gradient-primary rounded-lg flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gradient">Ethica.AI Dashboard</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="pt-24 pb-12 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-4xl font-bold mb-2">Ethical AI Analysis</h1>
            <p className="text-gray-600">Analyze your AI initiative through our comprehensive 10-module pipeline</p>
          </motion.div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Left Column - Input */}
            <div className="lg:col-span-1 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Select Scenario</CardTitle>
                  <CardDescription>Choose a pre-defined scenario or create your own</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  {sampleScenarios.map((s, index) => (
                    <button
                      key={index}
                      onClick={() => handleScenarioChange(index)}
                      className={cn(
                        "w-full p-4 rounded-lg text-left transition-all border-2",
                        selectedScenario === index
                          ? "border-blue-500 bg-blue-50"
                          : "border-gray-200 hover:border-blue-300 bg-white"
                      )}
                    >
                      <div className="font-semibold text-sm mb-1">{s.name}</div>
                      <div className="text-xs text-gray-600">{s.action.substring(0, 60)}...</div>
                    </button>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Scenario Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700 mb-1 block">Action</label>
                    <textarea
                      className="w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                      rows={3}
                      value={scenario.action}
                      onChange={(e) => setScenario({ ...scenario, action: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700 mb-1 block">Context</label>
                    <textarea
                      className="w-full p-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                      rows={3}
                      value={scenario.context}
                      onChange={(e) => setScenario({ ...scenario, context: e.target.value })}
                    />
                  </div>
                  <Button
                    onClick={handleAnalyze}
                    disabled={isAnalyzing}
                    className="w-full"
                    variant="gradient"
                    size="lg"
                  >
                    {isAnalyzing ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Play className="w-5 h-5" />
                        Start Analysis
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </div>

            {/* Right Column - Results */}
            <div className="lg:col-span-2 space-y-6">
              {/* Analysis Progress */}
              <AnimatePresence>
                {isAnalyzing && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                  >
                    <Card className="border-blue-300 bg-blue-50/50">
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                          Analysis in Progress
                        </CardTitle>
                        <Progress value={(currentModule / modules.length) * 100} className="mt-2" />
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {modules.map((module, index) => (
                            <motion.div
                              key={index}
                              initial={{ opacity: 0.3 }}
                              animate={{
                                opacity: index <= currentModule ? 1 : 0.3,
                                scale: index === currentModule ? 1.02 : 1
                              }}
                              className={cn(
                                "flex items-center gap-3 p-3 rounded-lg transition-all",
                                index === currentModule && "bg-blue-100 shadow-sm",
                                index < currentModule && "bg-green-50"
                              )}
                            >
                              {index < currentModule ? (
                                <CheckCircle2 className="w-5 h-5 text-green-600" />
                              ) : index === currentModule ? (
                                <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                              ) : (
                                <module.icon className="w-5 h-5 text-gray-400" />
                              )}
                              <div className="flex-1">
                                <div className="font-medium text-sm">{module.name}</div>
                                <div className="text-xs text-gray-600">{module.description}</div>
                              </div>
                            </motion.div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Results */}
              <AnimatePresence>
                {result && !isAnalyzing && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-6"
                  >
                    {/* Decision Card */}
                    <Card className={cn(
                      "border-2",
                      result.decision.approval_type === "APPROVED" && "border-green-300 bg-green-50/50",
                      result.decision.approval_type === "CONDITIONAL" && "border-yellow-300 bg-yellow-50/50",
                      result.decision.approval_type === "REJECTED" && "border-red-300 bg-red-50/50"
                    )}>
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div>
                            <CardTitle className="text-3xl mb-2 flex items-center gap-3">
                              {result.decision.approval_type === "APPROVED" && <CheckCircle2 className="w-8 h-8 text-green-600" />}
                              {result.decision.approval_type === "CONDITIONAL" && <AlertCircle className="w-8 h-8 text-yellow-600" />}
                              {result.decision.approval_type === "REJECTED" && <XCircle className="w-8 h-8 text-red-600" />}
                              {result.decision.approval_type}
                            </CardTitle>
                            <div className="inline-block px-4 py-2 rounded-full text-sm font-medium bg-white shadow-sm">
                              Confidence: {formatScore(result.decision.confidence)}
                            </div>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-gray-700 mb-6">{result.decision.reasoning}</p>

                        {result.decision.actions.length > 0 && (
                          <div className="mb-4">
                            <h4 className="font-semibold mb-2 flex items-center gap-2">
                              <CheckCircle2 className="w-4 h-4" />
                              Recommended Actions
                            </h4>
                            <ul className="space-y-1">
                              {result.decision.actions.map((action, i) => (
                                <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                                  <span className="text-blue-600 mt-0.5">•</span>
                                  {action}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {result.decision.conditions.length > 0 && (
                          <div>
                            <h4 className="font-semibold mb-2 flex items-center gap-2">
                              <AlertCircle className="w-4 h-4" />
                              Conditions
                            </h4>
                            <ul className="space-y-1">
                              {result.decision.conditions.map((condition, i) => (
                                <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                                  <span className="text-yellow-600 mt-0.5">•</span>
                                  {condition}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </CardContent>
                    </Card>

                    {/* Metrics Cards */}
                    <div className="grid md:grid-cols-2 gap-6">
                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Strategic Layer</CardTitle>
                          <CardDescription>Intent and purpose validation</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium">Impact Score</span>
                              <span className="text-sm font-bold">{formatScore(result.strategic.impact_score)}</span>
                            </div>
                            <Progress value={result.strategic.impact_score * 100} />
                          </div>
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium">Confidence</span>
                              <span className="text-sm font-bold">{formatScore(result.strategic.confidence)}</span>
                            </div>
                            <Progress value={result.strategic.confidence * 100} />
                          </div>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Operational Layer</CardTitle>
                          <CardDescription>Force balance analysis</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium">Harmony Score</span>
                              <span className="text-sm font-bold">{formatScore(result.operational.harmony_score)}</span>
                            </div>
                            <Progress value={result.operational.harmony_score * 100} />
                          </div>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Tactical Layer</CardTitle>
                          <CardDescription>Long-term viability</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium">Sustainability</span>
                              <span className="text-sm font-bold">{formatScore(result.tactical.sustainability)}</span>
                            </div>
                            <Progress value={result.tactical.sustainability * 100} />
                          </div>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader>
                          <CardTitle className="text-lg">Execution Layer</CardTitle>
                          <CardDescription>Implementation readiness</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium">Readiness Score</span>
                              <span className="text-sm font-bold">{formatScore(result.execution.readiness)}</span>
                            </div>
                            <Progress value={result.execution.readiness * 100} />
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Empty State */}
              {!result && !isAnalyzing && (
                <Card className="border-dashed border-2 border-gray-300">
                  <CardContent className="flex flex-col items-center justify-center py-20">
                    <Brain className="w-16 h-16 text-gray-400 mb-4" />
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">Ready to Analyze</h3>
                    <p className="text-gray-500 text-center max-w-md">
                      Select a scenario and click "Start Analysis" to begin comprehensive ethical evaluation
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
