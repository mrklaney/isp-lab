import numpy as np
import pytest
from isp.quantum import (
    density_matrix_to_stochastic_state,
    unitary_to_transition_matrix,
    make_qubit_sigmax_process,
    born_rule,
)


def test_density_matrix_to_stochastic_state_extracts_diagonal():
    rho = np.array([[0.7, 0.1 + 0.2j], [0.1 - 0.2j, 0.3]])
    p = density_matrix_to_stochastic_state(rho)
    np.testing.assert_allclose(p, [0.7, 0.3])


def test_density_matrix_to_stochastic_state_sums_to_one():
    rho = np.array([[0.6, 0.2], [0.2, 0.4]])
    p = density_matrix_to_stochastic_state(rho)
    assert abs(p.sum() - 1.0) < 1e-10


def test_unitary_to_transition_matrix_non_negative():
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # Hadamard
    T = unitary_to_transition_matrix(H)
    assert np.all(T >= 0)


def test_unitary_to_transition_matrix_columns_sum_to_one():
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    T = unitary_to_transition_matrix(H)
    np.testing.assert_allclose(T.sum(axis=0), [1.0, 1.0], atol=1e-10)


def test_make_qubit_sigmax_process_returns_stochastic_process():
    from isp.stochastic import StochasticProcess
    proc = make_qubit_sigmax_process(omega=1.0, times=[0.0, 1.0, 2.0])
    assert isinstance(proc, StochasticProcess)
    assert len(proc.transitions) == 2


def test_make_qubit_sigmax_process_identity_at_zero_dt():
    proc = make_qubit_sigmax_process(omega=1.0, times=[0.0, 0.0001])
    T = proc.transitions[0]
    np.testing.assert_allclose(T, np.eye(2), atol=1e-6)


def test_born_rule_matches_diagonal():
    rho = np.array([[0.7, 0.0], [0.0, 0.3]])
    M0 = np.array([[1, 0], [0, 0]])  # project onto |0⟩
    p0 = born_rule(rho, M0)
    assert abs(p0 - 0.7) < 1e-10


def test_born_rule_sums_to_one_for_complete_measurement():
    rho = np.array([[0.7, 0.0], [0.0, 0.3]])
    M0 = np.array([[1, 0], [0, 0]])
    M1 = np.array([[0, 0], [0, 1]])
    assert abs(born_rule(rho, M0) + born_rule(rho, M1) - 1.0) < 1e-10
