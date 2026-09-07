# Closed-loop observation claim recovery — 2026-09-07

Status: **cross-repository claim ledger**.

This document records which parts of the proposed closed-loop observation framework are already supported, at what evidence level, and which stronger statements remain open.

The intended loop is:

```text
Omega / possible worlds
        |
        v
observation / retention
        |
        v
compatible worlds
        |
        +--------------------+
        |                    |
        v                    v
       V3                   MROD
retained side info      future observation
refines current set     chosen for expected refinement
        |                    |
        +----------+---------+
                   v
          finer distinctions
                   |
                   v
              Boundary
                   |
                   v
          remaining ambiguity
                   |
                   v
        PolliPi / InsePi / ...
                   |
                   +----> new evidence
```

REC and TNOA are information-loss / preservation operators around this loop rather than necessarily one fixed serial stage.

## 1. Core compatible-world object

For latent worlds `omega in Omega` and an observation map `X`, define

\[
C_X(x)=\{\omega\in\Omega:X(\omega)=x\}.
\]

For a scientific distinction or estimand `theta`, the identified set is

\[
I_X(x)=\{\theta(\omega):\omega\in C_X(x)\}.
\]

The cross-repository synthesis is therefore about how observation-system operations enlarge, preserve, or contract compatible-world equivalence classes.

## 2. Recovered claim: REC identifies pre-entry selection as a real ecological distortion mechanism

**Evidence level: external empirical data.**

Supported:

1. record-entry selection can alter ecological composition before downstream semantic classification;
2. truth-positive rows lost upstream cannot be recreated by downstream semantic perfection alone;
3. retained entry provenance can support partial correction;
4. correction has a calibration/transport domain and can fail under broader transport.

Primary empirical anchors are the CCTV-referenced fox/badger camera-trap data, otter wet/dry transport analyses, and the protected BirdVox irreversibility stress test in `zuizui0223/rec`.

Current boundary:

- external-data H1-H5 is draft-ready;
- prospective same-system REC->TNOA H6 remains open.

Interpretation in the loop:

> REC audits when the observation/retention map removes support before a row exists. It therefore constrains which compatible worlds can be inferred from the retained table alone and which require an external exposure/reference channel.

## 3. Recovered claim: V3 retained side information can produce strict refinement in controlled worlds

**Evidence level: structural theorem + controlled synthetic evidence.**

Structural statement:

\[
C_{(X,R)}(x,r)\subseteq C_X(x),
\]

with equality allowed in general.

The stronger empirical question is whether a particular reference is strictly informative. That is already positive in the frozen PolliPi-derived synthetic evidence ledger:

### V3 temporal-subspace benchmark

Matched reference:

- balanced utility: `0.8327`;
- nuisance false-frame rate: `0.0272`;
- local-sway false-frame rate: `0.109`;
- target-episode recall: `1.0`.

No reference:

- balanced utility: `0.5688`;
- nuisance false-frame rate: `0.2986`;
- local-sway false-frame rate: `1.0`;
- target-episode recall: `1.0`.

Time-permuted reference balanced utility: `0.7301`.

This recovers the controlled claim:

> Correctly coupled retained reference information, not reference presence alone, can strictly improve observation refinement in a frozen synthetic world.

The robustness benchmark retained gains under one-frame lag and 75% temporal coupling.

The V3->TNOA bridge also showed that richer representation increased safe usable coverage, but failed its false-certainty ceiling. Therefore the stronger claim that representation improvement licenses semantic certainty is **not** recovered.

Still open:

- strict physical-domain reference benefit;
- named physical nuisance identification;
- universal or field-domain transfer;
- unconditional nuisance subtraction.

## 4. Recovered claim: TNOA preserves distinctions that deterministic semantic collapse destroys

**Evidence level: closed-world quantitative validation.**

The frozen known-truth composition analysis supports:

- median compatible target-prevalence width about `0.030` with B/T/N/U;
- median width about `0.266` after binary coarsening;
- median relative width reduction about `84.45%` among non-zero binary widths;
- low-target subset width about `0.000175` versus `0.07410` after binary collapse.

Thus the supported statement is:

> Premature semantic coarsening can merge worlds that remain distinguishable under a richer process-preserving observation state.

Not recovered:

- field visit-rate accuracy;
- semantic-specific superiority of the frozen U reasons;
- universal numerical thresholds;
- universal cross-system transfer.

## 5. Recovered claim: Boundary characterizes what the current observation map cannot identify

**Evidence level: structural identification theory + executable tests.**

For positive log-linear channels with observation matrix `M`, the exact structural unidentified dimension is

\[
k-\operatorname{rank}(M).
\]

A new scalar observation reduces this dimension iff its row lies outside the current row span.

This recovers:

> More precise replication along an existing observation direction can reduce sampling uncertainty without reducing structural mechanism ambiguity. A new identification direction is required to refine the equivalence classes.

