# eraser.py
#
# The delayed-choice quantum eraser of Kim, Yu, Kulik, Shih and Scully
# (arXiv:quant-ph/9903047; PRL 84, 1 (2000)) as a discrete model whose
# configurations are photon positions and detector clicks.
#
# Two photons. The pair is born in region A or region B of the crystal (the
# "slits"). Configurations:
#
#     t0  source
#     t1  path:   signal photon in A or B, idler photon in A or B (always equal)
#     t2  signal photon lands on D0 at pixel x          (short arm, early)
#     t3  idler photon clicks one of D1, D2, D3, D4     (long arm, ~8 ns later)
#
# Signal arm: far-field propagation U2 from the two regions to n_modes pixels,
# the same unitary DFT as isp.double_slit (notebook 05).
#
# Idler arm: a 4x2 isometry V from the idler path {A, B} to the detectors
# {D1, D2, D3, D4}. With probability t = 1 - r the idler is transmitted at
# BS_A / BS_B to the which-path detector D3 (from A) or D4 (from B). With
# probability r it is reflected to the final beamsplitter BS, whose outputs D1
# and D2 measure the path in a rotated basis:
#
#     V[D1] = sqrt(r) * ( cos th,  sin th)
#     V[D2] = sqrt(r) * (-sin th,  cos th)
#     V[D3] = sqrt(t) * ( 1,       0     )
#     V[D4] = sqrt(t) * ( 0,       1     )
#
# th = pi/4 is Kim et al.'s 50/50 eraser (D1 and D2 fringes shifted by pi);
# th = 0 turns BS into a which-path measurement too. The columns of V are
# orthonormal for every (r, th), so the joint Born probabilities normalise
# with no hand-applied rescaling.
#
# Joint amplitude for "signal at x, idler at d":
#
#     psi[x, d] = (1/sqrt 2) * sum_s U2[x, slit_s] * V[d, s]
#
# Everything the experiment reports is a sub-table of P[x, d] = |psi[x, d]|^2:
# R0j(x) is proportional to column j. The time order of the two detections
# never enters psi, which is the model-level statement that the "delay" does
# no work.

from typing import Dict
import numpy as np

from .double_slit import far_field_propagator

DETECTORS = ("D1", "D2", "D3", "D4")
PATHS = ("A", "B")


def idler_isometry(r: float = 0.5, theta: float = np.pi / 4) -> np.ndarray:
    """4x2 isometry from idler path {A, B} to detectors {D1, D2, D3, D4}."""
    if not 0.0 <= r <= 1.0:
        raise ValueError(f"r must be in [0, 1], got {r}")
    t = 1.0 - r
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [np.sqrt(r) * c, np.sqrt(r) * s],
        [-np.sqrt(r) * s, np.sqrt(r) * c],
        [np.sqrt(t), 0.0],
        [0.0, np.sqrt(t)],
    ], dtype=complex)


def kim_model(n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
              r: float = 0.5, theta: float = np.pi / 4) -> Dict[str, np.ndarray]:
    """
    Build the joint amplitudes and every probability table nb20 uses.

    Returns a dict with:
        psi           (n_modes, 4)  joint amplitude psi[x, d]
        P_joint       (n_modes, 4)  P(x, d)
        P_screen      (n_modes,)    P(x), the D0 singles (no sorting)
        P_detector    (4,)          P(d)
        P_x_given_d   (n_modes, 4)  P(x | d), the sorted D0 patterns (R0j, normalised)
        P_x_given_s   (n_modes, 2)  P(x | path s) = |U2[x, slit_s]|^2
        P_s_given_d   (2, 4)        P(path s | d)
        V             (4, 2)        the idler isometry
    """
    U2 = far_field_propagator(n_modes)
    signal = U2[:, [slit_a, slit_b]]              # (n, 2): amplitude x <- s
    V = idler_isometry(r, theta)                  # (4, 2): amplitude d <- s
    psi = signal @ V.T / np.sqrt(2.0)             # sum over s

    P_joint = np.abs(psi) ** 2
    P_detector = P_joint.sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        P_x_given_d = np.where(P_detector > 0, P_joint / P_detector, 0.0)

    P_x_given_s = np.abs(signal) ** 2
    P_s_d = 0.5 * np.abs(V.T) ** 2                # (2, 4): P(s, d); the signal arm sums to 1 per s
    with np.errstate(invalid="ignore", divide="ignore"):
        P_s_given_d = np.where(P_detector > 0, P_s_d / P_detector, 0.0)

    return {
        "psi": psi,
        "P_joint": P_joint,
        "P_screen": P_joint.sum(axis=1),
        "P_detector": P_detector,
        "P_x_given_d": P_x_given_d,
        "P_x_given_s": P_x_given_s,
        "P_s_given_d": P_s_given_d,
        "V": V,
    }


