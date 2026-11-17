# Literature check: energy quantization, Wallstrom's objection, and ISP (2026-11-15)

Scope: how discrete energy levels (e.g. hydrogen) look through Barandes' indivisible stochastic processes (ISP), set against Wallstrom's objection to Nelson stochastic mechanics. Each claim carries a tag:
- **[verified-on-page]**: I read the passage (abstract page, HTML full text, or local PDF text).
- **[verified-citing]**: the bibliographic details come from reference lists I read in other papers; I did not read the paper itself.
- **[best-match]** / **[unconfirmed]**: from memory or search snippets only. Check before citing.

Local Barandes texts were extracted with `pdftotext` from `papers to study/Barandes/` (SQC = "1 Stochastic-Quantum Correspondence 2025", QISP = "3 Q Theory as ISP 2025", SQT = "2 Stochastic-Quantum Theorem 2026") and from `papers to study/2608.04354 ...pdf`.

## Summary

- **Wallstrom's objection:** the Madelung/Nelson variables (ρ, S) with v = ∇S/m give the Schrödinger equation only if you add by hand that ψ = √ρ e^{iS/ħ} is single-valued. That means ∮∇S·dl = 2πħn around every loop, and n ≠ 0 is possible only around nodes of ρ. If S is single-valued, angular-momentum states are lost. If S may be multi-valued, you get a continuum of spurious solutions with non-quantized energy and angular momentum. Sources: Wallstrom, Found. Phys. Lett. 2, 113 (1989) and PRA 49, 1613 (1994).
- **The main responses:**
  - Each one imports a new postulate: Schmelzer's 0 < Δρ < ∞ at nodes, Derakhshani's zitterbewegung clock, and Kuipers' divergent-Lagrangian integral condition.
  - Or it disputes the premise: Smolin, Fritsche–Haugk, Hushwater.
  - Or it moves the condition into geometry: Khesin–Modin 2026, Reddiger–Poirier.
  - None is accepted as settled.
- **Barandes never mentions Wallstrom.** This holds in all four locally held papers and the two lecture transcripts. He discusses Nelson only to say his own approach "is not continuous with" Nelson's, and that the Nelson-type approaches "all assumed Markovian dynamical laws" (QISP §1; SQC §1; Mindscape podcast 1:18–1:19).
- **No ISP paper derives discrete spectra, bound states or hydrogen.** The closest passages:
  - SQT/2608.04354 §4: a periodic permutation process, interpolated as U(t) = Σ^t, "with energy eigenvalues".
  - QISP §3.6: "a Hamiltonian is not a gauge-invariant observable".
- **The Q4 claim is only partly prior art.**
  - The ingredients are published: no distinguishability revival under divisible dynamics (Doukas arXiv:2602.22095 Prop. 1; Buscemi–Datta; Smirne–Stabile–Vacchini), and the two-level Rabi Γ as a counterexample (Doukas §4.2.2; Pimenta arXiv:2505.08785; Gillespie 1994).
  - The general statement is not: "discrete spectrum ⇒ quantum recurrence ⇒ Γ is indivisible unless it is a permutation at all times". It is a short lemma (contractivity plus Bocchieri–Loinger recurrence). I checked it numerically for a random 4-level H: the minimum pairwise column distance is 0.344 at t=1 and revives to 0.999 at t≈15186.
- **What Γ(t) = |U(t)|² can and cannot record about the spectrum (my own result, checked numerically):**
  - It sees Bohr frequencies E_n − E_m only, never absolute energies.
  - It is invariant under H → −Hᵀ. For a real Hamiltonian such as hydrogen in the position basis, H and −H give the same Γ. So "spectrum bounded below" is not encoded in Γ.
- **Bottom line (skeptical):**
  - ISP inherits quantization from the Hilbert-space dilation and the domain of H. Indivisibility does not supply Wallstrom's missing condition.
  - The Wallstrom gap partly dissolves for a structural reason: the ISP law Γ is linear in p and does not depend on the state, whereas Nelson's drift is built from ψ.
  - The one live residue is a sector-selection question (the flux/twist angle on non-simply-connected configuration space). ISP leaves it to the choice of law, just as standard quantum mechanics does.

## Q1. Wallstrom's objection and the responses

### The objection, precisely

- **Wallstrom 1989:** T. C. Wallstrom, "On the derivation of the Schrödinger equation from stochastic mechanics," Found. Phys. Lett. 2, 113–126 (1989), doi:10.1007/BF00696108. Abstract: "It is shown that the existing formulations of stochastic mechanics are not equivalent to the Schrödinger equation, as had previously been believed. It is argued that this is a reflection of fundamental inadequacies in the physical foundations of stochastic mechanics." **[verified-on-page, Springer abstract]**
- **Wallstrom 1994:** T. C. Wallstrom, "Inequivalence between the Schrödinger equation and the Madelung hydrodynamic equations," Phys. Rev. A 49, 1613–1617 (1994). **[verified-citing]** It appears in the reference lists of Schmelzer 1101.5774 and Smolin quant-ph/0609109. Kuipers 2301.05467 lists it as "(1993)", and gives the 1989 paper as "(1988)". Use 1989/1994. I did not read the full text.
- **Content, as Derakhshani reconstructs it in arXiv:1510.06391 §3 "Wallstrom's Criticism":** **[verified-on-page]**
  - The Nelson–Yasue derivation leaves it unspecified whether S is "single-valued, arbitrarily multi-valued, or multi-valued in accordance with a quantization condition", and Wallstrom showed "all these possible conditions on S are problematic".
  - If S is single-valued, the theory "exclude[s] single-valued Schrödinger wave functions with angular momentum". Those have phase exp(imφ), so S = mħφ.
  - If S is arbitrarily multi-valued, the theory produces all the quantum solutions "along with infinitely many multi-valued 'wave functions', which smoothly interpolate between the single-valued wave functions".
  - In the central-potential example, the Hamilton–Jacobi–Madelung (HJM) equations "predict a continuum of energy and momentum states for the particle, which smoothly interpolate between the quantized energy and momentum eigenvalues".
  - Imposing the quantization condition "is logically circular if the objective of stochastic mechanics is to derive quantum mechanics".
