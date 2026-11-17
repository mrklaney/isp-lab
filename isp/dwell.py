# dwell.py
"""
Conditional ("weak-value") dwell times as a probe of indivisibility. Used by notebook 17.

For a binary intermediate variable b in {in, out} at time t and a post-selection f at the final time T,
the Margenau-Hill quasiprobability q(in, f; t) = Re <psi| Pi_in(t) Pi_f(T) |psi> splits exactly as

    q(in, f; t) = P_seq(in, f; t) + Delta_f(t) / 2,

where P_seq is the joint probability with a division event of b at t (a strong record of in/out at t), and
Delta_f = P(f) - P_seq(in, f) - P_seq(out, f) is the indivisibility defect of that division (Halliwell,
arXiv:1508.02271 v5, eqs. (2.1), (2.4)-(2.5); its printed "2 Re D" in (2.4) should read Re D, as in Halliwell et al.,
PRA 99, 012124 (2019), eq. (2.3); here Delta_f = 2 Re D). The conditional dwell time is
tau_f = int q dt / P(f) (Steinberg, PRA 52, 32 (1995)); sum_f P(f) tau_f is the unconditioned dwell time.

Two closed models (Gamma = |U|^2 throughout):
  ChiralChain   N two-level atoms in a one-way waveguide, single excitation, each atom with a private loss band:
                the negative photon excitation time of Angulo et al., arXiv:2409.03680.
  TunnelChain   a particle on a tight-binding chain with a rectangular barrier: Steinberg's tunnelling times.
"""

from dataclasses import dataclass
import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# The decomposition, for any closed model given by an eigendecomposition
# ---------------------------------------------------------------------------------------------------------------
class _Closed:
    w: np.ndarray
    V: np.ndarray

    def evolve(self, psi, t):
        return self.V @ (np.exp(-1j * self.w * t) * (self.V.conj().T @ psi))


def _trap(y, t):
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(t)))


def decompose(model, psi0, region, final, T, nt=400):
    """
    Time-resolved split of the conditional dwell time in `region` (bool mask over configurations), post-selected on
    `final` (bool mask) at time T. Returns a dict of arrays over t (q, seq, defect_half, p_in) and integrated values
    (P_f, tau, tau_seq, tau_defect, dwell) plus the largest violation of the identity, identity_err.
    """
    ts = np.linspace(0, T, nt)
    psiT = model.evolve(psi0, T)
    Pf = float(np.linalg.norm(psiT[final]) ** 2)
    q = np.zeros(nt); seq = np.zeros(nt); seq_out = np.zeros(nt); p_in = np.zeros(nt)
    for n, t in enumerate(ts):
        pt = model.evolve(psi0, t)
        a_in = np.where(region, pt, 0)
        a_out = pt - a_in
        u_in = model.evolve(a_in, T - t)[final]
        u_out = model.evolve(a_out, T - t)[final]
        q[n] = np.real(np.vdot(u_in + u_out, u_in))
        seq[n] = np.linalg.norm(u_in) ** 2
        seq_out[n] = np.linalg.norm(u_out) ** 2
        p_in[n] = np.linalg.norm(a_in) ** 2
    defect = Pf - seq - seq_out
    return dict(t=ts, q=q, seq=seq, defect_half=defect / 2, p_in=p_in, P_f=Pf,
                tau=_trap(q, ts) / Pf, tau_seq=_trap(seq, ts) / Pf, tau_defect=_trap(defect / 2, ts) / Pf,
                dwell=_trap(p_in, ts), identity_err=float(np.max(np.abs(q - seq - defect / 2))))


