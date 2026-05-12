import React, { useState, useEffect } from "react"
import { Tldraw, createShapeId } from "tldraw"
import "tldraw/tldraw.css"

const API_BASE = "http://localhost:8000"
const TOKEN = "admin-token" // Simulated Zero Trust Token

function App() {
  const [nodes, setNodes] = useState([])
  const [audit, setAudit] = useState([])
  const [showAudit, setShowAudit] = useState(false)

  useEffect(() => {
    fetch(`${API_BASE}/nodes`, {
      headers: { "Authorization": `Bearer ${TOKEN}` }
    })
    .then(res => res.json())
    .then(data => setNodes(data))
    .catch(err => console.error(err))
  }, [])

  const fetchAudit = () => {
    fetch(`${API_BASE}/audit`, {
      headers: { "Authorization": `Bearer ${TOKEN}` }
    })
    .then(res => res.json())
    .then(data => setAudit(data))
    .catch(err => console.error(err))
  }

  // Handle tldraw mount to populate data nodes
  const handleMount = (editor) => {
    nodes.forEach((node, index) => {
      editor.createShapes([
        {
          id: createShapeId(node.id),
          type: 'geo',
          x: 100 + (index * 300),
          y: 100,
          props: {
            geo: 'rectangle',
            color: node.type === 'source' ? 'blue' : 'violet',
            fill: 'pattern',
            dash: 'draw',
            size: 'l',
            text: `${node.content.name}\n[${node.type.toUpperCase()}]\nIdentity: ${node.owner}`,
          },
        },
      ])
    })
  }

  return (
    <div className="h-screen w-screen bg-[#020617] text-slate-200 flex flex-col overflow-hidden font-sans">
      {/* Header */}
      <header className="h-16 bg-slate-900/80 backdrop-blur-md border-b border-white/10 flex items-center justify-between px-6 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center font-black text-white text-xl shadow-lg shadow-indigo-500/20 rotate-3">
            <span className="-rotate-3">F</span>
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Flux-Lang Backbone</h1>
            <p className="text-[9px] text-indigo-400 font-bold uppercase tracking-widest leading-none">Autonomous Data Governance</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => { setShowAudit(!showAudit); if(!showAudit) fetchAudit(); }}
            className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-xs font-semibold transition-all backdrop-blur-xl"
          >
            {showAudit ? "Close Audit" : "Version History"}
          </button>
          <div className="h-8 w-px bg-white/10" />
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-[10px] font-bold text-white leading-none">Admin System</p>
              <p className="text-[9px] text-green-400 font-bold uppercase tracking-tighter mt-1 flex items-center justify-end gap-1">
                <span className="w-1 h-1 bg-green-400 rounded-full animate-pulse"></span> Zero Trust Active
              </p>
            </div>
            <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 border-2 border-white/20 shadow-lg" />
          </div>
        </div>
      </header>

      <main className="flex-1 relative flex overflow-hidden">
        {/* The Visual Canvas */}
        <div className="flex-1 relative z-0">
           <Tldraw onMount={handleMount} inferDarkMode />
        </div>

        {/* Audit Panel */}
        {showAudit && (
          <div className="w-96 bg-slate-950/60 backdrop-blur-3xl border-l border-white/10 p-6 z-50 overflow-y-auto animate-in slide-in-from-right duration-300">
            <h2 className="text-sm font-black mb-6 uppercase tracking-[0.3em] text-indigo-400 flex items-center gap-2">
              <span className="w-2 h-2 bg-indigo-500 rounded-full"></span> Audit Trail
            </h2>
            <div className="space-y-6">
              {audit.map((entry, i) => (
                <div key={i} className="relative pl-5 border-l border-white/5 pb-2">
                  <div className="absolute -left-[3px] top-1 w-1.5 h-1.5 bg-indigo-500/50 rounded-full" />
                  <p className="text-[9px] text-indigo-300/60 font-mono mb-1">{entry.timestamp}</p>
                  <p className="text-xs font-bold text-slate-100 uppercase tracking-tight">{entry.action}: {entry.resource}</p>
                  <p className="text-[10px] text-slate-500 mt-1">Actor: <span className="text-slate-300">{entry.actor}</span></p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="h-10 bg-slate-900/90 border-t border-white/5 px-6 flex items-center justify-between text-[10px] font-bold text-slate-500 z-50">
        <div className="flex gap-6">
          <span className="flex items-center gap-2">ENGINE: <span className="text-indigo-400">SURREALDB (SIM)</span></span>
          <span className="flex items-center gap-2">NODES: <span className="text-indigo-400">{nodes.length}</span></span>
        </div>
        <div className="flex gap-6">
          <span className="text-green-500/80 tracking-widest">ROW-LEVEL SECURITY ENFORCED</span>
          <span className="opacity-30">© 2026 FLUX-LANG BACKBONE</span>
        </div>
      </footer>
    </div>
  )
}
export default App
