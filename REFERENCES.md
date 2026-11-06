# References for the isp-lab project

This is the bibliography for the isp-lab project: the sixteen notebooks (01-16), their annotated versions, the builder scripts, the spike notes under `notes/`, and the README. It was first compiled offline by scanning those files, with bibliographic details copied as the project states them. On 2026-10-29 every from-memory entry was checked online (arXiv abstract pages, Crossref, publisher pages, DLMF, and the reference lists of the Barandes papers), and the corrections are applied here. The verification notes are in `notes/lit-recheck-2026-10-29/` (`bibliography.md` summarises them; `REFERENCES.corrected.md` is the checked copy). Only bibliographic details were checked online; no cited passage was checked in that pass. A matching BibTeX file is `references.bib`.

Every entry carries a status tag. An entry that is held locally or checked on the page and whose bibliographic details were also checked online carries both tags (for example **held-locally**; **verified 2026-10-29**).

- **verified-on-page**: the project checked a quote or passage against the actual PDF. The pages or sections that were checked are named in the entry. Passages cited from the same book but not named as checked are listed separately in that entry.
- **held-locally**: a PDF or transcript exists on disk (usually in `papers to study/` or `notes/barandes-lectures-2026-10/`), but no specific passage has been checked against it.
- **verified 2026-10-29**: the bibliographic details (authors, title, venue, volume, page or article number, year, DOI, arXiv number) were checked online on 2026-10-29. The passages the project cites were not checked. A few entries rest on standard citations because no online record could be retrieved; those entries say so.
- **best match, unconfirmed**: the 2026-10-29 check could not find the paper as the project describes it. The entry gives the best match, which has not been confirmed as the paper the project means.
- **from-memory**: written from memory or from a secondary mention, and not checked against the source. After the 2026-10-29 check no entry carries this tag alone.

Entries tagged best match, unconfirmed, and the details flagged inside entries as resting on standard citations, must be checked before this list is shared outside the project. A "To verify" checklist is at the end.

How to read "Cited in". Numbers such as 03 or 10 are notebooks (both the clean and annotated versions; the annotated text includes the clean text). Names such as "wigner spike" are files in `notes/`: aharonov-bohm-berry, fitting-hilbert-reps, gamma-only-query-bound, golden-rule-divisibility, grover-as-isp, identical-particles, margolus-levitin-gamma, matter-wave-gratings, wick-rotation, wigner and zeno-anti-zeno spikes; "surfaceology note" is `isp-and-surfaceology-2026-10-23.md`; "backlog" is `textbook-concepts-backlog-2026-10-24.md`. Page numbers are printed page numbers unless marked "PDF page". The backlog was converted from PDF pages to printed pages on 2026-10-25 (offsets: Griffiths +15, approximate; Gasiorowicz +12; Schleich +23; Peskin +22).

## Barandes and ISP

- **Barandes, J. A.** "The Stochastic-Quantum Correspondence." arXiv:2302.10778 (v3). Published in *Philosophy of Physics* 3(1), 8 (2025), doi:10.31389/pop.186. Local file: `papers to study/Barandes/1 Stochastic-Quantum Correspondence 2025.pdf`. Called "Paper 1" in notebook 03. **verified-on-page**; **verified 2026-10-29**
  - Cited in: 01, 02, 03, 04, 05, 06, 09, 10, 11, 12, 13; README; lecture README.
  - Sections cited: §2.1 (definition of a process, eqs. 1-3, divisibility eq. 6, "divisible" credited to Wolf and Cirac 2008, eq. 7 Gaussian example, eq. 12, footnotes 1 and 4); §2.2 (towers of conditional probabilities); §3.1-3.2 (eqs. 16, 17, 23); §3.4 (unistochastic, eqs. 30-31, footnote 6 on gauge); §3.5 "Interference" (eqs. 39-52, eq. 43); §3.7 "Division events and the Markov approximation" (eqs. 55-58, esp. eq. 57); §3.8; §4 and §4.1-4.2 (emergeables, measurement model). The notebooks quote §3.4-3.5 and §3.7 eqs. 56-58 directly.
- **Barandes, J. A.** "The Stochastic-Quantum Theorem." arXiv:2309.03085. No journal version found on the arXiv page. Local file: `papers to study/Barandes/2 Stochastic-Quantum Theorem 2026.pdf`. Called "Paper 2" in notebook 03. **verified-on-page**; **verified 2026-10-29** (arXiv record)
  - Cited in: 03, 04; README.
  - Sections cited: §3.5 (eq. 68, as cited in notebook 03); §4, §4.1-4.2 (statement (69): every indivisible stochastic process is a subsystem of a unistochastic one); §5.7 (eq. 94, dilation dimension N <= N-tilde <= N^3); footnote 9 (the 3x3 doubly stochastic matrix that is not unistochastic).
- **Barandes, J. A.** "Quantum Systems as Indivisible Stochastic Processes." arXiv:2507.21192. Published in *Studies in History and Philosophy of Science* 119, 102213 (2026), doi:10.1016/j.shpsa.2026.102213. Local file: `papers to study/Barandes/3 Q Theory as ISP 2025.pdf`. Called "Paper 3" in notebook 03 and "Barandes 2025" in notebook 01. **verified-on-page**; **verified 2026-10-29**
  - Cited in: 01, 02, 03, 04, 05, 06, 15; README; aharonov-bohm-berry spike.
  - Sections cited: abstract; §2.1 (eqs. 1, 4, 5, 7: Chapman-Kolmogorov, composition, n-th order Markov); §2.2 (division events, eq. 18, eqs. 22-23); §3.2 "Schur-Hadamard Gauge Transformations", eqs. 27-30 and footnote 11, pp. 12-13 (checked on the page for nb 15); §3.4 (eq. 46, Born rule for the configuration basis); eq. 41 (rho(0) diagonal); eq. 78.
- **Barandes, J. A., M. Hasan, and D. Kagan.** "The CHSH Game, Tsirelson's Bound, and Causal Locality." arXiv:2512.18105 (December 2025); doi:10.1103/xfpf-734d (journal not confirmed). Local file: `papers to study/2512.18105 CHSH Game Tsirelson Bound and Causal Locality.pdf`. **held-locally**; **verified 2026-10-29**
  - Cited in: 06 (§3.1, approximate division events) and 08 (§3.2 "division channels"); notebook 09 notes it does not treat algorithms.
  - The paper recasts the CHSH game as indivisible stochastic processes and derives Tsirelson's bound from Barandes's causal-locality condition. It is not about algorithms.
- **Barandes, J. A.** "The Born Representation Theorem and the Unistochastic Theorem." arXiv:2608.04354 (August 2026). Local file: `papers to study/2608.04354 Born Representation Theorem and Unistochastic Theorem.pdf`. Described in the fitting-hilbert-reps spike as about "existence of unistochastic dilations, not fitting"; the 2026-10-29 check found that description accurate. **held-locally**; **verified 2026-10-29**
  - Cited in: 09 (a "to check" item); fitting-hilbert-reps spike.
- **Pimenta, L. S.** "Divisible and indivisible Stochastic-Quantum dynamics." arXiv:2505.08785 (May 2025). Local file: `papers to study/2505.08785 Divisible and Indivisible Stochastic-Quantum Dynamics.pdf`. Described as on divisible vs. indivisible stochastic-quantum dynamics; the paper treats two-configuration systems only (conical bounds in the space of stochastic matrices). **held-locally**; **verified 2026-10-29**
  - Cited in: 03, 04, 05, 06, 07, 08, 09.

## Textbooks

The 2026-10-29 check confirmed the textbook editions below are real and correctly attributed (spot check, not a page check). The Ballentine edition remains unknown.