# ---------------------------------------------------------------------------------------------------------------
# Atoms in a chiral waveguide
# ---------------------------------------------------------------------------------------------------------------
class ChiralChain(_Closed):
    """
    N atoms (configurations 0..N-1 = 'atom j excited') in a one-way waveguide with M_f forward modes (spacing delta,
    coupling g_f e^{i eps_k x_j}), each atom with its own flat loss band of M_l modes. Rates: Gamma_1d = 2 pi g_f^2/delta,
    Gamma_loss = 2 pi g_l^2/delta, tau_sp = 1/(Gamma_1d + Gamma_loss). Continuum transmission t1(w)^N.
    """

    def __init__(self, N, G1d=0.1, Gl=0.9, delta=0.1, Wf=40.0, Wl=20.0, spacing=0.2, e0=0.0):
        self.N, self.G1d, self.Gl, self.delta, self.e0 = N, G1d, Gl, delta, e0
        Mf, Ml = int(round(Wf / delta)), int(round(Wl / delta))
        self.eps_f = (np.arange(Mf) - (Mf - 1) / 2) * delta
        eps_l = (np.arange(Ml) - (Ml - 1) / 2) * delta
        gf, gl = np.sqrt(G1d * delta / (2 * np.pi)), np.sqrt(Gl * delta / (2 * np.pi))
        self.D = N + Mf + N * Ml
        H = np.zeros((self.D, self.D), dtype=complex)
        self.atoms = np.zeros(self.D, bool); self.atoms[:N] = True
        self.forward = np.zeros(self.D, bool); self.forward[N:N + Mf] = True
        iF = np.arange(N, N + Mf)
        H[iF, iF] = self.eps_f
        for j in range(N):
            H[j, j] = e0
            H[j, iF] = gf * np.exp(1j * self.eps_f * j * spacing)
            H[iF, j] = np.conj(H[j, iF])
            il = N + Mf + j * Ml + np.arange(Ml)
            H[il, il] = eps_l
            H[j, il] = gl
            H[il, j] = gl
        self.H = H
        self.w, self.V = np.linalg.eigh(H)

    @property
    def recurrence_time(self):
        return 2 * np.pi / self.delta

    def t1(self, w):
        """Continuum transmission amplitude of one atom at frequency w."""
        return (w - self.e0 + 1j * (self.Gl - self.G1d) / 2) / (w - self.e0 + 1j * (self.G1d + self.Gl) / 2)

    def transmission(self, w):
        return self.t1(w) ** self.N

    @property
    def OD(self):
        return float(-self.N * np.log(abs(self.t1(self.e0)) ** 2))

    def pulse(self, sigma_t, t_in):
        """Single-photon Gaussian pulse, intensity rms duration sigma_t, peak reaching atom 0 at t_in."""
        a = np.sqrt(2) * sigma_t
        c = np.exp(-(self.eps_f * a) ** 2 / 2) * np.exp(1j * self.eps_f * t_in)
        psi = np.zeros(self.D, dtype=complex)
        psi[self.forward] = c / np.linalg.norm(c)
        return psi

    def run(self, sigma_t, nt=400):
        """Prepare the pulse, choose T (pulse past, atoms decayed, before the recurrence) and decompose."""
        t_in = 8 * sigma_t + 2
        T = t_in + 8 * sigma_t + 14 / (self.G1d + self.Gl)
        if T > 0.8 * self.recurrence_time:
            raise ValueError("pulse too long for this band spacing")
        psi0 = self.pulse(sigma_t, t_in)
        out = decompose(self, psi0, self.atoms, self.forward, T, nt)
        out["T"] = T
        out["tau_g"] = self.group_delay_pulse(sigma_t)
        # group delay of the model's own transmitted light: t(eps_k) read off the output modes
        cin = psi0[self.forward]
        cout = self.evolve(psi0, T)[self.forward] * np.exp(1j * self.eps_f * T)
        good = np.abs(cin) > 1e-6 * np.abs(cin).max()
        tk = cout[good] / cin[good]
        dphi = np.gradient(np.unwrap(np.angle(tk)), self.eps_f[good])
        wgt = np.abs(cout[good]) ** 2
        out["tau_g_model"] = float(np.sum(wgt * dphi) / np.sum(wgt))
        return out

    def group_delay_pulse(self, sigma_t, chi_p=0.0):
        """Pulse-averaged group delay of the transmitted light (continuum): sum |c t|^2 phi' / sum |c t|^2,
        with the atoms shifted by chi_p."""
        a = np.sqrt(2) * sigma_t
        eps = np.linspace(-12 / a - 8, 12 / a + 8, 4001)
        c2 = np.exp(-(eps * a) ** 2)
        tN = self.t1(eps - chi_p) ** self.N
        dphi = np.gradient(np.unwrap(np.angle(tN)), eps)
        T2 = np.abs(tN) ** 2
        return float(np.sum(c2 * T2 * dphi) / np.sum(c2 * T2))


