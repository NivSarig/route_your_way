# Route Your Way — Onboarding Guide

**Audience**: Nir Radian (and Bo Jensen on the optimization side)
**Maintained by**: Niv

---

## What This Project Is

**Route Your Way** is an interactive web game that challenges users to beat the Optibus optimization algorithm at the Traveling Salesman Problem (TSP). Players are shown a map with a set of bus stops in a real city and must click them in an order they think minimizes total walking distance. The backend simultaneously runs Concorde (a world-class TSP solver) and compares results on a live leaderboard.

It's an engaging demo/educational tool that showcases Optibus's optimization capabilities.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│              Frontend (React/TypeScript)                         │
│  CreateGamePage  →  MapWithPolyline  →  LeadingBoard            │
│  @react-google-maps, MUI, React Router v6                       │
└─────────────────────────┬────────────────────────────────────────┘
                          │ HTTP REST  (CORS open)
┌─────────────────────────▼────────────────────────────────────────┐
│              Backend (FastAPI / Python)                          │
│  app.py (endpoints)  →  game.py (in-memory state)               │
│                                                                   │
│  On game creation, a background task runs:                      │
│    optimization_engine_utils.py                                  │
│      → gmaps_integration_utils.py  (Google Maps Directions API) │
│      → optimization_engine/solve_tsp.py  (Concorde via pyconcorde)│
└──────────────────────────────────────────────────────────────────┘
```

**No database.** All game state is held in a Python dict in memory — server restart loses all games.

**Production URL**: `http://route-your-way.ops-optibus.com:8000`

---

## Repository Layout

```
route_your_way/
├── frontend4.0/                  # React TypeScript app (Create React App)
│   └── src/
│       ├── App.tsx               # Route definitions
│       ├── CreateGamePage.tsx    # Landing + city picker
│       ├── MapWithPolyline.tsx   # Main gameplay map
│       ├── LeadingBoard.tsx      # Results / leaderboard
│       ├── Marker.tsx            # Custom map pin
│       ├── Polyline.tsx          # Route line renderer
│       └── backend.ts            # Backend URL constant
│
├── server/
│   ├── app.py                    # FastAPI endpoints
│   ├── game.py                   # Game state + orchestration
│   ├── locations.py              # Pre-defined city stop coordinates
│   ├── utils.py                  # Misc helpers
│   ├── requirements.txt
│   └── up.sh                     # uvicorn launcher
│
├── external_integrations/
│   ├── gmaps_integration_utils.py        # Google Maps Directions API calls + caching
│   ├── optimization_engine_utils.py      # Full TSP pipeline (matrix → Concorde → result)
│   └── optimization_engine/
│       ├── solve_tsp.py                  # pyconcorde CLI wrapper
│       └── convert_oriblem.py            # ATSP → symmetric TSP helper
│
├── google_cache_path/            # File-based cache for Google Maps API responses
├── London/, Tel_Aviv/, Paris/... # Per-city cached TSP data / test artifacts
├── main_script.py                # Benchmarking / manual testing harness
├── tsp_model_solver.py           # Experimental GLPK solver (incomplete/unused)
├── logging_utils.py              # Logging (currently disabled)
└── utils/process_utils.py        # Subprocess wrappers
```

---

## Running the Project Locally

### Backend

```bash
cd server
pip install -r requirements.txt
# Set env vars
export NIV_PRIVATE_GOOGLE_MAP_API_TOKEN=<your-gmaps-key>
bash up.sh   # runs: uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend4.0
npm install
# Create .env with your Maps key:
echo "REACT_APP_GOOGLE_MAPS_API_KEY=<key>" > .env
npm start    # dev server on http://localhost:3000
```

Switch the backend URL between prod and localhost in `frontend4.0/src/backend.ts`.

---

## Available Cities

Defined in `server/locations.py` — each is a list of [lat, lng] coordinates for ~9 bus stops:

- London
- Tel Aviv
- New York
- San Francisco
- Paris (recently added; had API issues during development)

Adding a new city = add a new entry in `locations.py`.

---

## REST API

All endpoints on port 8000.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check |
| `PUT`  | `/game?location={city}&random=false` | Create game, triggers background solve |
| `PUT`  | `/game/{id}/contestant?name={name}` | Register a player |
| `GET`  | `/game/{id}` | Poll game state (frontend polls every 3 s) |
| `PUT`  | `/game/{id}/submit?name={name}` | Submit player's stop ordering |
| `PUT`  | `/game/{id}/done` | Mark game finished |

### Game State Shape

```json
{
  "game_id": "ABCD",
  "location": { "name": "London", "coordinates": [[lat, lng], ...] },
  "status": "running | done",
  "solution": {
    "url": "https://maps.google.com/...",
    "distance": 3.14,
    "duration": "00:42:00",
    "coordinates": [[lat, lng], ...]
  },
  "contestants": {
    "Alice": {
      "name": "Alice",
      "status": "done",
      "distance": 4.2,
      "duration": "00:55:00",
      "coordinates": [[lat, lng], ...]
    }
  }
}
```

---

## Optimization Backend (Bo Jensen's Domain)

### The Problem

