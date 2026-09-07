# Unified synthetic benchmark for the compatible-world framework

Status: **Layer-1 canonical finite-world protocol**.

## Purpose

This benchmark gives the unified theory its own synthetic evidence base without reusing the primary numerical endpoints of the standalone TNOA, MROD or InsePi papers. Each fixture is finite, exact and truth-complete. The fixtures are intentionally minimal: they test whether a structural information-order prediction becomes strict under a controlled world construction.

The benchmark is not intended to mimic natural frequencies, physical camera noise or ecological prevalence. It is a proof-of-activation suite between theorem-only evidence and larger domain-specific simulations.

## U1 — retained-reference strict refinement

Latent world:

- target bit `T in {0,1}`;
- nuisance bit `N in {0,1}`.

Primary observation:

`Y = T XOR N`.

Estimand: `theta=T`.

For either realised world with `Y=1`, the primary fibre contains two worlds:

- `(T=0,N=1)`;
- `(T=1,N=0)`.

A matched retained reference is `R=N`. The augmented observation `(Y,R)` point-identifies `T`, contracting compatible-set size from `2` to `1`.

A deliberately uninformative control reference is constant, `R0=0`, and leaves compatible-set size `2`.

Primary endpoint:

- matched strict contraction: `2 -> 1`;
- constant-reference control: `2 -> 2`.

## U2 — record-entry selection and omitted-support non-identifiability

The observational universe contains four fixed opportunities. Three enter the retained record and one leaves no row.

The two admissible full worlds share the same selected table:

- entered truths: `[1,1,0]`;
- omitted opportunity identity: the same fourth unit.

They differ only in omitted truth:

- world A omitted truth `0`, full prevalence `2/4 = 0.50`;
- world B omitted truth `1`, full prevalence `3/4 = 0.75`.

The selected table therefore has the same observed prevalence `2/3` in both worlds but leaves full prevalence identified set `{0.50,0.75}`.

A selection-independent denominator ledger identifies that one opportunity was omitted but does not collapse the prevalence identified set. An independent audit of the omitted truth makes the full prevalence singleton.

Primary endpoints:

- selected-table full-prevalence identified-set width: `0.25`;
- denominator-only width: `0.25`;
- denominator + omitted-truth audit width: `0`.

## U3 — deterministic semantic coarsening

Two latent worlds differ in target truth and rich retained state:

- world N: `truth=0`, rich state `nuisance_supported`;
- world U: `truth=1`, rich state `unresolved_overlap`.

The rich states are distinct and therefore each realised rich record has compatible-set size `1`.

A deterministic binary coarsener maps both states to `not_target`. The binary record then has compatible-set size `2` and target-truth identified set `{0,1}`.

Primary endpoint:

- rich compatible-set size `1` versus coarsened size `2`;
- rich truth-set width `0` versus binary truth-set width `1`.

The fixture is deliberately about information preservation, not about claiming that either rich label is a calibrated field truth category.

## U4 — prospective information-guided observation choice

Current mechanism set:

`S in {A,B,C,D}` with equal mass.

Current residual entropy:

`H(S)=2 bits`.

Three candidate future observations are available.

### Q_balanced

Partition:

- outcome 0: `{A,B}`;
- outcome 1: `{C,D}`.

Information value:

`I(S;Q_balanced)=1 bit`.

### Q_skew

Partition:

- outcome 0: `{A,B,C}`;
- outcome 1: `{D}`.

Information value:

`I(S;Q_skew)=h2(1/4)=0.811278... bits`.

### Q_null

Single constant outcome for all four mechanisms.

Information value:

`0 bits`.

An information-guided one-step policy therefore selects `Q_balanced`. Uniform random choice among the three candidates has mean immediate information

`(1 + 0.811278... + 0)/3 = 0.603759... bits`.

A second retained observation `Q_detail` partitions `{A,C}` versus `{B,D}`. Jointly `(Q_balanced,Q_detail)` uniquely identifies all four mechanisms, reducing residual entropy from `2 -> 1 -> 0 bits` along either realised first-step branch.

Primary endpoints:

- best immediate information: `1 bit`;
- uniform-random mean immediate information: `0.603759... bits`;
- nested entropy under the planned two-step sequence: `2 -> 1 -> 0 bits`.

## U5 — intervention responses break static observational equivalence

The same four mechanism classes `{A,B,C,D}` are statically indistinguishable under a constant baseline observation.

Two controlled interventions return deterministic binary responses:

| mechanism | I_event | I_observability |
|---|---:|---:|
| A | 1 | 0 |
| B | 0 | 1 |
| C | 1 | 1 |
| D | 0 | 0 |

Before intervention, all four mechanisms lie in one observational-equivalence class and residual entropy is `2 bits`.

Either single intervention creates a two-by-two partition and leaves `1 bit` residual entropy. The joint two-intervention response is unique for every mechanism and leaves `0 bits`.

Primary endpoint:

`4 compatible mechanisms -> 2 -> 1` under one then two retained intervention responses.

This fixture demonstrates conditional identifiability from designed response directions. It does not establish that a physical intervention will realise these ideal signatures.

## Interpretation contract

The benchmark may support:

- strict refinement can occur when retained side information is discriminating;
- support deletion can make an estimand non-identifiable from the selected table even with perfect semantics on entered rows;
- deterministic semantic coarsening can strictly enlarge compatible sets;
- prospective candidate observations can differ in expected information and an information-guided choice can outperform uninformed choice in a declared finite world;
- interventions can create new identification directions that break static observational equivalence.

The benchmark may not support:

- ecological or physical effect sizes;
- field prevalence or visit rates;
- universal optimality of information-guided design;
- universal value of any particular reference sensor;
- completeness of a mechanism vocabulary in nature;
- physical causal identification.

## Relation to larger synthetic benchmarks

The standalone V3, TNOA, MROD and InsePi repositories contain larger frozen synthetic benchmarks. Those results can be cited as scale/stress tests of related operators, but they are not the primary endpoints of this unified benchmark and should not be republished as if generated uniquely for the Layer-1 paper.
