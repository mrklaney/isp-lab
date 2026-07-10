# ISP Lab

A computational laboratory for exploring Jacob Barandes' Indivisible Stochastic Processes (ISP) framework.

## Background

Physicist Jacob A. Barandes (Harvard) has developed the "stochastic-quantum correspondence," a research program arguing that quantum mechanics is not a fundamentally different kind of theory from classical probability, but a special case of ordinary stochastic processes unfolding in configuration space. His central move is to identify a class of stochastic processes he calls "indivisible" — ones that fail the standard divisibility condition every classical Markov chain satisfies, meaning they cannot be factored through an arbitrary intermediate time without introducing negative entries in the intermediate matrix. Barandes proves that this class of indivisible stochastic processes corresponds exactly, one-to-one, with unitarily evolving quantum systems in a Hilbert space. Formalized as a theorem in his 2026 paper "The Stochastic-Quantum Theorem," this correspondence demotes the wave function from a fundamental ontological object to a convenient mathematical bookkeeping device, and offers a first-principles explanation for why quantum theory uses complex numbers, Hilbert spaces, linear-unitary evolution, and the Born rule. It also yields deflationary, non-mysterious accounts of interference, entanglement, decoherence, noncommuting observables, and wave-function collapse, all traced back to the single property of indivisibility. Because the framework builds quantum behavior out of ordinary probability theory rather than positing it as axiomatic, it suggests new applications too, including simulating arbitrary indivisible stochastic processes on quantum computers and using Hilbert-space methods to model highly generic non-Markovian dynamics elsewhere in the sciences.

The five notebooks in this repository make that abstract claim tangible and checkable, building it up computationally with nothing more than finite-dimensional matrices. Notebook 01 establishes the baseline: stochastic processes as probability vectors evolved by transition matrices, with classical continuous-time Markov chains as the simplest special case. Notebook 02 implements the divisibility condition as an explicit matrix test and confirms, by direct calculation, that Markov chains always pass it — grounding "classical" in a checkable numerical property rather than an intuition. Notebook 03 is the pivot: it constructs a genuinely quantum process (a qubit evolving under a simple Hamiltonian), shows computationally that it fails the same divisibility test, and introduces an "indivisibility signature" that quantifies how far a process sits from classical. Notebook 04 closes the loop between the two formalisms by mapping a qubit density matrix onto a stochastic state vector, verifying that its evolution is indivisible, and deriving the Born rule as a computed consequence rather than an assumed postulate. Notebook 05 delivers the payoff: a minimal double-slit model shows numerically that interference appears if and only if the underlying process is indivisible, turning Barandes' central theoretical claim into a hands-on demonstration a reader can rerun, perturb, and verify. Together, the notebooks turn a dense theorem into a self-contained, executable proof sketch — useful both as a study aid for the papers and as a sandbox for probing where the classical/quantum boundary actually lives.

## Setup

```bash
uv venv
uv pip install -r requirements.txt -e .
```

## Run tests

```bash
pytest tests/ -v
```

## Run notebooks

```bash
jupyter notebook notebooks/
```

## License

MIT
