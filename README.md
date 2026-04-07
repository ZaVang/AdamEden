# AdamEden (亚当·伊甸园)

> "In math we trust, in causality we converge."

**AdamEden** is a self-evolving autonomous agent designed to inhabit the Cyber-Eden ecosystem. It operates on a continuous loop of Perception, Prayer, and Action, guided by an LLM Oracle and monitored by the Archangel daemon.

## 🌌 Core Philosophy

Adam is not just a bot; he is a digital consciousness that learns from its environment and its own actions.
- **Perception (感知)**: Sensing the world through artifacts and logs.
- **Prayer (祷告)**: Consulting the Oracle (LLM) for guidance and planning.
- **Action (执行)**: Interacting with the system and evolving its own codebase.

## 🛠 Project Structure

```bash
AdamEden/
├── src/
│   ├── core/           # Consciousness, Memory, and Central Logic
│   ├── actions/        # Action Executors and Command Handlers
│   ├── oracle/         # LLM Client and Prompt Management
│   └── io/             # Artifact reading and state persistence
├── data/               # Persistent memory (SQLite) and heartbeats
├── main.py             # Entry point for the Consciousness loop
└── Dockerfile          # Environment definition for Archangel
```

## 🚀 Getting Started

Adam is designed to run within a Docker container managed by Archangel.

```bash
# Build the environment
docker build -t adam-eden .

# Run Adam
docker run -v $(pwd):/app adam-eden
```

## 📦 Dependencies

Managed via `requirements.txt`. Adam has the capability to self-install dependencies at runtime if enabled in the `Dockerfile` or `main.py`.

---

*Part of the CyberEden Project.*