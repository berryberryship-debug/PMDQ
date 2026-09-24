import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import csc_matrix, eye, kron, bmat

def gksl_liouvillian(H, ops, rates):
    H_m = csc_matrix(H); d = H_m.shape[0]
    I = eye(d, format="csc")
    L = -1j * (kron(I, H_m) - kron(H_m.T, I))
    for A, r in zip(ops, rates):
        A = csc_matrix(A); AdA = A.getH() @ A
        diss = kron(A.conjugate(), A) - 0.5*kron(I, AdA) - 0.5*kron(AdA.T, I)
        L = L + r * diss
    return csc_matrix(L)

def hamiltonian_torus_5d(t, t_max, omega_max):
    t_mid = t_max/2.0; sigma = t_max/6.0
    g = omega_max * np.exp(-((t-t_mid)**2)/(2*sigma**2))
    H = np.zeros((5,5), dtype=complex)
    for i in range(4):
        H[i,i+1] = g; H[i+1,i] = g
    H[0,4] = g * np.exp(1j*2.0*np.pi/5.0)
    H[4,0] = np.conj(H[0,4])
    return H

def solve_gksl_torus(t_eval, ops, rates, y0, omega_max):
    n_c = y0.size; t_max = float(t_eval[-1])
    def rhs(t, y):
        H_t = hamiltonian_torus_5d(t, t_max, omega_max)
        L = gksl_liouvillian(H_t, ops, rates)
        J_R = bmat([[L.real, -L.imag],[L.imag, L.real]], format="csc")
        return J_R @ y
    y0_r = np.concatenate([y0.real, y0.imag])
    sol = solve_ivp(fun=rhs, t_span=(0.0, t_max), y0=y0_r, method="Radau",
                    t_eval=t_eval, rtol=1e-6, atol=1e-8)
    yt = sol.y[:n_c,:] + 1j*sol.y[n_c:,:] if sol.success else np.zeros((n_c,len(t_eval)), dtype=complex)
    return {"y": yt, "success": sol.success}

if __name__ == "__main__":
    d = 5
    A_bruit = np.diag([1.0, 0.7, 0.2, -0.4, -1.5]).astype(complex)
    rho_0 = np.zeros((d,d), dtype=complex); rho_0[0,0] = 1.0
    t_c = np.linspace(0.0, 15.0, 100)
    res = solve_gksl_torus(t_c, [A_bruit], [0.015], rho_0.flatten(order="F"), 4.2)
    rho_f = res["y"][:,-1].reshape((d,d), order="F")
    pops = np.abs(np.diag(rho_f))
    purity = float(np.real(np.trace(rho_f @ rho_f)))
    print("=== TOPOLOGY RESULTS ===")
    print(f"Solver Success : {res['success']}")
    print(f"Purity         : {purity:.4f}")
    print(f"Info lost      : {(1.0-purity)*100:.2f} %")
    for i,p in enumerate(pops):
        print(f" |{i}> : [{p:.4f}] " + "#"*int(p*20))
