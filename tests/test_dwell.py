import numpy as np
from isp.dwell import ChiralChain, TunnelChain, decompose, pointer_shift


def test_identity_on_random_closed_model():
    rng = np.random.default_rng(1)
    A = rng.normal(size=(12, 12)) + 1j * rng.normal(size=(12, 12))

    class M:
        pass
    m = M(); m.w, m.V = np.linalg.eigh(A + A.conj().T)
    m.evolve = lambda psi, t: m.V @ (np.exp(-1j * m.w * t) * (m.V.conj().T @ psi))
    psi0 = rng.normal(size=12) + 1j * rng.normal(size=12); psi0 /= np.linalg.norm(psi0)
    reg = np.zeros(12, bool); reg[:4] = True
    fin = np.zeros(12, bool); fin[6:] = True
    d = decompose(m, psi0, reg, fin, 3.0, nt=50)
    assert d["identity_err"] < 1e-13
    assert np.all(d["seq"] >= 0)


def test_chiral_chain_tau_equals_group_delay_and_goes_negative():
    ch = ChiralChain(5)
    assert abs(ch.OD - 2.23) < 0.01
    narrow = ch.run(36 / 26, nt=200)
    broad = ch.run(10 / 26, nt=200)
    assert narrow["identity_err"] < 1e-12
    assert narrow["tau"] < 0 < broad["tau"]
    assert abs(narrow["tau"] - narrow["tau_g"]) < 0.06
    assert abs(broad["tau"] - broad["tau_g"]) < 0.02


def test_pointer_weak_limit_and_strong_limit():
    ch = ChiralChain(5, Wf=20, Wl=10)
    weak = pointer_shift(ch, 36 / 26, 1e3)
    assert abs(weak - ch.group_delay_pulse(36 / 26)) < 1e-3
    assert weak < 0 < pointer_shift(ch, 36 / 26, 0.3)
    assert abs(pointer_shift(ch, 36 / 26, 0.01)) < 0.01


def test_tunnelling_sum_rule_and_negative_time_behind_barrier():
    tc = TunnelChain(V0=0.8, w_bar=2)
    r = tc.run("behind", k0=0.6)
    tot = sum(v["P_f"] * v["tau"] for v in r.values())
    assert abs(tot - r["reflected"]["dwell"]) < 1e-6
    assert r["reflected"]["tau"] < -0.05
    assert max(v["identity_err"] for v in r.values()) < 1e-12