def conditional_defect(model: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Divisibility defect of each sorted sub-ensemble, through the path at t1:

        Delta[x, d] = P(x | d) - sum_s P(x | s) P(s | d)

    Zero for a detector d exactly when the d-sorted D0 pattern is what you get
    by first fixing the path and then propagating it: the sub-ensemble composes
    classically through t1. Nonzero means the d-sorted pattern is not a mixture
    of the two single-path patterns. This is the eq. 43-style defect of
    notebook 05, taken on one sorted sub-ensemble at a time. Returns (n_modes, 4).
    """
    mixed = model["P_x_given_s"] @ model["P_s_given_d"]
    return model["P_x_given_d"] - mixed


def path_predictability(model: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Pred_d = |P(A | d) - P(B | d)|: how well detector d tells the path. Shape (4,).

    This is the predictability P_k of the d-sorted subensemble in Englert &
    Bergou, Opt. Commun. 179, 337 (2000), defined in their Fig. 1 caption (their
    eq. 25, K, is its p_k-weighted sum). It is not Englert's distinguishability D
    (the maximum of K over sortings, their eq. 26).
    """
    Psd = model["P_s_given_d"]
    return np.abs(Psd[0] - Psd[1])


def sorted_visibility(model: Dict[str, np.ndarray]) -> np.ndarray:
    """
    Fringe visibility of each sorted pattern P(x | d), read from the amplitudes
    rather than from max/min of a discretised curve:

        V_d = 2 |V[d, A] V[d, B]| / (|V[d, A]|^2 + |V[d, B]|^2)

    For a pure two-path state this is the exact visibility of the d-sorted
    fringe. Shape (4,); 0 where P(d) = 0.
    """
    V = model["V"]
    num = 2.0 * np.abs(V[:, 0] * V[:, 1])
    den = np.abs(V[:, 0]) ** 2 + np.abs(V[:, 1]) ** 2
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, num / den, 0.0)


def path_record_check(n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
                      r: float = 0.5, theta: float = np.pi / 4) -> Dict[str, float]:
    """
    Is t1 (the path time) a division event? Rule T3 of
    notes/division-event-criterion-spike-2026-10-28.md, on the Kim model.

    Class the joint configuration at t1 by the signal path s (the idler path
    always equals it). For a later joint configuration z, write the history
    amplitude through class s as b[z, s]. Then

        actual    P(z) = |b[z, A] + b[z, B]|^2
        divided   P(z) = |b[z, A]|^2 + |b[z, B]|^2      (restart from the path at t1)
        defect    = sum_z |actual - divided|            (L1)
        bound     = 2 sum_z |b[z, A]| |b[z, B]|         (persistent-record bound;
                                                        each class has one member here)

    at two later times:
        t2: signal at D0 pixel x, idler still in its arm (z = (x, idler path))
        t3: signal at x, idler at D1..D4             (z = (x, d))

    T3 says t1 is a division event to accuracy eps iff the bound stays below eps
    at every later time. Caveat from that spike's round-3 audit: the bound needs
    the joint transitions re-rooted at t1, which Gamma(. <- 0) alone does not
    supply; this model supplies them.
    """
    U2 = far_field_propagator(n_modes)
    signal = U2[:, [slit_a, slit_b]]                       # (n, 2)
    out = {}
    for label, arm in (("t2", np.eye(2, dtype=complex)),
                       ("t3", idler_isometry(r, theta))):
        # b[x, k, s] = (1/sqrt2) signal[x, s] * arm[k, s]
        b = signal[:, None, :] * arm[None, :, :] / np.sqrt(2.0)
        actual = np.abs(b.sum(axis=2)) ** 2
        divided = (np.abs(b) ** 2).sum(axis=2)
        out[f"defect_{label}"] = float(np.abs(actual - divided).sum())
        out[f"bound_{label}"] = float(2.0 * (np.abs(b[..., 0]) * np.abs(b[..., 1])).sum())
        # the signal's own marginal (sum over the idler) at that time
        out[f"signal_marginal_defect_{label}"] = float(
            np.abs(actual.sum(axis=1) - divided.sum(axis=1)).sum())
    out["bound_sup"] = max(out["bound_t2"], out["bound_t3"])
    return out


