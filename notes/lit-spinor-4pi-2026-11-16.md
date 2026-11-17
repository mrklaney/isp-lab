# Literature check: spinors / 4π periodicity in ISP (2026-11-16)

Prior-art check for notebook 19 (`19_spinors_as_memory.ipynb`). Done using the arXiv API, Barandes's arXiv
author page and general web search. There was no Google Scholar or PhilSci full-text access, so treat it as a careful
search, not an exhaustive one.

## Verdicts

1. **Spin-½, 4π or SU(2) inside ISP: nothing found.** arXiv's index lists 8 papers matching "indivisible stochastic", and
   "indivisible + stochastic + spin" returns 0.
   - The only spin passage is Barandes, arXiv:2507.21192 §4.2 "Dilations". It adds spin by enlarging the Hilbert space with a
     D-dimensional representation of **SO(3)**, and says nothing of SU(2), the double cover or 4π. This is the hook for nb19:
     on 2 configurations, no such representation reproduces spin-½.
   - Papers checked and found silent on this: 2302.10778, 2309.03085, 2602.01043 (mentions "spinors" only in passing),
     2512.18105, Calvo 2601.18720, LeBlond 2511.02863, Egri et al. 2602.23491, Doukas 2602.22095.
2. **"Continuous symmetry on discrete configurations forces indivisibility": partially anticipated.** The math is classical.
   - A stochastic matrix with a stochastic inverse is a permutation (e.g. Ding & Rhee, Missouri J. Math. Sci. 26(1), 2014).
     Barandes uses it in 2302.10778 §3.5 and 2309.03085 fn. 5.
   - Pimenta, arXiv:2505.08785: "a continuous path connecting the identity and the permutation is necessarily
     indivisible" (two configurations).
   - No paper states it for rotation groups (SO(3) or SU(2)) or Lie-group symmetries. Nb19 presents the lemma as known and the
     rotation application as the addition.
3. **"The minimal composing lift is projective (SU(2)), so 4π is the price of composition": not in ISP; partial precedent
   elsewhere.**
   - Doukas 2602.22095 has the general idea that a Hilbert-space lift gives a composable description where the kernels have
     none, but nothing on SU(2).
   - The mechanism sits in Barandes's Schur–Hadamard gauge freedom of Θ (2302.10778; 2507.21192).
   - Nelson-school precedent: Dankel, Arch. Rational Mech. Anal. 37, 192 (1970); Dohrn, Guerra & Ruggiero, LNP 106 (1979);
     Faris, Found. Phys. 12, 1 (1982); Guerra & Marra, PRD 30, 2579 (1984). These are Markov diffusions, a different mechanism.
     Nelson's review reportedly credits them with explaining integer vs half-integer spin; that quote was seen only in a
     search summary.
4. **Neutron 4π as non-Markovian memory, or Γ detecting π1(SO(3)) = Z2 through path dependence: nothing found.** Only
   standard material (Rauch 1975; Werner 1975; arXiv:1601.07053 critique; Bernstein, Nature 315, 42 (1985)) and classical spin
   models (Christian 1211.0784; Baylis et al. 0710.3144) with no memory or indivisibility framing.

## Residual risk

- The Dankel, Faris and Dohrn–Guerra full texts were not read, only abstracts. These are the main risk for claim 3.
- Aharonov–Susskind (1967) and Bell (1966) were not re-read.
- Phrase novelty as "not found in the ISP literature as of Nov 2026".

## Independent audit (2026-11-16, same day): outcome

Two adversarial auditors (correctness; novelty/attribution) plus a theorem check of 2309.03085. The audit reports are not included here. All fixes applied; nb19 retitled "a Γ-Level Synthesis".

- **Downgraded to KNOWN:**
  - rotation ⇒ indivisibility: Barandes 2302.10778 §2.1 eq. 7; Pimenta 2505.08785 §§III–IV; Kingman 1962; Goodman 1970.
  - "720° is the price of a composing lift": Wigner–Bargmann projective representations.
  - Γ depends on the homotopy class: Schulman, Phys. Rev. 176, 1558 (1968); Kult–Åberg–Sjöqvist arXiv:0711.2140 (4π as a channel holonomy).
  - Interference as indivisibility: Barandes §§3.5, 3.7.
  - The relational sign: Aharonov–Susskind 1967.
  - The hidden-SU(2) escape hatch: Dankel 1970; Dohrn–Guerra–Ruggiero 1979.
- **Corrected:**
  - The "no generator" argument was invalid. A time-dependent rate tan(θ)/2 is divisible for turns of at most 90°, and Γ(t)Γ(s)⁻¹ is stochastic iff |cos t| ≤ |cos s|. (The auditor's own counterexample Γ(2.0)Γ(1.0)⁻¹ was in fact stochastic; corrected in the tests.)
  - The 720° and Z2 results need the arm-A law to have determinant 1 (no spin-independent energy). A phase-shifted law has the same isolated Γ and no 720° effect. "Isotropy fixes the sign" was wrong.
- **Barandes 2507.21192 §4.2 (p28) is hypothetical.** Quote: "If one wished to introduce spin as a dilation-emergeable, one could merely dilate … introduce a D-dimensional representation of SO(3)". "SU(2)", "double cover" and "spinor" are absent from Papers 1 and 3.
- **2309.03085 is a representation theorem, not a derivation.**
  - §4.1, eq. 69: "Every indivisible stochastic process can be regarded as a subsystem of a unistochastic process" (finite N).
  - §5.7 covers the dilation, with N ≤ Ñ ≤ N³.
  - §3.5: every 2×2 doubly stochastic matrix is unistochastic.
  - It says nothing on spin or rotations. "Open problem" was narrowed accordingly.
- **Metadata verified via Crossref (2026-11-16):**
  - Dankel, "Mechanics on manifolds and the incorporation of spin into Nelson's stochastic mechanics", ARMA 37, 192–221 (1970), doi 10.1007/BF00281477.
  - Rauch, Zeilinger, Badurek, Wilfing, Bauspiess, Bonse, Phys. Lett. A 54, 425–427 (1975): Bonse confirmed as an author.
  - Faris, "Spin correlation in stochastic mechanics", Found. Phys. 12, 1–26 (1982), doi 10.1007/BF00726872. Also Faris, "A stochastic picture of spin", LNP (doi 10.1007/3-540-11956-6_117).
  - Dohrn, Guerra, Ruggiero, "Spinning particles and relativistic particles in the framework of Nelson's stochastic mechanics", LNP 106, 165–181.
- **Local re-grep, 7 ISP PDFs:** Papers 1–3, 2608.04354, 2512.18105, Pimenta 2505.08785 and the nLab page. Zero hits for SU(2), "double cover" and "spinor". Pimenta's 2 "spin" hits are lattice spins.
- **Still unchecked:** the content of the Dankel, Dohrn–Guerra and Faris papers (paywalled Springer). This matters only for nb19's §7 phrase "diffusions on the rotation group", i.e. whether the stochastic mechanics there lives on SO(3) or SU(2). That phrase has since been softened in nb19 §7 to "incorporates spin through diffusions with rotational degrees of freedom". Once the full texts are available, check Dankel's configuration manifold and restore a sharper statement if it is supported.
