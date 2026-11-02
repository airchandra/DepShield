import { useEffect, useRef, useState } from 'react'
import { api } from '../api'

interface Props {
  runId: string
}

export default function ScanLog({ runId }: Props) {
  const [logs, setLogs] = useState<string[]>([])
  const [done, setDone] = useState(false)
  const logEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const unsubscribe = api.streamLogs(
      runId,
      (line) => {
        setLogs((prev) => [...prev, line])
      },
      () => {
        setDone(true)
      }
    )

    return unsubscribe
  }, [runId])

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  return (
    <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto" style={{ maxHeight: '400px', overflowY: 'auto' }}>
      {logs.length === 0 && !done ? (
        <p className="text-gray-500">Waiting for logs...</p>
      ) : (
        logs.map((line, idx) => (
          <div key={idx} className="whitespace-pre-wrap break-words">
            {line}
          </div>
        ))
      )}
      <div ref={logEndRef} />
      {done && logs.length > 0 && (
        <div className="text-green-400 mt-2">✅ Log stream closed</div>
      )}
    </div>
  )
}
