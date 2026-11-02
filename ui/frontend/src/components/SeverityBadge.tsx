import { Severity } from '../types'

interface Props {
  severity: Severity
}

export default function SeverityBadge({ severity }: Props) {
  const colors: Record<Severity, string> = {
    critical: 'bg-red-600 text-white',
    high: 'bg-orange-500 text-white',
    medium: 'bg-yellow-500 text-white',
    low: 'bg-blue-500 text-white',
    unknown: 'bg-gray-400 text-white',
  }

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${colors[severity]}`}>
      {severity.toUpperCase()}
    </span>
  )
}
