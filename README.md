# ISP Lab

A computational laboratory for exploring Jacob Barandes' Indivisible Stochastic Processes (ISP) framework.

**Read the notebooks in your browser, no install needed:** https://mrklaney.github.io/isp-lab/

## Sources

"Paper 1, 2, 3" in the notebooks are Jacob A. Barandes's papers:

- Paper 1: "The Stochastic-Quantum Correspondence", arXiv:2302.10778 (*Philosophy of Physics* 3(1), 8, 2025).
- Paper 2: "The Stochastic-Quantum Theorem", arXiv:2309.03085.
- Paper 3: "Quantum Systems as Indivisible Stochastic Processes", arXiv:2507.21192 (*Stud. Hist. Phil. Sci.* 119, 102213, 2026).

Every other work is cited in the text and listed in `REFERENCES.md` (with `references.bib`). Each entry there carries a verification status. `REFERENCES.md` was compiled for a larger set of notebooks, so it also lists works cited only in notebooks not published here.

## Background

Physicist Jacob A. Barandes (Harvard) has developed the "stochastic-quantum correspondence," a research program arguing that quantum mechanics is not a fundamentally different kind of theory from classical probability, but a special case of ordinary stochastic processes unfolding in configuration space. His central move is to identify a class of stochastic processes he calls "indivisible": processes that are not *required* to satisfy the divisibility condition every classical Markov chain satisfies (Markov chains are included as a special case). A process that does fail it cannot be factored through an arbitrary intermediate time without introducing negative entries in the intermediate matrix. He proves that every such process with finitely many configurations is a subsystem of a unitarily evolving quantum system, and argues that the converse also holds: every quantum system, measuring devices included, can be modelled as such a process (Paper 1). The association is not unique (in his words, a process is "associated (non-uniquely)" with a quantum system, arXiv:2608.04354 §4); indivisibility is the generic case. Approximate division events, times at which a process does divide, arise from interaction with an environment (Paper 1, §3.7). Formalized as a theorem in "The Stochastic-Quantum Theorem" (Paper 2; arXiv 2023, revised 2026), this correspondence, he argues, demotes the wave function from a fundamental ontological object to a convenient mathematical bookkeeping device, and offers a first-principles explanation for why quantum theory uses complex numbers, Hilbert spaces, linear-unitary evolution, and the Born rule. He argues that it yields deflationary accounts of interference, decoherence, entanglement, noncommuting observables and wave-function collapse.

## The notebooks

The notebooks make that claim tangible and checkable with nothing more than finite-dimensional matrices. They are a computational companion to Barandes's papers: they illustrate and test his results, and they credit his work and others' wherever an idea comes from them. They do not claim new physics.

Notebook 01 establishes the baseline: stochastic processes as probability vectors evolved by transition matrices, with classical continuous-time Markov chains as the simplest special case. Notebook 02 implements the divisibility condition as an explicit matrix test and confirms, by direct calculation, that Markov chains always pass it; divisibility constrains only first-order transition matrices, so it is not the same as having no memory. Notebook 03 is the pivot: it constructs a genuinely quantum process (a qubit evolving under a simple Hamiltonian), shows that it fails the same test except at the times where its transition matrix is a permutation, and introduces an "indivisibility signature" that detects failure at the sampled times (its size reflects how close the inverted matrix is to singular, not how quantum the process is). Barandes's Gaussian example (Paper 1, eq. 7) shows a process whose two starting points become indistinguishable and then recover their distinguishability, which no divisible process can do. Notebook 04 maps a qubit density matrix onto a stochastic state vector, verifies that its evolution is indivisible, and checks that in the configuration basis the Born rule returns the stochastic state by construction (Paper 1, eq. 16); Barandes's derivation for other observables is not tested. Notebook 05 builds a double slit as a unistochastic process and shows that the fringe pattern is, entry for entry, the source column of Γ(t₂,t₀) − Γ(t₂,t₁)Γ(t₁,t₀), the failure of the process's own two-stage composition. For the lab's completions of the slit unitary, fringes and indivisibility appear together; a symmetric completion shows that interference does not by itself make a process indivisible in Barandes's existential sense. Prior work: the double-slit identity is Barandes's Paper 1, eq. 43 (see also LeBlond, arXiv:2511.02863); the gap rule in notebook 03 is known (Buscemi–Datta 2016; Pimenta 2025); notebooks 01, 02 and 04 restate standard material and Barandes's definitions.

