# ISP Lab

A computational laboratory for exploring Jacob Barandes' Indivisible Stochastic Processes (ISP) framework.

## Background

Physicist Jacob A. Barandes (Harvard) has developed the "stochastic-quantum correspondence," a research program arguing that quantum mechanics is not a fundamentally different kind of theory from classical probability, but a special case of ordinary stochastic processes unfolding in configuration space. His central move is to identify a class of stochastic processes he calls "indivisible" — ones that fail the standard divisibility condition every classical Markov chain satisfies, meaning they cannot be factored through an arbitrary intermediate time without introducing negative entries in the intermediate matrix. Barandes proves that this class of indivisible stochastic processes corresponds exactly, one-to-one, with unitarily evolving quantum systems in a Hilbert space. Formalized as a theorem in his 2026 paper "The Stochastic-Quantum Theorem," this correspondence demotes the wave function from a fundamental ontological object to a convenient mathematical bookkeeping device, and offers a first-principles explanation for why quantum theory uses complex numbers, Hilbert spaces, linear-unitary evolution, and the Born rule. It also yields deflationary, non-mysterious accounts of interference, entanglement, decoherence, noncommuting observables, and wave-function collapse, all traced back to the single property of indivisibility. Because the framework builds quantum behavior out of ordinary probability theory rather than positing it as axiomatic, it suggests new applications too, including simulating arbitrary indivisible stochastic processes on quantum computers and using Hilbert-space methods to model highly generic non-Markovian dynamics elsewhere in the sciences.

The five notebooks in this repository make that abstract claim tangible and checkable, building it up computationally with nothing more than finite-dimensional matrices. Notebook 01 establishes the baseline: stochastic processes as probability vectors evolved by transition matrices, with classical continuous-time Markov chains as the simplest special case. Notebook 02 implements the divisibility condition as an explicit matrix test and confirms, by direct calculation, that Markov chains always pass it — grounding "classical" in a checkable numerical property rather than an intuition. Notebook 03 is the pivot: it constructs a genuinely quantum process (a qubit evolving under a simple Hamiltonian), shows computationally that it fails the same divisibility test, and introduces an "indivisibility signature" that quantifies how far a process sits from classical. Notebook 04 closes the loop between the two formalisms by mapping a qubit density matrix onto a stochastic state vector, verifying that its evolution is indivisible, and deriving the Born rule as a computed consequence rather than an assumed postulate. Notebook 05 delivers the payoff: a double-slit model built as a genuine unistochastic process shows numerically that interference appears if and only if the underlying process is indivisible — the fringe pattern turns out to be, entry for entry, the source column of the matrix Γ(t₂,t₀) − Γ(t₂,t₁)Γ(t₁,t₀) that measures the failure of divisibility — turning Barandes' central theoretical claim into a hands-on demonstration a reader can rerun, perturb, and verify. Together, the notebooks turn a dense theorem into a self-contained, executable proof sketch — useful both as a study aid for the papers and as a sandbox for probing where the classical/quantum boundary actually lives.

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

`notebooks/` holds each notebook twice, and the split is deliberate:

| | |
|---|---|
| `NN_name.ipynb` | **The clean original.** Succinct, minimal, the executable proof sketch. Kept deliberately spare — this is the version to read, run, or hand to someone else. **Do not add commentary here.** |
| `NN_name_annotated.ipynb` | **The study copy.** Same content plus long-form explanation, derivations, and notes on where the code's claims outrun what it demonstrates. All exploratory edits go here. |

Annotated sections are marked `📖 In depth` (concepts), `🔍 Reading the code`
(implementation detail and limitations), `🔭 Looking ahead` (forward references), and
`🔧 Corrected` (where the annotated copy diverges from the original because the original
is wrong — the header of each annotated notebook lists these explicitly).

The originals are the reference; the annotated copies are the working surface. Keeping
them apart means the clean version stays readable and the study version stays free to
sprawl.

## Two divisibility tests

`isp/divisibility.py` offers the condition two ways, and the difference matters.

| | |
|---|---|
| `check_divisibility()` | Solves Γ(t₂,t₁) = Γ(t₂,t₀)·inv(Γ(t₁,t₀)) and looks for negative entries. Direct and fast, but needs Γ(t₁,t₀) to be invertible, and reports `singular_matrix` when it is not. Used by notebooks 02 and 03. |
| `check_divisibility_lp()` | Asks the question Barandes actually asks — does *any* valid stochastic Γ(t₂,t₁) exist — as a linear program. No inverse, so singularity is irrelevant. `divisibility_defect()` is its continuous companion, zero exactly when divisible. Used by notebook 05. |

The second test exists because the first one cannot be applied to a balanced double slit
at all: if a unitary sends the source to (|A⟩+|B⟩)/√2, unitarity forces rows A and B of
|U|² to be identical, so Γ(t₁,t₀) is rank-deficient for *every* such model. That is a
theorem, not a tolerance problem — notebook 05's annotated copy proves it. Reach for
`check_divisibility()` when the first transition matrix is invertible and
`check_divisibility_lp()` when it is not.

Processes whose transition matrices do not compose into increments cannot be expressed as
a `StochasticProcess` (which stores increments and chains them). Use `PairwiseProcess`,
which holds the family {Γ(tⱼ,tᵢ)} directly — the form Barandes defines a process in.
`isp/double_slit.py` builds the notebook 05 model that way.

## License

MIT
