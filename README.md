# Sankalp Thakur

I build the operating layer where humans and agents collaborate on industrial data — across **SCADA, PLCs, OPC UA, ERP, MES, MRP, QMS, WMS and PLM** — within the plant safety boundary.

I run [Transient Labs](https://transientlabs.ai). The public work is about industrial decision AI, energy systems, portable edge inference and agents whose evidence can be audited near real equipment.

Controls and operations still speak one language. Enterprise systems speak another. Most days the translation is a person copying a number, then joining a call to explain why it changed.

## Current proof

| Project | What it demonstrates | Boundary |
| --- | --- | --- |
| Forge · [live](https://forgeagent.onrender.com) | Human-agent collaboration, machine identities, plant telemetry, policy proposals and authenticated approvals | Software-in-the-loop; no claim of commissioned PLC control |
| [Transient Energy](https://github.com/sankalpsthakur/transient-energy-ems) · [live](https://transient-energy-ems.onrender.com) | ISO 50001 EnMS prototype, simulator-backed control path and a 49-test browser harness | Synthetic plant scenario |
| [Pump edge-twin lab](https://huggingface.co/spaces/sankalpsthakur/forge-pump-edge-twin-lab) · [dataset](https://huggingface.co/datasets/sankalpsthakur/forge-pump-digital-twin-synthetic) · [model](https://huggingface.co/sankalpsthakur/forge-pump-surrogate-multiruntime) | 40k-row clean-room digital twin, PyTorch → ONNX/TensorFlow/LiteRT parity and browser ONNX/WASM inference | Read-only PLC/SIS boundary; synthetic data |
| [Electrolyser telemetry baseline](https://huggingface.co/sankalpsthakur/forge-electrolyser-telemetry-baseline) · [replay scenarios](https://huggingface.co/datasets/sankalpsthakur/forge-industrial-control-scenarios) | Anomaly baselines, replayable telemetry and versioned agent/control traces | Methodology proof, not plant savings evidence |
| [Carbon](https://github.com/sankalpsthakur/carbon) · [npm](https://www.npmjs.com/package/@sankalpsthakur/carbon) | Agent and MCP toolkit for auditable Scope 1/2/3 workflows | Accounting workflow infrastructure, not a finance-grade LCA |
| [IBM 150-variable Ising study](https://github.com/sankalpsthakur/ibm-quantum-150q-ising) · [results](https://huggingface.co/datasets/sankalpsthakur/ibm-150q-ising-hardware-results) · [lab](https://huggingface.co/spaces/sankalpsthakur/qaoa-depth-noise-lab) | 15 jobs and 599 quantum seconds on IBM Heron, depth/noise evidence, mitigation ablation and an exact classical baseline | No quantum-advantage claim; classical HiGHS wins this instance |

Render free-tier demos sleep when idle and can take a minute to wake.

## Open source

[![upstream merged PRs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fissues%3Fq%3Dtype%3Apr%2Bauthor%3Asankalpsthakur%2Bis%3Amerged%2B-user%3Asankalpsthakur&query=%24.total_count&label=upstream%20merged%20PRs&color=1f6feb&style=flat-square&cacheSeconds=3600)](https://github.com/search?q=is%3Apr+author%3Asankalpsthakur+is%3Amerged+-user%3Asankalpsthakur&type=pullrequests)
[![open upstream PRs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fissues%3Fq%3Dtype%3Apr%2Bauthor%3Asankalpsthakur%2Bis%3Aopen%2B-user%3Asankalpsthakur&query=%24.total_count&label=open%20upstream%20PRs&color=8250df&style=flat-square&cacheSeconds=3600)](https://github.com/search?q=is%3Apr+author%3Asankalpsthakur+is%3Aopen+-user%3Asankalpsthakur&type=pullrequests)

Merged fixes upstream across industrial protocols, SCADA and MES, energy systems, database clients, edge runtimes and scientific computing. Both counters above are live queries against the GitHub search API, so they stay honest without me editing this file.

| Domain | Upstream repositories with merged work |
| --- | --- |
| Industrial protocols and control | [pymodbus](https://github.com/pymodbus-dev/pymodbus) · [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio) · [FUXA](https://github.com/frangoteam/FUXA) · [OpenMes](https://github.com/Mes-Open/OpenMes) · [thin-edge.io](https://github.com/thin-edge/thin-edge.io) |
| Energy and climate | [FlexMeasures](https://github.com/FlexMeasures/flexmeasures) · [Electricity Maps](https://github.com/electricitymaps/electricitymaps-contrib) · [CodeCarbon](https://github.com/mlco2/codecarbon) · [Home Assistant](https://github.com/home-assistant/core) |
| Data infrastructure | [clickhouse-connect](https://github.com/ClickHouse/clickhouse-connect) · [dbt-clickhouse](https://github.com/ClickHouse/dbt-clickhouse) · [mcp-clickhouse](https://github.com/ClickHouse/mcp-clickhouse) · [clickhouse-go](https://github.com/ClickHouse/clickhouse-go) · [influxdb-client-python](https://github.com/influxdata/influxdb-client-python) · [kagglehub](https://github.com/Kaggle/kagglehub) |
| Formal methods and quantum | [Lean 4](https://github.com/leanprover/lean4) · [physlib](https://github.com/leanprover-community/physlib) · [Mitiq](https://github.com/unitaryfoundation/mitiq) · [Cirq](https://github.com/quantumlib/Cirq) |
| Platform and tooling | [Svelte](https://github.com/sveltejs/svelte) · [uutils/coreutils](https://github.com/uutils/coreutils) · [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) · [quicklink](https://github.com/GoogleChromeLabs/quicklink) · [docker-library/docs](https://github.com/docker-library/docs) |

A few representative merges:

- [pymodbus #2971](https://github.com/pymodbus-dev/pymodbus/pull/2971) — fix synchronous response timeout on continuous garbage
- [opcua-asyncio #2002](https://github.com/FreeOpcUa/opcua-asyncio/pull/2002) — fix `XmlImporter._sort_nodes` hang on Type-class TypeDefinition cycles
- [FlexMeasures #2345](https://github.com/FlexMeasures/flexmeasures/pull/2345) — keep explicit zero directional capacity hard under relax-constraints
- [Home Assistant #177925](https://github.com/home-assistant/core/pull/177925) — migrate `growatt_server` off `hass.data[DOMAIN]`
- [Electricity Maps #8797](https://github.com/electricitymaps/electricitymaps-contrib/pull/8797) — add v4 demand-based `fetch_consumption` for OpenNEM
- [Svelte #18625](https://github.com/sveltejs/svelte/pull/18625) — skip controlled each fast path while another batch is pending
- [coreutils #13651](https://github.com/uutils/coreutils/pull/13651) — `fmt`: measure `-w` in UTF-8 bytes to match GNU

[Browse every merged upstream PR →](https://github.com/search?q=is%3Apr+author%3Asankalpsthakur+is%3Amerged+-user%3Asankalpsthakur&type=pullrequests)

## Public activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=sankalpsthakur&hide_border=true&area=true&bg_color=00000000&color=c9d1d9&line=58a6ff&point=f0f6fc&area_color=1f6feb&custom_title=Public%20contribution%20activity">
  <img alt="Sankalp Thakur's live public contribution activity" src="https://github-readme-activity-graph.vercel.app/graph?username=sankalpsthakur&hide_border=true&area=true&bg_color=00000000&color=24292f&line=0969da&point=1f2328&area_color=54aeff&custom_title=Public%20contribution%20activity">
</picture>

## How the work connects

Meters are disputed. Spreadsheets outlive their authors. Finance, controls and operations rarely agree on one baseline. This is an attempt to build the factory operating system.

The production path stays classical and bounded: replay first, verify invariants independently, keep safety in the PLC/SIS, and require an operator before any consequential action. ONNX, TensorFlow, PyTorch, CUDA and quantum accelerators are implementation choices behind that.

## Find me

[Hugging Face](https://huggingface.co/sankalpsthakur) · [Kaggle](https://www.kaggle.com/sankalpsthakur) · [LinkedIn](https://www.linkedin.com/in/sankalpthakur/) · [X](https://x.com/sankalpsthakur) · [Transient Labs](https://transientlabs.ai)
