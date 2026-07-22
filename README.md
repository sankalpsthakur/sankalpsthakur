# Sankalp Thakur

I run [Transient Labs](https://transientlabs.ai). Most of my public work sits around industrial AI, energy systems, and making agent workflows auditable enough that you'd trust them near a plant — SCADA/PLC/OPC UA on one side, ERP/MES/PLM on the other.

What follows is stuff you can actually open. Demos and toolkits, not claims about live plants.

## What I've shipped

**[Transient Energy](https://github.com/sankalpsthakur/transient-energy-ems)** is a fictional ISO 50001 energy-management prototype for a made-up site called Nordhaven. Browser UI, simulator-only control plane, 49 browser tests, [live demo](https://transient-energy-ems.onrender.com). Nothing here talks to real equipment — that's intentional.

**[Carbon](https://github.com/sankalpsthakur/carbon)** is an agent + MCP toolkit for Scope 1/2/3 accounting. On npm as [`@sankalpsthakur/carbon`](https://www.npmjs.com/package/@sankalpsthakur/carbon) (`0.2.0`).

**[Scope 3 Calculation](https://github.com/sankalpsthakur/scope3-calculation)** is the local MVP behind that: ingest → factor mapping → data-quality scoring → versioned runs, approvals, restatements. Baseline inventory work, not finance-grade LCA.

## Still cooking

- [Scope 3 Strategy](https://github.com/sankalpsthakur/scope3-strategy) — CSRD double-materiality / LCA → ESRS direction
- [PlantOpsBench](https://github.com/sankalpsthakur/plantopsbench) — stub Inspect AI evals for plant-ops decisions (synthetic vignettes only)
- [Plugins](https://github.com/sankalpsthakur/plugins) — Claude plugins for the Scope 3 stack plus delivery workflows

## How things connect

I wrote about a small [poker simulation on X](https://x.com/sankalpsthakur/status/1888895644628087220) in Feb 2025 — three cards, bet/check/call/fold, fixed opponent policy, a few RL methods. That thread did better than most of my posts (~15k views), mostly because the point was concrete: predictable strategies lose under imperfect information.

That experiment grew into [`games`](https://github.com/sankalpsthakur/games): 18 game-theoretic environments (poker included), PPO/A2C/DQN, mock video tells, opponent profiling, multi-seed significance. Same idea, wider harness.

The Scope 3 line ([carbon](https://github.com/sankalpsthakur/carbon) → [calculation](https://github.com/sankalpsthakur/scope3-calculation) → [strategy](https://github.com/sankalpsthakur/scope3-strategy)) is the same pattern on a different problem: agents are useful only if the trail is versioned and reviewable.

## Find me

[X](https://x.com/sankalpsthakur) · [LinkedIn](https://www.linkedin.com/in/sankalpthakur/) · [Kaggle](https://www.kaggle.com/sankalpsthakur) · [Scalematics](https://scalematics.substack.com/) · [Transient Labs](https://transientlabs.ai)
