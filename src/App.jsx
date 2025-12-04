// src/App.jsx
import { useState } from 'react'
import './App.css'

const API_BASE = 'http://localhost:5000/api'

function App() {
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleRequest = async (fn) => {
    setLoading(true)
    setError('')
    setResult('')
    try {
      const data = await fn()
      setResult(JSON.stringify(data, null, 2))
    } catch (err) {
      console.error(err)
      setError(err.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  // ---- BUTTON HANDLERS ----

  const addPlayer = () =>
    handleRequest(async () => {
      const name = window.prompt('Player name?')
      if (!name) throw new Error('Cancelled')
      const height = window.prompt('Height (inches)?')
      const weight = window.prompt('Weight (lbs)?')
      const age = window.prompt('Age?')
      const position = window.prompt('Position (e.g. PG, SG, SF, PF, C)?')
      const teamId = window.prompt('TeamID?')

      const res = await fetch(`${API_BASE}/player`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          height,
          weight,
          age,
          position,
          team_id: teamId,
        }),
      })
      if (!res.ok) throw new Error('Failed to add player')
      return await res.json()
    })

  const addTeam = () =>
    handleRequest(async () => {
      const name = window.prompt('Team name?')
      const city = window.prompt('City?')
      const division = window.prompt('Division?')
      const conference = window.prompt('Conference?')

      const res = await fetch(`${API_BASE}/team`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, city, division, conference }),
      })
      if (!res.ok) throw new Error('Failed to add team')
      return await res.json()
    })

  const updatePlayer = () =>
    handleRequest(async () => {
      const playerId = window.prompt('PlayerID to update?')
      const column = window.prompt('Column to update (Name, Height, Weight, Age, Position, TeamID)?')
      const newValue = window.prompt('New value?')

      const res = await fetch(`${API_BASE}/player`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_id: playerId, column, new_value: newValue }),
      })
      if (!res.ok) throw new Error('Failed to update player')
      return await res.json()
    })

  const updateTeam = () =>
    handleRequest(async () => {
      const teamId = window.prompt('TeamID to update?')
      const column = window.prompt('Column to update (Name, City, Division, Conference)?')
      const newValue = window.prompt('New value?')

      const res = await fetch(`${API_BASE}/team`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ team_id: teamId, column, new_value: newValue }),
      })
      if (!res.ok) throw new Error('Failed to update team')
      return await res.json()
    })

  const searchTeam = () =>
    handleRequest(async () => {
      const teamName = window.prompt('Team name?')
      const res = await fetch(`${API_BASE}/team/roster?team_name=${encodeURIComponent(teamName)}`)
      if (!res.ok) throw new Error('Failed to get team roster')
      return await res.json()
    })

  const searchPlayerName = () =>
    handleRequest(async () => {
      const name = window.prompt('Player name?')
      const res = await fetch(`${API_BASE}/player/search?name=${encodeURIComponent(name)}`)
      if (!res.ok) throw new Error('Failed to get player')
      return await res.json()
    })

  const searchTeamPlayersByPosition = () =>
    handleRequest(async () => {
      const teamName = window.prompt('Team name?')
      const position = window.prompt('Position (PG, SG, SF, PF, C)?')
      const res = await fetch(
        `${API_BASE}/team/players-by-position?team_name=${encodeURIComponent(
          teamName
        )}&position=${encodeURIComponent(position)}`
      )
      if (!res.ok) throw new Error('Failed to get players by position')
      return await res.json()
    })

  const logPlayerGame = () =>
    handleRequest(async () => {
      const gameId = window.prompt('GameID?')
      const playerId = window.prompt('PlayerID?')
      const points = window.prompt('Points?')
      const rebounds = window.prompt('Rebounds?')
      const assists = window.prompt('Assists?')

      const res = await fetch(`${API_BASE}/player/log-game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, player_id: playerId, points, rebounds, assists }),
      })
      if (!res.ok) throw new Error('Failed to log game')
      return await res.json()
    })

  const topPoints = () =>
    handleRequest(async () => {
      const res = await fetch(`${API_BASE}/players/top/points`)
      if (!res.ok) throw new Error('Failed to get top scorers')
      return await res.json()
    })

  const topAssists = () =>
    handleRequest(async () => {
      const res = await fetch(`${API_BASE}/players/top/assists`)
      if (!res.ok) throw new Error('Failed to get top assist leaders')
      return await res.json()
    })

  const topRebounds = () =>
    handleRequest(async () => {
      const res = await fetch(`${API_BASE}/players/top/rebounds`)
      if (!res.ok) throw new Error('Failed to get top rebounders')
      return await res.json()
    })

  return (
    <>
      <h1 className='HeaderColor'>Select From the Following:</h1>
      <div>
        <ul>
          {/* This button just writes to a database */}
          <button onClick={addPlayer}>Add Player</button>
          {/* This button just writes to a database */}
          <button onClick={addTeam}>Add Team</button>
          {/* This button just writes to a database */}
          <button onClick={updatePlayer}>Update Player</button>
          {/* This button just writes to a database */}
          <button onClick={updateTeam}>Update Team</button>
          {/* This button returns the roster including coach */}
          <button onClick={searchTeam}>Search Team</button>
          {/* This button just returns the name and everything else about the player */}
          <button onClick={searchPlayerName}>Search Player Name</button>
          {/* This button just returns the players on a team with Position X */}
          <button onClick={searchTeamPlayersByPosition}>Search Team Players by Position</button>
          {/* This button writes to a database */}
          <button onClick={logPlayerGame}>Log Player Game</button>
          {/* This button just returns the names of the players */}
          <button onClick={topPoints}>Top Ten Players for Points</button>
          {/* This button just returns the names of the players */}
          <button onClick={topAssists}>Top Ten Players for Assists</button>
          {/* This button just returns the names of the players */}
          <button onClick={topRebounds}>Top Ten Players for Rebounds</button>
        </ul>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <pre
          style={{
            textAlign: 'left',
            background: '#111',
            color: '#0f0',
            padding: '1rem',
            marginTop: '1rem',
            maxHeight: '300px',
            overflow: 'auto',
          }}
        >
          {result}
        </pre>
      )}
    </>
  )
}

export default App
