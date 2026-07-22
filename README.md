# Sankalp Thakur

I run [Transient Labs](https://transientlabs.ai). Public work is industrial AI, energy systems, and auditable agents near plant systems — SCADA/PLC/OPC UA ↔ ERP/MES/PLM.

## What I've shipped

**[Transient Energy](https://github.com/sankalpsthakur/transient-energy-ems)** — fictional ISO 50001 EnMS prototype: simulator-only control, 49 browser tests. Live: [EMS](https://transient-energy-ems.onrender.com). No real equipment.

**Forge** — system-of-action demo. Live: [forgeagent.onrender.com](https://forgeagent.onrender.com).

**[Carbon](https://github.com/sankalpsthakur/carbon)** — agent + MCP toolkit for Scope 1/2/3 accounting. [`@sankalpsthakur/carbon`](https://www.npmjs.com/package/@sankalpsthakur/carbon) (`0.2.0`).

**[Scope 3 Calculation](https://github.com/sankalpsthakur/scope3-calculation)** — local MVP behind that. Baseline inventory, not finance-grade LCA.

## Still cooking

- [Scope 3 Strategy](https://github.com/sankalpsthakur/scope3-strategy) — CSRD double-materiality / LCA → ESRS
- [PlantOpsBench](https://github.com/sankalpsthakur/plantopsbench) — stub Inspect AI evals for plant-ops decisions
- [Plugins](https://github.com/sankalpsthakur/plugins) — Claude plugins for Scope 3 + delivery

## How things connect

A [poker sim note on X](https://x.com/sankalpsthakur/status/1888895644628087220) (predictable strategies lose under imperfect info) grew into [`games`](https://github.com/sankalpsthakur/games) — 18 game-theoretic environments, same idea, wider harness.

I've been a contributor to pymodbus, opcua-asyncio, FlexMeasures, and electricitymaps-contrib.

## Classical ↔ quantum

Energy flexibility and intervention choice are binary optimization problems — MIP in production today. The same QUBO can run through Qiskit QAOA on IBM Runtime for a side-by-side comparison. Classical stays the production path; quantum is just another solver behind the same interface. I'm exploring that bridge, not claiming advantage.

Experiments I'm interested in:

- Small FlexMeasures-style storage schedule as QUBO; Gurobi/CBC vs QAOA (objective gap + wall time)
- Transient Energy opportunity portfolio under budget/interlocks — MIP vs QAOA, same harness
- Carbon-intensity-aware load shift (Electricity Maps–style signals) as discount/shift QUBO
- Keep PlantOpsBench / agent / OT I/O paths classical; only swap the optimizer when the decision is combinatorial

## Find me

[X](https://x.com/sankalpsthakur) · [LinkedIn](https://www.linkedin.com/in/sankalpthakur/) · [Kaggle](https://www.kaggle.com/sankalpsthakur) · [Transient Labs](https://transientlabs.ai)
