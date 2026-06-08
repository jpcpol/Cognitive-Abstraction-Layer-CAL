# CAL — Cognitive Abstraction Layers

**Author:** Juan Pablo Chancay · Aural Syncro  
**Pre-paper:** [DOI 10.5281/zenodo.20430343](https://doi.org/10.5281/zenodo.20430343) · arXiv pending endorsement  
**License:** CC BY-NC 4.0 (docs) · AGPL-3.0 (code in sub-repos)  
**Status:** Active research — L2 validated, L3/L4 in development

---

## What is CAL?

**Cognitive Abstraction Layers (CAL)** is a research framework that proposes a five-layer hierarchy for compressing the semantic state of multi-agent AI pipelines into progressively more compact, decision-relevant representations — without losing the causal structure that makes human oversight meaningful.

Each layer answers a different question:

| Layer | Name | Question answered |
|-------|------|-------------------|
| L0 | Token / Artifact Layer | What did the agents produce? (raw) |
| L1 | Semantic Feature Layer | What do those outputs mean? (embeddings) |
| **L2** | **Cognitive Tensor Layer** | **What is the system's quality state?** (tensor T[d,i,j,k]) |
| L3 | Tensor Volume Layer | How does quality evolve across sessions? (volume V = C({T⁽ˢ⁾})) |
| L4 | Meta-Inference Layer | What should the system do next? (M(V)) |

The key claim: **a human operator at L2 can govern a multi-agent AI pipeline more accurately and with lower cognitive load than one reviewing raw L0 outputs** — even without seeing a single line of code.

---

## Architecture

```
L4  Meta-Inference         M(V) → {decisions, predictions, adaptations}
     ↑ depends on C (L3)
L3  Tensor Volume          V = C({T⁽ˢ⁾}_{s=1}^{n})
     ↑ consumes L2 corpus
L2  Cognitive Tensor       T[d,i,j,k] + NCF (Natural Cognitive Frontier)
     ↑ aggregates from L1
L1  Semantic Features      quality vectors V ∈ [0,1]¹¹
     ↑ extracted from L0
L0  Raw Artifacts          AI-generated code, configs, logs
```

---

## Repositories

Each layer is an independent git repository. This repo (`CAL`) documents the framework and hosts the pre-paper.

| Layer | Repo | Venue | Status |
|-------|------|-------|--------|
| CAL (framework) | ← you are here | arXiv | Pre-paper v1.3 |
| [L2 — TCO](https://github.com/jpcpol/TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO) | TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO | CHI 2027 | RCT n=40 · platform deployed |
| [L3 — Tensor Volume](https://github.com/jpcpol/Tensor-Volume-Layer-L3) | Tensor-Volume-Layer-L3 | NeurIPS/ICML | Composition operator C — open problem |
| [L4 — Meta-Inference](https://github.com/jpcpol/Meta-Inference-Layer-L4) | Meta-Inference-Layer-L4 | NeurIPS/ICML | Efficiency Hypothesis · AMD baseline active |

---

## Papers

| Document | Location | Description |
|----------|----------|-------------|
| CAL Pre-paper v1.3 | [`CAL_PrePaper_v1.3.md`](CAL_PrePaper_v1.3.md) | Full CAL framework — L0–L4 definitions, hypotheses, roadmap |
| TCO-L2 Working Paper v3.0 | [L2 repo / README](https://github.com/jpcpol/TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO) | RCT design, NCF theory, experimental platform |
| L3 Paper | L3 repo / `paper/` | Composition operator C — in development |
| L4 Paper | L4 repo / `paper/` | L4 Efficiency Hypothesis — in development |

---

## Key Concepts

**Natural Cognitive Frontier (NCF):** The abstraction level at which human cognitive demand is calibrated to human capacity. At NCF, an operator reads `{Ω, Δ, Ρ, Ξ}` — four aggregate state signals — and injects policy in natural language, without touching raw artifacts.

**Composition Operator C:** The central open problem of L3. Must map a collection of L2 tensors `{T⁽ˢ⁾}` to a unified volume V while preserving causal structure, temporal coherence, and dimensional stability. Current candidate: Tucker decomposition (`tensorly`). Pre-registration required before running empirical tests.

**L4 Efficiency Hypothesis:** The cost of M(V) scales with κ(V) — the effective structural complexity of V — which grows significantly slower than O(n²) in the number of raw artifacts. Requires C defined (L3 gate) + AMD-Instinct hardware baseline.

**Governance Manifold Hypothesis:** Governance-relevant states occupy a low-dimensional manifold M_gov embedded in the full tensor space. If confirmed, C = manifold projection, and the L4 Efficiency Hypothesis follows as a consequence.

---

## Collaboration

**AMD-Instinct Labs** contributes the hardware layer of L4:

- `fa_dme` (Flash Attention with DME async, validated on MI300X) provides the empirical flat-context O(n²) baseline that the L4 Efficiency Hypothesis requires for comparison.
- Post gate-C: `fa_dme` becomes the kernel proxy for M(V) in the O(n²) vs O(κ) contrast.
- `probe_mfma_mapping.hip` characterizes the lane↔output mapping of `v_mfma_f32_16x16x16f16` — the low-level access required by the Representational Convergence Conjecture (RCC §6.4).

Canonical collaboration document: `Obsidian/wiki/proyectos/cal-collaboration.md`

---

## Roadmap

| Milestone | Owner | Gate |
|-----------|-------|------|
| RCT n=40 (TCO-L2) — recruit & run | L2 / partner institutions | DT-028 Fase 3 complete |
| Synthetic C proof of tractability (S1–S4) | L3 | pre-register first |
| O(n²) baseline confirmed in MI300X (log-log) | AMD-Instinct | VM session |
| M(V) kernel proxy contrast (S5) | AMD-Instinct + L3 | C validated |
| L4 Efficiency Hypothesis — synthetic test | L4 | M(V) + C |

---

## Citation

```bibtex
@misc{chancay2026cal,
  title   = {Cognitive Abstraction Layers: A Framework for Human Orchestration
             of Multi-Agent AI Pipelines},
  author  = {Chancay, Juan Pablo},
  year    = {2026},
  doi     = {10.5281/zenodo.20430343},
  note    = {Working paper v1.3. arXiv submission pending endorsement.}
}
```
