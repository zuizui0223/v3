# Methods in Ecology and Evolution submission checklist — Observation

Status: production checklist for the integrated Observation paper.

Official guidance rechecked: **2026-09-09**.

Primary sources:

- Author Guidelines: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/author-guidelines
- Policy on Publishing Code: https://besjournals.onlinelibrary.wiley.com/hub/journal/2041210x/policyonpublishingcode.html

## Article identity

- [x] Planned article type: Standard Research Article.
- [x] Central contribution is a broadly applicable ecological observation method/framework, not a single-taxon result.
- [x] Computational/structural claims are tested with exact finite worlds and frozen simulation/benchmark results before the external empirical block.
- [x] External camera-trap/acoustic data provide reality-facing validation without becoming the definition of the method.

## Initial manuscript requirements

- [x] Anonymous main manuscript title/front matter separated from author metadata.
- [x] Abstract is numbered 1–4 and aims below 350 words.
- [x] Data/Code for peer review statement prepared directly below the abstract.
- [x] Eight or fewer alphabetized keywords prepared.
- [ ] Build single-column, double-line-spaced reviewer manuscript with continuous line numbering and page numbering.
- [ ] Ensure final total word count, including references/captions/statements, remains within the journal's 7,000–8,000-word Standard Article ceiling.
- [ ] Embed or attach final Figures 1–5 with captions where referenced.

## Title page — separate, not for review

Template: `submission/TITLE_PAGE_TEMPLATE.md`.

- [x] Manuscript title prepared.
- [x] Running headline prepared and below 45 characters.
- [ ] Final author names.
- [ ] Institutions and addresses.
- [ ] Corresponding-author postal/email details.
- [ ] Acknowledgements.
- [ ] Author contributions.
- [ ] Funding statement.
- [ ] Conflict-of-interest statement.
- [ ] Final Data Availability / Data Sources wording approved by authors.

These unchecked identity/governance fields must not be inferred automatically.

## Code / reproducibility

- [x] Structural theorem tests and integrated Observation regression tests are in CI.
- [x] Imported quantitative panels are tied to pinned source blobs/results.
- [x] Deterministic Figure 2–5 generators exist.
- [x] Source-text overlap guard exists for old V3 / REC / TNOA abstracts.
- [x] Core Observation bibliography and literature ownership registry exist.
- [ ] **BLOCKER: choose and add a fully open-source software LICENSE.** MEE states that submissions containing code without an accompanying open-source license cannot be considered. License choice is an author/ownership decision and is not selected automatically here.
- [ ] Add the selected license to `pyproject.toml` metadata if appropriate.
- [ ] Build reviewer-only anonymized archive containing the exact submitted code/tests/results/figures and no owner-identifying public repository links or metadata.
- [ ] Retain an external SHA-256 receipt for the final reviewer archive.

## AI / LLM disclosure — author confirmation required

MEE requires a clear Methods statement when LLM/comparable AI tools were used to produce the work, including application name/version; a corresponding or senior author must take responsibility for generated code/text, and generated code should be annotated where required.

A factual draft may state that OpenAI ChatGPT (GPT-5.6 Sol) was used during code review/debugging and manuscript drafting/editing, with mathematical claims and numerical outputs checked through executable tests/CI. **Do not insert a final accountability statement until the responsible author(s) approve it.**

## Research ethics / external data

- [x] No new organismal field experiment is reported by this initial integrated paper; the empirical block reuses external/public camera-trap and acoustic data.
- [ ] Add a concise Methods ethics/data-reuse statement matching the provenance and the terms of the external datasets.
- [ ] Confirm whether any source-specific permits/ethics documentation needs to be cited rather than uploaded, since no new animal use was conducted for this paper.
- [ ] Verify third-party data reuse status before actual upload, as MEE requires public unrestricted reuse or permission.

## Double-anonymous peer review

- [x] Active manuscript does not depend on author-identifying repository self-citation as evidence.
- [x] Old source abstracts are explicitly source/provenance material, not concurrent submissions.
- [ ] Recursively scan the final manuscript, figures, ZIP contents and document/image metadata for author names, emails, GitHub usernames and absolute local paths.
- [ ] Use reviewer-upload ZIP/private archive rather than the public owner-identifying repository in the anonymous article.

## Final scientific gate

- [x] Observation structural theory is closed at T1–T23 under declared assumptions.
- [x] V3/REC/TNOA claim ownership is fixed.
- [x] External empirical REC result is the primary reality-facing endpoint.
- [x] Adverse correction transport is retained rather than rescued.
- [x] TNOA semantic-specific overclaim is blocked by the D5 control.
- [x] U4/U5 prospective design/intervention are excluded from Observation headline novelty and left to Evidence.
- [ ] Re-run the full claim and overlap audits after the final journal-facing manuscript is assembled.

## Final upload gate

Do not submit until all applicable unchecked items above are resolved, especially the open-source LICENSE, author/title-page approval, anonymous reviewer archive, journal-facing word count and final visual/citation audit.