- **Schmelzer's restatement (arXiv:1101.5774 §1.2):** **[verified-on-page]**
  - The condition is ∮ m v·dl = 2πħm around closed loops, m ∈ ℤ.
  - Quoting Wallstrom: "to the best of my knowledge, this condition has not yet found any convincing explanation outside the context of the Schrödinger equation".
- **Bacciagaluppi (quant-ph/9811040):** derivations relying on the continuity plus Hamilton–Jacobi pair "rely on the tacit assumption that the resulting wave function be single-valued. As pointed out by Wallstrom (1994), this is a non-trivial requirement, which is in fact equivalent to the Bohr–Sommerfeld stability condition, i.e. to a standard quantisation condition." **[verified-on-page]**
- **Prehistory:** Derakhshani (footnote 11) notes that Albeverio–Høegh-Krohn and Goldstein had already observed that Nelson's equations have extra solutions when nodal surfaces disconnect the configuration space. **[verified-on-page]** Reddiger–Poirier call the condition "like the one proposed by Takabayasi". **[verified-on-page, abstract]** Takabayasi's 1952 paper itself is **[unconfirmed]**.
- **What this means for energy levels (hydrogen):** for hydrogen with m ≠ 0, a non-integer "m" in the HJM equations is a legitimate solution with the effective potential V + m²ħ²/(2μr²). It gives a continuum of energies between the hydrogen levels. Quantization of l and m, and hence of the levels, comes from the single-valuedness/regularity condition, not from the dynamics. This is my reading of Derakhshani's §3 example. **[verified-on-page for the general-potential example; the hydrogen specialization is mine]**

### Responses (with arXiv IDs)

- **Schmelzer, "An answer to the Wallstrom objection against Nelsonian stochastics", arXiv:1101.5774 (2011).** **[verified-on-page]**
  - He adds Postulate 1: "If ρ(q)=0, then 0<Δρ(q)<∞".
  - From it the quantization condition follows: generic nodes are simple zeros of ψ, which have winding ±1.
  - He calls this "a quite natural consequence of subquantum theories, as far as they conform to a simple principle of minimal distortion".
  - Same author: arXiv:1103.3506 ("paleoclassical interpretation", a regularity principle for zeros) **[verified-on-page, abstract]**. Also arXiv:1905.03075, which accepts the inequivalence and adds the restriction |ψ(q)|²>0 for all q as a falsifiable augmentation of QM **[verified-on-page, abstract]**.
- **Derakhshani, "A Suggested Answer To Wallstrom's Criticism: Zitterbewegung Stochastic Mechanics I", arXiv:1510.06391.** **[verified-on-page]**
  - Each particle carries an internal clock at ω_c = mc²/ħ (de Broglie–Bohm zitterbewegung).
  - S is the mean zbw phase, so its circulation is quantized because a physical clock phase is single-valued mod 2π.
  - He shows angular-momentum quantization for central potentials.
  - Part II, many particles: arXiv:1607.08838 **[verified-on-page, abs]**. Thesis: arXiv:1804.01394, "Stochastic Mechanics Without Ad Hoc Quantization" **[verified-on-page, abs]**.
  - Cost: a new physical postulate, and a relativistic frequency inside a non-relativistic theory.
- **Kuipers, "Stochastic Mechanics and the Unification of Quantum Mechanics with Brownian Motion", arXiv:2301.05467 (Springer Briefs 2023).** **[verified-on-page, HTML]**
  - §3.8 claims that when "the divergent part of the Lagrangian is properly taken into account", the equivalence relation on Hamilton's principal functions S± "follows from the integral condition (3.72), which is part of the theory".
  - In his words, Wallstrom's issue arises when the divergent part is ignored, and then "must be imposed by hand".
  - His framework is a Wiener process "rotated in the complex plane". Note that it is no longer a real Markov diffusion.
- **Smolin, "Could quantum mechanics be an approximation to another theory?", arXiv:quant-ph/0609109, §IV "Answering Wallstrom's objections to Nelson".** **[verified-on-page, HTML]**
  - For a particle on a circle, the objection "does not apply to the ground state where S=0".
  - More generally, a discontinuous ψ is still in L²(S¹) and is a Fourier superposition of integer modes.
  - My skeptical note: Nelson's solution with non-integer winding has a single frequency ω = mw²/2. The Schrödinger evolution of its Fourier decomposition has many frequencies, so the two time evolutions differ. Smolin's reply establishes kinematic membership in L², not dynamical equivalence.
