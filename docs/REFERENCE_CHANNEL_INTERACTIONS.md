# Multi-reference complementarity on the audit-burden scale

Status: **finite-world design diagnostic**.

A general observation system may retain several side-information channels: another image region, a second camera, illumination sensor, inertial sensor, acoustic reference, or other measurement-side information. Evaluating channels one at a time can miss two opposite cases:

- two channels may be largely redundant;
- two channels may be individually uninformative yet jointly resolve an ambiguity.

Using worst-case audit burden

\[
B(O)=\log_2 m^*(O,\theta),
\]

let

\[
B_0=B(O),\quad
B_1=B(O,R_1),\quad
B_2=B(O,R_2),\quad
B_{12}=B(O,R_1,R_2).
\]

The isolated reliefs are

\[
G_1=B_0-B_1,\qquad G_2=B_0-B_2,
\]

and joint relief is

\[
G_{12}=B_0-B_{12}.
\]

Define the burden interaction

\[
\boxed{I_B=G_{12}-G_1-G_2=B_1+B_2-B_0-B_{12}.}
\]

Interpretation under this specific worst-case metric:

- `I_B > 0`: **complementary** — the pair resolves ambiguity that isolated channels do not account for additively;
- `I_B < 0`: **redundant** — isolated relief overlaps;
- `I_B = 0`: additive on this scale.

The conditional marginal value of `R2` after already retaining `R1` is

\[
G_{2|1}=B_1-B_{12}.
\]

This is often more useful for sensor design than the isolated value `G2`.

## Design implication

Do not select a target-free reference solely because it performs best as a single channel. A weak individual channel can be valuable in combination if it resolves a different ambiguity. Conversely, two individually strong references may be wastefully redundant.

For V3-like applications this means the candidate reference set can include heterogeneous channels rather than one privileged image ROI. The theory remains target/application independent.

## Boundary

`I_B` is not Shannon interaction information, mutual information synergy, PID, or a causal interaction measure. It is a combinatorial interaction of **worst-case point-identification audit burden** in a supplied finite world model.

With incomplete empirical truth, plug-in values can underestimate the real burden and therefore can also mischaracterize channel interaction. Held-out or probability-audit truth remains necessary for empirical use.
