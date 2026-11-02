interface Props {
  ecosystem: string
}

export default function EcosystemChip({ ecosystem }: Props) {
  const colors: Record<string, string> = {
    jvm: 'bg-blue-100 text-blue-800',
    python: 'bg-cyan-100 text-cyan-800',
    javascript: 'bg-yellow-100 text-yellow-800',
    go: 'bg-indigo-100 text-indigo-800',
    rust: 'bg-orange-100 text-orange-800',
  }

  return (
    <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${colors[ecosystem] || 'bg-gray-100 text-gray-800'}`}>
      {ecosystem}
    </span>
  )
}