- **Fritsche & Haugk, "Stochastic Foundation of Quantum Mechanics and the Origin of Particle Spin", arXiv:0912.3442, §VIII "Quantization of angular momentum".** **[verified-on-page, HTML]** They state the objective is "to disprove Wallstrom's notable objection". They argue the circulation condition follows from uniqueness/continuity arguments going back to Pauli and Born–Jordan, and call Wallstrom's quoted sentence "definitely incorrect".
- **Hushwater, "Comment on 'Inequivalence between the Schrodinger equation and the Madelung hydrodynamic equations'", arXiv:1005.2420 (2010).** It disputes that the conservative diffusion is inequivalent to QM. **[verified-on-page, abstract only; argument not read]**
- **Geometric reframings (no new physics, condition reinterpreted):**
  - Khesin, Misiołek & Modin, "Geometry of the Madelung transform", arXiv:1807.07172. The Madelung transform is a Kähler map; this paper does not itself treat Wallstrom. **[verified-on-page, abs]**
  - Khesin & Modin, "Madelung hydrodynamics and Poisson geometry of wave functions", arXiv:2607.01024 (July 2026). For noncritical zeros the Madelung transform is a symplectomorphism to coadjoint orbits, giving "a novel momentum map point of view on the Wallstrom quantization condition". **[verified-on-page, abs]**
  - Reddiger & Poirier, "Towards a mathematical Theory of the Madelung Equations", arXiv:2207.11367. Its "primary objective ... is to clarify in which sense Wallstrom's objections are justified". **[verified-on-page, abs]**
- **Taking the objection as a feature:** Roser & Scoggins, "Non-Quantum Behaviors of Configuration-Space Density Formulations of quantum mechanics", arXiv:2303.04959. They relax the single-valuedness condition and simulate the resulting deviations from QM. **[verified-on-page, abs]**
- **Requested but not found or verified:** a Wallstrom response by "Carroll" (Robert Carroll?) **[unconfirmed; nothing located]**. Bacciagaluppi's quant-ph/9811040 acknowledges the objection but does not answer it **[verified-on-page]**. Nelson's own late assessment ("Review of stochastic mechanics", J. Phys. Conf. Ser. 361, 012011 (2012)) **[best-match; not read]**.

## Q2. Has Barandes / the ISP literature addressed Wallstrom, Nelson, or quantization?

### (a) Wallstrom

- **Not addressed anywhere I could check:**
  - The four local Barandes PDFs have zero hits for "Wallstrom" (SQC 2302.10778 v2025, QISP 2507.21192, SQT 2026, 2608.04354).
  - So do the local lecture transcripts (`notes/barandes-lectures-2026-10/*.txt`).
  - A web search pairing Barandes or ISP with Wallstrom found nothing. **[verified-on-page for the local files; web absence is a search result, not proof]**

### (b) Nelson vs ISP

- **SQC §1 (Introduction):** "The present work is not continuous with earlier efforts to identify a fundamental relationship that connects stochastic processes and quantum theory. The most well-known of these approaches are due to Bopp (1947, 1952, 1953), Fényes (1952), and Nelson (1967, 1985)." **[verified-on-page, local pdftotext]**
- **QISP §1 (Introduction):** "...the most well-known stochastic-process formulation was due to Nelson's work in the 1960s through the 1980s, and is known today as Nelsonian stochastic mechanics (Nelson 1966, 1985)... These stochastic approaches were all based on adaptations of methods like Brownian motion, and so they all assumed Markovian dynamical laws. This constraint limited the ability of these approaches to capture the full behavior of quantum systems without becoming very complicated, and also made it difficult to generalize them beyond systems of fixed numbers of finitely many non-relativistic particles." **[verified-on-page, local]**
- **Mindscape podcast #323 (28 Jul 2025):**
  - At 1:18:31: "All of these approaches assume the Markov assumption, that was key."
  - At 1:19:49 he says of Nelson-type equations: "they've got forward-in-time evolving parts and backward-in-time evolving parts... It kind of looks like someone took the predictions of standard quantum mechanics and... reverse-engineered some set of differential equations".
  - **[verified-on-page, preposterousuniverse.com transcript]**
- **"New formulation" lecture transcript** (`notes/barandes-lectures-2026-10/new-formulation-lecture-transcript.txt`, [6m]): "non-Markovianity, indivisibility, seemed to have been the key missing pieces... And that's why, arguably earlier efforts like the [Fényes–]Nelson stochastic approach to quantum mechanics didn't ultimately pan out." **[verified-on-page, local transcript, auto-transcribed]**
- **A skeptical gloss:**
  - Barandes' diagnosis is "Markovianity". Wallstrom's diagnosis is "flow variables (ρ, ∇S) lose the global phase winding".
  - These are different defects. Nelson's process is Markovian, but its transition law depends on the state ψ, and that state dependence is what makes the admissible-state set ambiguous.
  - Barandes has not argued that dropping Markovianity cures Wallstrom's problem.

### (c) Discrete spectra / quantization in ISP

