# Literature positioning for general observation-information theory

Status: **novelty audit / positioning note**. This document is deliberately conservative: it separates classical ingredients from the candidate contribution of the present framework.

## 1. Core conclusion

The individual mathematical ingredients of the current 18-proposition ledger should **not** be presented as wholly new mathematics.

There are strong established neighbours in:

- comparison and value of information;
- deterministic data processing / sufficient representations;
- coarsened and missing data;
- partial identification;
- unified measurement-error / missing-data frameworks;
- selective labels and decision-dependent missingness;
- imperfect detection and observation-process decomposition in ecology.

The candidate contribution is instead the **observation-system synthesis**: refinement, support selection, and semantic coarsening are treated as different information operations whose composition, timing and order determine what can still be identified, audited, or safely concluded.

## 2. Blackwell informativeness — direct foundation for refinement and decision risk

Blackwell's comparison of experiments gives the clearest classical foundation for the statement that a richer experiment weakly dominates a garbled one across decision problems.

Relevant references:

- Blackwell, D. (1951). *Comparison of Experiments*. Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, 93–102.
- Blackwell, D. (1953). *Equivalent Comparisons of Experiments*. Annals of Mathematical Statistics 24(2):265–272. DOI: 10.1214/aoms/1177729032.

Implication for this project:

- T1 reference refinement and T7 decision-risk ordering belong in the Blackwell/value-of-information neighbourhood;
- they are useful structural foundations, not standalone novelty claims;
- the present framework differs by applying information ordering to the **design and retention history of a scientific observation system**, including support deletion and semantic collapse, rather than only comparing alternative experiments/signals presented to a final decision maker.

## 3. Data processing, sufficiency and injective recoding

The idea that downstream processing cannot create information absent from its input is standard in information theory and statistics. The data-processing inequality formalizes non-increase of mutual information under post-processing. Sufficient-statistic theory formalizes when a reduction retains all information relevant to a parameter.

Implication for this project:

- T16 no-downstream-repair is structurally aligned with data-processing logic;
- T17 injective-recoding invariance is elementary information preservation;
- T6 reversible decomposition is a concrete linear-algebraic instance of the same principle.

The contribution should therefore not be phrased as discovering that reversible transforms preserve information. The useful observation-design step is to make **injectivity / reversibility an explicit scientific requirement before derived representations are allowed to replace raw records**.

## 4. Coarsened and missing data — direct foundation for support selection

Heitjan and Rubin developed a general model of coarse data including rounded, censored, categorized and missing observations, with conditions under which the coarsening mechanism is ignorable.

Reference:

- Heitjan, D.F. & Rubin, D.B. (1991). *Ignorability and Coarse Data*. Annals of Statistics 19(4):2244–2253.

The key connection is that a scientific record can be a coarsened observation of a richer latent/full-data object. When coarsening or missingness is stochastic and nonignorable, treating the retained sample as if selection were fixed can be misleading.

Implication for this project:

- T13 support-selection non-identifiability and T14 denominator-not-state are close to standard missing/coarse-data logic;
- the present framing emphasizes a design-stage distinction between **support deletion** (a row/opportunity disappears) and **semantic coarsening** (a retained row loses distinctions), because the audit information required for the two losses is different.

## 5. Partial identification — direct foundation for preserving compatible sets

Manski's partial-identification programme explicitly asks what can be inferred from available evidence without adding assumptions strong enough to force point identification. Missing data naturally generate identification regions obtained from all compatible completions of the unobserved part.

Reference:

- Manski, C.F. (2005). *Partial identification with missing data: concepts and findings*. International Journal of Approximate Reasoning 39:151–165. DOI: 10.1016/j.ijar.2004.10.006.

Implication for this project:

- set-valued V3/TNOA representations should be positioned as an application of partial-identification logic to observation-system states;
- the novelty claim is not “we invented unresolved sets,” but that **measurement-side compatible sets, omitted-support compatible completions, and semantic unresolved states can be placed in one retention architecture**.

## 6. Existing unified measurement-error and missing-data frameworks — a major novelty constraint

There are already explicit frameworks that unify measurement error and missing data, so the present work must not claim novelty simply for placing those two problems under one umbrella.

Relevant references:

- Blackwell, M., Honaker, J. & King, G. (2017). *A Unified Approach to Measurement Error and Missing Data: Overview and Applications*. Sociological Methods & Research 46(3):303–341. DOI: 10.1177/0049124115585360.
- Blackwell, M., Honaker, J. & King, G. (2017). *A Unified Approach to Measurement Error and Missing Data: Details and Extensions*. Sociological Methods & Research 46(3). DOI: 10.1177/0049124115589052.
- Edwards, J.K., Cole, S.R. & Westreich, D. (2015). *All your data are always missing: incorporating bias due to measurement error into the potential outcomes framework*. International Journal of Epidemiology 44(4):1452–1459. DOI: 10.1093/ije/dyu272.

These works show that measurement error can be handled jointly with missingness / other bias sources within established inferential frameworks.

Implication for this project:

