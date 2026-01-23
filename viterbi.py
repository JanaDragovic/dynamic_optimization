import numpy as np

# Definicija stanja i opservacija
stanja = ['Kisa', 'Oblak', 'Sunce']
opservacije = ['NE', 'DA']

# Tranziciona matrica P(s_t | s_{t-1})
A = np.array([
    [0.5, 0.3, 0.2],
    [0.4, 0.2, 0.4],
    [0.0, 0.3, 0.7]
])

# Emisiona matrica P(y | s)
B = np.array([
    [0.9, 0.1],
    [0.6, 0.4],
    [0.2, 0.8]
])

def viterbi(obs_seq, pocetno_stanje='Kisa'):
    T = len(obs_seq)
    N = len(stanja)
    
    obs_idx = [opservacije.index(o) for o in obs_seq]
    
    delta = np.zeros((T, N))
    psi = np.zeros((T, N), dtype=int)
    
    # Pocetni uslov
    pocetni_idx = stanja.index(pocetno_stanje)
    for i in range(N):
        if i == pocetni_idx:
            delta[0, i] = 1.0 * B[i, obs_idx[0]]
        else:
            delta[0, i] = 0.0
    
    # Rekurzija
    for t in range(1, T):
        for j in range(N):
            probs = delta[t-1, :] * A[:, j]
            delta[t, j] = np.max(probs) * B[j, obs_idx[t]]
            psi[t, j] = np.argmax(probs)
    
    # Pronalazenje najbolje putanje
    best_path = np.zeros(T, dtype=int)
    best_path[T-1] = np.argmax(delta[T-1, :])
    best_prob = delta[T-1, best_path[T-1]]
    
    # Pracenje unazad
    for t in range(T-2, -1, -1):
        best_path[t] = psi[t+1, best_path[t+1]]
    
    best_states = [stanja[i] for i in best_path]
    
    return best_states, best_prob

def generisi_sve_sekvence(duzina, br_stanja):
    # Generise sve moguce sekvence duzine 'duzina' sa 'br_stanja' mogucih vrednosti
    if duzina == 0:
        return [[]]
    rezultat = []
    krace = generisi_sve_sekvence(duzina - 1, br_stanja)
    for seq in krace:
        for s in range(br_stanja):
            rezultat.append(seq + [s])
    return rezultat

def izracunaj_sve_verovatnoce(obs_seq, pocetno_stanje='Kisa'):
    T = len(obs_seq)
    obs_idx = [opservacije.index(o) for o in obs_seq]
    pocetni_idx = stanja.index(pocetno_stanje)
    
    rezultati = []
    
    # Generisanje svih mogucih sekvenci stanja (prvo stanje fiksirano)
    sve_sekvence = generisi_sve_sekvence(T - 1, len(stanja))
    
    for seq in sve_sekvence:
        stanja_seq = [pocetni_idx] + seq
        
        prob = 1.0
        prob *= B[stanja_seq[0], obs_idx[0]]
        
        for t in range(1, T):
            prob *= A[stanja_seq[t-1], stanja_seq[t]]
            prob *= B[stanja_seq[t], obs_idx[t]]
        
        nazivi = [stanja[i] for i in stanja_seq]
        rezultati.append((nazivi, prob))
    
    rezultati.sort(key=lambda x: x[1], reverse=True)
    return rezultati

def test_sekvenca(obs_seq, naziv=""):
    print(f"\n{naziv}")
    print(f"Opservaciona sekvenca: {obs_seq}")
    
    best_states, best_prob = viterbi(obs_seq)
    print(f"Viterbi rezultat: {best_states}")
    print(f"Verovatnoca: {best_prob:.6e}")
    
    sve = izracunaj_sve_verovatnoce(obs_seq)
    print(f"Top 10 sekvenci po verovatnoci:")
    for i, (seq, prob) in enumerate(sve[:10]):
        oznaka = " <-- Optimalna putanja" if seq == best_states else ""
        print(f"  {i+1}. {seq} : {prob:.6e}{oznaka}")

if __name__ == "__main__":
    print("Viterbijevo dekodovanje za HMM")
    print("Skrivena stanja: Kisa, Oblak, Sunce")
    print("Opservacije: NE, DA")
    print("Pocetno stanje: Kisa")
    
    test_sekvenca(['NE', 'DA', 'NE', 'NE', 'NE'], "Test 1: Sekvenca iz zadatka")
    test_sekvenca(['DA', 'DA', 'DA', 'DA', 'DA'], "Test 2: Stalno dobro raspolozenje")
    test_sekvenca(['NE', 'NE', 'NE', 'NE', 'NE'], "Test 3: Stalno lose raspolozenje")
    test_sekvenca(['NE', 'DA', 'NE', 'DA', 'NE'], "Test 4: Naizmenicno raspolozenje")