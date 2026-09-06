# Randomized audit-window protocol

Status: **prospective application protocol derived from the generic observation-information theory**.

The goal is to obtain the two currently missing visitation-validation surfaces with one additional sampling mechanism:

1. independent biological truth on opportunities that include operationally omitted cases;
2. pre-selection primary + target-free reference windows for V3 strict-refinement tests.

The audit mechanism is distinct from the scientific/adaptive selection being audited.

## 1. Two retention variables

For each opportunity `i`, distinguish:

- `K_i` — operational/scientific selection: would the adaptive system retain a high-information record?
- `A_i` — audit inclusion: does an independent probability audit retain a truth/reference window?

Never reuse `K_i` as `A_i`.

The essential requirement is

\[
P(A=1\mid K=0)>0.
\]

Otherwise omitted support remains unaudited by construction.

## 2. Default: equal-rate policy-independent audit

The cleanest design sets

\[
P(A=1\mid K=1)=P(A=1\mid K=0)=q.
\]

Then audit inclusion does not depend on the operational selection state.

`v3.audit_sampling.audit_draw` implements a deterministic hash draw from:

```text
frozen_seed + opportunity_id
```

so the same seed and opportunity ledger reproduce exactly the same sample.

The seed is not a biological secret. It is a reproducibility parameter and may be committed before data collection.

## 3. Optional efficiency design: predeclared selection-stratified audit

When storage is limiting, allow

\[
q_1=P(A=1\mid K=1),\qquad q_0=P(A=1\mid K=0),
\]

with both strictly positive.

For example, one may audit omitted opportunities more heavily than selected opportunities. This is statistically valid only when:

- `q_1` and `q_0` are frozen before inspecting biological truth;
- every audited row retains its inclusion probability;
- population estimates use the known sampling design;
- zero audit probability is never assigned to an estimand-relevant stratum.

The code rejects `q_0=0` or `q_1=0`.

## 4. One audit centre, one combined information package

For a V3 temporal window with `T=9`, an included audit centre should retain the data needed for **both** mechanism and biological audits:

### Primary sequence

- 9 consecutive low-resolution primary probe frames or a scientifically equivalent frozen primary representation;
- four before the audit centre, the centre frame, and four after where feasible.

### Target-free reference sequence

- the corresponding 9-frame target-free reference stream / ROI / sensor representation;
- acquired independently of whether `K=1`.

### Biological truth source

- synchronized high-information truth covering the same interval;
- preferably an independent camera/view or another truth source that does not depend on the adaptive trigger.

### Existing metadata

Join from PolliPi logs:

- opportunity ID;
- operational selection / would-be mode;
- actual saved record;
- decision state and policy version;
- TNOA raw evidence;
- device/site/flower/session provenance.

Thus one randomized audit sample can support V3, REC and TNOA questions without collecting three independent datasets.

## 5. Online implementation concept — ring buffer, not continuous archive

The current PolliPi runtime already captures one low-resolution primary frame per probe but normally discards most raw frames.

A low-storage audit implementation can maintain a rolling in-memory buffer containing at least the previous four primary/reference frames.

At an included audit centre:

1. preserve the previous four buffered primary/reference frames;
2. preserve the centre frame;
3. preserve the next four primary/reference frames;
4. associate the resulting 9-frame window with the audit-centre opportunity ID;
5. preserve/associate the independent truth interval.

This requires a future application implementation; this protocol alone does not modify PolliPi runtime.

## 6. Edge windows

The first/last four probes of a run may not support a complete centred 9-frame window.

Do not silently delete those audit draws after observing outcomes.

Choose and freeze one handling rule before collection, for example:

- sampling is enabled only after a four-probe warm-up, with run termination logic retaining incomplete trailing windows and marking them incomplete; or
- all audit draws are retained in the audit ledger, with `window_complete=false` for windows lacking required frames.

Incomplete-window frequency itself is an observation-process diagnostic.

## 7. Overlapping audit windows

Two included centres can be closer than 9 probes.

This is not a statistical error. The audit centres remain distinct sampled opportunities.

Storage may deduplicate identical physical frames, but the metadata must retain every sampled centre and its inclusion probability. Do not collapse overlapping centres into one sampled opportunity.

## 8. Truth acquisition must not perturb the audited system unnoticed

If audit truth is recorded by the same physical camera, audit capture can itself alter timing, encoding load or scientific recording.

Preferred options:

- independent synchronized truth camera;
- separate continuous/low-duty truth stream on designated audit sessions;
- hardware path proven not to perturb primary acquisition.

If the audit path shares hardware, its effect on the primary observation process must be measured and declared.

## 9. Population inference under probability audit

Let numerical truth be `Z_i`, known only for audited opportunities. With known audit probability `pi_i`, finite-population totals can be estimated by Horvitz–Thompson weighting.

The implementation in `v3.audit_sampling.estimate_selection_from_probability_audit` uses the complete opportunity denominator plus audited truth values to estimate:

- full-universe mean;
- selected mean;
- omitted mean;
- selected-minus-full shift;
- the omitted-support contrast form.

This is the correct route when audit truth is probability sampled rather than complete.

Clustered field inference, variance estimation and biological hierarchical models remain application-specific and should be prespecified separately.

## 10. V3 analysis on the same sample

For each complete audit window, freeze the primary representation and reference representation before held-out scoring.

Test:

- primary-only truth-compatible partition;
- primary + reference truth-compatible partition;
- strict contraction frequency;
- target-preservation / overprojection under nuisance-absent and nuisance-present truth;
- matched versus time-destroyed reference where a valid falsification can be constructed.

Do not use biological truth to choose whether V3 is applied on the same held-out window.

## 11. REC analysis on the same sample

The complete probe ledger supplies `K` and denominator counts; audited truth supplies `Z` on a known probability sample from both retained and omitted opportunities.

Estimate:

\[
\Delta_{sel}=E[Z\mid K=1]-E[Z]
\]

and decompose it into omission amount and retained-versus-omitted contrast.

The audit sample is valuable precisely because it does not disappear when `K=0`.

## 12. TNOA analysis on the same sample

Join the existing TNOA raw evidence to audited truth windows without converting the raw evidence into truth.

Freeze any later mapping from rich evidence to semantic categories on development data, then compare held-out truth ambiguity before and after coarse semantic collapse.

The audit data may reveal that `U` is common. That is a scientific result, not a failure condition.

## 13. Promotion boundary

The randomized audit system is not itself evidence that adaptive capture is superior.

It only creates the data needed to ask, without circularity:

- whether side information is strictly informative;
- whether selection changes the estimand;
- whether semantic coarsening discards relevant distinctions;
- whether observer failures match controlled physical mechanisms.

Only after those quantities are measured should live adaptive promotion be evaluated.