def marker_model(pA: float, mA: np.ndarray, mB: np.ndarray,
                 eA: np.ndarray, eB: np.ndarray, W: np.ndarray,
                 n_modes: int = 24, slit_a: int = 10, slit_b: int = 13) -> Dict[str, np.ndarray]:
    """
    Imperfect which-path records (nb20 §5; after notes/eraser-impure-record-spike-2026-11-18.py).

    Path s (prior pA, 1 - pA) leaves marker |m_s> in the idler and |e_s> in an
    environment that is never measured. The idler is measured in the orthonormal
    basis given by the columns of W (outcome d). The environment is summed out.

    Returns the same tables as kim_model (P_joint, P_detector, P_x_given_d,
    P_x_given_s, P_s_given_d) plus
        coherence_d  C_d = sum_e alpha_A(d, e)^* alpha_B(d, e), the cross amplitude
                     left in sub-ensemble d (alpha_s(d, e) = <d|m_s><e|e_s>)
        kappa        |C_d| / sqrt(P(d|A) P(d|B)): the coherence fraction that
                     sorting on d leaves (1 for a pure record)
    Rows with P(d) = 0 give zeros in the conditional tables.
    """
    U2 = far_field_propagator(n_modes)
    a, b = U2[:, slit_a], U2[:, slit_b]
    pB = 1.0 - pA
    alA = np.outer(W.conj().T @ mA, eA)                  # (nd, ne)
    alB = np.outer(W.conj().T @ mB, eB)
    psi = (np.sqrt(pA) * a[:, None, None] * alA[None]
           + np.sqrt(pB) * b[:, None, None] * alB[None])
    P_joint = (np.abs(psi) ** 2).sum(axis=2)
    P_detector = P_joint.sum(axis=0)
    P_d_given_s = np.array([(np.abs(alA) ** 2).sum(1), (np.abs(alB) ** 2).sum(1)])
    P_s_d = np.array([[pA], [pB]]) * P_d_given_s
    ok = P_detector > 1e-15
    safe = np.where(ok, P_detector, 1.0)
    C_d = (alA.conj() * alB).sum(1)
    den = np.sqrt(P_d_given_s[0] * P_d_given_s[1])
    return {
        "P_joint": P_joint,
        "P_screen": P_joint.sum(axis=1),
        "P_detector": P_detector,
        "P_x_given_d": np.where(ok, P_joint / safe, 0.0),
        "P_x_given_s": np.stack([np.abs(a) ** 2, np.abs(b) ** 2], axis=1),
        "P_s_given_d": np.where(ok, P_s_d / safe, 0.0),
        "coherence_d": C_d,
        "kappa": np.where(den > 1e-15, np.abs(C_d) / np.where(den > 1e-15, den, 1.0), 0.0),
    }