Notebook 06 asks what makes a process divide physically. A qubit is recorded by a fresh environment qubit every δt, and a full system-plus-environment simulation shows each record time becomes an exact division event. This reproduces Barandes's Paper 1, §3.7. Varying ωδt then moves the same qubit from indivisible oscillation, through divisible relaxation (a Markov chain at the record times), toward Zeno freezing. The process is divisible over every pair of times exactly when ωδt ≤ π/2. Imperfect records no longer guarantee division events: record times fail to divide once the records are blurry enough for the spacing, though short spacings tolerate fairly blurry records. Prior work: the construction is Paper 1's (§3.7, which already names the time scale δt; what is added here is the system's own time scale 1/ω); whether a time is a division event is a property of Γ (Paper 2, eq. 35), and approximate division events at a stated precision are in Barandes, Hasan and Kagan (arXiv:2512.18105, §3.1). The forgetting rate is the population-relaxation form of the repeated-measurement Zeno rate (Misra–Sudarshan; Itano et al.), the revival measure R is Smirne, Stabile and Vacchini's classical memory witness (2013), and the π/2 threshold follows from Buscemi–Datta (2016) and Pimenta (arXiv:2505.08785).

These versions (November 2026) were checked line by line: every printed number re-run, every attribution to Barandes checked against his papers, and every "prior work" note searched. "Not found in our searches" means exactly that, not a claim of novelty.

## Setup

There isn't one. There is no virtualenv to create and nothing to install. Both commands
below use `uvx`, which builds a throwaway environment from `requirements.txt` on each
invocation and discards it afterward. The only prerequisite is
[uv](https://docs.astral.sh/uv/).

> The notebooks import the local package directly (`from isp.stochastic import ...`).
> Each one bootstraps its own path in the imports cell
> (`sys.path.insert(0, os.path.abspath('..'))`), so `isp` resolves whether you launch
> from the repo root or from inside `notebooks/`. Keep that line if you add a notebook.

## Run notebooks

```bash
cd isp-lab
uvx --with-requirements requirements.txt --from jupyter-core --with jupyterlab jupyter lab
```

## Run tests

```bash
uvx --with-requirements requirements.txt --from pytest pytest tests/ -v
```

## Two tracks of notebooks

`notebooks/` holds each notebook twice:

- `NN_name.ipynb` is **the clean original**: succinct, minimal, the executable proof sketch. This is the version to read, run, or hand to someone else.
- `NN_name_annotated.ipynb` is **the study copy**: the same content plus long-form explanation, derivations, glossaries and quoted passages from the papers. Some study notes mention files from the author's local reading folder; those files are not part of this repository.

Rendered pages for both tracks are in `docs/` and served at https://mrklaney.github.io/isp-lab/.

## Two divisibility tests

`isp/divisibility.py` offers the condition two ways, and the difference matters.

- `check_divisibility()` solves Γ(t₂,t₁) = Γ(t₂,t₀)·inv(Γ(t₁,t₀)) and looks for negative entries. It is direct and fast, but needs Γ(t₁,t₀) to be invertible, and returns "undecided" (`singular_matrix`) when it is not. Used by notebooks 02 and 03.
- `check_divisibility_lp()` asks the question Barandes actually asks, whether *any* valid stochastic Γ(t₂,t₁) exists, as a linear program. No inverse, so singularity is irrelevant. `divisibility_defect()` is its continuous companion, zero exactly when divisible. Used by notebook 05.

The second test exists because the first one cannot be applied to a balanced double slit
at all: if a unitary sends the source to (|A⟩+|B⟩)/√2, unitarity forces rows A and B of
|U|² to be identical, so Γ(t₁,t₀) is rank-deficient for *every* such model. Notebook 05's
annotated copy proves it. Reach for `check_divisibility()` when the first transition matrix
is invertible and `check_divisibility_lp()` when it is not.

Processes whose transition matrices do not compose into increments cannot be expressed as
a `StochasticProcess` (which stores increments and chains them). Use `PairwiseProcess`,
which holds the family {Γ(tⱼ,tᵢ)} directly. That is more general than Barandes's form,
which gives Γ(t←t₀) only from division events (Paper 3, §2.2). `isp/double_slit.py`
builds the notebook 05 model that way.

## License

MIT