- **Ballentine, L. E.** *Quantum Mechanics: A Modern Development.* Edition and publisher not stated in the project: either World Scientific, 1998, or the 2nd edition of 2014 (the 2026-10-29 notes say Cambridge University Press for the 2014 edition; that publisher is not confirmed). The two have different pagination. Local file: `papers to study/Ballentine_L_Quantum_mechanics_a_modern.pdf`. **held-locally**
  - Cited in: 04, 05, 07; README.
  - Sections cited: §2.1 Postulate 2, eq. 2.1, and §2.4 eq. 2.26 (nb 04); Ch. 5 "Double slit diffraction", with the Tonomura et al. (1989) remark (nb 05); §12.3 "Energy-Time Indeterminacy Relations", eq. 12.33 and the Mandelstam-Tamm bound (nb 07). The notebooks quote these passages, but no page-level check against the PDF is recorded.
- **Gasiorowicz, S.** *Quantum Physics.* 3rd ed. New York: Wiley, 2003. **verified-on-page**
  - Cited in: 10, 11; backlog.
  - Checked: ch. 15, printed p. 240, "the reader may well feel swindled" (nb 10).
  - Cited from the scanned book but not individually checked: ch. 18 quantum jumps/electron shelving and dark states/EIT (nb 11 future work; backlog, pp. 278-281), ch. 4 ammonia (backlog, pp. 79-80), ch. 20 delayed choice and GHZ (backlog, pp. 319-325), p. 29, p. 320, p. 328 quotations (backlog). Backlog pages are now printed.
- **Griffiths, D. J.** *Introduction to Quantum Mechanics.* 1st ed. Prentice Hall, 1995. **verified-on-page**
  - Cited in: 10, 11, 14, 15; README; zeno-anti-zeno spike; identical-particles spike; aharonov-bohm-berry spike; backlog.
  - Checked: §9.2.3, footnote 9, printed p. 310 (summing over frequencies assumes independent components; eqs. 9.39, 9.43) (nb 10); Afterword A.4 "The Quantum Zeno Paradox", eqs. A.14-A.20, printed pp. 383-384, including eq. A.20 and the bubble-chamber remark (nb 10, 11; zeno-anti-zeno spike); §5.1.2 "Exchange Forces", printed p. 184 (nb 14; identical-particles spike); §5.4.3 "The Most Probable Configuration", printed p. 209 (nb 14); §10.2.2, printed p. 338 ("Is Berry's phase measurable?": interference with a reference beam) (nb 15); §10.2.3, printed p. 342 (geometric phase is "minus one half the solid angle swept out by the magnetic field vector") (nb 15); §10.2.4 "The Aharonov-Bohm Effect", printed pp. 343-349, incl. p. 349 "There can be electromagnetic effects in regions where the fields are zero" (nb 15).
  - Cited but not individually checked: §9.3 (name A for the rate, nb 10); backlog items §4.4.2 p. 164, p. 3, pp. 380-383 (converted from PDF pages with an approximate offset).
- **Nielsen, M. A., and I. L. Chuang.** *Quantum Computation and Quantum Information.* Cambridge University Press, 2000 (10th anniversary ed. 2010). The project says "Cambridge 2000/2010". **verified-on-page**
  - Cited in: 03, 04, 06, 07, 08, 09; README; backlog.
  - Sections cited: Postulate 2 (nb 03); §2.2.3 Postulate 3, eq. 2.94 (nb 04); §8.3.6 phase damping, eqs. 8.127-8.130 (nb 06, 08); §8.4.1 non-Markovian dynamics and eq. 8.134 (nb 08); ch. 8 operator-sum form (nb 08); ch. 9 fidelity, trace distance, Fig. 9.1 (nb 07); ch. 6 Grover search, §6.1.3 (nb 09).
- **Norris, J. R.** *Markov Chains.* Cambridge University Press, 1997. Local file: `papers to study/norris.pdf`. **verified-on-page**
  - Cited in: 01, 02, 03, 10; README.
  - Checked: §1.1, after Example 1.1.5 (lumping can destroy the Markov property) (nb 10).
  - Cited but not individually named as checked: §1.1 definition of Markov(lambda, P); Example 1.1.4 (two-state chain); §2.1 "Q-matrices and their exponentials"; Thm 2.1.1 and Thm 2.1.2 (nb 01, 02, 03). Norris uses row-stochastic matrices; the notebooks use the column convention.
- **Peskin, M. E., and D. V. Schroeder.** *An Introduction to Quantum Field Theory.* Addison-Wesley/Perseus, 1995. **verified-on-page**
  - Cited in: 10, 12, 14, 15; README; wick-rotation spike; identical-particles spike; aharonov-bohm-berry spike; backlog.
  - Checked: §4.5, eq. 4.62, printed p. 101 (decay rate) (nb 10); §9.1, printed p. 276 (real-time path integral, "coherent sum of the amplitudes") (nb 12; wick-rotation spike); §9.3, printed pp. 292-293 (rotation to imaginary time, partition-function analogy) (nb 12); §9.5, printed p. 299 (Grassmann rules "might seem ad hoc") (nb 14; identical-particles spike); §15.3, printed p. 492 ("all gauge-invariant functions of A_mu can be thought of as combinations of Wilson loops") (nb 15).
  - Cited in the backlog but not individually checked: §7.3 (pp. 231, 236), §2.1/2.4, §12.1 (backlog pages now printed).
- **Schleich, W. P.** *Quantum Optics in Phase Space.* Wiley-VCH, 2001. **verified-on-page**
  - Cited in: 13, 16; README; wigner and matter-wave-gratings spikes; backlog.
  - Checked: §3.2.3 "Shape of Wigner Function", printed p. 73 (Wigner functions can take negative values); §3.3.2 "Quantum Liouville Equation", printed p. 76 (quadratic potentials: each phase-space point moves along classical trajectories); §19.3, printed p. 558 (Raman-Nath: the atom moves "a distance which is much less than a wavelength of the light") (nb 16); §19.4.2, printed p. 563 (momentum quantization "emerges from the periodicity of the potential") (nb 16); problem 9.6, printed pp. 250-251 (Talbot effect) (nb 16); reference lists on printed p. 253 (Talbot; Clauser and Li) and p. 576 (Kapitza and Dirac) (nb 16).
  - Cited in the backlog but not individually checked: ch. 7, §4.5, §9.2/9.5, §15.1, §16.2, §18.2-18.4, §19.3-19.4; backlog pages now printed.

## Research papers

- **Aaronson, S., and A. Arkhipov.** "The computational complexity of linear optics." *Proc. 43rd ACM Symposium on Theory of Computing (STOC 2011)*, 333-342; expanded in *Theory of Computing* 9, 143 (2013); arXiv:1011.3245. Boson sampling; the "bosonic birthday paradox" is in §13, and Haar averages. Cite this first; Arkhipov and Kuperberg (next entry) is the follow-up. **verified 2026-10-29**; §13 confirmed 2026-11-05 (Appendix: The Bosonic Birthday Paradox); Theorem 72 is a collision bound; 1/2 vs 2/3 quoted as well known
  - Cited in: 14; identical-particles spike.
- **Arkhipov, A., and G. Kuperberg.** "The bosonic birthday paradox." *Geometry & Topology Monographs* 18, 1-7 (2012), arXiv:1106.0849, doi:10.2140/gtm.2012.18.1. The follow-up paper on the bosonic birthday paradox; the project names only Aaronson and Arkhipov. **verified 2026-10-29**
  - Cited in: alongside Aaronson and Arkhipov (14; identical-particles spike).
- **Aharonov, Y., and D. Bohm.** "Significance of Electromagnetic Potentials in the Quantum Theory." *Phys. Rev.* 115, 485-491 (1959). The Aharonov-Bohm effect. Details as cited on disk by Griffiths (p. 343, footnote 14) and Peskin (p. 491 footnote) agree; the paper's text not checked. **verified 2026-10-29**
  - Cited in: 15; aharonov-bohm-berry spike.
- **Aharonov, Y., and J. Anandan.** "Phase Change during a Cyclic Quantum Evolution." *Phys. Rev. Lett.* 58, 1593-1596 (1987). Non-adiabatic geometric phase. **verified 2026-10-29**
  - Cited in: 15; aharonov-bohm-berry spike.
