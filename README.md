sankalp thakur

i run transient labs.

the public work lives in the gap between the plant floor and the rest of the company: industrial ai, energy systems, and agents that have to be auditable near real equipment.

scada / plc / opc ua still speak one language.  
erp / mes / plm speak another.  
most days the translation is a person copying a number, then joining a call to explain why it changed.  
we call it process. it is usually just a bug with a salary.

## what i have shipped

[transient energy](https://github.com/sankalpsthakur/transient-energy-ems)  
iso 50001 enms prototype. simulator-backed control path. 49 browser tests.  
live: [ems](https://transient-energy-ems.onrender.com). some sections still under nda.

forge  
system-of-action demo.  
live: [forgeagent.onrender.com](https://forgeagent.onrender.com)

[carbon](https://github.com/sankalpsthakur/carbon)  
agent + mcp toolkit for scope 1/2/3.  
[@sankalpsthakur/carbon](https://www.npmjs.com/package/@sankalpsthakur/carbon) (0.2.0)

[scope 3 calculation](https://github.com/sankalpsthakur/scope3-calculation)  
the local mvp behind it. baseline inventory. not finance-grade lca.

## still cooking

[scope 3 strategy](https://github.com/sankalpsthakur/scope3-strategy) — csrd double-materiality / lca → esrs  
[plantopsbench](https://github.com/sankalpsthakur/plantopsbench) — stub inspect ai evals for plant-ops decisions  
[plugins](https://github.com/sankalpsthakur/plugins) — claude plugins for scope 3 + delivery

## how things connect

a few years ago a [simple poker simulation](https://x.com/sankalpsthakur/status/1888895644628087220) showed something obvious once you see it: any predictable strategy loses under imperfect information.  
that note grew into [games](https://github.com/sankalpsthakur/games) eighteen game-theoretic environments that keep testing the same idea with a wider harness.

the same lesson shows up on the plant floor.  
meters that nobody fully trusts. spreadsheets built by someone who left in 2022. finance, controls, and operations that rarely agree on one baseline.  
decarbonisation stays a pdf until those three can share the same numbers and the same control loop.

i have contributed to pymodbus, opcua-asyncio, flexmeasures, and electricitymaps-contrib. the quiet libraries that keep the lights talking to the models.

## classical ↔ quantum

energy flexibility and intervention choice are binary optimisation problems.  
mip runs in production today. the same qubo can be handed to qiskit qaoa on ibm runtime for a side-by-side look.  
classical stays the production path. quantum is just another solver behind the same interface.  
exploring the bridge. not claiming advantage.

## experiments that still interest me:

- small flexmeasures-style storage schedule as qubo: gurobi/cbc vs qaoa (objective gap + wall time)
- transient energy opportunity portfolio under budget and interlocks — same harness
- carbon-intensity-aware load shift (electricity maps style signals) as discount/shift qubo
- keep plantopsbench, the agents, and the ot i/o classical; only swap the optimiser when the decision is combinatorial

the work is ordinary in the best sense.  
baselines that survive contact with production. agents that can be audited. handoffs that no longer need a human salary to stay honest.

## find me

[x](https://x.com/sankalpsthakur) · [linkedin](https://www.linkedin.com/in/sankalpthakur/) · [kaggle](https://www.kaggle.com/sankalpsthakur) · [transient labs](https://transientlabs.ai)