Boundary therefore supplies the current-map half of the loop:

```text
current observation map -> compatible / identified set -> unresolved distinctions
```

Still open:

- a flagship natural-system demonstration in which a biologically important mechanism distinction is shown to sit exactly on this boundary and is then resolved by a subsequent designed observation.

## 6. Recovered claim: MROD can choose future observations that reduce residual mechanism ambiguity efficiently

**Evidence level: controlled sequential benchmark.**

For admissible mechanism region `A_epsilon` and candidate observation `Q`, MROD uses

\[
V(Q)=I(S;Q\mid A_\epsilon)/K.
\]

The frozen G2 benchmark recovered a strong controlled result.

At budget 2:

- initial confounding edges resolved: `1.000` information-guided vs `0.6045` random;
- systems converged: `0.990` vs `0.435`;
- observations used: `1.505` vs `1.821`.

At budget 4, both policies resolved all initial confounding edges on average, while the information-guided policy selected `0.014` mechanism-independent nuisance measurements per system versus `1.169` under random order and used `1.518` versus `2.673` observations.

This recovers:

> Given a declared compatible mechanism region and a verified candidate-outcome vocabulary, future observations can be ranked by expected incremental mechanism information and can resolve ambiguity more efficiently than random ordering in controlled systems.

Important asymmetry with V3:

- V3 refinement is retrospective with already-retained side information;
- MROD refinement is prospective and expected before the observation outcome is known.

Still open:

- natural/physical-system demonstration that the selected real measurement produces the predicted refinement;
- universal optimality beyond the declared candidate/model family.

## 7. Recovered claim: V3 and MROD are two refinement branches over the same compatible-world geometry

**Evidence level: synthesis of already-supported operators; no new empirical claim.**

The useful distinction is:

\[
\boxed{\text{V3 = exploit retained discriminating information}}
\]

versus

\[
\boxed{\text{MROD = acquire expected discriminating information}}
\]

Both can be written as partition refinement of compatible worlds, but they differ in timing and epistemic status.

V3:

\[
C_E \to C_{E,R}\subseteq C_E
\]

after `R` already exists.

MROD:

\[
Q^*=\arg\max_Q E[\operatorname{refinement}(C_E\mid Q)]
\]

before the future outcome is revealed.

This is the defensible basis for placing V3 and MROD in parallel under `compatible worlds`.

## 8. Physical-system status: loop infrastructure exists, decisive closure is still open

### PolliPi

Implemented:

- fixed primary timelapse record;
- low-resolution probes;
- per-probe provenance and shadow logging;
- whole-frame mesh decisions;
- opt-in adaptive still/video acquisition;
- deployment and safety gates.

Still required before broad scientific use of classified adaptive modes:

- real flower/camera sequences;
- manual truth comparison;
- false-positive and missed-signal analysis across wind, flower sway, illumination, shadow and camera motion;
- hardware endurance checks;
- threshold calibration and promotion rule.

### InsePi

Current mainline:

```text
V7   FAIL / C
V10  partial / C
V11  FAIL / D
V12  B
V13  RESULT PENDING
```

V12 recovered controlled causal intervention diagnosis in simulation. V13 is the frozen blinded physical validation over new recording days and physical scenes. Its protocol and no-peek pipeline are ready, but the scientific result has not yet been materialized.

## 9. Overall claim state

### Already recoverable now

1. **Selection loss is scientifically consequential** — REC, external empirical.
2. **Retained side information can strictly refine observations** — V3, controlled synthetic.
3. **Premature semantic collapse destroys compatible-world distinctions** — TNOA, closed-world quantitative.
4. **Current-map ambiguity is a structural identification object** — Boundary, mathematical/executable.
5. **Future observations can be selected to efficiently reduce that ambiguity** — MROD, controlled sequential.
6. **A physical acquisition platform capable of logging the necessary provenance and adaptive actions exists** — PolliPi implementation.
7. **Controlled intervention diagnosis exists synthetically and a blinded physical test is frozen** — InsePi V12/V13.

### Not yet recoverable

The strongest unified statement is still open:

> In one held-out physical observation system, retained side information and/or a MROD-selected observation measurably contracts the same predeclared compatible-world set, the resulting Boundary becomes finer, and the improvement survives blinded truth evaluation without post-hoc retuning.

That is the missing closure experiment.

## 10. Safe umbrella claim now

The current cross-repository evidence supports the following umbrella statement:

> Scientific observation can be treated as management of compatible-world distinctions. Existing evidence shows separately that upstream selection can erase ecological support, retained side information can refine observations in controlled systems, semantic coarsening can destroy downstream identification, structural observation maps define mechanism-equivalence boundaries, and information-guided future measurements can reduce those boundaries efficiently in controlled systems. The remaining step is a single blinded physical loop that demonstrates these operations on the same observation system.

This statement does not claim that the full loop has already been validated in nature.
