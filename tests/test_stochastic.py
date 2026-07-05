import numpy as np
import pytest
from isp.stochastic import StochasticProcess, make_markov_chain


def test_evolve_with_identity_transition():
    T = np.eye(2)
    proc = StochasticProcess(states=["0", "1"], transitions=[T], times=[0.0, 1.0])
    p0 = np.array([0.7, 0.3])
    dists = proc.evolve(p0)
    assert len(dists) == 2
    np.testing.assert_allclose(dists[0], p0)
    np.testing.assert_allclose(dists[1], p0)


def test_evolve_preserves_normalization():
    T = np.array([[0.8, 0.3], [0.2, 0.7]])
    proc = StochasticProcess(states=["0", "1"], transitions=[T], times=[0.0, 1.0])
    p0 = np.array([1.0, 0.0])
    dists = proc.evolve(p0)
    assert abs(dists[1].sum() - 1.0) < 1e-10


def test_transition_from_to_single_step():
    T = np.array([[0.8, 0.3], [0.2, 0.7]])
    proc = StochasticProcess(states=["0", "1"], transitions=[T], times=[0.0, 1.0])
    np.testing.assert_allclose(proc.transition_from_to(0, 1), T)


def test_transition_from_to_composite():
    T1 = np.array([[0.8, 0.3], [0.2, 0.7]])
    T2 = np.array([[0.6, 0.4], [0.4, 0.6]])
    proc = StochasticProcess(states=["0", "1"], transitions=[T1, T2], times=[0.0, 1.0, 2.0])
    # T(0->2) = T2 @ T1
    np.testing.assert_allclose(proc.transition_from_to(0, 2), T2 @ T1)


def test_transition_from_to_identity_at_same_index():
    T = np.array([[0.8, 0.3], [0.2, 0.7]])
    proc = StochasticProcess(states=["0", "1"], transitions=[T], times=[0.0, 1.0])
    np.testing.assert_allclose(proc.transition_from_to(0, 0), np.eye(2))


def test_make_markov_chain_columns_sum_to_one():
    # Generator: columns sum to 0 (not rows)
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    times = [0.0, 0.5, 1.0]
    proc = make_markov_chain(2, L, times)
    assert len(proc.transitions) == 2
    for T in proc.transitions:
        np.testing.assert_allclose(T.sum(axis=0), [1.0, 1.0], atol=1e-10)


def test_make_markov_chain_non_negative_entries():
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    times = [0.0, 0.5, 1.0]
    proc = make_markov_chain(2, L, times)
    for T in proc.transitions:
        assert np.all(T >= -1e-10)