def fringe_visibility_exact(P_x_given_d: np.ndarray, slit_a: int = 10, slit_b: int = 13) -> np.ndarray:
    """
    Exact visibility of each column of P(x | d) on the DFT model, read from its single
    Fourier component at the slit separation: P = (A + B cos(k x + phase)), V = |B| / A.
    """
    n = P_x_given_d.shape[0]
    k = 2 * np.pi * (slit_b - slit_a) / n
    phase = np.exp(1j * k * np.arange(n))
    tot = P_x_given_d.sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(tot > 0, 2 * np.abs(phase @ P_x_given_d) / np.where(tot > 0, tot, 1.0), 0.0)


def _history_amplitudes(n_modes: int, slit_a: int, slit_b: int,
                        r: float, theta: float) -> np.ndarray:
    """b[x, d, s]: amplitude from the source through path s at t1 to (x, d) at t3."""
    U2 = far_field_propagator(n_modes)
    signal = U2[:, [slit_a, slit_b]]
    return signal[:, None, :] * idler_isometry(r, theta)[None, :, :] / np.sqrt(2.0)


def per_run_record_check(n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
                         r: float = 0.5, theta: float = np.pi / 4) -> Dict[str, np.ndarray]:
    """
    T3 restricted to the runs that end at one idler detector d (nb20 §4, per-run question).

        bound_d  = 2 sum_x |b[x, d, A]| |b[x, d, B]|
        defect_d = sum_x |P(x, d) - P_divided(x, d)|

    and the same divided by P(d) (the sub-ensemble's own normalisation). The
    per-detector bounds and defects add up to path_record_check's t3 values.
    """
    b = _history_amplitudes(n_modes, slit_a, slit_b, r, theta)
    actual = np.abs(b.sum(axis=2)) ** 2
    divided = (np.abs(b) ** 2).sum(axis=2)
    P_d = actual.sum(axis=0)
    bound = 2.0 * (np.abs(b[..., 0]) * np.abs(b[..., 1])).sum(axis=0)
    defect = np.abs(actual - divided).sum(axis=0)
    safe = np.where(P_d > 0, P_d, 1.0)
    return {"P_d": P_d, "bound_d": bound, "defect_d": defect,
            "bound_given_d": np.where(P_d > 0, bound / safe, 0.0),
            "defect_given_d": np.where(P_d > 0, defect / safe, 0.0)}


def delay_check(n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
                r: float = 0.5, theta: float = np.pi / 4) -> Dict[str, float]:
    """
    nb20 §6: the delay does no work.

    Two time orders: D0 first (Kim et al.) and idler first. For each, test T3 at
    the first detection time t2 with two different classings of the joint
    configuration:
      - by the detected photon's configuration only (pixel x, or detector d);
      - by the full joint configuration (detected photon AND the other photon's path).
    Also returns R01's visibility under the (wrong) prediction that divides on the
    full joint configuration at t2, and checks that the joint table P(x, d) is the
    same in both orders.

    Two of these outputs hold by construction and check the code, not the physics:
    order_difference (both orders build the same amplitude; the detections act on
    different factors), and the detected-only bounds (the detected photon's own
    configuration is part of every later configuration, so each later z has a
    single class and the bound is 0). The non-trivial output is bound_full_joint.
    """
    b = _history_amplitudes(n_modes, slit_a, slit_b, r, theta)       # [x, d, s]
    actual = np.abs(b.sum(axis=2)) ** 2

    # Both orders build the same history amplitudes; build the idler-first one
    # explicitly (idler isometry applied before the signal propagator).
    U2 = far_field_propagator(n_modes)
    V = idler_isometry(r, theta)
    psi_idler_first = np.einsum("xs,ds->xd", U2[:, [slit_a, slit_b]], V) / np.sqrt(2.0)
    order_diff = float(np.abs(np.abs(psi_idler_first) ** 2 - actual).max())

    # Classing by the detected photon only. D0 first: class = pixel x at t2; the
    # history amplitude through class c to the later z = (x', d) is
    # delta(c, x') psi(x', d). Idler first: class = detector d, likewise.
    psi = b.sum(axis=2)                                                # (x, d)
    n, nd = psi.shape
    def _bound(amp):            # amp[z, class]
        A = np.abs(amp)
        return float((A.sum(axis=1) ** 2 - (A ** 2).sum(axis=1)).sum())  # 2 sum_{c<c'} |a_c||a_c'|
    amp_D0_first = np.zeros((n, nd, n), dtype=complex)
    amp_idler_first = np.zeros((n, nd, nd), dtype=complex)
    for x in range(n):
        amp_D0_first[x, :, x] = psi[x, :]
    for d in range(nd):
        amp_idler_first[:, d, d] = psi[:, d]
    bound_D0_first = _bound(amp_D0_first.reshape(n * nd, n))
    bound_idler_first = _bound(amp_idler_first.reshape(n * nd, nd))
    # Classing by the full joint configuration: within a fixed detected value, the
    # classes are the two paths, so the bound is the t1 bound again.
    bound_full = float(2.0 * (np.abs(b[..., 0]) * np.abs(b[..., 1])).sum())

    divided_full = (np.abs(b) ** 2).sum(axis=2)
    Pd = divided_full.sum(axis=0)
    R01_div = divided_full[:, 0] / Pd[0] if Pd[0] > 0 else divided_full[:, 0]
    k = 2 * np.pi * (slit_b - slit_a) / n_modes
    vis = lambda p: float(2 * np.abs(np.exp(1j * k * np.arange(n_modes)) @ p) / p.sum())
    return {
        "order_difference": order_diff,
        "bound_detected_only_D0_first": bound_D0_first,
        "bound_detected_only_idler_first": bound_idler_first,
        "bound_full_joint": bound_full,
        "R01_visibility_actual": vis(actual[:, 0]),
        "R01_visibility_if_fully_divided_at_t2": vis(R01_div),
    }


