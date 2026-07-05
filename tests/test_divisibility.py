import numpy as np
import pytest
from isp.stochastic import StochasticProcess, make_markov_chain
from isp.divisibility import check_divisibility, indivisibility_signature


def test_markov_chain_is_divisible():
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    times = [0.0, 0.5, 1.0, 1.5]
    proc = make_markov_chain(2, L, times)
    result = check_divisibility(proc)
    assert result["divisible"] is True
    assert result["failure_mode"] is None


def test_indivisible_process_detected_negative_entries():
    # Qubit under sigma_x rotation: indivisible at times [0, 3pi/4, 5pi/6] with omega=1
    # T_32_candidate has off-diagonal ≈ -0.111 (negative entries failure)
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    result = check_divisibility(proc)
    assert result["divisible"] is False
    assert result["failure_mode"] == "negative_entries"


def test_indivisibility_signature_zero_for_markov():
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    times = [0.0, 0.5, 1.0]
    proc = make_markov_chain(2, L, times)
    sig = indivisibility_signature(proc)
    assert sig < 1e-10


def test_indivisibility_signature_positive_for_quantum():
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    sig = indivisibility_signature(proc)
    assert sig > 0.0


def test_check_divisibility_returns_at_times_on_failure():
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    result = check_divisibility(proc)
    assert result["at_times"] is not None
    assert len(result["at_times"]) == 3