- **No derivation found** of discrete spectra, bound states, or hydrogen in any Barandes paper or the ISP secondary literature I checked: Pimenta 2505.08785, Doukas 2602.22095, Barandes 2602.01043 abstract, and the nLab page.
- **Closest passages:**
  - **SQT / 2608.04354 §4 "Potential Applications":** "For example, consider a discrete-time, time-homogeneous, logically reversible, deterministic process... Γ = Σ is an N×N permutation matrix... let U(t) ≡ Σ^t ... This time-evolution operator U(t) satisfies the requirements of Stone's theorem (Stone 1930), so it has a generator H, which can be identified as a quantum-theoretic Hamiltonian... thus one obtains an analytic interpolation of the discrete-time deterministic process as a continuous-time quantum process, with energy eigenvalues and a Schrödinger equation." **[verified-on-page, local]**
    - Comment: this is a "quantization" of a periodic process. The spectrum is roots of unity, i.e. discrete energies 2πk/period.
    - Σ^t is not unique: the branch of log Σ is a choice, which shifts each eigenphase by 2πn. Different branches agree at integer t and give different intermediate Γ(t).
    - So the energies are fixed only modulo 2π per step by the discrete data. That is a precise analogue of the Wallstrom ambiguity.
  - **QISP §3.6 "Foldy-Wouthuysen Gauge Transformations":** "the Hamiltonian H(t) ... transforms precisely as a non-Abelian gauge potential... This transformation behavior makes clear that a Hamiltonian is not a gauge-invariant observable, even though it may happen to coincide with various observables according to particular gauge choices." The Heisenberg-picture gauge sets H_V = 0 (eq. 80). **[verified-on-page, local]**
    - Consequence: in ISP the spectrum of H is not by itself physical. Only what survives in Γ is, which motivates the Γ-level analysis in the Research angle section.
  - **SQC §5.1:** "canonical quantization need not be regarded as the promotion of classical observables to noncommutative operators by fiat but can be implemented (when mathematically feasible) simply by generalizing a classical system's dynamics from being deterministic to being stochastic". Barandes gives no worked bound-state example. **[verified-on-page, local]**

## Q3. Known results the notebook will lean on

### (a) A continuous-time finite-state Markov generator has no nonzero purely imaginary eigenvalues

- **Clean proof route (Gershgorin):**
  - For a generator Q (off-diagonals ≥ 0, columns summing to 0, or rows depending on convention), every Gershgorin disc is centred at Q_ii ≤ 0 with radius |Q_ii|.
  - So every disc lies in {Re z ≤ 0} and touches the imaginary axis only at 0.
  - Hence any eigenvalue with Re λ = 0 is λ = 0, and e^{Qt} has no undamped oscillating modes.
  - Citation: S. Gershgorin, Izv. Akad. Nauk SSSR (1931) **[verified-on-page: Wikipedia "Gershgorin circle theorem" confirms the 1931 publication]**. Textbook form: Horn & Johnson, *Matrix Analysis*, Thm 6.1.1 **[best-match]**.
- **Equivalent uniformization argument:** Q = q(P − I) with P stochastic and |μ| ≤ 1, so Re λ = q(Re μ − 1) ≤ 0 with equality only for μ = 1. Norris, *Markov Chains* (CUP 1997) is held locally. I grepped it and it does not state the lemma explicitly; it only computes example spectra (e.g. "Q has distinct eigenvalues 0, −2, −4"). **[verified-on-page: absence]**
- **Literature statement for the embedding problem:** E. B. Davies, "Embeddable Markov Matrices", arXiv:1001.1693 (Electron. J. Probab. 15 (2010) 1474 **[best-match for the journal]**): "its eigenvalues must lie in a certain region in the unit ball". **[verified-on-page, abs]** Classic sources are Elfving 1937, Kingman 1962 and Runnenberg 1962 **[best-match]**.
- **Caveat for the notebook:** this rules out only the homogeneous case. A time-inhomogeneous divisible chain (periodic Q(t)) can have periodic marginals. That is why (b) below is the stronger tool.

### (b) Contractivity, distinguishability, and revival as a non-Markovianity witness

- **ℓ1 contraction:** stochastic matrices contract the ℓ1/Kolmogorov (total-variation) distance. Doukas gives the three-line proof in arXiv:2602.22095, Prop. 1, eqs. (78)–(82). **[verified-on-page]**
- **Smirne, Stabile & Vacchini, "Signatures of non-Markovianity in classical single-time probability distributions", arXiv:1211.5913, Phys. Scr. T153, 014057 (2013).** "the Kolmogorov distance allows to quantify memory effects in classical stochastic processes by studying the evolution of the single-time probability distribution." **[verified-on-page, abs]**
- **Breuer, Laine & Piilo, "Measure for the Degree of Non-Markovian Behavior of Quantum Processes in Open Systems", arXiv:0908.0238, PRL 103, 210401 (2009).** The trace-distance revival measure. **[verified-on-page, abs]**
- **Buscemi & Datta, "Equivalence between divisibility and monotonic decrease of information in classical and quantum stochastic processes", arXiv:1408.7062, PRA 93, 012101 (2016).** Divisibility holds if and only if information decreases monotonically. This is the converse direction, so revival is a complete witness for a suitable family of information measures, not for TV distance alone. **[verified-on-page, abs]**
- **Doukas, "On the emergence of quantum mechanics from stochastic processes", arXiv:2602.22095, §4.2.1.** Proposition 1 (No distinguishability revival): "a revival of configuration-space distinguishability rules out every Markovian realizer on that space". No continuity or homogeneity assumed. **[verified-on-page, HTML]**

### (c) RAGE theorem

- **Ruelle 1969:** D. Ruelle, "A remark on bound states in potential-scattering theory," Nuovo Cimento A 61, 655–662 (1969). **[verified-citing: search snippets from citing papers]**
- **Amrein & Georgescu 1973:** W. O. Amrein & V. Georgescu, "On the characterization of bound states and scattering states in quantum mechanics," Helv. Phys. Acta 46, 635–658 (1973). **[verified-citing; sources disagree on the title wording and the first page (633 vs 635), so check before citing]**
- **Enss 1978:** V. Enss, "Asymptotic completeness for quantum mechanical potential scattering. I. Short range potentials," Commun. Math. Phys. 61, 285–291 (1978). **[verified-citing]**
- **Statement used:** ψ ∈ H_pp if and only if sup_t ‖(1−χ_R)e^{−iHt}ψ‖ → 0 as R → ∞ (it stays in bounded regions). ψ ∈ H_c if and only if the time-average of ‖χ_R e^{−iHt}ψ‖² → 0 for each R (it escapes on average). **[best-match]** A textbook source is Reed–Simon III, or Cycon–Froese–Kirsch–Simon, *Schrödinger Operators* (1987), §5 **[best-match]**.

