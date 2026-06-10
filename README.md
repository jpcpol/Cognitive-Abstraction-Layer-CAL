# CAL — Cognitive Abstraction Layers

**Author:** Juan Pablo Chancay · Aural Syncro  
**Pre-paper:** [DOI 10.5281/zenodo.20430343](https://doi.org/10.5281/zenodo.20430343) · arXiv pending endorsement  
**License:** CC BY-NC 4.0 (docs) · AGPL-3.0 (code in sub-repos)  
**Status:** Active research — L2 validated · L3 characterization closed (~95%) · L4 baseline operator validated (L4-A), at-scale cost contrast active

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
| [L3 — Tensor Volume](https://github.com/jpcpol/Tensor-Volume-Layer-L3) | Tensor-Volume-Layer-L3 | NeurIPS/ICML | Operator C characterized — causal conservation = sparsity preservation (closed) |
| [L4 — Meta-Inference](https://github.com/jpcpol/Meta-Inference-Layer-L4) | Meta-Inference-Layer-L4 | NeurIPS/ICML | Efficiency Hypothesis · gate-C closed · κ vs n² contrast active |

---

## Papers

| Document | Location | Description |
|----------|----------|-------------|
| CAL Pre-paper v1.4 | [`CAL_PrePaper_v1.4.md`](CAL_PrePaper_v1.4.md) | Full CAL framework — L0–L4 definitions, hypotheses, roadmap; §5.7 = L3 closure summary |
| TCO-L2 Working Paper v3.0 | [L2 repo / README](https://github.com/jpcpol/TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO) | RCT design, NCF theory, experimental platform |
| L3 Paper + Closure | L3 repo / `paper/` + [`L3_CLOSURE.md`](L3/L3_CLOSURE.md) | Operator C characterized; causal conservation = structural sparsity preservation |
| L4 Paper v0.2 | L4 repo / `paper/` | L4 Efficiency Hypothesis — gate-C closed, conditions (a)+(b) met |

---

## Key Concepts

**Natural Cognitive Frontier (NCF):** The abstraction level at which human cognitive demand is calibrated to human capacity. At NCF, an operator reads `{Ω, Δ, Ρ, Ξ}` — four aggregate state signals — and injects policy in natural language, without touching raw artifacts.

**Composition Operator C:** L3's central operator, now characterized. L3 showed that **reconstruction-faithful compression (Tucker) destroys causal structure** while preserving variance — so C is built as `C = C_causal ∘ C_compress`, where Tucker compresses and a causal step preserves structure. The operative property: an operator is *causally conservative* iff it preserves the observational invariants **Ω₀ = (R, C, S)** (reachability, coverage, consistency) under compression — **not** reconstruction fidelity. Tucker's failure mode is *spurious-edge fabrication*; a structural prune to the causal support recovers 75% of the causal-conservation gap with no ground truth.

**U — unsupervised causal metric:** a ground-truth-free score (PCMCI val-matrix flow correlation) that orders causal fidelity. Validated (the TCI calibration test) so that C can be optimized for causal conservation *at deployment*, where no causal graph is known.

**L4 Efficiency Hypothesis:** The cost of M(V) scales with κ(V) — the effective structural complexity of V — which grows significantly slower than O(n²) in the number of raw artifacts. **Gate-C now closed:** L3 delivers κ(V)=1296 (195.6× compression); the AMD-Instinct O(n²) baseline is measured (n^1.90, R²=0.996); the κ vs n² contrast is active.

**Governance Manifold Hypothesis:** Governance-relevant states occupy a low-dimensional manifold M_gov (confirmed: dim≈2–3, trustworthiness ≥0.96). L3 found this manifold is *static* (time-averaged) while causality is *temporal*, so M_gov is retained as a **descriptor**, not as a projection driver — whether a low-dimensional *causal* manifold exists is an open L4 question.

---

## Collaboration

**AMD-Instinct Labs** contributes the hardware layer of L4:

- `fa_dme` (Flash Attention with DME async, validated on MI300X) provides the empirical flat-context O(n²) baseline (measured: n^1.90, R²=0.996, confirmed quadratic).
- **Gate-C now closed:** with L3's operator delivering κ(V), `fa_dme` moves to its second role — the kernel proxy for M(V) in the at-scale O(n²) vs O(κ) contrast (active).
- `probe_mfma_mapping.hip` characterizes the lane↔output mapping of `v_mfma_f32_16x16x16f16` — the low-level access required by the Representational Convergence Conjecture (RCC §6.4).

Canonical collaboration document: `Obsidian/wiki/proyectos/cal-collaboration.md`

---

## Roadmap

| Milestone | Owner | Status / Gate |
|-----------|-------|---------------|
| Synthetic C tractability + manifold (S1–S4) | L3 | ✅ Done — Tucker tractable, dim(M_gov)≈2–3 |
| Causal conservation characterized (TCI → Q_L3.2A → Form 1) | L3 | ✅ Done — L3 closed (~95%) |
| O(n²) baseline confirmed in MI300X (log-log) | AMD-Instinct | ✅ Done — n^1.90, R²=0.996 |
| L4-A operator: dual V at κ-bounded cost | L4 | ✅ Done — C1/C2/C5 pass |
| At-scale κ vs n² contrast (seqLen 512→4k, D=128) | AMD-Instinct | Active — unblocked by L4-A |
| RCT n=40 (TCO-L2) — recruit & run | L2 / partner institutions | DT-028 Fase 3 complete |
| L4 Efficiency Hypothesis — full test (condition c) | L4 | Pending — gates (a),(b) met |
| L4-B (single-V) + residual-25% characterization | L3/L4 | Frozen — after AMD contrast freeze |

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
