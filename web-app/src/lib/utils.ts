import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatScore(score: number): string {
  return `${(score * 100).toFixed(0)}%`
}

export function getScoreColor(score: number): string {
  if (score >= 0.8) return "text-green-600"
  if (score >= 0.6) return "text-yellow-600"
  return "text-red-600"
}

export function getApprovalColor(type: string): string {
  switch (type) {
    case "APPROVED":
      return "bg-green-100 text-green-800 border-green-300"
    case "CONDITIONAL":
      return "bg-yellow-100 text-yellow-800 border-yellow-300"
    case "REJECTED":
      return "bg-red-100 text-red-800 border-red-300"
    default:
      return "bg-gray-100 text-gray-800 border-gray-300"
  }
}
