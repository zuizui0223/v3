# Closed-loop compatible-world theory

Status: **structural synthesis layer**.

This document closes the mathematical interface among V3, REC, TNOA, Boundary and MROD. It does not add a field-accuracy claim. The component projects remain independently reproducible; this file states the common compatible-world geometry that makes their interfaces precise.

## 1. Scientific object

Let \(\Omega\) be a set of possible worlds and let \(\theta:\Omega\to\Theta\) be the scientific distinction or estimand of interest. For any retained observation map \(E:\Omega\to\mathcal E\), the compatible-world fiber at realized evidence \(e\) is

\[
\mathcal C_E(e)=\{\omega\in\Omega:E(\omega)=e\},
\]

and the identified set is

\[
\mathcal I_E(e)=\{\theta(\omega):\omega\in\mathcal C_E(e)\}.
\]

The **identification boundary** is the equivalence relation induced by \(E\): two worlds are equivalent when the current observation map does not distinguish them. Boundary therefore concerns the geometry of the current fibers, not generic sampling uncertainty.

We write

\[
E'\succeq E
\]

when \(E'\) is at least as informative as \(E\) in the present structural sense: every realized fiber under \(E'\) is contained in the corresponding fiber under \(E\). Equivalently, the partition induced by \(E'\) refines the partition induced by \(E\).

## 2. T19 — realized future observation is ordinary refinement

Let \(Q:\Omega\to\mathcal Q\) be a candidate future observation. Before acquisition, its outcome is unknown. After outcome \(q\) is observed, the retained state is

\[
E^+=(E,Q).
\]

For every compatible realized pair \((e,q)\),

\[
\boxed{\mathcal C_{(E,Q)}(e,q)\subseteq\mathcal C_E(e)}
\]

and therefore

\[
\boxed{\mathcal I_{(E,Q)}(e,q)\subseteq\mathcal I_E(e)}.
\]

**Proof.** Every world satisfying both \(E(\omega)=e\) and \(Q(\omega)=q\) necessarily satisfies \(E(\omega)=e\). The identified-set result follows by applying \(\theta\). □

This is the precise bridge between the two refinement branches:

- **V3:** the extra channel already exists and is retained side information;
- **MROD:** the extra channel is selected prospectively, then becomes an ordinary refinement after its outcome is acquired.

The distinction is timing, not compatible-set algebra.

## 3. T20 — sequential non-destructive acquisition gives a nested chain

Let

\[
E_{t+1}=(E_t,Z_{t+1})
\]

where each \(Z_{t+1}\) is retained in addition to the previous record rather than replacing it. Then along the realized sequence,

\[
\boxed{
\mathcal C_{E_0}\supseteq
\mathcal C_{E_1}\supseteq
\cdots\supseteq
\mathcal C_{E_T}
}
\]

and likewise

\[
\boxed{
\mathcal I_{E_0}\supseteq
\mathcal I_{E_1}\supseteq
\cdots\supseteq
\mathcal I_{E_T}.
}
\]

Equality is allowed. Strict refinement is an empirical or model-specific property of the added channel.

This is the structural closed-loop invariant: **if the loop only adds valid retained evidence, compatible-world distinctions cannot become intrinsically coarser.**

## 4. T21 — prospective information value is expected refinement, not guaranteed pointwise shrinkage

Let \(S\) denote the declared residual mechanism variable inside the current admissible region and let \(Q\) be a candidate observation with a coherent predictive joint law. Then

\[
I(S;Q\mid E)
=
H(S\mid E)-H(S\mid E,Q)
\ge 0.
\]

Therefore

\[
\boxed{
\mathbb E[H(S\mid E,Q)]\le H(S\mid E)
}
\]

with strict expected entropy reduction exactly when

\[
I(S;Q\mid E)>0.
\]

This justifies reading the MROD score

\[
V(Q)=I(S;Q\mid A_\epsilon)/K
\]

as **expected prospective refinement of residual mechanism ambiguity** under its declared predictive model.

Important boundary: a positive expected value does **not** imply that every realized outcome must reduce set cardinality by the same amount, nor does zero singleton information rule out informative bundles unless the joint candidate model is also checked.

## 5. T22 — Boundary is the state variable shared by V3 and MROD

Define the current boundary as the partition of \(\Omega\) induced by the retained observation map, optionally projected through \(\theta\) to identified sets.

Then:

1. a V3 side-information augmentation can only refine or preserve the current boundary;
2. a realized MROD-selected observation can only refine or preserve the current boundary;
3. a candidate with zero information about the declared residual mechanism may leave the mechanism boundary unchanged even if it improves measurement precision;
4. in the Boundary project's exact log-linear special case, a new scalar observation changes structural dimension exactly when its row adds rank to the current observation matrix.

Thus Boundary and MROD answer complementary questions:

```text
Boundary: what distinctions remain unresolved now?
MROD:     which feasible future observation is predicted to split them?
V3:       which already-retained side information can split them now?
```

No claim is made that rank, entropy and identified-set diameter are interchangeable metrics. They are different summaries of the same underlying observational-equivalence problem under different model classes.

## 6. T23 — irreversible loss versus new-information recovery

Let \(L\) be a deterministic information-losing transformation of a richer record \(E\). Suppose there exist worlds \(\omega_1,\omega_2\) such that

\[
L(E(\omega_1))=L(E(\omega_2))
\]

but

\[
\theta(\omega_1)\ne\theta(\omega_2).
\]

Then no deterministic downstream map \(g\) receiving only \(L(E)\) can recover that distinction:

\[
g(L(E(\omega_1)))=g(L(E(\omega_2))).
\]

However, a genuinely new or independently retained channel \(Q\) can restore the distinction if

\[
(L(E(\omega_1)),Q(\omega_1))
\ne
(L(E(\omega_2)),Q(\omega_2)).
\]

This gives the exact role of REC and TNOA inside the loop:

- **REC** studies support lost because selection prevents opportunities from becoming rows; audit channels must therefore be retained before or independently of that loss.
- **TNOA** delays semantic coarsening so distinctions still present in rich evidence are not destroyed before the decision boundary.
- **V3/MROD** can refine what remains, or recover a lost distinction only when they supply genuinely independent retained/new information; deterministic reprocessing of an already-collapsed record is insufficient.

## 7. Closed-loop theorem

Consider a sequence of retained states with optional loss operators:

\[
E_t
\xrightarrow{\text{refine/acquire}}
(E_t,Z_{t+1})
\xrightarrow{\text{optional }L_{t+1}}
E_{t+1}.
\]

Then:

### Loss-free segment

If \(L_{t+1}\) is injective on the realized range, or no loss operator is applied, compatible-world and identified sets form a nested non-expanding chain.

### Lossy segment

If \(L_{t+1}\) is non-injective on scientifically distinct states, the boundary may become coarser. No later deterministic processing of \(E_{t+1}\) alone can undo that collapse.

### Recovery

A later independently retained or newly acquired channel may refine the coarsened boundary again. Whether it does so **strictly for the target scientific distinction** is empirical/model-specific.

Hence the safe design rule is

\[
\boxed{
\text{retain before loss; refine with justified information; acquire new information for unresolved distinctions; coarsen only when licensed.}
}
\]

## 8. Relationship to the five projects

| Project | Structural role | Theoretical status |
|---|---|---|
| REC | support-selection / pre-row loss | selection non-identifiability, denominator separation, retention-before-loss, no downstream repair |
| V3 | retrospective refinement by retained side information | compatible-set contraction, coverage transfer, reversible decomposition, refinement-order results |
| TNOA | semantic preservation and controlled coarsening | deterministic coarsening order, unresolved-state preservation, no manufactured certainty |
| Boundary | current observational-equivalence / identification boundary | rank and identified-set characterization under declared observation maps |
| MROD | prospective observation selection | conditional information value and sequential acquisition over residual mechanism ambiguity |

The five projects are therefore not five unrelated theories. They are operators or diagnostics on one compatible-world state space.

## 9. What is now structurally closed, and what remains empirical

Structurally closed:

- definition of compatible worlds and identified sets;
- refinement by retained side information;
- selection loss and its audit boundary;
- semantic coarsening and irreversibility;
- current identification boundary;
- prospective observation as expected refinement;
- realized future observation as ordinary refinement;
- sequential nesting under non-destructive acquisition;
- recovery distinction between deterministic reprocessing and genuinely new information.

Still empirical:

- whether a particular physical reference yields strict contraction;
- whether a particular real selection mechanism materially shifts a target estimand;
- whether an approximate observer represents the compatible-world geometry correctly;
- whether an MROD-selected physical measurement achieves its predicted refinement;
- transport across physical scenes, devices, ecological systems and domains;
- natural biological interpretation beyond the declared observation/mechanism vocabulary.

The theory therefore does **not** require V13 or field data to be mathematically complete. V13 tests whether the strict-refinement and diagnostic consequences survive a blinded physical system.
