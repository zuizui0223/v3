# Empirical constrained-proxy audit

Status: application-independent bridge from the ideal audit-burden benchmark to an actually observed physical proxy.

## Question

For each observation opportunity retain:

- frozen primary representation `O` (`primary_key`);
- independent scientific truth `theta` (`truth_state`) when available;
- candidate physical proxy/reference `Z` in an opportunity-keyed overlay.

The ideal benchmark

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|
\]

states how many audit symbols an unconstrained latent-world audit mapping would need. It does **not** show that the measured proxy `Z` can realize those distinctions.

The constrained-proxy audit asks:

> Does the actually observed proxy `Z`, possibly after deterministic recoding, distinguish all truth states that remain confounded under `O`?

## Exact complete-truth regime

When truth, primary and proxy are complete on the supplied finite opportunity universe:

1. group worlds by `(O,Z)`;
2. if any such cell contains more than one truth value, the proxy is infeasible — no deterministic `g(Z)` can repair it;
3. otherwise construct the proxy confusability graph;
4. the minimum output alphabet for deterministic proxy recoding is the graph chromatic number `chi(G_Z)`.

The summary reports:

- ideal unconstrained alphabet and burden;
- exact proxy feasibility;
- minimum proxy alphabet/burden when feasible;
- realizability gap

\[
\Gamma_Z=\log_2\chi(G_Z)-\log_2m^*;
\]

- number of confusability edges.

## Partial truth

Missing truth does not license optimistic feasibility.

A one-sided conclusion is still possible:

- if already-observed truth contains two different values in the same `(O,Z)` cell, proxy infeasibility is certified even while other truth labels remain missing;
- if no observed conflict exists, feasibility remains `undetermined_partial_truth` because a missing label could still create a conflict.

This asymmetry is intentional: additional truth can reveal a new contradiction, but cannot erase a contradiction already observed.

## Missing primary or proxy support

If `primary_key` or proxy `Z` is missing on any supplied opportunity, the result is

`undetermined_partial_coverage`.

Truth completeness cannot repair missing sensor support.

## Data layout

Opportunity ledger:

```json
{"opportunity_id":"...","selected":true,"primary_key":"...","truth_state":"..."}
```

Proxy overlay:

```json
{"opportunity_id":"...","value":"..."}
```

A null proxy means not observed; it is not a scientific state.

## CLI

```bash
python scripts/summarize_constrained_proxy_audit.py \
  --opportunities opportunities.jsonl \
  --proxy reference_proxy.jsonl \
  --output constrained_proxy_summary.json
```

## Relation to V3

The audit separates three levels that must not be collapsed:

1. **ideal refinement need** — how much estimand-relevant distinction is absent from `O` in principle;
2. **physical proxy realizability** — whether the retained reference channel actually carries enough distinctions;
3. **implemented observer performance** — whether a practical algorithm successfully uses those distinctions.

A useful V3-like physical reference should therefore be evaluated not only by predictive performance, but also by whether it can realize the distinctions the compatible-world analysis says are needed.

## Claim boundary

This is a finite, deterministic, noiseless, single-shot audit. It is not noisy-channel capacity, average coding rate, causal sensor value, or proof that an approximate learned representation preserves all proxy distinctions.
