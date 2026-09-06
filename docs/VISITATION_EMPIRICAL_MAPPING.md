# Mapping the generic empirical audit to flower-visitation observation

Status: **domain instantiation only**. The generic theory and audit protocol are defined without flower visitation. This note maps the generic opportunity schema onto PolliPi/InsePi-style observation systems.

## 1. Choose the opportunity universe at the decision cadence

If an adaptive policy evaluates one probe every 5 seconds, define one opportunity per 5-second decision epoch:

\[
i=(\text{camera},\text{session},\text{probe epoch}).
\]

Do not define the opportunity universe only from files that were actually saved. That would condition the denominator on the selection mechanism under study.

A 30-second plain-timelapse still is useful as a policy-independent baseline record, but it does not by itself provide truth for every 5-second opportunity. Truth/audit coverage must match the estimand and decision cadence.

## 2. Generic field mapping

| Generic field | Visitation-observation candidate |
|---|---|
| `opportunity_id` | device/session/probe-epoch ID created regardless of trigger |
| `selected` | whether adaptive policy would save denser still / candidate clip / retained scientific row |
| `estimand_value` | predeclared numeric truth such as visit indicator, contact duration, taxon score, or another domain estimand |
| `truth_state` | independent review/control state: visit, nuisance, overlap, unresolved, etc. under a frozen truth rubric |
| `primary_key` | frozen primary-image/probe representation before side-reference refinement |
| `side_key` | frozen target-free/reference state used to test strict refinement |
| `audit_key` | selection-independent low-cost reference, independent camera/video, or audit stratum |
| `rich_evidence` | process-preserving evidence state before final binary visit/no-visit collapse |
| `coarse_label` | final operational/scientific simplified label |

The exact truth vocabulary is not prescribed by the general theory.

## 3. PolliPi role

PolliPi supplies three empirically useful surfaces:

### A. Opportunity and policy ledger

The low-resolution probe cadence can define the decision opportunities, while shadow logs record what each policy *would have done* without requiring live adaptive selection during development.

This directly supports support-selection analysis.

### B. Fixed versus adaptive allocation

The scientific comparison remains:

- fixed scheduled still allocation;
- any-motion responsive allocation;
- nuisance-filtered adaptive allocation;
- optional candidate video as a separate high-information product.

For each policy, calculate retention fraction and biological/process contrast between retained and omitted opportunities rather than treating image count as event frequency.

### C. Synthetic mechanism evidence

The existing PolliPi simulations remain useful for predeclaring nuisance families, counterexamples, and failure modes. They should inform the physical validation design without being counted as natural-field efficacy evidence.

## 4. InsePi role

InsePi contributes **mechanism truth**, not automatically biological visit truth.

Controlled intervention blocks can establish whether an observation failure is event-side, nuisance/observability-side, shared-optical, or no-fault under the frozen physical protocol.

This is especially valuable for:

- validating that a proposed reference channel responds to the intended measurement-side perturbation;
- testing whether representation changes are entitled under nuisance-present versus nuisance-absent conditions;
- separating observer failure from ecological absence;
- producing controlled physical examples before natural-field transport.

InsePi does not by itself estimate natural visitation prevalence.

## 5. V3-style empirical question

For each truth-scored opportunity, compare the truth-state partition under:

\[
\text{primary only}
\]

and

\[
\text{primary + target-free side information}.
\]

Report strict refinement frequency/cardinality gain on held-out opportunities.

Also preserve nuisance-absent and weak-coupling opportunities. A reference that appears useful only when strong nuisance is present may still be valuable, but an unconditional correction rule must not be licensed by that result.

The preferred representation remains reversible or set-valued:

\[
(Y,R,\text{explained},\text{residual})
\]

rather than only a corrected image.

## 6. REC-style empirical question

Let `K_i` denote whether the adaptive policy would retain opportunity `i` at the relevant scientific resolution.

For a predeclared numerical estimand `Z_i`, estimate:

\[
\Delta_{sel}=\bar Z_{K=1}-\bar Z.
\]

Decompose it as:

\[
\Delta_{sel}=P(K=0)(\bar Z_{K=1}-\bar Z_{K=0}).
\]

This gives two directly interpretable quantities:

1. how much of the opportunity universe the policy discards;
2. how biologically/process-different the discarded opportunities are.

The second term requires truth/audit information on omitted support. A selected-only event table cannot supply it.

## 7. TNOA-style empirical question

Before final visit/no-visit collapse, retain a richer evidence state that can distinguish, when supported:

- target-positive evidence;
- nuisance-positive evidence;
- observability/measurement support;
- overlap;
- unresolved/no-support states;
- independently justified absence evidence if available.

Then quantify what truth distinctions are merged by the later coarse label.

The goal is not to ban binary outputs. It is to keep the rich scientific record available so the binary decision does not become irreversible evidence loss.

## 8. Minimum prospective visitation bundle

A strong prospective field dataset should retain:

1. complete 5-second (or other frozen cadence) opportunity IDs;
2. shadow policy decision for every opportunity;
3. low-cost primary probe provenance for every opportunity;
4. side/reference channel before selection when testing V3-style refinement;
5. probability-sampled or independent high-information truth covering **both selected and omitted** opportunities;
6. rich evidence state before binary collapse;
7. recording day / scene / flower / camera grouping identifiers;
8. exact policy, threshold, and representation version IDs.

This allows one observation universe to answer multiple questions without defining any of the general theories in visitation-specific terms.

## 9. Practical truth options

Depending on cost and field conditions, truth can be supplied by:

- synchronized continuous/high-duty-cycle video on an audit subset;
- a second independent camera view;
- manual review of probability-sampled probe windows including omitted opportunities;
- controlled staged events for physical validation;
- sensor/intervention logs for nuisance/observability truth.

The biological and physical truth channels can be different. That separation is desirable when the scientific question requires both event truth and observer-mechanism truth.

## 10. Research sequence

1. use PolliPi simulation to preserve/falsify candidate mechanisms;
2. use InsePi-style controlled physical intervention to validate observation-mechanism effects;
3. freeze opportunity, side-information, selection, and semantic contracts;
4. collect prospective visitation opportunities with audit truth on selected and omitted support;
5. test V3-style strict refinement, REC-style selection shift, and TNOA-style coarsening loss as separate estimands;
6. only then evaluate whether adaptive capture improves ecological efficiency without unacceptable information loss.

The final question is therefore not merely whether the detector finds insects. It is whether the observation system uses limited recording effort while preserving enough information to audit what was refined, omitted, and left unresolved.
