# General observation-information theory

Status: **application-independent conceptual/mathematical core**.

This document deliberately does **not** define a flower-visitation pipeline. V3, REC and TNOA are treated as three recurring information operations that may appear in any scientific observation system: imaging, acoustics, microscopy, industrial inspection, remote sensing, medical monitoring, behavioural sensing, ecological monitoring, or other measurement domains.

## 1. Scientific object

Let `Omega` be a set of latent worlds `omega`. A world contains the process of interest, measurement-side states, observation opportunities, and any latent variables needed by the scientific estimand.

An observation map

\[
X:\Omega\to\mathcal X
\]

induces a compatible-world fiber

\[
\mathcal C_X(x)=\{\omega\in\Omega:X(\omega)=x\}.
\]

For an estimand `theta`, its identified set under `X=x` is

\[
\mathcal I_X(x)=\{\theta(\omega):\omega\in\mathcal C_X(x)\}.
\]

The theory asks how scientific observation systems change these compatible sets before a final estimate or decision is made.

## 2. Three information operations

### 2.1 Refinement

A refinement adds retained information rather than replacing an existing observation. If `R` is an added side-information channel,

\[
X^+=(X,R).
\]

Then

\[
\mathcal C_{X^+}(x,r)\subseteq\mathcal C_X(x)
\]

and therefore

\[
\boxed{\mathcal I_{X^+}(x,r)\subseteq\mathcal I_X(x).}
\]

The inclusion may be equality. The theorem says only that retained side information cannot make the information set intrinsically poorer. Whether a physical reference is actually informative is empirical.

**V3 is one refinement theory:** target-free reference information is used to restrict measurement-side compatible states before interpretation.

### 2.2 Selection

A selection operator retains only part of the support of a richer observation universe. Let a full exposure/record object be `L`, with a retention indicator `K`. A selected record is

\[
S_K(L).
\]

Selection is generally many-to-one: different full worlds can produce the same retained record after omitted units leave no row.

Thus a downstream analyst who sees only `S_K(L)` cannot in general identify properties of the omitted support without information retained independently of `K`.

**REC is one selection theory:** it studies what can and cannot be learned about observation opportunities or events that fail to enter a scientific record.

### 2.3 Coarsening

A coarsening maps a rich retained record `E` to a simpler semantic state

\[
C=c(E).
\]

Because `c` is deterministic,

\[
\mathcal C_E(e)\subseteq\mathcal C_C(c(e))
\]

and hence

\[
\boxed{\mathcal I_E(e)\subseteq\mathcal I_C(c(e)).}
\]

Semantic simplification can be useful operationally, but it cannot create distinctions absent from the richer evidence.

**TNOA is one coarsening/entitlement theory:** preserve distinct positive evidence and unresolved states until a unique semantic conclusion is justified.

## 3. These are operator types, not a mandatory three-step pipeline

The theory does not require every system to execute

`V3 -> REC -> TNOA`

in that literal order.

A real observation system may contain:

- several refinement operations;
- repeated selections at acquisition, triggering, storage or analysis;
- several semantic coarsenings;
- no useful side-information channel at all;
- feedback between stages.

The useful abstraction is the **type of information operation**, not a domain-specific flow chart.

## 4. No-downstream-repair theorem

Let `T` be any deterministic transformation of a rich retained state `X`, and suppose two latent worlds satisfy

\[
T(X(\omega_1))=T(X(\omega_2))
\]

while the scientific quantity of interest differs:

\[
\theta(\omega_1)\neq\theta(\omega_2).
\]

For every deterministic downstream transformation `g`,

\[
g(T(X(\omega_1)))=g(T(X(\omega_2))).
\]

Therefore no downstream processing that receives only `T(X)` can recover the distinction lost by `T`.

This applies equally to:

- rows omitted by a selection rule;
- rich evidence collapsed to a binary state;
- a measurement representation irreversibly replaced by a residual-only transform.

The theorem does **not** say recovery is impossible if new independent information is acquired later. It says post-processing of the already-coarsened object cannot recreate distinctions that object no longer contains.

## 5. Retention-before-loss principle

Suppose a scientific audit will later need a side-information variable `R` to distinguish states that a selection rule `K` may omit.

If `R` is retained only when `K=1`, then the selected reference record still contains no information about `R` in the omitted support. A reference intended to audit selection must therefore be acquired or logged before, or independently of, the selection being audited.

General design rule:

\[
\boxed{\text{retain audit information before the irreversible loss it is meant to diagnose.}}
\]

This is not specific to event cameras. It applies to missing laboratory measurements, filtered telemetry, quality-control rejection, clinical triage records, remote-sensing cloud masks, and other selected data products.

## 6. Reversible transformation versus irreversible replacement

A transformation need not be information-losing. If derived channels jointly reconstruct the original observation, the representation can be lossless.

For a linear decomposition,

\[
E=PY,\qquad Z=(I-P)Y,
\]

we have

\[
Y=E+Z.
\]

Thus retaining `(E,Z)` is reversible. Retaining only `Z` need not be.

The generic lesson is:

> **Computation is not the same as information loss. Loss occurs when a non-injective representation replaces richer retained information.**

## 7. Decision-theoretic consequence

For any fixed finite decision problem and loss, a decision maker with a richer retained observation can always ignore extra information and emulate any rule available from a poorer observation.

Therefore the minimum achievable risk under richer retained information is weakly no worse than under its deterministic coarsening.

This is an information-order statement, not a guarantee that a particular trained model or heuristic will exploit the richer record correctly.

## 8. Compatible-set preservation as the safe default

When the available observation does not point-identify the requested quantity, the output should remain set-valued or explicitly unresolved.

Three general safe defaults follow:

1. **refinement:** add justified information without discarding the original record;
2. **selection:** preserve the denominator / opportunity ledger needed to audit what was omitted;
3. **coarsening:** preserve unresolved alternatives rather than inventing a unique label.

These are different implementations of one principle:

\[
\boxed{\text{do not turn missing information into manufactured certainty.}}
\]

## 9. Relation among the three sister methods

| Theory | Information operation | Generic question |
|---|---|---|
| V3 | refinement | What additional retained information can validly contract measurement-side compatible states? |
| REC | selection | What information disappears because some opportunities or records never enter the retained dataset? |
| TNOA | semantic preservation / coarsening | What semantic conclusion is justified by the retained evidence, and what must remain unresolved? |

The theories are sisters because they operate on the same compatible-world geometry, not because they were designed for the same biological application.

## 10. What remains empirical

The structural results above do not establish:

- that any particular reference channel is informative in nature;
- that a practical selection mechanism creates scientifically important bias;
- that a particular rich semantic representation improves a downstream ecological estimate;
- that an approximate observer represents the true compatible-set geometry well;
- transport across domains.

Those questions require empirical systems.

## 11. Empirical systems are tests, not definitions

PolliPi and InsePi are useful because they make otherwise abstract losses observable and manipulable:

- PolliPi can compare fixed versus adaptive acquisition policies and preserve shadow/provenance information;
- InsePi can intervene on candidate failure mechanisms to determine whether a representation defect is event-side, nuisance-side, shared-optical, or unresolved.

Neither system defines the general theory. They are candidate experimental platforms for testing consequences of the theory.

## 12. Compact formulation

The most general formulation is:

> **Refine before irreversible loss; preserve the support needed to audit selection; retain semantic alternatives until evidence licenses contraction.**

Or more compactly:

\[
\boxed{\text{Add information when justified. Preserve information when loss is avoidable. Do not claim distinctions the retained record cannot support.}}
\]