def pointer_shift(chain, sigma_t, sigma_x, chi=1.0, npts=801):
    """
    Conditional mean shift (divided by chi) of a Gaussian pointer with position spread sigma_x, coupled by
    H_int = chi p Pi_e for the whole run, given that the photon is transmitted. Each pointer momentum p shifts the
    atoms by chi p, so (continuum, using int q dt = -Im <out_f | d out_f / d eta>):
        shift = int phi(p)^2 N(chi p) dp / int phi(p)^2 P(chi p) dp,
    N = sum |c|^2 |t|^2 phi',  P = sum |c|^2 |t|^2.  sigma_x -> infinity gives the weak value tau_T.
    """
    a = np.sqrt(2) * sigma_t
    eps = np.linspace(-12 / a - 8, 12 / a + 8, 4001)
    c2 = np.exp(-(eps * a) ** 2); c2 /= c2.sum()
    sp = 1 / (2 * sigma_x)
    p = np.linspace(-6 * sp, 6 * sp, npts)
    wp = np.exp(-p ** 2 / (2 * sp ** 2)); wp /= wp.sum()
    num = den = 0.0
    for pi, wi in zip(p, wp):
        tN = chain.transmission(eps - chi * pi)
        dphi = np.gradient(np.unwrap(np.angle(tN)), eps)
        T2 = np.abs(tN) ** 2
        num += wi * np.sum(c2 * T2 * dphi)
        den += wi * np.sum(c2 * T2)
    return float(num / den)


def pointer_shift_discrete(chain, sigma_t, sigma_x, chi=1.0, npts=21, h=1e-4):
    """The same quantity from the closed discrete model, one eigendecomposition per pointer momentum."""
    t_in = 8 * sigma_t + 2
    T = t_in + 8 * sigma_t + 14 / (chain.G1d + chain.Gl)
    psi0 = chain.pulse(sigma_t, t_in)
    sp = 1 / (2 * sigma_x)
    p = np.linspace(-4 * sp, 4 * sp, npts)
    wp = np.exp(-p ** 2 / (2 * sp ** 2)); wp /= wp.sum()
    num = den = 0.0
    for pi, wi in zip(p, wp):
        outs = []
        for s in (-h, 0.0, h):
            Hs = chain.H.copy()
            Hs[chain.atoms, chain.atoms] += chi * pi + s
            w, V = np.linalg.eigh(Hs)
            outs.append((V @ (np.exp(-1j * w * T) * (V.conj().T @ psi0)))[chain.forward])
        d = (outs[2] - outs[0]) / (2 * h)
        num += wi * (-np.imag(np.vdot(outs[1], d)))
        den += wi * np.linalg.norm(outs[1]) ** 2
    return float(num / den)


# ---------------------------------------------------------------------------------------------------------------
# A tunnelling particle
# ---------------------------------------------------------------------------------------------------------------
@dataclass
class TunnelChain(_Closed):
    """Tight-binding chain (hopping 1) of L sites with a barrier of height V on sites [L//2, L//2 + w)."""
    L: int = 400
    V0: float = 1.2
    w_bar: int = 4

    def __post_init__(self):
        self.b0 = self.L // 2
        H = -(np.eye(self.L, k=1) + np.eye(self.L, k=-1))
        self.barrier = np.zeros(self.L, bool); self.barrier[self.b0:self.b0 + self.w_bar] = True
        H[self.barrier, self.barrier] += self.V0
        self.H = H
        self.w, self.V = np.linalg.eigh(H)
        x = np.arange(self.L)
        self.left = x < self.b0
        self.right = x >= self.b0 + self.w_bar

    def region(self, name, width=10):
        r = np.zeros(self.L, bool)
        if name == "barrier":
            return self.barrier.copy()
        if name == "behind":
            r[self.b0 + self.w_bar:self.b0 + self.w_bar + width] = True
        elif name == "front":
            r[self.b0 - width:self.b0] = True
        return r

    def run(self, region, k0=1.0, sigma=12.0, x0=120, nt=300):
        x = np.arange(self.L)
        psi0 = np.exp(-(x - x0) ** 2 / (4 * sigma ** 2) + 1j * k0 * x)
        psi0 = psi0 / np.linalg.norm(psi0)
        vg = 2 * np.sin(k0)
        T = (self.b0 - x0) / vg + 70 / vg + 6 * sigma / vg
        reg = self.region(region) if isinstance(region, str) else region
        return {name: decompose(self, psi0, reg, F, T, nt) for name, F in
                (("transmitted", self.right), ("reflected", self.left))}
