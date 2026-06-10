# CAL — Cognitive Abstraction Layers

**Author:** Juan Pablo Chancay · Aural Syncro  
**Pre-paper:** [concept DOI 10.5281/zenodo.20430343](https://doi.org/10.5281/zenodo.20430343) · v1.4: [10.5281/zenodo.20628125](https://doi.org/10.5281/zenodo.20628125) · arXiv pending endorsement  
**Layer deposits:** L2 [10.5281/zenodo.20628131](https://doi.org/10.5281/zenodo.20628131) · L3 [10.5281/zenodo.20628133](https://doi.org/10.5281/zenodo.20628133)  
**License:** CC BY-NC 4.0 (docs) · AGPL-3.0 (code in sub-repos)  
**Status:** Active research — L2 validated · L3 characterization closed (~95%) · L4 efficiency-mechanism confirmed on MI300X (S5) · L4 representation closed (L4-B0 NO-GO: dual is terminal). Sole open gate: L4 governance accuracy (condition c, RCT-bound).

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
| CAL (framework) | ← you are here | arXiv | Pre-paper v1.4 |
| [L2 — TCO](https://github.com/jpcpol/TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO) | TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO | CHI 2027 | RCT n=40 · platform deployed |
| [L3 — Tensor Volume](https://github.com/jpcpol/Tensor-Volume-Layer-L3) | Tensor-Volume-Layer-L3 | NeurIPS/ICML | Operator C characterized — causal conservation = sparsity preservation (closed) |
| [L4 — Meta-Inference](https://github.com/jpcpol/Meta-Inference-Layer-L4) | Meta-Inference-Layer-L4 | NeurIPS/ICML | Efficiency Hyp. **mechanism confirmed** (S5: κ decouples, flat ~n^1.91, D(n)→52.8×) · representation closed (L4-B0 NO-GO) · condition (c) open |

---

## Papers

| Document | Location | Description |
|----------|----------|-------------|
| CAL Pre-paper v1.4 | [`CAL_PrePaper_v1.4.md`](CAL_PrePaper_v1.4.md) | Full CAL framework — L0–L4 definitions, hypotheses, roadmap; §5.7 = L3 closure summary |
| TCO-L2 Working Paper v3.0 | [L2 repo / README](https://github.com/jpcpol/TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO) | RCT design, NCF theory, experimental platform |
| L3 Paper + Closure | L3 repo / `paper/` + [`L3_CLOSURE.md`](L3/L3_CLOSURE.md) | Operator C characterized; causal conservation = structural sparsity preservation |
| L4 Paper v0.4 | L4 repo / `paper/` | L4 Efficiency Hypothesis — S5 mechanism confirmed (§5.4); L4-B0 residual NO-GO (§5.5); condition (c) open |

---

## Key Concepts

**Natural Cognitive Frontier (NCF):** The abstraction level at which human cognitive demand is calibrated to human capacity. At NCF, an operator reads `{Ω, Δ, Ρ, Ξ}` — four aggregate state signals — and injects policy in natural language, without touching raw artifacts.

**Composition Operator C:** L3's central operator, now characterized. L3 showed that **reconstruction-faithful compression (Tucker) destroys causal structure** while preserving variance — so C is built as `C = C_causal ∘ C_compress`, where Tucker compresses and a causal step preserves structure. The operative property: an operator is *causally conservative* iff it preserves the observational invariants **Ω₀ = (R, C, S)** (reachability, coverage, consistency) under compression — **not** reconstruction fidelity. Tucker's failure mode is *spurious-edge fabrication*; a structural prune to the causal support recovers 75% of the causal-conservation gap with no ground truth.

**U — unsupervised causal metric:** a ground-truth-free score (PCMCI val-matrix flow correlation) that orders causal fidelity. Validated (the TCI calibration test) so that C can be optimized for causal conservation *at deployment*, where no causal graph is known.

**L4 Efficiency Hypothesis:** The cost of M(V) scales with κ(V) — the effective structural complexity of V — which grows significantly slower than O(n²) in the number of raw artifacts. **Mechanism confirmed on MI300X (S5, 2026-06):** flat-context cost grows as ~n^1.91 (R²=0.997) while the governance-state cost is bounded by κ(V)=1296 and independent of n — the decoupling ratio D(n) reaches 52.8× at seqLen 4096. This demonstrates the cost *mechanism* (coupling vs decoupling), not a production-scale or accuracy claim; **condition (c) — governance accuracy of M(V) vs flat-context — is the sole remaining gate** (RCT-bound).

**L4-B0 — the residual is non-linear (the dual is terminal):** with the cost mechanism frozen, the residual `ΔU≈0.138` that compression leaves was characterized. Only 19% is linear-edge-representable; 81% is non-linearity a single *linear* volume cannot carry. Folding the dual `(V_Tucker, G_pruned)` into one linear V′ (L4-B) was therefore **not opened** — a clean negative result. This bounds the RCC (below): no single linear compressed state is both κ-minimal and causally complete at this rank. It is the second time the ordering *causality ≻ reconstruction* prevents a collapse (after L3's S3-bis).

**Governance Manifold Hypothesis:** Governance-relevant states occupy a low-dimensional manifold M_gov (confirmed: dim≈2–3, trustworthiness ≥0.96). L3 found this manifold is *static* (time-averaged) while causality is *temporal*, so M_gov is retained as a **descriptor**, not as a projection driver — whether a low-dimensional *causal* manifold exists is an open L4 question.

---

## Collaboration

**AMD-Instinct Labs** contributes the hardware layer of L4:

- `fa_dme` (Flash Attention with DME async, validated on MI300X) provides the empirical flat-context O(n²) baseline (n^1.90–1.91, R²≈0.997, confirmed quadratic across independent runs).
- **S5 cost contrast done (2026-06):** combining the measured O(n²) law with L3's κ(V)=1296, the κ vs n² decoupling was confirmed on MI300X (D(n)→52.8× @ 4k). Frozen.
- **Research→application arc closed (2-A/2-C, 2026-06):** the research kernel runs a full LLM (Qwen2.5-0.5B, 24/24 layers) preserving the top-1 next-token (2-A PASS); against production SDPA it is 8.5–15× slower (expected) — the gap (idle-CU occupancy) is the upstream-portability target, reported honestly, not a win claim.
- `probe_mfma_mapping.hip` characterizes the lane↔output mapping of `v_mfma_f32_16x16x16f16` — the low-level access the Representational Convergence Conjecture (RCC §6.4) would require. The RCC remains a long-horizon conjecture, now **bounded by L4-B0**: any convergent state is not a single low-rank *linear* folding at this scale.

Canonical collaboration document: `Obsidian/wiki/proyectos/cal-collaboration.md`

---

## Roadmap

| Milestone | Owner | Status / Gate |
|-----------|-------|---------------|
| Synthetic C tractability + manifold (S1–S4) | L3 | ✅ Done — Tucker tractable, dim(M_gov)≈2–3 |
| Causal conservation characterized (TCI → Q_L3.2A → Form 1) | L3 | ✅ Done — L3 closed (~95%) |
| O(n²) baseline confirmed in MI300X (log-log) | AMD-Instinct | ✅ Done — n^1.90, R²=0.996 |
| L4-A operator: dual V at κ-bounded cost | L4 | ✅ Done — C1/C2/C5 pass |
| κ vs n² cost contrast — mechanism (S5, seqLen 512→4k, D=128) | AMD-Instinct | ✅ Done — D(n)→52.8× @4k; frozen |
| Research→application arc (2-A full LLM, 2-C vs production) | AMD-Instinct | ✅ Done — 2-A PASS (top-1 preserved); 2-C gap measured |
| L4-B0 residual characterization | L3/L4 | ✅ Done — NO-GO (81% non-linear); dual is terminal |
| L4-B (single-V via inverse projection) | L3/L4 | ❌ Not opened — refuted by L4-B0 |
| RCT n=40 (TCO-L2) — recruit & run | L2 / partner institutions | DT-028 Fase 3 + delegation (MoU) |
| **L4 Efficiency Hypothesis — full test (condition c)** | L4 | **Open — sole remaining gate; needs governance corpus from the RCT** |

---

## Citation

```bibtex
@misc{chancay2026cal,
  title   = {Cognitive Abstraction Layers: A Framework for Human Orchestration
             of Multi-Agent AI Pipelines},
  author  = {Chancay, Juan Pablo},
  year    = {2026},
  doi     = {10.5281/zenodo.20430343},
  note    = {Working paper v1.4. arXiv submission pending endorsement.}
}
```