### (d) Infinite-time average of |⟨i|e^{−iHt}|j⟩|²

- **Formula:** for a nondegenerate spectrum, lim_{T→∞} (1/T)∫_0^T |⟨i|e^{−iHt}|j⟩|² dt = Σ_n |ψ_n(i)|² |ψ_n(j)|². For i = j this is the inverse participation ratio of |i⟩ in the energy basis.
  - Degeneracies only need the projector form Σ_E |⟨i|P_E|j⟩|².
  - Nondegenerate gaps are not needed for this two-point quantity. They are needed for fluctuation bounds.
  - **[derivation standard; numerically verified here: random 4-level H, error 4×10⁻⁵ over T = 4000]**
- **Wiener's lemma:** for a finite measure μ, lim (1/T)∫_0^T |μ̂(t)|² dt = Σ_x μ({x})². Applied to the spectral measure, only the point spectrum survives the time average. That is the "Wiener" route to the RAGE dichotomy. Citation: Katznelson, *An Introduction to Harmonic Analysis*, Ch. VI **[best-match]**. Y. Last, "Quantum dynamics and decompositions of singular continuous spectra," J. Funct. Anal. 142, 406–445 (1996), doi:10.1006/jfan.1996.0155 **[verified-citing for the bibliographic data; I did not read the formula on the page]**.
- **Dephasing and time-averaged state:** Linden, Popescu, Short & Winter, arXiv:0812.2385, PRE 79, 061103 (2009) **[verified-on-page, abs]**. Reimann, arXiv:0810.3092 (PRL 101, 190403 (2008) **[best-match for the journal]**) **[verified-on-page, abs]**.

### (e) Bohr frequencies read as frequencies of transition probabilities in a stochastic or hidden-variable framework

- **Barandes 2608.04354 §4:** see Q2(c). Energies appear as the generator of an interpolated periodic process. **[verified-on-page]**
- **Stochastic electrodynamics (de la Peña, Cetto, Valdés-Hernández):**
  - *The Emerging Quantum: The Physics Behind Quantum Mechanics*, Springer 2015, doi:10.1007/978-3-319-07893-9 **[verified-citing: front matter seen]**.
  - Their EmQM13 talk says the system responds resonantly to zero-point modes and "the resonance frequencies are the frequencies of transition between stationary states" **[verified-citing: search snippet of the Fetzer-Franklin PDF; I did not read the derivation]**.
  - This is the closest published "spectral lines = resonance frequencies of a stochastic dynamics" claim. Caveat: SED is known to fail for nonlinear systems and for hydrogen (self-ionization, Nieuwenhuizen 2020 **[best-match]**).
- **Bell–Vink beables:** J. S. Vink, "Quantum mechanics in terms of discrete beables," PRA 48, 1808–1818 (1993) **[verified-citing, APS DOI page]**. The jump rates are built from Im(ψ_i* H_ij ψ_j), so they oscillate at Bohr frequencies **[best-match on the formula]**.
  - Important for Q4: the Bell–Vink process is Markovian (time-inhomogeneous, ψ-dependent) and reproduces quantum one-time marginals. It escapes the Q4 obstruction only because its transition matrix depends on ψ. It is not one linear Γ valid for all initial distributions.
- **Gillespie, "Why quantum mechanics cannot be formulated as a Markov process," PRA 49, 1607–1612 (1994):** the two-state Rabi example **[verified-citing, Doukas refs + Garbaczewski–Olkiewicz abstract]**. Garbaczewski & Olkiewicz reply that dichotomic jump processes can reproduce it if "measurement probabilities" are not identified with transition probabilities: arXiv:quant-ph/9601016, PRA 54, 1733 (1996) **[verified-on-page, abs]**. This exchange is the 1994–96 version of the ψ-dependent loophole above.
- **Schrödinger's 1926 reading:** emission frequencies are beat frequencies of the oscillating charge density |ψ|². This is the historical root of "Bohr frequency = frequency of a probability". **[best-match; cite from a secondary source after checking]**

## Q4. Is "discrete spectrum ⇒ persistent recurrences of Γ ⇒ indivisible unless Γ is a permutation" already stated?

### What is published

- **Doukas arXiv:2602.22095:**
  - §4.2.1 gives the general revival obstruction (Prop. 1).
  - §4.2.2 applies it to Rabi oscillations: Γ = [[cos²ωt, sin²ωt],[sin²ωt, cos²ωt]], D_{e1,e2}(t) = |cos 2ωt|, which vanishes at t* = π/4ω and then revives.
  - Conclusion: "any stochastic realizer of this rooted family on the same configuration space must be non-Markovian".
  - Full-text search: no hits for "recurren" or "discrete spectrum". **[verified-on-page]**
