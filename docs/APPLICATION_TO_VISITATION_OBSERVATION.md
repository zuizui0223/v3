# Application note — implications for visitation observation

Status: **application of the general theory, not part of its definition**.

The V3 / REC / TNOA theory is not derived from flower visitation as a privileged domain. This note asks only what the general information principles imply if one chooses flower-visitation imaging as an empirical test system.

## 1. Why visitation observation is a useful application

Visitation cameras combine several difficult observation processes in one system:

- focal events are local and temporally sparse;
- wind, flower movement, illumination and camera motion can mimic or mask events;
- recording policies determine which opportunities become high-resolution records;
- final scientific use often requires a semantic decision such as visit / no visit;
- exhaustive manual review is expensive, so adaptive acquisition is attractive.

This makes visitation imaging a strong stress test for refinement, selection and semantic entitlement, but these properties are not unique to ecology.

## 2. PolliPi simulation results are substantive empirical-method development

PolliPi should not be reduced to hardware plumbing. Its simulation sequence produced useful method results about adaptive observation under nuisance.

The development history established at least four substantive points:

1. an ideal event-matched target-free reference can strongly improve target–nuisance separation in simulation;
2. pixelwise / spatial subtraction is brittle to misregistration and distinct nuisance mechanisms fail for different reasons;
3. a temporal reference subspace can exploit shared temporal disturbance without spatial correspondence and retained gains under lag / partial coupling tests;
4. downstream bridge failures showed that representation improvement does not automatically license semantic certainty, and unconditional projection can remove target information.

These are useful results even before natural-field confirmation because they identify failure mechanisms, rule out overly strong architectures, and motivate non-destructive information refinement.

The correct boundary is:

> PolliPi simulation establishes behaviour of specified synthetic observation systems and informs apparatus design; it does not by itself establish natural visitation accuracy.

## 3. PolliPi and InsePi belong on the empirical side

### PolliPi

PolliPi is best viewed as an **observation-allocation testbed**.

Its practical comparison is not `simulation versus timelapse`. It is approximately:

- fixed scheduled observation;
- any-motion responsive observation;
- nuisance-filtered adaptive observation;
- optional high-information candidate video.

Simulation is used to develop and falsify the adaptive logic before or alongside physical validation.

### InsePi

InsePi is best viewed as an **interventional diagnostic testbed**.

When an observer fails, it asks whether controlled restoration of event-side, nuisance/observability-side, or shared-optical conditions changes the response as predicted.

Thus PolliPi asks mainly **how to allocate observation effort**, whereas InsePi asks **why an observation system failed**.

Neither platform defines V3, REC or TNOA.

## 4. What V3 implies for a visitation camera

The general V3 implication is not `subtract wind`.

It is:

> if a target-free channel contains independently useful information about measurement-side state, retain it and use it to contract compatible explanations without discarding the primary observation.

For visitation observation this suggests candidate designs such as:

- a target-free image region;
- a separate view of vegetation / illumination / camera motion;
- an inert visual reference;
- a non-image sensor that carries measurement-side state.

But no particular reference should be assumed useful in advance.

A safe representation keeps

\[
(Y,R,\text{explained},\text{residual})
\]

or an equivalent reversible/set-valued object rather than replacing `Y` with a corrected image.

## 5. What REC implies for visitation observation

The key REC implication is that an adaptive camera must preserve an **opportunity universe** independent of the adaptive entry rule.

If high-resolution records are created only when the detector fires, then the final event table cannot reveal what was missed.

A visitation validation design should therefore preserve, as far as feasible:

- a fixed or externally defined sequence of observation opportunities;
- the entry / trigger decision for every opportunity;
- enough audit information about non-entered opportunities to estimate or bound their biological composition.

Plain timelapse is useful here because it can provide a policy-independent observation baseline. It should not automatically be called biological truth; truth still requires manual or independent validation appropriate to the question.

## 6. What TNOA implies for visitation observation

The key TNOA implication is to avoid treating low visit support as proof of no visit.

A field observer should distinguish, when supported:

- positive visit-like evidence;
- positive nuisance evidence;
- observability / measurement support;
- unresolved overlap or no-support states;
- independently validated absence evidence, if such a channel exists.

This makes `uncertain` a scientific output rather than merely a classifier defect.

## 7. One empirical programme can test all three theories without redefining them

A strong field programme can use one prospectively defined observation universe while evaluating different theoretical questions.

### Reference-retained world

For each opportunity `i`, preserve a primary observation `Y_i` and, where predeclared, a side-information channel `R_i`.

### Selection audit

Define the operational record-entry decision `K_i` independently of later truth scoring.

This permits comparison between the full opportunity universe and the record that an adaptive policy would have retained.

### Semantic audit

For entered and/or audit-sampled opportunities, preserve rich evidence and an unresolved state before any final visit/not-visit coarsening.

### Independent truth

Use manual review, independent camera/sensor evidence, controlled event truth, or another predeclared source that is not the same mechanism being audited.

The same dataset can then ask:

- **V3:** did retained side information validly contract measurement ambiguity?
- **REC:** what biological/process composition was altered by record-entry selection?
- **TNOA:** how much additional information was lost by semantic coarsening, and when should uncertainty remain?

These are different estimands on the same observation system, not three visitation-specific theories.

## 8. Recommended order of research

The theory should be developed first because it determines what an empirical system must retain before data are collected.

Recommended order:

1. finish the application-independent information theory and theorem/claim boundaries;
2. derive generic design requirements for empirical observation systems;
3. instantiate those requirements in PolliPi / InsePi without changing the theory definitions;
4. run controlled physical validation for mechanism and observer-diagnosis questions;
5. run prospective visitation observation as a domain transport / ecological demonstration.

## 9. Main practical implication for visitation work

The general theory changes the design target from

> build the best insect detector

into

> build an observation system that preserves enough information to audit what it adds, what it discards, and what it still cannot uniquely interpret.

For flower visitation, this favours a system with:

- fixed baseline observation opportunities;
- shadow logging of adaptive decisions;
- retained reference channels when scientifically justified;
- independent truth sampling;
- explicit unresolved states;
- controlled interventions for diagnosing observer failure;
- later adaptive promotion only after the observation process itself has been audited.

That is a visitation application of the theory, not the origin or limit of the theory.