- **“measurement error + missingness are one problem” is not a defensible novelty claim**;
- our remaining distinction is that we focus on **what an observation system must acquire and retain before those inferential problems exist as a dataset**, and on how later support selection or semantic collapse can erase previously available audit information;
- the order-sensitive acquisition claim (T18) and the separation between reversible representation, support deletion and semantic coarsening therefore become more central to the contribution.

## 7. Selective labels — a close analogue for decision-dependent truth availability

The selective-labels literature shows that labels/outcomes can be observed only for cases admitted by a previous decision. In such systems, evaluation on the observed labels can be badly misleading because the observed outcome sample is itself decision-selected.

Reference:

- Lakkaraju, H., Kleinberg, J., Leskovec, J., Ludwig, J. & Mullainathan, S. (2017). *The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables*. KDD 2017:275–284. DOI: 10.1145/3097983.3098066.

Implication for this project:

- REC's warning that entered records cannot identify the biological/process composition of non-entered opportunities has a clear conceptual neighbour;
- T18 order sensitivity sharpens the observation-design consequence: a reference/audit stream acquired only after the same selection cannot resolve the selected-away support.

## 8. Measurement science — neighbouring emphasis on observation equations and uncertainty

Measurement science already treats observations as outputs of explicit measurement/observation models and emphasizes propagation and reporting of measurement uncertainty.

A relevant entry point is NIST work on measurement uncertainty and observation equations (e.g. Possolo and collaborators).

Implication:

The present framework should not claim novelty for representing measurement uncertainty itself. Its proposed extension is to connect measurement-side uncertainty to **later support retention and semantic retention decisions** and to specify when audit channels must exist relative to those losses.

## 9. Ecology already recognizes multi-stage detection loss

Ecological observation literature already separates detection into component processes and documents that missed events alter downstream inference.

Examples:

- Findlay, M.A., Briers, R.A. & White, P.J.C. (2020). *Component processes of detection probability in camera-trap studies: understanding the occurrence of false-negatives*. Mammal Research 65:167–180. DOI: 10.1007/s13364-020-00478-y. This work separates pass, trigger, registration and image-quality processes and uses independent CCTV reference observations.
- Dokter et al. (2017). *Analyzing time-ordered event data with missed observations*. Ecology and Evolution. DOI: 10.1002/ece3.3281. This work models how missed events distort event-time data.
- Santoro et al. (2025). *Essential tools but overlooked bias: Artificial intelligence and citizen science classification affect camera trap data*. Methods in Ecology and Evolution. DOI: 10.1111/2041-210X.70132. This shows that classification error can propagate into downstream ecological estimates.

Implication:

The visitation application should not claim novelty for the generic fact that cameras miss events or classifiers bias ecological estimates. Its value is to instantiate the more general information-order requirements in a prospective observation system with explicit pre-selection audit channels, adaptive allocation, reference refinement and unresolved semantic states.

## 10. Where the candidate novelty now sits

The strongest defensible contribution is **not any one theorem and not the mere unification of measurement error with missing data**. It is the combination of the following design claims in one compatible-world framework:

1. **three operation types are distinguished** — refinement, support selection and semantic coarsening;
2. **the operations need not form one fixed pipeline** and may recur in different orders;
3. **order matters** — refinement and selection are not generally commutative when side information is unavailable on omitted support;
4. **audit information has a timing requirement** — information intended to diagnose a loss must be retained before or independently of that loss;
5. **representation changes are classified by injectivity/reversibility**, separating harmless computation from irreversible retention loss;
6. **partial identification is propagated across measurement, support and semantics** rather than resolved by forced point corrections or binary labels;
7. **synthetic and physical failures are used diagnostically** to determine which representation or retention assumption is invalid, rather than merely retuning a final classifier;
8. the framework is intended to operate **at observation-system design time**, before a final analysis dataset has silently inherited the system's losses.

This is an observation-system methodology claim, not a claim to have replaced Blackwell, missing-data theory, partial identification, measurement science or ecological detection theory.

## 11. PolliPi simulation in this positioning

PolliPi's synthetic programme is useful precisely because it supplied counterexamples that forced the general theory away from a detector-specific architecture:

- spatial subtraction failure showed that apparently informative references can fail through representation mismatch;
- temporal-subspace success showed that strict spatial correspondence is unnecessary when temporal coupling is informative;
- lag/partial-coupling robustness gave controlled evidence that the gain was not limited to perfect matching;
- bridge false-certainty failure showed that upstream information gain does not itself license downstream semantic commitment;
- trajectory overprojection showed that a derived representation can destroy target information even when its reference is target-free.

These results are therefore best described as **mechanism-discovery and falsification evidence** for the observation-information framework. They remain synthetic-domain results, not field efficacy evidence.

## 12. Current claim language

Avoid:

> We introduce a new general theory of information ordering.

Avoid:

> We unify measurement error and missing data for the first time.

Avoid:

> We prove for the first time that post-processing cannot recover lost information.

Prefer:

> We synthesize established information-order, coarsening, measurement-error and partial-identification principles into an observation-system framework that distinguishes information refinement, support selection and semantic coarsening, derives order-sensitive acquisition and retention requirements, and connects those requirements to executable sensing-system designs.

A stronger novelty claim should be made only after a broader systematic search fails to identify a prior framework making this same cross-layer **acquisition-time + retention-time + semantic-time** synthesis.