- **Pimenta arXiv:2505.08785** (N = 2 geometry; local PDF): **[verified-on-page, local]**
  - Fig. 4 caption: "A continuous path connecting the identity and the permutation is necessarily indivisible".
  - "Continuous and discontinuous dynamics": "An example of indivisible but continuous evolution is quantum 2-level system oscillating between two orthogonal states".
  - Around eq. (59): "The process as a whole is indivisible but the dynamics is divisible as long as the stochastic matrix moves towards the centre".
  - "every passage through a permutation matrix constitutes a proper division event".
- **Gillespie 1994:** the same two-state argument with "re-rooted" matching (see Doukas footnote 9). **[verified-citing]**
- **Related, not the claim:**
  - Buscemi et al., "Causal and Non-Causal Revivals of Information", arXiv:2405.05326, PRX Quantum 6, 020316 (2025) **[verified-on-page, abs]**.
  - Nakagawa, arXiv:2602.09054: classical relative-entropy revivals from memory-induced loss of divisibility **[verified-on-page, abs]**.
  - Settimo et al., arXiv:2606.30751: Schrödinger- vs Heisenberg-picture non-Markovianity, including stochastic-propagator divisibility **[verified-on-page, abs]**.
- **Quantum recurrence:**
  - P. Bocchieri & A. Loinger, "Quantum Recurrence Theorem," Phys. Rev. 107, 337–338 (1957), doi:10.1103/PhysRev.107.337. Recurrence for pure point spectrum. **[verified-citing: Wikipedia "Quantum revival" reference + sciencegate record]**
  - Schulman, "Note on the quantum recurrence theorem," PRA 18 (1978) **[verified-citing, title only]**.
  - Hogg & Huberman, "Recurrence phenomena in quantum dynamics," PRL 48, 711 (1982) **[unconfirmed; the search did not return it]**.

### What is not published (as far as these searches reach)

- **The general statement:** for any H with pure point spectrum, Γ(t) = |e^{−iHt}|² recurs arbitrarily close to I infinitely often, so it is indivisible on [0, T] for all large T unless Γ(t) is a permutation for all t.
- No paper I found states it. Searches covered "quantum recurrence non-Markovian", "recurrence divisibility", "almost periodic non-Markovian", and ISP plus recurrence.
- Treat it as **probably folklore-adjacent but unstated in this form**. It is a lemma, not a discovery.

### The lemma, with the steps the notebook needs

1. **Divisible on [0, T] ⇒ for all s ≤ T and all i, j:** D(Γ(T)e_i, Γ(T)e_j) ≤ D(Γ(s)e_i, Γ(s)e_j). This is ℓ1 contraction (Doukas Prop. 1).
2. **Recurrence:** for pure point spectrum and any ε, there are arbitrarily large T with ‖Γ(T) − I‖ < ε. This is Bocchieri–Loinger in finite dimension, via Dirichlet/Kronecker simultaneous approximation of the phases E_n T. In infinite dimension with pure point spectrum, use strong almost-periodicity, applied to each finite set of configurations.
3. **Combining 1 and 2:** every pair of columns of Γ(s) has TV distance > 1 − 2ε for all s ≤ T.
4. **ε → 0:** N columns that are pairwise almost disjoint and live on N rows force Γ(s) to be within O(ε) of a permutation. By continuity from Γ(0) = I, Γ(s) is within O(ε) of I.
5. **Conclusion:** a pure-point-spectrum Γ is divisible on arbitrarily long windows only if Γ(t) ≡ I. That means H is diagonal in the configuration basis, up to the trivial case.
   - Γ(t) a non-identity permutation at some times is impossible for continuous t if Γ is divisible, by step 4.
   - Permutations appear only in discrete time, as in Pimenta's σ_x example and Barandes' Σ^t.
- **Numerical sanity check** (a scratch script, not saved):
  - Random 4-level H: the minimum pairwise column TV of Γ is 0.344 at t = 1.
  - The best recurrence up to t = 2×10⁴ is at t ≈ 15186, with max column TV to I ≈ 7×10⁻⁴; there the minimum pairwise TV is 0.9992.
  - So the revival is 0.344 → 0.999, and no divisible realizer exists.
- **Scope caveats:**
  - This concerns the state-independent Γ. ψ-dependent Markov processes (Bell–Vink, Nelson) are not covered.
  - It says nothing about systems with continuous spectrum, which may or may not be indivisible.
  - Mixed spectrum: the recurrence holds only on the pure point subspace, weighted by the IPR from Q3(d).

## Research angle: does indivisibility supply Wallstrom's missing condition, or does ISP inherit quantization?

**Verdict: inherited, not supplied.** The reasons below are concrete.

### Where quantization actually enters ISP

- **Finite configuration spaces:** every Barandes theorem I checked (SQC, SQT, 2608.04354) is stated for finite N, where every H has a discrete spectrum. "Quantization" is automatic there and carries no information.
- **Hydrogen:** hydrogen needs configuration space ℝ³ (or ℝ³ minus a point). The only known way to write down its Γ is Γ(x, t | x′, 0) = |⟨x|e^{−iHt}|x′⟩|², with H self-adjoint on L²(ℝ³).
  - The domain of H, made of single-valued L² functions with the Coulomb self-adjoint extension, is exactly where the single-valuedness condition lives.
  - So ISP's hydrogen Γ is built from the Hilbert-space dilation and imports the condition Wallstrom says Nelson lacks.
  - Nothing in the ISP axioms (stochastic Γ, indivisibility) produces Γ for ℝ³ from scratch.
- **Indivisibility points the wrong way to be the source:** the Q4 lemma shows discrete spectrum ⇒ indivisibility, not the converse. A Γ with continuous spectrum (scattering) is typically also indivisible, so indivisibility cannot single out discrete levels. A periodic permutation process is divisible and still has a "discrete spectrum" (2608.04354 §4). So indivisibility is neither necessary nor sufficient for discreteness.

