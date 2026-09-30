#!/usr/bin/env python3
"""Benchmark avant/après Numba sur les moteurs réels du PMDQ."""
import time
import numpy as np

# ─────────────────────────────────────────────────────────────
# Cas 1 : Bootstrap (moteur_provisionnement.py)
# ─────────────────────────────────────────────────────────────

def bootstrap_python(data, n_boot=10_000, seed=42):
    """Bootstrap naïf en Python pur."""
    rng = np.random.default_rng(seed)
    n = len(data)
    moyens = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        echantillon = rng.choice(data, size=n, replace=True)
        moyens[i] = np.mean(echantillon)
    return moyens


def bootstrap_python_loop(data, n_boot=10_000, seed=42):
    """Bootstrap avec boucle Python explicite (pire cas)."""
    rng = np.random.default_rng(seed)
    n = len(data)
    moyens = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        somme = 0.0
        for j in range(n):
            idx = rng.integers(0, n)
            somme += data[idx]
        moyens[i] = somme / n
    return moyens


try:
    from numba import njit

    @njit(cache=True)
    def _bootstrap_numba_kernel(data, indices, n_boot, n):
        moyens = np.empty(n_boot, dtype=np.float64)
        for i in range(n_boot):
            somme = 0.0
            for j in range(n):
                somme += data[indices[i, j]]
            moyens[i] = somme / n
        return moyens

    def bootstrap_numba(data, n_boot=10_000, seed=42):
        rng = np.random.default_rng(seed)
        n = len(data)
        indices = rng.integers(0, n, size=(n_boot, n))
        return _bootstrap_numba_kernel(data, indices, n_boot, n)

    NUMBA_DISPONIBLE = True
except ImportError:
    NUMBA_DISPONIBLE = False
    print("⚠ Numba non installé : pip install numba")


# ─────────────────────────────────────────────────────────────
# Cas 2 : Monte-Carlo (analyse des dépassements)
# ─────────────────────────────────────────────────────────────

def monte_carlo_python(n_sim=10_000, n_etapes=100, seed=42):
    """Simulation Monte-Carlo de trajectoires de coûts."""
    rng = np.random.default_rng(seed)
    resultats = np.empty(n_sim, dtype=np.float64)
    for i in range(n_sim):
        cout = 1.0
        for t in range(n_etapes):
            choc = rng.normal(0, 0.05)
            cout *= (1.0 + choc)
        resultats[i] = cout
    return resultats


if NUMBA_DISPONIBLE:
    @njit(cache=True)
    def _monte_carlo_numba_kernel(chocs, n_sim, n_etapes):
        resultats = np.empty(n_sim, dtype=np.float64)
        for i in range(n_sim):
            cout = 1.0
            for t in range(n_etapes):
                cout *= (1.0 + chocs[i, t])
            resultats[i] = cout
        return resultats

    def monte_carlo_numba(n_sim=10_000, n_etapes=100, seed=42):
        rng = np.random.default_rng(seed)
        chocs = rng.normal(0, 0.05, size=(n_sim, n_etapes))
        return _monte_carlo_numba_kernel(chocs, n_sim, n_etapes)


# ─────────────────────────────────────────────────────────────
# Benchmark
# ─────────────────────────────────────────────────────────────

def bench(func, n_runs=3, *args, **kwargs):
    temps = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        resultat = func(*args, **kwargs)
        t1 = time.perf_counter()
        temps.append(t1 - t0)
    return np.mean(temps), resultat


def main():
    print("=" * 68)
    print("  BENCHMARK — MOTEURS PMDQ (avant/après Numba)")
    print("=" * 68)

    # Données de test réalistes
    data_prov = np.random.lognormal(mean=10, sigma=0.5, size=200)

    # ─── CAS 1 : BOOTSTRAP ───
    print("\n[1] Bootstrap (10 000 rééchantillonnages, n=200)")
    t_py, r_py = bench(bootstrap_python, 3, data_prov)
    print(f"    Python + NumPy  : {t_py*1000:8.2f} ms")

    if NUMBA_DISPONIBLE:
        _ = bootstrap_numba(data_prov, n_boot=100)  # warmup
        t_nb, r_nb = bench(bootstrap_numba, 3, data_prov)
        print(f"    Numba           : {t_nb*1000:8.2f} ms")
        print(f"    Gain            : x{t_py/t_nb:.1f}")
        ecart = np.max(np.abs(np.sort(r_py) - np.sort(r_nb)) / np.abs(r_py).mean())
        print(f"    Écart (rel.)    : {ecart:.2e}")

    # ─── CAS 2 : MONTE-CARLO ───
    print("\n[2] Monte-Carlo (10 000 simulations × 100 étapes)")
    t_py, r_py = bench(monte_carlo_python, 3)
    print(f"    Python          : {t_py*1000:8.2f} ms")

    if NUMBA_DISPONIBLE:
        _ = monte_carlo_numba(n_sim=100, n_etapes=10)  # warmup
        t_nb, r_nb = bench(monte_carlo_numba, 3)
        print(f"    Numba           : {t_nb*1000:8.2f} ms")
        print(f"    Gain            : x{t_py/t_nb:.1f}")
        ecart = np.max(np.abs(r_py - r_nb)) / np.abs(r_py).mean()
        print(f"    Écart (rel.)    : {ecart:.2e}")

    print("\n" + "=" * 68)


if __name__ == "__main__":
    main()
