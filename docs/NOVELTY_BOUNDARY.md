# Novelty boundary

V3 does not claim novelty for SVD, orthogonal projection, background subtraction, compatible-set inclusion, decision-theoretic Blackwell-style information ordering, partial identification, missing-data selection, or abstention in isolation.

The candidate contribution is the **observation-design synthesis**:

1. target-free reference information is treated as retained side information rather than a nuisance label;
2. measurement-side uncertainty is represented by compatible states/sets rather than automatically collapsed to a point correction;
3. decomposition is non-destructive when possible, retaining enough channels to reconstruct the original observation;
4. record-entry selection is recognized as a distinct upstream support-loss operation that downstream classifiers cannot repair;
5. semantic commitment is treated as a separate entitlement step, so richer representation does not automatically license a more certain biological statement;
6. all three operations are described in one compatible-world information order.

The paper should therefore avoid claims such as “we introduce a new SVD denoising algorithm.” The stronger and safer claim is:

> **We formulate reference refinement, record-entry selection, and semantic coarsening as distinct information operations on an observation pipeline, derive their compatible-set consequences, and use those consequences to specify what must be retained before irreversible loss.**

## Empirical boundary

The structural propositions do not establish the value of a physical reference. Real-data work is required to estimate or validate:

- physical reference informativeness;
- compatible-set calibration;
- target/nuisance overlap in a domain;
- finite-sample representation stability;
- application transport;
- named causal nuisance attribution.
