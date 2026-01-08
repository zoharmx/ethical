import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "@/styles/globals.css"
import { cn } from "@/lib/utils"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Ethica.AI - Enterprise Ethical AI Decision System",
  description: "Advanced multi-provider AI system for comprehensive ethical analysis of AI decisions",
  keywords: ["AI Ethics", "Decision Analysis", "Enterprise AI", "Risk Assessment"],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn(inter.className, "min-h-screen antialiased")}>
        {children}
      </body>
    </html>
  )
}
