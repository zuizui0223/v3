# Third-party data rights — integrated Observation paper

Status: submission-governance carryover from the REC source audit; **not legal advice**.

## BirdVox-full-night

Source used by the integrated acoustic irreversibility analysis:

- BirdVox-full-night v3.0, Zenodo record `1205569`, DOI `10.5281/zenodo.1205569`.
- Creators: Vincent Lostanlen, Justin Salamon, Andrew Farnsworth, Steve Kelling, Juan Pablo Bello.
- Zenodo states that the dataset is available under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Submission state: **clear for reuse with attribution**. Cite the dataset and retain the licence acknowledgement in the Data Sources / Data Availability material.

## Findlay camera-trap/CCTV source

Source used by the integrated record-entry selection and correction analyses:

- Findlay, Briers & White (2020), *Mammal Research* 65:167–180, DOI `10.1007/s13364-020-00478-y`;
- the article explicitly points readers to the associated `CT-Detection` GitHub repository for the R file and datasets;
- the article is published open access under CC BY 4.0;
- the linked GitHub repository itself does not currently expose a root/machine-readable software/data licence.

The REC source audit therefore judged the public-reuse evidence to be strong but recommended obtaining short written confirmation from the data owner/corresponding author before full MEE submission, because MEE asks authors to confirm that third-party datasets are unrestricted for reuse or used with permission.

Submission state: **written clarification recommended / not yet recorded in the integrated Observation package**.

## Required pre-upload action for Findlay data

Archive a confirmation covering:

1. reanalysis of the linked public CSV data;
2. publication of derived numerical summaries and figures;
3. the preferred citation/licence wording for those linked datasets.

Do not redistribute the original source CSV files in the anonymous reviewer archive unless the confirmed terms explicitly permit it. Prefer pinned acquisition scripts/hashes and derived manuscript-facing summaries where sufficient for review.

## Distinguish data rights from our software licence

Third-party source-data terms and the Observation code licence are different blockers:

- BirdVox / Findlay terms govern reuse of external data;
- the missing root open-source `LICENSE` in `v3` governs reuse of the submitted Observation code and must be chosen separately by the author(s).

## Provenance

Carried from `zuizui0223/rec/THIRD_PARTY_DATA_RIGHTS_H1_H5.md`, source blob `360c20f24a5b641ff2c53ce0087868ec777a6464`, with BirdVox creator metadata checked against Zenodo record `1205569` on 2026-09-09.