- **Ambainis, A.** "Quantum lower bounds by quantum arguments." *J. Comput. Syst. Sci.* 64, 750-767 (2002) (conference version STOC 2000, pp. 636-643). The adversary method (query lower bounds). **verified 2026-10-29**
  - Cited in: 09 (pending literature); gamma-only-query-bound spike.
- **Arkani-Hamed, N., Q. Cao, J. Dong, C. Figueiredo, and S. He.** "Surface Kinematics and the Canonical Yang-Mills All-Loop Integrand." *Phys. Rev. Lett.* 134, 171601 (2025). The surfaceology note says local copies are in `~/Desktop/figueiredo/surfaceology/`, outside this project; which file matches which citation is not stated. **held-locally**; **verified 2026-10-29**
  - Cited in: surfaceology note.
- **Azuma, H.** "Decoherence in Grover's quantum algorithm: Perturbative approach." *Phys. Rev. A* 65, 042311 (2002); erratum *Phys. Rev. A* 66, 019903(E) (2002); arXiv:quant-ph/0110101. Grover under noise. This is the closest match for the project's "Azuma 2002"; not confirmed as the paper meant. **best match, unconfirmed**
  - Cited in: 09; grover-as-isp spike.
- **Bennett, C. H., E. Bernstein, G. Brassard, and U. Vazirani.** "Strengths and Weaknesses of Quantum Computing." *SIAM J. Comput.* 26(5), 1510-1523 (1997) ("BBBV"). Optimality of the square-root query bound; hybrid argument. **verified 2026-10-29**
  - Cited in: 09; gamma-only-query-bound spike; grover-as-isp spike.
- **Bernard, D., and T. Jin.** "Open Quantum Symmetric Simple Exclusion Process." *Phys. Rev. Lett.* 123, 080601 (2019). "Quantum SSEP" (dephased free fermions to symmetric exclusion; the 2026-10-29 check found this a fair short description). **verified 2026-10-29**
  - Cited in: 14; identical-particles spike.
- **Berry, M. V.** "Quantal phase factors accompanying adiabatic changes." *Proc. R. Soc. Lond. A* 392, 45-57 (1984). Berry's phase. Details as cited on disk by Griffiths (§10.2.2) agree; the paper's text not checked. **verified 2026-10-29**
  - Cited in: 15; aharonov-bohm-berry spike.
- **Boyer, M., G. Brassard, P. Hoyer, and A. Tapp.** "Tight Bounds on Quantum Searching." *Fortschr. Phys.* 46, 493-505 (1998) ("BBHT98"), arXiv:quant-ph/9605034. Cited as the source N&C's search proof follows. **verified 2026-10-29** (arXiv number from standard citation)
  - Cited in: 09.
- **Braunstein, S. L., and C. M. Caves.** "Statistical distance and the geometry of quantum states." *Phys. Rev. Lett.* 72, 3439-3443 (1994). Classical Fisher information from any measurement is at most the quantum Fisher information. **verified 2026-10-29**
  - Cited in: 07, 09.
- **Bravyi, S., D. P. DiVincenzo, R. I. Oliveira, and B. M. Terhal.** "The complexity of stoquastic local Hamiltonian problems." *Quantum Inf. Comput.* 8(5), 361-385 (2008). Stoquastic Hamiltonians. **verified 2026-10-29**
  - Cited in: 12; wick-rotation spike.
- **Breuer, H.-P., E.-M. Laine, and J. Piilo.** "Measure for the Degree of Non-Markovian Behavior of Quantum Processes in Open Systems." *Phys. Rev. Lett.* 103, 210401 (2009). The "BLP" trace-distance measure of non-Markovianity. **verified 2026-10-29**
  - Cited in: 03, 06, 07, 08, 10.
- **Brezger, B., L. Hackermüller, S. Uttenthaler, J. Petschinka, M. Arndt, and A. Zeilinger.** "Matter-Wave Interferometer for Large Molecules." *Phys. Rev. Lett.* 88, 100404 (2002). Talbot-Lau interferometer for large molecules. **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Brown, H. R.** "Aspects of objectivity in quantum mechanics." In J. Butterfield and C. Pagonis (eds.), *From Physics to Philosophy*, Cambridge University Press, 1999, pp. 45-70. Mentioned in the Barandes lecture map as "V(t) gauge, Brown 1999"; identified from the reference lists of Barandes's Papers 1 and 3, which give only "H. Brown". **verified 2026-10-29**
  - Cited in: lecture README.
- **Busch, P.** "Quantum States and Generalized Observables: A Simple Proof of Gleason's Theorem." *Phys. Rev. Lett.* 91, 120403 (2003). Extension of Gleason's theorem to POVMs (covers dimension 2). **verified 2026-10-29**
  - Cited in: 04.
- **Carrôlo, S., and C. Figueiredo.** "How gluon leading singularities discover curves on surfaces." *JHEP* 07 (2026) 101, arXiv:2512.17019. Local copies as for Arkani-Hamed et al. above. **held-locally**; **verified 2026-10-29**
  - Cited in: surfaceology note.
- **Chruściński, D., A. Kossakowski, and A. Rivas.** "Measures of non-Markovianity: Divisibility versus backflow of information." *Phys. Rev. A* 83, 052128 (2011). Flagged as a "next to check" paper cited by Rivas et al. **verified 2026-10-29**
  - Cited in: 08.
- **Clauser, J. F., and S. Li.** "Talbot-von Lau atom interferometry with cold slow potassium." *Phys. Rev. A* 49, R2213-R2216 (1994). Details as cited on disk by Schleich (printed p. 253) agree. **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Eisler, V.** "Crossover between ballistic and diffusive transport: the quantum exclusion process." *J. Stat. Mech.* (2011) P06007. Dephased free fermions and symmetric exclusion. **verified 2026-10-29**
  - Cited in: 14; identical-particles spike.
- **Farhi, E., and S. Gutmann.** "Analog analogue of a digital quantum computation." *Phys. Rev. A* 57, 2403-2406 (1998). Analog (Hamiltonian) search. **verified 2026-10-29**
  - Cited in: 09; grover-as-isp spike; margolus-levitin-gamma spike.
- **Figueiredo, C., and M. Skowronek.** "Cuts and Contours." arXiv:2506.05456. Local copies as for Arkani-Hamed et al. above. **held-locally**; **verified 2026-10-29**
  - Cited in: surfaceology note.
- **Fischer, M. C., B. Gutiérrez-Medina, and M. G. Raizen.** "Observation of the Quantum Zeno and Anti-Zeno Effects in an Unstable System." *Phys. Rev. Lett.* 87, 040402 (2001). Both Zeno and anti-Zeno effects observed in an unstable system. **verified 2026-10-29**
  - Cited in: 11; zeno-anti-zeno spike.
- **Fonda, L., G. C. Ghirardi, and A. Rimini.** "Decay theory of unstable quantum systems." *Rep. Prog. Phys.* 41, 587-631 (1978). Non-exponential decay review. **verified 2026-10-29**
  - Cited in: 10; golden-rule-divisibility spike.
- **Gerlich, S., L. Hackermüller, K. Hornberger, A. Stibor, H. Ulbricht, M. Gring, F. Goldfarb, T. Savas, M. Müri, M. Mayor, and M. Arndt.** "A Kapitza-Dirac-Talbot-Lau interferometer for highly polarizable molecules." *Nature Physics* 3, 711-715 (2007). **verified 2026-10-29** (first five authors confirmed in Crossref; the rest from standard citation)
  - Cited in: 16; matter-wave-gratings spike.
- **Giardinà, C., J. Kurchan, and F. Redig.** "Duality and exact correlations for a model of heat conduction." *J. Math. Phys.* 48, 033301 (2007). Origin of the symmetric inclusion process. **verified 2026-10-29**
  - Cited in: 14. See the inconsistency note below (resolved).