Route stops form an **Asymmetric TSP (ATSP)**: walking A→B takes different time than B→A (one-way streets, elevation, etc.). The goal is an *open* route (start at stop 1, end at last stop, no return).

### Full Pipeline (`optimization_engine_utils.py`)

```
coordinates list (N stops)
        │
        ▼
1. Build NxN duration matrix
   gmaps_integration_utils.get_duration_matrix()
   - Calls Google Maps Directions API in walking mode
   - Each (origin, destination) pair fetched and cached on disk
   - Cache key = "{origin_lat}_{origin_lng}_{dest_lat}_{dest_lng}"
        │
        ▼
2. Convert ATSP → Symmetric TSP  (Jonker-Volgenant 1983)
   optimization_engine_utils.convert_asymmetric_to_symmetric()
   - Doubles nodes: N → 2N   (city_i + dummy_i)
   - Symmetric cost matrix:
       [ INF  | C^T ]
       [  C   | INF ]
   - Large INF penalties prevent traveling between dummy nodes
        │
        ▼
3. Add auxiliary start/end nodes (open route, not circular)
   - From start: cost 0 to every city
   - Every city to end: cost 0
   - Start→end cross-over: prohibitive cost
        │
        ▼
4. Solve with Concorde (world-class exact TSP solver)
   optimization_engine/solve_tsp.py
   - Serializes problem to TSPLIB 95 format
   - Calls pyconcorde Python bindings
   - Returns tour as index sequence
        │
        ▼
5. Transform solution back to original N-stop ordering
   - Strip dummy nodes
   - Remove auxiliary start/end
   - Validate all original stops present
        │
        ▼
6. Build Google Maps URL + compute distance/duration
   gmaps_integration_utils.build_google_maps_url()
```

### Key Source Files for Optimization

| File | Responsibility |
|------|---------------|
| `external_integrations/optimization_engine_utils.py` | Full pipeline, matrix building, ATSP conversion, result mapping |
| `external_integrations/optimization_engine/solve_tsp.py` | Concorde wrapper — takes cost matrix, returns tour |
| `external_integrations/optimization_engine/convert_oriblem.py` | ATSP-to-symmetric conversion utility |
| `external_integrations/gmaps_integration_utils.py` | Google Maps API calls, file-based caching, URL generation |
| `main_script.py` | Standalone benchmarking; also includes brute-force O(N!) validator |

### Brute-Force Validator

`main_script.py` contains a `brute_force_solution()` that exhaustively tries all permutations. Only practical for ≤10 stops but useful for asserting that Concorde's answer is optimal.

### Caching

- **Google Maps responses** cached at `google_cache_path/<origin>_<dest>` (one file per pair)
- **Corruption handling** added after a Paris incident: if a cache file is unreadable, re-fetch from API
- TSP solved results are also written per-city so repeat runs skip the solver

---

## Frontend Details

### User Flow

1. **CreateGamePage** — user picks a city → `PUT /game` → navigate to `/map?game_id=ABCD`
2. **MapWithPolyline** — numbered bus stop markers on Google Map; user clicks in preferred order; pink polyline drawn; real-time distance/duration shown; Submit enabled only when all stops selected
3. **LeadingBoard** — polls `GET /game/{id}` every 3 s; shows algorithm row first then players sorted by distance

### Marker Colors

- Grey = unselected stop
- Pink (#FF2C95) = selected; route polyline is the same pink

### State

All via React hooks (`useState`, `useCallback`, `useEffect`). No Redux or global store — state lives in components and is re-fetched from backend as needed.

---

## Known Issues / Gotchas

- **No persistence**: Restarting the server wipes all games. A simple DB (SQLite or Redis) would fix this.
- **Paris was problematic**: Repeated issues with corrupted Google Maps cache files for Paris stops. The corruption-recovery logic was added as a fix; Paris is back in `locations.py`.
- **CORS**: Currently `allow_origins=["*"]` — fine for demo, needs tightening for production.
- **Single-process concurrency**: FastAPI runs in one process; simultaneous games share the same in-memory dict. No locking — potential race conditions if many games run at once.
- **Concorde installation**: Requires native Concorde binary + pyconcorde installed from GitHub. Not trivially pip-installable — document system deps for any new environment.

---

## Environment Variables

| Variable | Where Used | Description |
|----------|-----------|-------------|
| `NIV_PRIVATE_GOOGLE_MAP_API_TOKEN` | Backend `.env` | Google Maps Directions API key |
| `REACT_APP_GOOGLE_MAPS_API_KEY` | Frontend `.env` | Google Maps JS API key (can be same key) |
| `TSP_PATH` | Optional backend | Override path to Concorde binary |

---

## Possible Next Steps

- **Add a database** (SQLite is enough) for game persistence across restarts
- **Leaderboard across sessions** — currently each game is isolated
- **More cities** — just add coordinates to `locations.py`
- **Difficulty levels** — more/fewer stops, different cities
- **Timed mode** — force users to submit within N seconds
- **Solver performance tuning** — Concorde is exact but slow for large N; LKH3 heuristic is faster for 15+ stops
- **Replace CRA** — Create React App is deprecated; migrate to Vite

---

*Questions? Reach out to Niv or Bo Jensen for the optimization internals.*
