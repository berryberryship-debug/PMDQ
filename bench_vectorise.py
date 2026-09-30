#!/usr/bin/env python3
"""Benchmark : boucle Python vs NumPy vectorisé (sans Numba)."""
import time
import numpy as np


def bootstrap_python_loop(data, n_boot=10_000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(data)
    moyens = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        somme = 0.0
        for j in range(n):
            somme += data[rng.integers(0, n)]
        moyens[i] = somme / n
    return moyens


def bootstrap_numpy_vectorise(data, n_boot=10_000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(data)
    indices = rng.integers(0, n, size=(n_boot, n))
    echantillons = data[indices]
    return echantillons.mean(axis=1)


def monte_carlo_python(n_sim=10_000, n_etapes=100, seed=42):
    rng = np.random.default_rng(seed)
    resultats = np.empty(n_sim, dtype=np.float64)
    for i in range(n_sim):
        cout = 1.0
        for t in range(n_etapes):
            cout *= (1.0 + rng.normal(0, 0.05))
        resultats[i] = cout
    return resultats


def monte_carlo_numpy_vectorise(n_sim=10_000, n_etapes=100, seed=42):
    rng = np.random.default_rng(seed)
    chocs = rng.normal(0, 0.05, size=(n_sim, n_etapes))
    return (1.0 + chocs).prod(axis=1)


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
    print("  BENCHMARK — Boucle Python vs NumPy vectorisé")
    print("=" * 68)

    data_prov = np.random.lognormal(mean=10, sigma=0.5, size=200)

    print("\n[1] Bootstrap (10 000 rééchantillonnages, n=200)")
    t_py, r_py = bench(bootstrap_python_loop, 3, data_prov)
    print(f"    Boucle Python    : {t_py*1000:8.2f} ms")

    t_np, r_np = bench(bootstrap_numpy_vectorise, 3, data_prov)
    print(f"    NumPy vectorisé  : {t_np*1000:8.2f} ms")
    print(f"    Gain             : x{t_py/t_np:.1f}")

    print("\n[2] Monte-Carlo (10 000 simulations × 100 étapes)")
    t_py, r_py = bench(monte_carlo_python, 3)
    print(f"    Boucle Python    : {t_py*1000:8.2f} ms")

    t_np, r_np = bench(monte_carlo_numpy_vectorise, 3)
    print(f"    NumPy vectorisé  : {t_np*1000:8.2f} ms")
    print(f"    Gain             : x{t_py/t_np:.1f}")

    print("\n" + "=" * 68)


if __name__ == "__main__":
    main()
