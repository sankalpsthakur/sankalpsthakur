# Sankalp Thakur

i build software for systems that touch the physical world.

building the operating layer(factoryOS) where humans and agents collaborate around factory operations on industrial data {SCADA, PLCs, OPC UA, ERP, MES, MRP, QMS, WMS, PLM}. control systems and enterprise systems speak different languages. today the translation is still often a person copying a number, then joining a call to explain why

[Transient Labs](https://transientlabs.ai) — industrial decision AI, energy systems, portable edge inference, and agents whose evidence can be audited near real equipment.

## Projects

| Project | Functionality | Bounds |
| --- | --- | --- |
| [kiota](https://github.com/sankalpsthakur/kiota) | from-scratch Lean 4 kernel checker in Rust; Arena-pinned revision: **116/116 good accepted, 62/62 bad rejected** | experimental; mathlib benchmark pending |
| Forge · [live](https://forgeagent.onrender.com) | Human-agent collaboration, machine identities, plant telemetry, policy proposals, authenticated approvals | Software-in-the-loop; no commissioned PLC control |
| [Transient Energy](https://github.com/sankalpsthakur/transient-energy-ems) · [live](https://transient-energy-ems.onrender.com) | energy-management system {ISO 50001}, simulator-backed control path, 49-test browser harness | Synthetic plant scenario |
| [Pump edge-twin lab](https://huggingface.co/spaces/sankalpsthakur/forge-pump-edge-twin-lab) · [dataset](https://huggingface.co/datasets/sankalpsthakur/forge-pump-digital-twin-synthetic) · [model](https://huggingface.co/sankalpsthakur/forge-pump-surrogate-multiruntime) | 40k-row clean-room twin, browser inference across {PyTorch, ONNX, TensorFlow, LiteRT} | Read-only {PLC, SIS} boundary; synthetic data |
| [Electrolyser baseline](https://huggingface.co/sankalpsthakur/forge-electrolyser-telemetry-baseline) · [replay scenarios](https://huggingface.co/datasets/sankalpsthakur/forge-industrial-control-scenarios) | Anomaly baselines, replayable telemetry, versioned agent/control traces | Methodology proof, not plant savings evidence |
| [Carbon](https://github.com/sankalpsthakur/carbon) · [npm](https://www.npmjs.com/package/@sankalpsthakur/carbon) | Agent and MCP toolkit for auditable Scope 1/2/3 workflows | Workflow infrastructure, not finance-grade LCA |
| [Game theory simulations](https://github.com/sankalpsthakur/games) | 18 games × {PPO, A2C, DQN}, 30-seed evaluation, behavioral-signal/tell sensitivity | Deterministic synthetic environments; not evidence about real human behaviour |
| [IBM 150-variable Ising study](https://github.com/sankalpsthakur/ibm-quantum-150q-ising) · [results](https://huggingface.co/datasets/sankalpsthakur/ibm-150q-ising-hardware-results) · [lab](https://huggingface.co/spaces/sankalpsthakur/qaoa-depth-noise-lab) | 15 jobs, 599 quantum seconds on IBM Heron, depth/noise evidence, mitigation ablation, exact classical baseline | No quantum-advantage claim; classical HiGHS wins this instance |

render demos sleep when idle; first load can take a minute.

## Open source

[![upstream merged PRs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fissues%3Fq%3Dtype%3Apr%2Bauthor%3Asankalpsthakur%2Bis%3Amerged%2B-user%3Asankalpsthakur&query=%24.total_count&label=upstream%20merged%20PRs&color=1f6feb&style=flat-square&cacheSeconds=3600)](https://github.com/search?q=is%3Apr+author%3Asankalpsthakur+is%3Amerged+-user%3Asankalpsthakur&type=pullrequests)


repositories with merged contributions:

| Domain | Upstream |
| --- | --- |
| Industrial systems {SCADA, MES} | [pymodbus](https://github.com/pymodbus-dev/pymodbus) · [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio) · [FUXA](https://github.com/frangoteam/FUXA) · [OpenMes](https://github.com/Mes-Open/OpenMes) · [thin-edge.io](https://github.com/thin-edge/thin-edge.io) |
| Energy and climate | [FlexMeasures](https://github.com/FlexMeasures/flexmeasures) · [Electricity Maps](https://github.com/electricitymaps/electricitymaps-contrib) · [CodeCarbon](https://github.com/mlco2/codecarbon) · [Home Assistant](https://github.com/home-assistant/core) |
| Data infrastructure | [clickhouse-connect](https://github.com/ClickHouse/clickhouse-connect) · [dbt-clickhouse](https://github.com/ClickHouse/dbt-clickhouse) · [mcp-clickhouse](https://github.com/ClickHouse/mcp-clickhouse) · [clickhouse-go](https://github.com/ClickHouse/clickhouse-go) · [influxdb-client-python](https://github.com/influxdata/influxdb-client-python) · [kagglehub](https://github.com/Kaggle/kagglehub) |
| Formal methods, quantum, ML | [Lean 4](https://github.com/leanprover/lean4) · [Lean Kernel Arena](https://github.com/leanprover/lean-kernel-arena) · [physlib](https://github.com/leanprover-community/physlib) · [Mitiq](https://github.com/unitaryfoundation/mitiq) · [Cirq](https://github.com/quantumlib/Cirq) · [TensorFlow](https://github.com/tensorflow/tensorflow) |
| Platform, tooling | [Svelte](https://github.com/sveltejs/svelte) · [coreutils](https://github.com/uutils/coreutils) · [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) · [quicklink](https://github.com/GoogleChromeLabs/quicklink) · [docker-library/docs](https://github.com/docker-library/docs) |

## Public activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=sankalpsthakur&hide_border=true&area=true&bg_color=00000000&color=c9d1d9&line=58a6ff&point=f0f6fc&area_color=1f6feb&custom_title=Public%20contribution%20activity">
  <img alt="Sankalp Thakur's live public contribution activity" src="https://github-readme-activity-graph.vercel.app/graph?username=sankalpsthakur&hide_border=true&area=true&bg_color=00000000&color=24292f&line=0969da&point=1f2328&area_color=54aeff&custom_title=Public%20contribution%20activity">
</picture>

## How everything connects

meter data is conflicted, faults propogate through subsystems, spreadsheets outlive their authors. finance, controls and operations rarely agree. this is an attempt to build the factory operating system.

the path is classical and bounded: replay first, verify invariants independently, keep safety in {PLC, SIS}, require an operator before any consequential action. implementation details {ONNX, TensorFlow, PyTorch, CUDA, quantum accelerators} stay behind that boundary.

## Reach out/Find me

[Hugging Face](https://huggingface.co/sankalpsthakur) · [Kaggle](https://www.kaggle.com/sankalpsthakur) · [LinkedIn](https://www.linkedin.com/in/sankalpthakur/) · [X](https://x.com/sankalpsthakur) · [Transient Labs](https://transientlabs.ai)