- **Giardinà, C., J. Kurchan, F. Redig, and K. Vafayi.** "Duality and Hidden Symmetries in Interacting Particle Systems." *J. Stat. Phys.* 135, 25-55 (2009). This is the paper the identical-particles spike cites as "Giardina, Kurchan, Redig & Vafayi 2009/2010"; the year is 2009. Split out of the 2010 entry on 2026-10-29; it has no key of its own in `references.bib` (see the note there). **verified 2026-10-29**
  - Cited in: identical-particles spike.
- **Giardinà, C., F. Redig, and K. Vafayi.** "Correlation Inequalities for Interacting Particle Systems with Duality." *J. Stat. Phys.* 141, 242-263 (2010). Symmetric inclusion process; a different paper from the 2009 one. **verified 2026-10-29**
  - Cited in: 14.
- **Giovannetti, V., S. Lloyd, and L. Maccone.** "Quantum limits to dynamical evolution." *Phys. Rev. A* 67, 052109 (2003). Unified and non-orthogonal speed limits (the project's description, not the title). **verified 2026-10-29**
  - Cited in: 09; margolus-levitin-gamma spike.
- **Gleason, A. M.** "Measures on the Closed Subspaces of a Hilbert Space." *J. Math. Mech.* 6(6), 885-893 (1957) (the journal is now *Indiana Univ. Math. J.*). Gleason's theorem (dimension at least 3). The local file `papers to study/Gleason's.pdf` is not this paper: it is M. Sassoli de Bianchi, "Why qubits are exceptional in Gleason's theorem: a Bloch-space perspective," arXiv:2603.07745 (2026), an exposition. If notebook 04 drew on that file, cite it as well. **verified 2026-10-29** (no longer held-locally, since the local file is a different paper)
  - Cited in: 04 (statement of the theorem, and why it does not cover a qubit).
- **Glick, J. R., and C. Adami.** "Markovian and Non-Markovian Quantum Measurements." *Found. Phys.* 50, 1008-1055 (2020), arXiv:1701.05636, doi:10.1007/s10701-020-00362-4. Cited by Barandes in the lecture Q&A (about 66-70 min) on empirical distinction from literal collapse; the transcript spelling is "Glickadami". Identified from the reference lists of Barandes's Papers 1 and 3. **verified 2026-10-29**
  - Cited in: 02, 06, 08; README; lecture README.
- **Gould, P. L., G. A. Ruff, and D. E. Pritchard.** "Diffraction of atoms by light: The near-resonant Kapitza-Dirac effect." *Phys. Rev. Lett.* 56, 827-830 (1986). **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Gross, D.** "Hudson's theorem for finite-dimensional quantum systems." *J. Math. Phys.* 47, 122107 (2006). Discrete Wigner function and discrete Hudson theorem. **verified 2026-10-29**
  - Cited in: 13; README; wigner spike.
- **Gu, M., K. Wiesner, E. Rieper, and V. Vedral.** "Quantum mechanics can reduce the complexity of classical models." *Nat. Commun.* 3, 762 (2012), doi:10.1038/ncomms1761, arXiv:1102.1994 (arXiv title: "Occam's Quantum Razor: How Quantum Mechanics can reduce the complexity of classical models"). Quantum models of a known process need less memory. The article number 762 is correct (Nature and Crossref); a suggested change to 763 was wrong. **verified 2026-10-29**
  - Cited in: fitting-hilbert-reps spike.
- **Hackermüller, L., K. Hornberger, B. Brezger, A. Zeilinger, and M. Arndt.** "Decoherence of matter waves by thermal emission of radiation." *Nature* 427, 711-714 (2004). **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Hall, M. J. W., J. D. Cresser, L. Li, and E. Andersson.** "Canonical form of master equations and characterization of non-Markovianity." *Phys. Rev. A* 89, 042120 (2014). Decay-rate measure of non-Markovianity, as discussed in Rivas et al. §4.4. **verified 2026-10-29**
  - Cited in: 08.
- **Hong, C. K., Z. Y. Ou, and L. Mandel.** "Measurement of subpicosecond time intervals between two photons by interference." *Phys. Rev. Lett.* 59, 2044-2046 (1987). Hong-Ou-Mandel effect. **verified 2026-10-29**
  - Cited in: 12, 14; README; identical-particles spike; backlog.
- **Horn, A.** "Doubly Stochastic Matrices and the Diagonal of a Rotation Matrix." *Amer. J. Math.* 76(3), 620-630 (1954), doi:10.2307/2372705. Called "ortho-stochastic" matrices; credited in Paper 1 (as relayed in notebook 03). **verified 2026-10-29**
  - Cited in: 03.
- **Hornberger, K., S. Uttenthaler, B. Brezger, L. Hackermüller, M. Arndt, and A. Zeilinger.** "Collisional Decoherence Observed in Matter Wave Interferometry." *Phys. Rev. Lett.* 90, 160401 (2003). **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Itano, W. M., D. J. Heinzen, J. J. Bollinger, and D. J. Wineland.** "Quantum Zeno effect." *Phys. Rev. A* 41, 2295-2300 (1990). Zeno experiment with trapped ions. **verified 2026-10-29**
  - Cited in: 11; zeno-anti-zeno spike.
- **Kapitza, P. L., and P. A. M. Dirac.** "The reflection of electrons from standing light waves." *Proc. Camb. Philos. Soc.* 29, 297-300 (1933), doi:10.1017/S0305004100011105. Details as cited on disk by Schleich (printed p. 576) agree. **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Khalfin, L. A.** "Contribution to the decay theory of a quasi-stationary state." *Zh. Eksp. Teor. Fiz.* 33, 1371 (1957) [English translation: *Sov. Phys. JETP* 6, 1053 (1958)]. Non-exponential decay. The project's "1958" is the year of the translation. **verified 2026-10-29** (from standard citations; no online record retrieved)
  - Cited in: 10; golden-rule-divisibility spike.
- **Kofman, A. G., and G. Kurizki.** "Acceleration of quantum decay processes by frequent observations." *Nature* 405, 546-550 (2000). Anti-Zeno effect more common than Zeno; overlap formula. **verified 2026-10-29**
  - Cited in: 10, 11; golden-rule-divisibility spike; zeno-anti-zeno spike.
- **Levitin, L. B., and T. Toffoli.** "Fundamental Limit on the Rate of Quantum Dynamics: The Unified Bound Is Tight." *Phys. Rev. Lett.* 103, 160502 (2009). Tightness of max(Mandelstam-Tamm, Margolus-Levitin). **verified 2026-10-29**
  - Cited in: margolus-levitin-gamma spike.
- **Long, G. L., Y. S. Li, W. L. Zhang, and C. C. Tu.** "Dominant gate imperfection in Grover's quantum search algorithm." *Phys. Rev. A* 61, 042305 (2000). The project cites "Long et al." for Grover under decoherence and noisy oracles; no Long paper matching that description exactly was found, and this one is about gate imperfections. **best match, unconfirmed**
  - Cited in: 09; grover-as-isp spike.
- **Lukacs, E.** *Characteristic Functions.* 2nd ed. London: Griffin, 1970. Zeros of characteristic functions and infinite divisibility. **verified 2026-10-29** (existence and edition from standard catalogue records and a 1972 review in Crossref; the claim about zeros and infinite divisibility not checked on the page)
  - Cited in: 16; matter-wave-gratings spike.
- **Mandelstam, L., and I. Tamm.** "The uncertainty relation between energy and time in non-relativistic quantum mechanics." *J. Phys. (USSR)* 9, 249-254 (1945); reprinted in *Selected Papers* (Springer, 1991), pp. 115-123. Quantum speed limit. **verified 2026-10-29** (original-journal details from standard citations; the reprint confirmed in Crossref)
  - Cited in: 07, 09; grover-as-isp spike; margolus-levitin-gamma spike.
- **Margolus, N., and L. B. Levitin.** "The maximum speed of dynamical evolution." *Physica D* 120, 188-195 (1998). Margolus-Levitin speed limit. **verified 2026-10-29**
  - Cited in: 07, 09, 12; grover-as-isp spike; margolus-levitin-gamma spike.
- **Mari, A., and J. Eisert.** "Positive Wigner Functions Render Classical Simulation of Quantum Computation Efficient." *Phys. Rev. Lett.* 109, 230503 (2012). Wigner negativity and efficient classical simulation. **verified 2026-10-29**
  - Cited in: 13; wigner spike.
- **Misra, B., and E. C. G. Sudarshan.** "The Zeno's paradox in quantum theory." *J. Math. Phys.* 18, 756-763 (1977). The quantum Zeno effect. The project notes it is "confirmed as cited in Griffiths's Afterword"; that claim was not re-checked on 2026-10-29. **verified 2026-10-29**
  - Cited in: 06, 10, 11; zeno-anti-zeno spike.
- **Monras, A., A. Beige, and K. Wiesner.** "Hidden Quantum Markov Models and non-adaptive read-out of many-body states." arXiv:1002.2337 (2010). Defines hidden quantum Markov models. **verified 2026-10-29**
  - Cited in: fitting-hilbert-reps spike.
- **Nelson, E.** "Derivation of the Schrödinger Equation from Newtonian Mechanics." *Phys. Rev.* 150, 1079-1085 (1966). Stochastic mechanics. (Barandes also cites Nelson's book *Dynamical Theories of Brownian Motion*, 1967.) **verified 2026-10-29**
  - Cited in: 12; wick-rotation spike; backlog.
- **Ness, G., A. Alberti, and Y. Sagi.** "Quantum Speed Limit for States with a Bounded Energy Spectrum." *Phys. Rev. Lett.* 129, 140403 (2022), arXiv:2206.14803. The project notes the full text was not read and the prefactor is unchecked; that is still true. **verified 2026-10-29**
  - Cited in: 07, 09; margolus-levitin-gamma spike.
- **Okuyama, M., and M. Ohzeki.** "Quantum Speed Limit is Not Quantum." *Phys. Rev. Lett.* 120, 070402 (2018), arXiv:1710.03498. Speed limits for classical dynamics. **verified 2026-10-29**
  - Cited in: 07.
- **Osterwalder, K., and R. Schrader.** "Axioms for Euclidean Green's functions." *Commun. Math. Phys.* 31, 83-112 (1973) (Part II: 42, 281-305 (1975)). Reflection positivity. **verified 2026-10-29**
  - Cited in: 12; wick-rotation spike; backlog.
- **Pablo-Norman, B., and M. Ruiz-Altaba.** "Noise in Grover's quantum search algorithm." *Phys. Rev. A* 61, 012301 (2000; published online 1999). Grover under noise. **verified 2026-10-29**
  - Cited in: 09.
- **Rivas, A., S. F. Huelga, and M. B. Plenio.** "Quantum non-Markovianity: characterization, quantification and detection." *Rep. Prog. Phys.* 77, 094001 (2014), arXiv:1405.0303v2. Local file: `papers to study/Quantum Non-Markovianity Rivas.pdf`. **held-locally**; **verified 2026-10-29**
  - Cited in: 01, 02, 03, 06, 07, 08; README.
  - Sections cited: §2 (Def. 2.1 Markov, Def. 2.2 divisible, eqs. 1, 4, 11-19, Cor. 2.2, Thm 2.3, Thm 2.4); §3.2 (Def. 3.1 P-divisible, Def. 3.2 Markovian, eqs. 23-29, Thm 3.1 GKSL); §3.4 (eq. 50); §4.3 (eqs. 64-69, RHP); §4.4 (eqs. 92-94); §5.1.1 (eqs. 102-105, BLP); §5.1.4 (eq. 123, Fisher information; ref. [209] is Braunstein-Caves); Examples 4.1, 4.2, 5.1. The notebooks quote these places in detail, but no page-level check is recorded.
- **Rosenblatt, J., and P. D. Seymour.** "The structure of homometric sets." *SIAM J. Algebraic Discrete Methods* 3(3), 343-350 (1982). One-dimensional phase retrieval uniqueness (homometric sets). **verified 2026-10-29**
  - Cited in: margolus-levitin-gamma spike.
- **Shahbeigi, F., C. Chubb, R. Kukulski, L. Pawela, and K. Korzekwa.** "Quantum-embeddable stochastic matrices." *Quantum* 8, 1404 (2024), doi:10.22331/q-2024-07-10-1404. **verified 2026-10-29**
  - Cited in: fitting-hilbert-reps spike.
- **Shanahan, B., A. Chenu, N. Margolus, and A. del Campo.** "Quantum Speed Limits across the Quantum-to-Classical Transition." *Phys. Rev. Lett.* 120, 070401 (2018), arXiv:1710.07335. Speed limits for classical dynamics. **verified 2026-10-29**
  - Cited in: 07.
- **Shenvi, N., K. R. Brown, and K. B. Whaley.** "Effects of a random noisy oracle on search algorithm complexity." *Phys. Rev. A* 68, 052313 (2003). Grover under noise. **verified 2026-10-29**
  - Cited in: 09; grover-as-isp spike.
- **Smirne, A., A. Stabile, and B. Vacchini.** "Signatures of non-Markovianity in classical single-time probability distributions." *Phys. Scr.* T153, 014057 (2013). Flagged as a "next to check" paper cited by Rivas et al. **verified 2026-10-29**; **verified 2026-11-05** (arXiv:1211.5913; Crossref doi:10.1088/0031-8949/2013/t153/014057)
  - Cited in: 06 (R = Kolmogorov-distance revival), 08.
- **Spekkens, R. W.** "Evidence for the epistemic view of quantum states: A toy theory." *Phys. Rev. A* 75, 032110 (2007). Classical toy theory reproducing stabilizer behaviour. The wigner spike writes "2007/2016"; the toy theory is 2007 only. **verified 2026-10-29**
  - Cited in: 13; wigner spike.
- **Srinivasan, S., G. Gordon, and B. Boots.** "Learning Hidden Quantum Markov Models." arXiv:1710.09016 (2017); *Proc. AISTATS 2018*, PMLR 84. **verified 2026-10-29** (arXiv record; the AISTATS venue from standard citation)
  - Cited in: fitting-hilbert-reps spike.
- **Stern, A., Y. Aharonov, and Y. Imry.** "Phase uncertainty and loss of interference: A general picture." *Phys. Rev. A* 41, 3436-3448 (1990). Dephasing of Aharonov-Bohm interference. **verified 2026-10-29**
  - Cited in: 15; aharonov-bohm-berry spike.
- **Talbot, H. F.** "Facts relating to optical science. No. IV." *Philos. Mag.* (3rd series) 9(56), 401-407 (1836), doi:10.1080/14786443608649032. Details as cited on disk by Schleich (printed p. 253). **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **Thompson, R. C.** "Lecture Notes from a Johns Hopkins University Lecture Series." Unpublished lecture notes, 1989. Credited in Paper 1 (ref. [62], as relayed in notebook 03) with the modern name "unistochastic". **verified 2026-10-29** (against Barandes's reference list only; the notes are unpublished)
  - Cited in: 03.
- **Tomaz, A. A., R. S. Mattos, and M. Barbatti.** "The Quantum Measurement Problem: A Review of Recent Trends." arXiv:2502.19278 (2025); doi:10.1080/14786435.2025.2601922. Local file: `papers to study/Quantum Measurement Problem review.pdf` (the file name gives no author; identified from the PDF's title page). Previously listed as an unattributed "Quantum measurement problem review". **held-locally**; **verified 2026-10-29**
  - Cited in: 04 (survey of where Zurek's derivation is and is not accepted).
- **Tonomura, A., J. Endo, T. Matsuda, T. Kawasaki, and H. Ezawa.** "Demonstration of single-electron buildup of an interference pattern." *Am. J. Phys.* 57, 117-120 (1989). Electron interference built up one arrival at a time; cited through Ballentine Ch. 5. **verified 2026-10-29**
  - Cited in: 05.
- **Troyer, M., and U.-J. Wiese.** "Computational Complexity and Fundamental Limitations to Fermionic Quantum Monte Carlo Simulations." *Phys. Rev. Lett.* 94, 170201 (2005). The sign problem. **verified 2026-10-29**
  - Cited in: 12; wick-rotation spike.
- **Vacchini, B., A. Smirne, E.-M. Laine, J. Piilo, and H.-P. Breuer.** "Markovianity and non-Markovianity in quantum and classical systems." *New J. Phys.* 13, 093004 (2011). Flagged as a "next to check" paper cited by Rivas et al. **verified 2026-10-29**
  - Cited in: 02, 06, 08.
- **Veitch, V., C. Ferrie, D. Gross, and J. Emerson.** "Negative quasi-probability as a resource for quantum computation." *New J. Phys.* 14, 113011 (2012). Negativity and efficient classical simulation. **verified 2026-10-29**
  - Cited in: 13; wigner spike.
- **Wolf, M. M., and J. I. Cirac.** "Dividing Quantum Channels." *Commun. Math. Phys.* 279, 147-168 (2008), arXiv:math-ph/0611057v3. Local file: `papers to study/Dividing Quantum Channels.pdf`. **held-locally**; **verified 2026-10-29**
  - Cited in: 01, 02, 03, 05, 08; README.
  - Sections cited: abstract and Fig. 1; §I (infinite divisibility, de Finetti); §II (Markovian channel as a CP semigroup element); §IV Definition 8 (an indivisible channel); §V; §VI (qubit channels by Lorentz normal form). The notebooks quote these places, but no page-level check is recorded.
- **Wootters, W. K.** "A Wigner-function formulation of finite-state quantum mechanics." *Ann. Phys.* 176, 1-21 (1987). Discrete Wigner function. **verified 2026-10-29**
  - Cited in: 13; README; wigner spike; backlog.
- **Zalka, C.** "Grover's quantum searching algorithm is optimal." *Phys. Rev. A* 60, 2746-2751 (1999). Grover search is "asymptotically, exactly optimal". **verified 2026-10-29**
  - Cited in: 09; gamma-only-query-bound spike; grover-as-isp spike.
- **Zurek, W. H.** "Probabilities from entanglement, Born's rule p_k = |psi_k|^2 from envariance." *Phys. Rev. A* 71, 052105 (2005), arXiv:quant-ph/0405161. Derivation of the Born rule from envariance. Local file: `papers to study/Born Rule Wojciech.pdf` (the arXiv v2 preprint). The notebook says the argument is not tested anywhere in the lab. **held-locally**; **verified 2026-10-29**
  - Cited in: 04.

## Other (lectures, transcripts, web pages)

- **Barandes, J. A.** "A New Formulation of Quantum Theory." Lecture to a Zoom philosophy-of-physics seminar (about 57 minutes of talk plus about 60 minutes of Q&A). Source video ID given in the project: sshJyD0aWXg. Local file: `notes/barandes-lectures-2026-10/new-formulation-lecture-transcript.txt` (auto-transcribed with whisper.cpp, base.en; contains name errors, and `[Nm]` minute markers). **held-locally** (not re-checked on 2026-10-29)
  - Cited in: 03, 05, 06, 07; README; lecture README; fitting-hilbert-reps spike.
  - Cited points: about 17-18 min (squaring is a re-description, not an axiom); about 31-32 min (dilated Hilbert space size); about 38-39 min (squared entries do not compose); about 42-44 min (division events); double-slit segment (Markov assumption); Q&A about 66-70 min (Glick and Adami). Notebook 03 notes that lecture quotations come from an auto-generated transcript and that the paper is the reference for exact wording.
- **Barandes, J. A., interview clip on entanglement and non-locality** ("Harvard Scientist Beautifully Explains Quantum Entanglement and Non-Locality", Theories of Everything podcast, about 15 minutes). Source video ID given in the project: QTa-YQCMUFs. Local file: `notes/barandes-lectures-2026-10/entanglement-interview-transcript.txt`. **held-locally** (not re-checked on 2026-10-29)
  - Cited in: lecture README only.
- **Figueiredo, C.** "The Joy of Surfaceology: Part 2." Lecture at the Kavli Institute for Theoretical Physics (KITP); speaker affiliation Princeton. https://www.youtube.com/watch?v=qXaI3yC_-PI. Part 1 "was not available". **verified 2026-10-29** (title, channel and speaker via YouTube oEmbed; recording date not retrieved)
  - Cited in: surfaceology note.
- **NIST Digital Library of Mathematical Functions (DLMF).** §10.23(ii), addition theorems for Bessel functions (Neumann's, eq. 10.23.2; Graf's, eq. 10.23.7; eq. 10.23.6 defines w and chi). Both equation numbers confirmed. **verified 2026-10-29**
  - Cited in: 16; matter-wave-gratings spike.
- **nLab.** "Indivisible stochastic process interpretation of quantum mechanics." Local file: `papers to study/indivisible stochastic process interpretation of quantum mechanics in nLab.pdf`. Notebook 01 uses its statement of divisibility, P(t1,t0) = P(t1,t) P(t,t0), and its short reason quantum processes fail it (P_ij = |Theta_ij|^2). **held-locally**
  - Cited in: 01.

### Local PDFs with no citation found

The folder `papers to study/` also holds these files, which none of the scanned sources cite by name: `Barandes/` (holds the three papers above), `DISCRETE STOCHASTIC PROCESSES.pdf`, `Intro to prob.pdf`, `ModernQuantumMechanics.pdf`, `TheTheoryOfQuantumSystems.pdf`, `Vol 3 Ch 01 - Quantum Behavior.pdf`. They have no entries above because the project gives no bibliographic details for them. The README says the notebooks were written from "the Barandes papers and lecture transcripts, Nielsen & Chuang, Rivas, Dividing Quantum Channels, Norris and Ballentine".

The three PDFs added on 2026-10-29 (`2505.08785 ...`, `2512.18105 ...`, `2608.04354 ...`) are cited and have entries above. Two older files are mislabelled: `Gleason's.pdf` is Sassoli de Bianchi, arXiv:2603.07745 (see the Gleason entry), and `Quantum Measurement Problem review.pdf` is Tomaz, Mattos and Barbatti, arXiv:2502.19278. The files have not been renamed.

## Inconsistencies noted while compiling

- The Barandes papers' years differ between sources. Local file names say 2025 (Correspondence), 2026 (Theorem) and 2025 (ISP), while the arXiv numbers (2302, 2309, 2507) imply first postings in 2023, 2023 and 2025. Updated 2026-10-29: Paper 1 is published as *Philosophy of Physics* 3(1), 8 (2025), and Paper 3 as *Stud. Hist. Phil. Sci.* 119, 102213 (2026); no journal version of Paper 2 was found. Cite the published versions where possible. `references.bib` now gives the journal years for Papers 1 and 3 (the bib keys keep their old years).
- Resolved 2026-11-05: Paper 2 (2309.03085v2) §3.5 'Unistochastic Processes', display (68), p. 17, checked; Paper 1 §3.4 eq. 30 also correct.
- Resolved 2026-10-29: the inclusion-process citations are three separate papers. Notebook 14's "Giardina, Kurchan & Redig (2007)" is J. Math. Phys. 48 (2007) and its "Giardina, Redig & Vafayi (2010)" is J. Stat. Phys. 141 (2010); the identical-particles spike's "Giardina, Kurchan, Redig & Vafayi 2009/2010" is J. Stat. Phys. 135 (2009), and should read 2009.
- Resolved 2026-10-29: Spekkens, Phys. Rev. A 75, 032110 is 2007. The wigner spike's "2007/2016" is unsupported.
- Resolved 2026-11-05: notebook 09 now describes arXiv:2512.18105 correctly (the CHSH game and Tsirelson's bound, not algorithms); notebooks 06 and 08 cite §3.1 and §3.2.
- New 2026-10-29: two local PDFs are mislabelled (`Gleason's.pdf`, `Quantum Measurement Problem review.pdf`); see the Local PDFs section above.
- Resolved 2026-10-25: the backlog mixed printed and PDF page numbers (e.g. Peskin p. 276 vs p. 298; Griffiths footnote 9 p. 310 vs p. 325). It now uses printed pages throughout.

## Added 2026-10-29: sources for the notebooks' "Prior work" notes

These were added when the notebooks were brought in line with the 2026-10-29 literature recheck. Every entry was checked against its arXiv record or Crossref on 2026-10-29 (**verified 2026-10-29**); passages were not checked unless the recheck reports say so (`notes/lit-recheck-2026-10-29/`).

- **F. Buscemi, N. Datta** "Equivalence between divisibility and monotonic decrease of information in classical and quantum stochastic processes." Phys. Rev. A, 93, 012101 (2016). arXiv:1408.7062. **verified 2026-10-29**
  - Cited in: 03, 06, 08, README. Note: gap rule; π/2 threshold.
- **S. Milz, K. Modi** "Quantum stochastic processes and quantum non-Markovian phenomena." PRX Quantum, 2, 030201 (2021). arXiv:2012.01894. **verified 2026-10-29**
  - Cited in: 03. Note: cited by Paper 1 for generic indivisibility.
- **S. Milz, D. Egloff, P. Taranto, T. Theurer et al.** "When is a non-Markovian quantum process classical?." Phys. Rev. X, 10, 041049 (2020). arXiv:1907.05807. **verified 2026-10-29**
  - Cited in: 10, README. Note: the defect Δ.
- **D. LeBlond** "The electron double-slit experiment from an ISP perspective." (2025). arXiv:2511.02863. **verified 2026-10-29**
  - Cited in: 05, README. Note: preprint; double slit in ISP.
- **S. Calvo** "On the Stochastic-Quantum Correspondence." (2026). arXiv:2601.18720. **verified 2026-10-29**
  - Cited in: 05, 06. Note: preprint; matched divisibility, division-event criteria.
- **J. Doukas** "On the emergence of quantum mechanics from stochastic processes." (2026). arXiv:2602.22095. **verified 2026-10-29**
  - Cited in: 05. Note: preprint (v3, Oct 2026); §5.1.1 one Γ, distinct processes.
- **S. L. Braunstein, C. M. Caves, G. J. Milburn** "Generalized uncertainty relations: Theory, examples, and Lorentz invariance." Ann. Phys., 247, 135–173 (1996). arXiv:quant-ph/9507004. **verified 2026-10-29**
  - Cited in: 07, README. Note: journal details from the DOI 10.1006/aphy.1996.0040.
- **T. Nishiyama, Y. Hasegawa** "Unified speed limits in classical and quantum dynamics via temporal Fisher information." Phys. Rev. E, 114, 014120 (2026). arXiv:2504.04790. **verified 2026-10-29**
  - Cited in: 07, README.
- **F. Benatti, D. Chruściński, G. Nichele** "Quantum versus classical P-divisibility." Phys. Rev. A, 110, 052212 (2024). arXiv:2405.05794. **verified 2026-10-29**
  - Cited in: 06, 08, README. Note: Example 2.
- **A. Smirne, D. Egloff, M. G. Díaz, M. B. Plenio, S. F. Huelga** "Coherence and non-classicality of quantum Markov processes." Quantum Sci. Technol., 4, 01LT01 (2019). arXiv:1709.05267. **verified 2026-10-29**
  - Cited in: 06, 08.
- **G. S. Bloom** "A counterexample to a theorem of S. Piccard." J. Combin. Theory Ser. A, 22, 378–379 (1977). **verified 2026-10-29**
  - Cited in: 07. Note: checked on Crossref, doi:10.1016/0097-3165(77)90013-9; homometric sets.
- **E. Biham, O. Biham, D. Biron, M. Grassl, D. A. Lidar** "Grover's Quantum Search Algorithm for an Arbitrary Initial Amplitude Distribution." Phys. Rev. A, 60, 2742 (1999). arXiv:quant-ph/9807027. **verified 2026-10-29**
  - Cited in: 09, README.
- **J. J. Alvarez, C. Gómez** "A Comment on Fisher Information and Quantum Algorithms." (1999). arXiv:quant-ph/9910115. **verified 2026-10-29**
  - Cited in: 09, README. Note: preprint IFT-UAM/CSIC-99-43.
- **D. Reitzner, M. Hillery** "Grover search under localized dephasing." Phys. Rev. A, 99, 012339 (2019). arXiv:1712.06558. **verified 2026-10-29**
  - Cited in: 09.
- **O. Regev, L. Schiff** "Impossibility of a Quantum Speed-up with a Faulty Oracle." (2012). arXiv:1202.1027. **verified 2026-10-29**
  - Cited in: 09. Note: ICALP 2008 version not checked.
- **H. Friedman, D. A. Kessler, E. Barkai** "Quantum walks: The first detected passage time problem." Phys. Rev. E, 95, 032141 (2017). **verified 2026-10-29**
  - Cited in: 09. Note: checked on Crossref, doi:10.1103/PhysRevE.95.032141.
- **S. Aaronson** "Quantum Computing and Hidden Variables." Phys. Rev. A, 71, 032325 (2005). arXiv:quant-ph/0408035. **verified 2026-10-29**
  - Cited in: 09. Note: journal version of the arXiv paper 'Quantum Computing and Hidden Variables I'.
- **S. Aaronson** "Quantum Computing and Hidden Variables II: The Complexity of Sampling Histories." (2004). arXiv:quant-ph/0408119. **verified 2026-10-29**
  - Cited in: 09. Note: preprint; sampling histories gives O(N^1/3) search.
- **P. Facchi, S. Pascazio** "Quantum Zeno effects with "pulsed" and "continuous" measurements." in Time's Arrows, Quantum Measurements and Superluminal Behavior, ed. D. Mugnai, A. Ranfagni and L. S. Schulman (CNR, Rome), 139 (2001). arXiv:quant-ph/0101044. **verified 2026-10-29**
  - Cited in: 10, 11, README. Note: §3: the Zeno/anti-Zeno criterion.
- **P. Facchi, H. Nakazato, S. Pascazio** "From the quantum Zeno to the inverse quantum Zeno effect." Phys. Rev. Lett., 86, 2699–2703 (2001). arXiv:quant-ph/0006094. **verified 2026-10-29**
  - Cited in: 10, 11, README.
- **A. G. Kofman, G. Kurizki** "Universal dynamical control of quantum mechanical decay: Modulation of the coupling to the continuum." Phys. Rev. Lett., 87, 270405 (2001). arXiv:quant-ph/0107076. **verified 2026-10-29**
  - Cited in: 11.
- **L. S. Schulman** "Continuous and pulsed observations in the quantum Zeno effect." Phys. Rev. A, 57, 1509–1515 (1998). **verified 2026-10-29**
  - Cited in: 11. Note: checked on Crossref, doi:10.1103/PhysRevA.57.1509.
- **R. Yin, E. Barkai** "Restart Expedites Quantum Walk Hitting Times." Phys. Rev. Lett., 130, 050802 (2023). **verified 2026-10-29**
  - Cited in: 11. Note: checked on Crossref, doi:10.1103/PhysRevLett.130.050802.
- **H. Pashayan, J. J. Wallman, S. D. Bartlett** "Estimating outcome probabilities of quantum circuits using quasiprobabilities." Phys. Rev. Lett., 115, 070501 (2015). arXiv:1503.07525. **verified 2026-10-29**
  - Cited in: 13, README. Note: eq. 3 (Born rule as quasi-probability sum), eq. 7 (circuits), eq. 6 (unitary negativity); passage checked 2026-11-05 against arXiv text.
- **C. Ferrie, J. Emerson** "Frame representations of quantum mechanics and the necessity of negativity in quasi-probability representations." J. Phys. A: Math. Theor., 41, 352001 (2008). arXiv:0711.2658. **verified 2026-10-29**
  - Cited in: 13.
- **C. Giardinà, J. Kurchan, F. Redig, K. Vafayi** "Duality and Hidden Symmetries in Interacting Particle Systems." J. Stat. Phys., 135, 25–55 (2009). **verified 2026-10-29**
  - Cited in: 14. Note: checked 2026-10-29 in the recheck.
- **K. Yamaga** "Stochastic process emerged from lattice fermion systems by repeated measurements and large-time limit." Axioms, 9, 90 (2020). arXiv:2007.13940. **verified 2026-10-29**
  - Cited in: 14, README. Note: doi:10.3390/axioms9030090.
- **D. Wellnitz, G. Preisser, V. Alba, J. Dubail, J. Schachenmayer** "Rise and fall, and slow rise again, of operator entanglement under dephasing." Phys. Rev. Lett., 129, 170401 (2022). arXiv:2201.05099. **verified 2026-10-29**
  - Cited in: 14, README. Note: App. E.
- **A. Arkhipov, G. Kuperberg** "The bosonic birthday paradox." Geom. Topol. Monogr., 18, 1–7 (2012). arXiv:1106.0849. **verified 2026-10-29**
  - Cited in: 14. Note: follow-up to Aaronson–Arkhipov §13.
- **Z. Zimborás, M. Faccin, Z. Kádár, J. D. Whitfield, B. P. Lanyon, J. D. Biamonte** "Quantum Transport Enhancement by Time-Reversal Symmetry Breaking." Sci. Rep., 3, 2361 (2013). arXiv:1208.4049. **verified 2026-10-29**
  - Cited in: 15, README.
- **D. Lu, J. D. Biamonte, J. Li, H. Li et al.** "Chiral Quantum Walks." Phys. Rev. A, 93, 042302 (2016). arXiv:1405.6209. **verified 2026-10-29**
  - Cited in: 15, README.
- **C. Antonakos, A. F. Terzis** "Aharonov-Bohm effect as a diffusion phenomenon." (2023). arXiv:2307.06683. **verified 2026-10-29**
  - Cited in: 15. Note: preprint.
- **D. de Falco, D. Tamascelli** "Quantum walks: a Markovian perspective." in SOFSEM 2008, LNCS 4910 (Springer), 519–530 (2008). arXiv:0801.4515. **verified 2026-10-29**
  - Cited in: 16, README.
- **A. Ullah, S. K. Ruddell, J. A. Currivan, M. D. Hoogerland** "Quantum resonant effects in the delta-kicked rotor revisited." Eur. Phys. J. D (2012). arXiv:1202.3166. **verified 2026-10-29**
  - Cited in: 16. Note: doi:10.1140/epjd/e2012-30171-8; volume not checked.
- **J. A. Currivan, A. Ullah, M. D. Hoogerland** "The initial momentum dependence of the quantum resonance in the delta-kicked rotor." EPL, 85, 30005 (2009). arXiv:0806.3107. **verified 2026-10-29**
  - Cited in: 16. Note: doi:10.1209/0295-5075/85/30005.
- **K. Hornberger, J. E. Sipe, M. Arndt** "Theory of decoherence in a matter wave Talbot-Lau interferometer." Phys. Rev. A, 70, 053608 (2004). arXiv:quant-ph/0407245. **verified 2026-10-29**
  - Cited in: 16, README.
- **K. Hornberger, S. Gerlich, P. Haslinger, S. Nimmrichter, M. Arndt** "Colloquium: Quantum interference of clusters and molecules." Rev. Mod. Phys., 84, 157 (2012). arXiv:1109.5937. **verified 2026-10-29**
  - Cited in: 16.
- **D. Cohen** "Quantum chaos, dynamical correlations, and the effect of noise on localization." Phys. Rev. A, 44, 2292–2313 (1991). **verified 2026-10-29**
  - Cited in: 16. Note: checked on Crossref, doi:10.1103/PhysRevA.44.2292.
- **D. Hangleiter, I. Roth, D. Nagaj, J. Eisert** "Easing the Monte Carlo sign problem." Sci. Adv., 6, eabb8341 (2020). arXiv:1906.02309. **verified 2026-10-29**
  - Cited in: 12, README.
- **A. Babakhani, A. Karakashian** "Stoquasticity is not enough: towards a sharper diagnostic for Quantum Monte Carlo simulability." (2025). arXiv:2508.14382. **verified 2026-10-29**
  - Cited in: 12, README. Note: preprint.
- **H. Singh, S. Chandrasekharan** "Few-body physics on a space-time lattice in the worldline approach." Phys. Rev. D, 99, 074511 (2019). arXiv:1812.05080. **verified 2026-10-29**
  - Cited in: 12, README.

## Added 2026-11-05: sources from the third audit

Bibliographic details of these entries were checked on 2026-11-05 against the arXiv abstract page and Crossref (**verified 2026-11-05**); passages were not checked. The Smirne–Stabile–Vacchini, Breuer–Laine–Piilo, Glick–Adami, Facchi–Nakazato–Pascazio, Benatti–Chruściński–Nichele, Vacchini et al., Pashayan et al., Aaronson–Arkhipov, Arkhipov–Kuperberg and Pimenta entries already existed above or in the 2026-10-29 section and were updated in place (Cited-in lists and notes).

- **J. A. Barandes** "A Deflationary Account of Quantum Theory and its Implications for the Complex Numbers." (2026). arXiv:2602.01043. **verified 2026-11-05**
  - Cited in: 13, README. Note: preprint; no journal reference on the arXiv page.
- **I. Hen** "Determining quantum Monte Carlo simulability with geometric phases." Phys. Rev. Research, 3, 023080 (2021). arXiv:2012.02022. doi:10.1103/PhysRevResearch.3.023080. **verified 2026-11-05**
  - Cited in: 12, README. Note: the arXiv title reads "Determining QMC simulability with geometric phases".
- **S. Bhattacharya, B. Bhattacharya, A. S. Majumdar** "Convex resource theory of non-Markovianity." J. Phys. A: Math. Theor., 54, 035302 (2021). arXiv:1803.06881. doi:10.1088/1751-8121/abd191. **verified 2026-11-05**
  - Cited in: 13. Note: Crossref gives the issue year as 2020 (online); the volume is 54 (2021).
- **G. D. Berk, A. J. P. Garner, B. Yadin, K. Modi, F. A. Pollock** "Resource theories of multi-time processes: A window into quantum non-Markovianity." Quantum, 5, 435 (2021). arXiv:1907.07003. doi:10.22331/q-2021-04-20-435. **verified 2026-11-05**
  - Cited in: 13.
- **A. Miyake, M. Wadati** "Geometric strategy for the optimal quantum search." Phys. Rev. A, 64, 042317 (2001). arXiv:quant-ph/0109109. doi:10.1103/PhysRevA.64.042317. **verified 2026-11-05**
  - Cited in: 09, README.

## To verify before external sharing

Still unconfirmed after the 2026-10-29 check:

- [ ] Long et al.: confirm which Long paper notebook 09 and the grover-as-isp spike mean (best match: Long, Li, Zhang, Tu, PRA 61, 042305 (2000), which is about gate imperfection)
- [ ] Azuma 2002: confirm PRA 65, 042311 (erratum 66, 019903(E)) is the intended paper
- [ ] Ballentine: which edition the local PDF and the notebooks' section numbers follow (World Scientific 1998, or 2nd ed. 2014, whose publisher is also unconfirmed)
- [ ] Khalfin, Mandelstam and Tamm (original journal), Lukacs, Thompson: confirmed only from standard or secondary citations
- [ ] Partly from standard citation: Srinivasan, Gordon, Boots (AISTATS venue); Boyer, Brassard, Hoyer, Tapp (arXiv number); Gerlich et al. (authors six to eleven)
- [ ] Barandes, Hasan, Kagan, arXiv:2512.18105: which journal the DOI 10.1103/xfpf-734d belongs to
- [x] Aaronson and Arkhipov: that the bosonic birthday paradox is in §13 of arXiv:1011.3245 (confirmed 2026-11-05)
- [ ] Passage-level checks: no cited passage in any entry tagged verified 2026-10-29 has been checked against the source
