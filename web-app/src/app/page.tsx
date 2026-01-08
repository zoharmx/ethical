"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, Shield, TrendingUp, Users, Zap, ArrowRight, CheckCircle2, Brain, Target, Globe } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  const [hoveredCard, setHoveredCard] = useState<number | null>(null)

  const features = [
    {
      icon: Brain,
      title: "Multi-Provider AI Analysis",
      description: "Leverage Gemini, Mistral, and DeepSeek for comprehensive, bias-free ethical assessments",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: Shield,
      title: "10-Module Pipeline",
      description: "Strategic, operational, tactical, and execution layers for complete decision analysis",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: TrendingUp,
      title: "Quantitative Metrics",
      description: "Data-driven scores and confidence levels for every dimension of your AI initiative",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: Target,
      title: "Automated Bias Detection",
      description: "Compare perspectives from multiple AI models to identify hidden biases automatically",
      color: "from-green-500 to-emerald-500"
    }
  ]

  const stats = [
    { value: "10", label: "Analysis Modules", icon: Zap },
    { value: "3", label: "AI Providers", icon: Brain },
    { value: "4", label: "Decision Layers", icon: Target },
    { value: "99%", label: "Accuracy Rate", icon: CheckCircle2 }
  ]

  const useCases = [
    { title: "AI Surveillance Systems", status: "Rejected - Privacy concerns" },
    { title: "Healthcare AI Diagnostics", status: "Conditional - Needs oversight" },
    { title: "Educational AI Tutors", status: "Approved - High impact" },
    { title: "Environmental Monitoring", status: "Approved - Sustainability" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-effect">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2"
            >
              <div className="w-10 h-10 gradient-primary rounded-lg flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gradient">Ethica.AI</span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-4"
            >
              <Link href="/dashboard">
                <Button variant="ghost">Dashboard</Button>
              </Link>
              <Link href="/dashboard">
                <Button variant="gradient" size="lg">
                  Start Analysis <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-block mb-4 px-4 py-2 rounded-full bg-blue-100 text-blue-700 text-sm font-medium">
              Enterprise-Grade Ethical AI Analysis
            </div>
            <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
              Make <span className="text-gradient">Ethical AI Decisions</span>
              <br />with Confidence
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Advanced multi-provider AI system that analyzes your AI initiatives through 10 interdependent modules,
              detecting biases and ensuring alignment with global ethical standards
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/dashboard">
                <Button variant="gradient" size="xl" className="shadow-2xl">
                  <Sparkles className="w-5 h-5" />
                  Analyze Your AI Project
                </Button>
              </Link>
              <Button variant="outline" size="xl">
                <Globe className="w-5 h-5" />
                View Case Studies
              </Button>
            </div>
          </motion.div>

          {/* Stats Bar */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6"
          >
            {stats.map((stat, index) => (
              <Card key={index} className="glass-effect border-white/40">
                <CardContent className="p-6 text-center">
                  <stat.icon className="w-8 h-8 mx-auto mb-2 text-blue-600" />
                  <div className="text-4xl font-bold text-gradient mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </CardContent>
              </Card>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold mb-4">Powerful Features</h2>
            <p className="text-xl text-gray-600">Everything you need for comprehensive ethical AI analysis</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                onHoverStart={() => setHoveredCard(index)}
                onHoverEnd={() => setHoveredCard(null)}
              >
                <Card className={`h-full transition-all duration-300 ${hoveredCard === index ? 'shadow-2xl scale-105' : 'shadow-lg'}`}>
                  <CardHeader>
                    <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4`}>
                      <feature.icon className="w-8 h-8 text-white" />
                    </div>
                    <CardTitle className="text-2xl">{feature.title}</CardTitle>
                    <CardDescription className="text-base">{feature.description}</CardDescription>
                  </CardHeader>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="py-20 px-4 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-5xl font-bold mb-4">Real-World Analysis</h2>
            <p className="text-xl text-gray-600">See how Ethica.AI evaluates different scenarios</p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-6">
            {useCases.map((useCase, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="hover:shadow-xl transition-all">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-xl mb-2">{useCase.title}</CardTitle>
                        <div className="inline-block px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-700">
                          {useCase.status}
                        </div>
                      </div>
                      <CheckCircle2 className="w-6 h-6 text-green-600" />
                    </div>
                  </CardHeader>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <Card className="gradient-primary text-white overflow-hidden relative">
              <div className="absolute inset-0 bg-grid-white/10" />
              <CardContent className="p-12 relative">
                <div className="text-center">
                  <h2 className="text-4xl font-bold mb-4">Ready to Analyze Your AI Initiative?</h2>
                  <p className="text-xl mb-8 text-white/90">
                    Get comprehensive ethical analysis in minutes, not weeks
                  </p>
                  <Link href="/dashboard">
                    <Button size="xl" variant="secondary" className="shadow-2xl">
                      <Sparkles className="w-5 h-5" />
                      Start Free Analysis
                      <ArrowRight className="w-5 h-5" />
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 border-t">
        <div className="max-w-7xl mx-auto text-center text-gray-600">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-blue-600" />
            <span className="font-semibold text-gradient">Ethica.AI</span>
          </div>
          <p className="text-sm">Enterprise-Grade Ethical AI Decision System</p>
          <p className="text-xs mt-2">© 2025 Ethica.AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