### Why the Wallstrom gap partly dissolves anyway (a structural point, not a solution)

- **Nelson's law depends on the state:** the drift b = (∇S + ∇log√ρ)ħ/m is built from ψ.
  - The set of admissible processes is the set of admissible (ρ, S) pairs, so one must say which S are allowed. That is the Wallstrom question.
  - Equivalently, Nelson's "transition kernel" is a nonlinear functional of the initial data.
- **The ISP law does not:** Γ(t←0) is one linear map applied to every initial p.
  - Given Γ, there is no further choice of "which states are admissible", because every p is admissible. The spectrum is a property of the single kernel.
  - The question moves from "which S are allowed?" to "which Γ is the law?". Standard QM answers that question with "which self-adjoint H" in the same way.
- **The residual ambiguity is a sector choice, not a defect:**
  - On non-simply-connected configuration space (a ring, or ℝ³ minus a flux line), twisted boundary conditions ψ(θ + 2π) = e^{iα}ψ(θ) give legitimate self-adjoint H_α with spectra (n + α/2π)². Each gives a legitimate unistochastic Γ_α.
  - Wallstrom's non-quantized Nelson solutions on the ring are, mode by mode, stationary states of some H_α.
  - So ISP does not exclude them. It treats α as part of the law, the Aharonov–Bohm flux, which is physical. The hydrogen value α = 0 is put in, not derived.
  - See also nb15 (Aharonov–Bohm/Berry) and Antonakos–Terzis 2023 on AB in Nelson mechanics (already cited in nb15).
- **The sharp skeptical test:** can ISP data alone, the family Γ(t←0) for all t, tell α = 0 from α ≠ 0?
  - Yes in principle, because the Bohr frequencies differ.
  - But that only says Γ encodes the spectrum. Nothing says why nature's Γ has α = 0. Wallstrom's challenge, "explain the condition outside the Schrödinger equation", is not met. It is relocated into the choice of Γ.

### What Γ does and does not encode about energies (useful for the notebook)

- **Γ_ij(t)** = Σ_{n,m} ψ_n(i)ψ_n*(j)ψ_m*(i)ψ_m(j) e^{−i(E_n−E_m)t}. Only Bohr differences appear, with weights. Γ is real, so ±ω appear in pairs.
- **Invariances:** Γ is invariant under H → H + c·1, as expected, and under H → −Hᵀ.
  - The second follows from e^{iHᵀt} = conj(e^{−iHt}).
  - For any real symmetric H, such as hydrogen in the position basis, H and −H give identical Γ. So Γ cannot see that the hydrogen spectrum is bounded below.
  - Checked numerically: max |ΔΓ| = 0 at t = 0.3, 1.7, 9.1 for a random complex 5×5 H, and the eigenvalues flip sign.
  - This fits QISP §3.6 ("Hamiltonian is not a gauge-invariant observable"), with a sharper point: even the spectrum's sign is not Γ-observable without extra structure such as coupling to a heat bath or a second system.
- **Long-time content:** the time average of Γ_ij equals Σ_n |ψ_n(i)|²|ψ_n(j)|² (Q3d), where only the point spectrum survives (Wiener/RAGE). That is the Γ-level signature of bound states: non-decaying return probability, with fluctuations at Bohr frequencies.

### Concrete next steps (ranked)

1. **Notebook cell for the lemma:** write up the Q4 lemma as a short notebook cell, with the 4-level numeric and the 2-level Rabi case. Cite Doukas Prop. 1 for step 1 and Bocchieri–Loinger for step 2. Frame it as "a direct generalization of Gillespie/Doukas/Pimenta's two-level case", not a new theorem.
2. **Ring experiment:** compute Γ_α(t) for a particle on a discretized ring with twist α. Show Γ_α ≠ Γ_0 (Bohr frequencies shift). Then show that the stochastic data contain no internal criterion preferring α = 0. That is the honest ISP version of Wallstrom.
3. **The H vs −H point:** test whether coupling the system to a second ISP system (a "detector" or bath) breaks the H ↔ −Hᵀ degeneracy. If only couplings do, then "energy bounded below" is a relational property in ISP. That is a possibly novel angle, and worth a targeted search for "time reversal |U|^2 sign of Hamiltonian" before claiming it.
4. **Don't overclaim:** do not write "ISP explains quantization". The defensible line is: "ISP's law is linear in the initial distribution, so Wallstrom's admissible-state ambiguity has no foothold; the quantization data sit in the choice of Γ, exactly as they sit in the choice of self-adjoint H."

## Citation list with tags

