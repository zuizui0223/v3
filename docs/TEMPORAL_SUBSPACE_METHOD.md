# Temporal-subspace V3 implementation

Status: **historical promoted simulation implementation and one computational approximation to the general theory**.

The temporal-subspace implementation was the first V3 generation to escape spatial pixel correspondence.

## Frozen simulation representation

- sequence length: `T = 9`;
- reference temporal rank: `K = 3`;
- target-free reference sequence;
- reference and primary scenes need not be spatially aligned;
- reference basis derived only from reference temporal variation;
- primary temporal variation projected onto that basis;
- no target labels enter the basis.

Let primary and reference temporal deviations from their backgrounds be matrices

\[
D_P\in\mathbb R^{T\times p},\qquad D_R\in\mathbb R^{T\times q}.
\]

Compute an SVD

\[
D_R = U\Sigma V^\top
\]

and retain the first `K` temporal columns `U_K`. The primary decomposition is

\[
E = U_KU_K^\top D_P,
\]

\[
Z = D_P-E.
\]

The original PolliPi V3 experiment formed a corrected image sequence from `Z` and passed it to an unchanged downstream observer. The standalone V3 API now returns **both** `E` and `Z`, consistent with the later reversible-decomposition theory.

Implementation: `src/v3/temporal_subspace.py`.

## Frozen negative control

A time-permuted reference preserved reference marginal appearance while destroying the temporal coupling. A no-reference condition provided the raw baseline.

The primary synthetic generation showed a substantial advantage of correctly coupled reference over both controls. A second frozen generation showed the gain survived a one-frame lag and 75% temporal coupling.

Machine-readable historical metrics: `results/synthetic_evidence_summary.json`.

## Why this implementation is not the theory

The temporal SVD projector is one approximation to reference-guided measurement-state refinement. The general theory also permits nonlinear forward models, geometric latent-state models, learned embeddings, set-valued references, probabilistic reference models, other sensors, and no projection at all.

The invariant is the information contract:

> retain the reference as additional information, avoid unsupported restrictions of compatible measurement states, and do not assign target/nuisance semantics to a derived component without independent entitlement.

## Failure boundary discovered later

A short-window reference-derived subspace may overlap target temporal structure by chance. In the V3–TNOA trajectory bridge, unconditional matched projection degraded target-only trajectory geometry. This is expected from the exact projection result: energy-ratio improvement requires nuisance capture to exceed target capture.

Therefore this implementation should be used as a diagnostic representation candidate, not as a universal “denoised truth” generator.
