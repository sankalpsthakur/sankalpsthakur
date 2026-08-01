# Sankalp Thakur

I build the operating layer where humans and agents turn industrial data into governed action — across **SCADA, PLCs, OPC UA, ERP, MES and PLM** — without crossing the plant safety boundary.

I run [Transient Labs](https://transientlabs.ai). The public work is about industrial decision AI, energy systems, portable edge inference and agents whose evidence can be audited near real equipment.

Controls and operations still speak one language. Enterprise systems speak another. Most days the translation is a person copying a number, then joining a call to explain why it changed. We call it process. It is usually just a bug with a salary.

## Current proof

| Artifact | What it demonstrates | Boundary |
| --- | --- | --- |
| [Forge](https://forgeagent.onrender.com) | Human-agent collaboration, machine identities, plant telemetry, policy proposals and authenticated approvals | Software-in-the-loop; no claim of commissioned PLC control |
| [Transient Energy](https://github.com/sankalpsthakur/transient-energy-ems) · [live](https://transient-energy-ems.onrender.com) | ISO 50001 EnMS prototype, simulator-backed control path and 49 browser tests | Synthetic plant scenario |
| [Pump edge-twin lab](https://huggingface.co/spaces/sankalpsthakur/forge-pump-edge-twin-lab) · [dataset](https://huggingface.co/datasets/sankalpsthakur/forge-pump-digital-twin-synthetic) · [model](https://huggingface.co/sankalpsthakur/forge-pump-surrogate-multiruntime) | 40k-row clean-room digital twin, PyTorch → ONNX/TensorFlow/LiteRT parity and browser ONNX/WASM inference | Read-only PLC/SIS boundary; synthetic data |
| [Electrolyser telemetry baseline](https://huggingface.co/sankalpsthakur/forge-electrolyser-telemetry-baseline) · [replay scenarios](https://huggingface.co/datasets/sankalpsthakur/forge-industrial-control-scenarios) | Anomaly baselines, replayable telemetry and versioned agent/control traces | Methodology proof, not plant savings evidence |
| [Carbon](https://github.com/sankalpsthakur/carbon) · [npm](https://www.npmjs.com/package/@sankalpsthakur/carbon) | Agent and MCP toolkit for auditable Scope 1/2/3 workflows | Accounting workflow infrastructure, not a finance-grade LCA |
| [IBM 150-qubit Ising study](https://huggingface.co/datasets/sankalpsthakur/ibm-150q-ising-hardware-results) · [lab](https://huggingface.co/spaces/sankalpsthakur/qaoa-depth-noise-lab) | Hardware execution, depth/noise evidence, mitigation ablation and exact classical comparison | No quantum-advantage claim; classical HiGHS wins this instance |

## Open source

I contribute fixes and tests upstream across industrial protocols, energy systems, databases, edge runtimes and scientific computing — including pymodbus, opcua-asyncio, FlexMeasures, Electricity Maps, ClickHouse, Home Assistant, ExecuTorch, Qiskit and PennyLane.

[Browse merged contributions →](https://github.com/pulls?q=is%3Apr+author%3Asankalpsthakur+is%3Amerged)

## Public activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=sankalpsthakur&hide_border=true&area=true&bg_color=00000000&color=c9d1d9&line=58a6ff&point=f0f6fc&area_color=1f6feb&custom_title=Public%20contribution%20activity">
  <img alt="Sankalp Thakur's live public contribution activity" src="https://github-readme-activity-graph.vercel.app/graph?username=sankalpsthakur&hide_border=true&area=true&bg_color=00000000&color=24292f&line=0969da&point=1f2328&area_color=54aeff&custom_title=Public%20contribution%20activity">
</picture>

## How the work connects

Meters are disputed. Spreadsheets outlive their authors. Finance, controls and operations rarely agree on one baseline. Decarbonisation stays a PDF until those systems can share the same state, constraints and audit trail.

The production path stays classical and bounded: replay first, verify invariants independently, keep safety in the PLC/SIS, and require an operator before any consequential action. ONNX, TensorFlow, PyTorch, CUDA and quantum accelerators are implementation choices behind that contract — not reasons to weaken it.

## Find me

[Hugging Face](https://huggingface.co/sankalpsthakur) · [Kaggle](https://www.kaggle.com/sankalpsthakur) · [LinkedIn](https://www.linkedin.com/in/sankalpthakur/) · [X](https://x.com/sankalpsthakur) · [Transient Labs](https://transientlabs.ai)