def trigger_predictions(trigger: str, r: float = 0.5, theta: float = np.pi / 4,
                        n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
                        rstar: int = 3, lam: float = 0.0, hold: float = 0.0,
                        eps: float = 1e-9) -> Dict[str, np.ndarray]:
    """
    nb20 §7: R01..R04 under the reset triggers of notes/objective-division-events-2026-10-29.md.

    In Kim's setup exactly one fragment (the idler) holds a perfect path record,
    from t1 until the idler's two paths are mixed at BS, a time `hold`.

      QM : no reset.
      T1 : reset as soon as one perfect record exists      -> fires at t1.
      T2 : reset when >= rstar fragments hold the record   -> fires iff rstar <= 1.
      G  : graded dephasing, coherence factor exp(-lam * R * hold), R = 1.
      T3 : retrospective: computes path_record_check's bound_sup (the T3
           bound at t2 and t3) and fires iff it is <= eps.

    A reset (or dephasing) at t1 multiplies the path cross term by c:
        P_c(x, d) = P_divided(x, d) + c * (P(x, d) - P_divided(x, d)).
    Returns {"c": c, "P_x_given_d": (n, 4), "visibility": (4,)}.
    """
    if trigger == "QM":
        c = 1.0
    elif trigger == "T1":
        c = 0.0
    elif trigger == "T2":
        c = 0.0 if rstar <= 1 else 1.0
    elif trigger == "G":
        c = float(np.exp(-lam * 1 * hold))
    elif trigger == "T3":
        sup = path_record_check(n_modes, slit_a, slit_b, r, theta)["bound_sup"]
        c = 0.0 if sup <= eps else 1.0
    else:
        raise ValueError(f"unknown trigger {trigger!r}")
    b = _history_amplitudes(n_modes, slit_a, slit_b, r, theta)
    actual = np.abs(b.sum(axis=2)) ** 2
    divided = (np.abs(b) ** 2).sum(axis=2)
    P = divided + c * (actual - divided)
    Pd = P.sum(axis=0)
    Pxd = P / np.where(Pd > 0, Pd, 1.0)
    return {"c": c, "P_x_given_d": Pxd,
            "visibility": fringe_visibility_exact(Pxd, slit_a, slit_b)}