- Wallstrom, Found. Phys. Lett. 2, 113 (1989), doi:10.1007/BF00696108: verified-on-page (abstract)
- Wallstrom, PRA 49, 1613 (1994): verified-citing
- Schmelzer, arXiv:1101.5774: verified-on-page
- Schmelzer, arXiv:1103.3506; arXiv:1905.03075: verified-on-page (abstracts)
- Derakhshani, arXiv:1510.06391 (I): verified-on-page; arXiv:1607.08838 (II), arXiv:1804.01394 (thesis): verified-on-page (abstracts)
- Kuipers, arXiv:2301.05467 §3.8: verified-on-page
- Smolin, arXiv:quant-ph/0609109 §IV: verified-on-page
- Fritsche & Haugk, arXiv:0912.3442 §VIII: verified-on-page
- Hushwater, arXiv:1005.2420: verified-on-page (abstract only)
- Bacciagaluppi, arXiv:quant-ph/9811040: verified-on-page
- Khesin–Misiołek–Modin, arXiv:1807.07172; Khesin–Modin, arXiv:2607.01024: verified-on-page (abstracts)
- Reddiger & Poirier, arXiv:2207.11367: verified-on-page (abstract)
- Roser & Scoggins, arXiv:2303.04959: verified-on-page (abstract)
- Nelson, "Review of stochastic mechanics" (2012): best-match
- Takabayasi (1952): unconfirmed
- Barandes SQC (arXiv:2302.10778) §1, §5.1; QISP (arXiv:2507.21192) §1, §3.6; 2608.04354 §4: verified-on-page (local)
- Barandes, Mindscape #323 transcript, 1:18:31–1:19:49: verified-on-page
- Barandes, arXiv:2602.01043: verified-on-page (abstract)
- Pimenta, arXiv:2505.08785: verified-on-page (local)
- Doukas, arXiv:2602.22095 §4.2: verified-on-page
- Gillespie, PRA 49, 1607 (1994): verified-citing
- Garbaczewski & Olkiewicz, arXiv:quant-ph/9601016: verified-on-page (abstract)
- Smirne, Stabile & Vacchini, arXiv:1211.5913: verified-on-page (abstract)
- Breuer, Laine & Piilo, arXiv:0908.0238: verified-on-page (abstract)
- Buscemi & Datta, arXiv:1408.7062: verified-on-page (abstract)
- Buscemi et al., arXiv:2405.05326; Nakagawa, arXiv:2602.09054; Settimo et al., arXiv:2606.30751: verified-on-page (abstracts)
- Davies, arXiv:1001.1693: verified-on-page (abstract)
- Gershgorin (1931): verified-on-page (Wikipedia)
- Horn & Johnson, Thm 6.1.1: best-match
- Ruelle 1969; Amrein–Georgescu 1973; Enss 1978: verified-citing (Amrein–Georgescu title and first page disputed)
- Last, JFA 142 (1996): verified-citing
- Katznelson (Wiener's lemma): best-match
- Linden–Popescu–Short–Winter, arXiv:0812.2385: verified-on-page (abstract)
- Reimann, arXiv:0810.3092: verified-on-page (abstract)
- Bocchieri & Loinger, Phys. Rev. 107, 337 (1957): verified-citing
- Hogg & Huberman, PRL 48, 711 (1982): unconfirmed
- Vink, PRA 48, 1808 (1993): verified-citing (the rate formula is best-match)
- de la Peña, Cetto & Valdés-Hernández, *The Emerging Quantum* (2015): verified-citing (front matter only)
- Schrödinger 1926 (charge-density beats): best-match

## Independent audit (2026-11-16): outcome

There were two adversarial auditors, one for correctness and one for novelty and attribution. The audit reports are not included here. All fixes were applied, and nb18 was retitled "Discrete Spectra in Γ: a Γ-Level Synthesis".

- **Downgraded to KNOWN:**
  - Γ_jj is the survival probability, and its time average is the inverse participation ratio.
  - "Nonzero average iff point spectrum" is Wiener's theorem; RAGE is the infinite-volume statement, and the box only illustrates it.
  - Recurrence is Bocchieri–Loinger, Phys. Rev. 107, 337 (1957), and was uncredited.
  - The ring is Smolin's test case (quant-ph/0609109 §IV).
  - Twist = flux is the standard fluxoid/holonomy equivalence (Foskett–Tronci arXiv:2003.08664).
  - Glick–Adami (2020) is closed-system non-Markovianity.
- **Corrected:**
  - **The lemma.** It needs a time-independent H, and reads "indivisible at every t′ where Γ(t′) is not a permutation". A return to a permutation (σ_x at t = π) is divisible there.
  - **The variance formula.** The exponents are |v|⁴|v|⁴. The code now groups coinciding gaps; the Z = 0 variance was half the true value.
  - **"Discrete iff never forgets".** Only the time-average part is an iff.
  - **"Markov chains cannot oscillate at all".** Only undamped oscillation is excluded, and only for time-homogeneous chains. A one-way 20-cycle chain shows damped oscillation.
  - **Relaxation to 1/N.** It needs |λ₂| < 1, not just double stochasticity.
  - **The Wallstrom blind spot is wider than first stated.** Γ(α) = Γ(N/2 − α) on all bare rings, and a constant potential does not break the tie.
  - **The "branch choice" remark** is ours, not Barandes's: 2608.04354 §4 (eq. 58) and Paper 2 fn. 12 define E_m = −ħθ_m/δt without comment.
  - **Barandes on Nelson.** He says "limited", not "failure".
  - **Kuipers** moved to "disputes the premise".
- **Unchecked:**
  - The Gillespie 1994 full text.
  - Amrein–Georgescu 1973 and Enss 1978 (not resolved on Crossref).
  - Pauli 1939.


## Later corrections (2026-11-17 review)

- Pauli 1939 could not be confirmed and was dropped from nb18.
- Long-lasting oscillation is also an "exactly when" in the long-time-variance sense: it occurs exactly when the start overlaps two or more distinct point-spectrum levels (singular-continuous parts drop out of long-time averages). The "only the time-average part is an iff" line above is superseded.
- "Markov chains cannot oscillate undamped" holds for finite, time-homogeneous, continuous-time chains; discrete-time chains such as a permutation can.
