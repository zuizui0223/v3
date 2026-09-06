# Derived design requirements for flower-visitation observation

Status: **application-layer design consequences**. These requirements are derived from the general observation-information theory; they do not define that theory.

## 1. Scientific objective

The design target is not simply a better insect detector. It is an observation system from which one can later audit:

1. what information was added;
2. what observation opportunities were selected or omitted;
3. what distinctions were preserved or collapsed;
4. which remaining ambiguities were genuinely unresolved.

Flower visitation is useful because sparse local events, environmental motion, adaptive recording, and later semantic interpretation all occur in one concrete system.

## 2. Requirement A — define opportunities before adaptive selection

Let `Omega` be a prospective sequence of observation opportunities defined independently of the adaptive entry rule.

Every opportunity should have at least an identity and timing record even when it does not produce a high-resolution scientific record.

This does not require saving every opportunity as a full image. It requires preserving enough support/provenance to know that the opportunity existed and what the adaptive policy did with it.

For PolliPi, fixed low-resolution probes and per-probe policy/shadow logs are a natural implementation candidate.

## 3. Requirement B — retain audit information before the loss it is meant to audit

T18 shows that refinement and support selection do not generally commute.

If a side-information channel is saved only after an adaptive trigger fires, it cannot describe side information for the opportunities the trigger omitted.

Therefore an audit channel intended to evaluate adaptive capture must be acquired or retained independently of that adaptive capture decision.

Candidate implementations include:

- low-resolution probes on every predefined opportunity;
- a fixed-rate auxiliary stream;
- a target-free reference region or separate camera stream;
- a non-image environmental/reference sensor;
- a probability-sampled audit stream independent of the adaptive policy.

The theory does not prescribe which channel is best. It prescribes the information-order constraint.

## 4. Requirement C — use reversible representation changes where possible

If nuisance/reference processing is applied, do not make the corrected/residual frame the only retained representation.

For a linear decomposition retain at least the equivalent of

\[
(\text{explained},\text{residual})
\]

so that the original observation is reconstructible, or retain the raw observation explicitly as an audit copy.

This prevents a representation algorithm from becoming an irreversible hidden selection/coarsening stage.

## 5. Requirement D — separate record entry from semantic truth

A record being saved and a visit being supported are different questions.

Adaptive capture policy should be represented by a variable such as `K` (record entered / not entered), while visit evidence and truth are stored separately.

This enables a same-system decomposition:

\[
\text{opportunity universe}
\to
\text{entry-selected record}
\to
\text{rich semantic state}
\to
\text{final coarse decision}.
\]

It also prevents missed visits from being silently converted into biological absence.

## 6. Requirement E — preserve unresolved semantic states

A low target score is not independent absence evidence.

Where the available record supports neither a unique visit interpretation nor a unique nuisance interpretation, an unresolved state should remain available.

The empirical question is then not only classification accuracy but how much scientifically useful coverage is obtained at a controlled false-certainty budget.

## 7. Requirement F — diagnose failure mechanisms by intervention

When the observation system fails, threshold retuning should not be the first scientific response.

InsePi supplies a complementary empirical strategy: intervene separately on event-side, nuisance/observability-side, and shared optical conditions and ask which intervention restores the expected response.

This tests the mechanism that produced a failure rather than merely finding another parameterization that fits the same data.

## 8. PolliPi simulation as substantive evidence

The PolliPi simulation programme already contributed substantive method evidence:

- ideal event-matched references demonstrated that nuisance information can in principle improve separation;
- spatial subtraction exposed misregistration and boundary failure mechanisms;
- temporal-subspace V3 showed that useful reference information need not be pixel-corresponding;
- lag and partial-coupling robustness showed that the synthetic gain was not restricted to perfect temporal matching;
- V3–TNOA bridge failures demonstrated that better representation does not automatically authorize stronger semantic decisions;
- trajectory follow-up exposed target overprojection, motivating reversible rather than destructive decomposition.

These are not field-efficacy results, but they are more than engineering preliminaries: they are falsification results that changed the general theory and the design of the empirical system.

## 9. Minimal prospective visitation architecture

A theory-compatible visitation study can use one observation universe with multiple retained channels:

```text
predeclared opportunity i
  -> low-cost primary probe Y_i
  -> optional target-free/reference information R_i
  -> shadow adaptive decision K_i
  -> policy-independent audit / truth sample
  -> if K_i=1, high-information record
  -> rich semantic evidence T/N/O/U
  -> optional final visit/not-visit decision
```

Crucially, `Y_i`, `R_i`, or another audit channel must exist for enough `K_i=0` opportunities to evaluate selection. Otherwise REC-type questions remain unidentifiable from the entered records alone.

## 10. What should be compared empirically

The first field comparison should not be framed as one global leaderboard. It should decompose the observation process.

### Observation allocation

Compare fixed timelapse, any-motion adaptive, and nuisance-filtered adaptive policies under a common opportunity universe and explicit observation cost.

### Reference value

Compare no-reference, valid-reference, and deliberately broken/mismatched-reference representations while retaining raw information.

### Selection consequence

Estimate how adaptive entry changes the target/process composition of retained records relative to the audit universe.

### Semantic consequence

At fixed false-certainty tolerance, compare safely resolvable coverage of rich process-preserving evidence with later binary coarsening.

### Failure diagnosis

Use controlled InsePi-style interventions on cases where the observer behaves unexpectedly.

## 11. Promotion logic

A possible development sequence is:

1. structural theory and executable witnesses;
2. synthetic falsification of candidate representations and acquisition policies;
3. blinded controlled physical intervention;
4. prospective field shadow evaluation with a policy-independent audit channel;
5. only then live adaptive promotion for scientific acquisition.

This preserves the distinction between mathematical results, synthetic mechanism evidence, physical mechanism validation, and ecological transport.

## 12. Compact implication

The general theory does not tell flower-visitation researchers to build a particular camera.

It tells them to build an observation process in which useful information is acquired before it can be lost, loss is auditable from outside the mechanism that caused it, representation changes remain reversible when feasible, and unresolved meaning is not forced into biological absence.
