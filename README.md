# Sankalp Thakur

I build software for systems that touch the physical world.

**Industrial control · formal verification · energy systems · quantum experiments**

Currently:
- building [kiota](https://github.com/sankalpsthakur/kiota), a from-scratch Lean 4 kernel checker in Rust. Arena-validated snapshot: **116/116 valid exports accepted, 62/62 invalid exports rejected** on the attempted set.
- contributing bug fixes upstream across industrial protocols, energy systems, data infrastructure, Lean, quantum and ML.
- building safety-bounded factory software around one rule: **the cloud proposes, the operator approves, the PLC clamps, the SIS overrides.**

[Transient Labs](https://transientlabs.ai) — industrial decision AI, energy systems, portable edge inference, and agents whose evidence can be audited near real equipment.

## Start here

| Project | What it proves |
| --- | --- |
| [kiota](https://github.com/sankalpsthakur/kiota) | A Lean 4 kernel checker built from scratch in Rust; recomputes recursor invariants instead of trusting exported metadata |
| [Transient Energy EMS](https://github.com/sankalpsthakur/transient-energy-ems) · [live](https://transient-energy-ems.onrender.com) | Synthetic ISO 50001 energy-management system with simulation, M&V, benchmarking and read-only control boundaries |
| [IBM 150-variable Ising study](https://github.com/sankalpsthakur/ibm-quantum-150q-ising) | 15 IBM Heron jobs, 599 quantum seconds, mitigation ablations and an exact classical baseline — including the negative result that classical HiGHS wins this instance |
| [Mercator visualizer](https://github.com/sankalpsthakur/mercator-visualizer) | Interactive Mercator-vs-true-area map; drag landmasses and watch projection distortion disappear |
| [Pump edge-twin lab](https://huggingface.co/spaces/sankalpsthakur/forge-pump-edge-twin-lab) · [dataset](https://huggingface.co/datasets/sankalpsthakur/forge-pump-digital-twin-synthetic) | 40k-row clean-room digital twin with PyTorch → ONNX/TensorFlow/LiteRT parity and browser inference |
| [FactoryOS / Forge demo](https://forgeagent.onrender.com) | Human-agent collaboration, plant telemetry, authenticated approvals and bounded policy proposals; no commissioned PLC control |

Render demos sleep when idle; first load can take a minute.

## Open source

[![upstream merged PRs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fissues%3Fq%3Dtype%3Apr%2Bauthor%3Asankalpsthakur%2Bis%3Amerged%2B-user%3Asankalpsthakur&query=%24.total_count&label=upstream%20merged%20PRs&color=1f6feb&style=flat-square&cacheSeconds=3600)](https://github.com/search?q=is%3Apr+author%3Asankalpsthakur+is%3Amerged+-user%3Asankalpsthakur&type=pullrequests)

I prefer small upstream fixes with a concrete failure mode, a regression test and evidence that the change actually solves the bug.

| Domain | Upstream repositories with merged contributions |
| --- | --- |
| Industrial protocols / SCADA / MES | [pymodbus](https://github.com/pymodbus-dev/pymodbus) · [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio) · [FUXA](https://github.com/frangoteam/FUXA) · [OpenMes](https://github.com/Mes-Open/OpenMes) · [thin-edge.io](https://github.com/thin-edge/thin-edge.io) |
| Energy / climate | [FlexMeasures](https://github.com/FlexMeasures/flexmeasures) · [Electricity Maps](https://github.com/electricitymaps/electricitymaps-contrib) · [CodeCarbon](https://github.com/mlco2/codecarbon) · [Home Assistant](https://github.com/home-assistant/core) |
| Data infrastructure | [clickhouse-connect](https://github.com/ClickHouse/clickhouse-connect) · [dbt-clickhouse](https://github.com/ClickHouse/dbt-clickhouse) · [mcp-clickhouse](https://github.com/ClickHouse/mcp-clickhouse) · [clickhouse-go](https://github.com/ClickHouse/clickhouse-go) · [influxdb-client-python](https://github.com/influxdata/influxdb-client-python) · [kagglehub](https://github.com/Kaggle/kagglehub) |
| Formal methods / quantum / ML | [Lean 4](https://github.com/leanprover/lean4) · [Lean Kernel Arena](https://github.com/leanprover/lean-kernel-arena) · [physlib](https://github.com/leanprover-community/physlib) · [Mitiq](https://github.com/unitaryfoundation/mitiq) · [Cirq](https://github.com/quantumlib/Cirq) · [TensorFlow](https://github.com/tensorflow/tensorflow) |
| Platform / tooling | [Svelte](https://github.com/sveltejs/svelte) · [coreutils](https://github.com/uutils/coreutils) · [LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) · [quicklink](https://github.com/GoogleChromeLabs/quicklink) · [docker-library/docs](https://github.com/docker-library/docs) |

## How I work

**Replay first. Verify invariants independently. Keep safety in the PLC/SIS. Publish negative results.**

That applies whether the system is an industrial control loop, a kernel checker or a quantum experiment. Optimizers, agents and accelerators can propose; independent checks decide what is trustworthy.

## Find me

[Hugging Face](https://huggingface.co/sankalpsthakur) · [Kaggle](https://www.kaggle.com/sankalpsthakur) · [LinkedIn](https://www.linkedin.com/in/sankalpthakur/) · [X](https://x.com/sankalpsthakur) · [Transient Labs](https://transientlabs.ai)
