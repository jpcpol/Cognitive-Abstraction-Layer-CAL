# CAL — Cognitive Abstraction Layers

**Autor:** Juan Pablo Chancay (Aural Syncro)  
**Pre-paper:** DOI [10.5281/zenodo.20430343](https://doi.org/10.5281/zenodo.20430343)  
**Estado:** Investigación activa — L2 validado, L3/L4 en desarrollo

Framework de abstracción cognitiva para supervisión de pipelines multi-agente de IA.
Propone una jerarquía de 5 capas (L0–L4) donde cada capa comprime el estado semántico
del sistema preservando la estructura decision-relevante.

```
L4  Meta-Inference Layer       M(V) → {decisions, predictions}     ← repo L4/
L3  Tensor Volume Layer        V = C({T⁽ˢ⁾})                        ← repo L3/
L2  Cognitive Tensor Layer     T[d,i,j,k] + NCF (TCO-L2)           ← repo L2/
L1  Semantic Feature Layer     {embeddings, quality signals}
L0  Token/Artifact Layer       raw AI outputs
```

## Estructura

| Carpeta | Contenido | Repo |
| --- | --- | --- |
| `L2/` | TCO-L2 — tensor cognitivo + RCT n=40 + plataforma experimento | GitHub: TENSOR-BASED-COGNITIVE-OVERSIGHT-TCO |
| `L3/` | Tensor Volume Layer — operador de composición C + paper L3 | GitHub: por asignar |
| `L4/` | Meta-Inference Layer — M(V) + L4 Efficiency Hypothesis + paper L4 | GitHub: por asignar |

Cada sub-carpeta es un repositorio git independiente.
Este repo CAL documenta el framework completo y el pre-paper.

## Papers

| Capa | Documento | Venue objetivo |
| --- | --- | --- |
| CAL (framework) | `CAL_PrePaper_v1.3.md` | arXiv (pendiente endorsement) |
| L2 | `L2/Documentacion/TCO_Paper_Final_v3.md` | CHI 2027 (sep 2026) |
| L2 SID | `L2/analysis/sid_study/` | FAccT |
| L3 | `L3/paper/` (en desarrollo) | NeurIPS/ICML |
| L4 | `L4/paper/` (en desarrollo) | NeurIPS/ICML |

## Colaboración

- **AMD-Instinct Labs** — capa L4: `fa_dme` (Flash Attention MI300X) provee el baseline
  de hardware O(n²) para la L4 Efficiency Hypothesis. Kernel proxy de M(V) post-gate-C.
  Registro canónico: `Obsidian/wiki/proyectos/cal-collaboration.md`

## Licencia

CC BY-NC 4.0 (documentación) · AGPL-3.0 (código en sub-repos)
