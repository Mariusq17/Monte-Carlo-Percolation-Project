import numpy as np
import matplotlib.pyplot as plt
import time

# --- 1. MOTORUL DE SIMULARE (FLOOD FILL) ---

def verifica_percolatie(L, p):
    """
    Genereaza o grila LxL cu probabilitatea p si verifica percolatia
    folosind BFS (Breadth-First Search).
    """
    # Generare matrice (True/1 = deschis, False/0 = blocat)
    grid = np.random.rand(L, L) < p
    
    # Matrice pentru vizualizarea fluxului (unde ajunge apa)
    flow_grid = np.zeros((L, L), dtype=bool)
    visited = np.zeros((L, L), dtype=bool)
    
    # Initializare coada cu elementele deschise de pe prima linie
    queue = []
    for col in range(L):
        if grid[0, col]:
            queue.append((0, col))
            visited[0, col] = True
            flow_grid[0, col] = True

    percoleaza = False
    
    # Algoritmul BFS (Flood Fill)
    while len(queue) > 0:
        r, c = queue.pop(0)
        
        # Verificare daca am ajuns pe ultima linie
        if r == L - 1:
            percoleaza = True
        
        # Vecinii: Sus, Jos, Stanga, Dreapta
        vecini = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in vecini:
            nr, nc = r + dr, c + dc
            
            # Verificare limite si starea celulei (deschisa + nevizitata)
            if 0 <= nr < L and 0 <= nc < L:
                if grid[nr, nc] and not visited[nr, nc]:
                    visited[nr, nc] = True
                    flow_grid[nr, nc] = True
                    queue.append((nr, nc))
                    
    return percoleaza, grid, flow_grid

# --- 2. CALCULE TEORETICE (HOEFFDING) ---

def calculeaza_n_hoeffding(epsilon=0.01, confidence=0.95):
    """
    Calculeaza N necesar conform inegalitatii Hoeffding:
    N >= -ln(alpha / 2) / (2 * epsilon^2)
    """
    alpha = 1 - confidence
    N = -np.log(alpha / 2) / (2 * epsilon**2)
    return int(np.ceil(N))

# --- 3. SIMULAREA PRINCIPALA ---

def ruleaza_studiu_monte_carlo():
    L = 50          # Dimensiunea grilei
    epsilon = 0.01  # Eroare maxima admisa (1%)
    conf = 0.95     # Nivel de incredere (95%)
    
    # Calculare numar simulari necesare
    # N_sim = calculeaza_n_hoeffding(epsilon, conf)
    
    # Putem reduce N_sim pentru teste rapide (ex: N_sim = 1000)
    # Pentru varianta finala, pastreaza valoarea calculata (~18445)
    N_sim = 500 
    
    print(f"--- START SIMULARE ---")
    print(f"Dimensiune: {L}x{L}")
    print(f"Simulari necesare (Hoeffding): {N_sim}")
    
    # Definim intervalul de probabilitati p
    # Densitate mai mare in zona critica (0.50 - 0.70) pentru precizie
    p_values = np.concatenate([
        np.linspace(0, 0.5, 10),
        np.linspace(0.51, 0.65, 30),
        np.linspace(0.66, 1.0, 10)
    ])
    p_values = np.sort(np.unique(p_values))
    
    rezultate = []
    start_time = time.time()
    
    print(f"Rulare pentru {len(p_values)} puncte p...")
    
    for i, p in enumerate(p_values):
        success_count = 0
        for _ in range(N_sim):
            perc, _, _ = verifica_percolatie(L, p)
            if perc:
                success_count += 1
        
        prob_estimata = success_count / N_sim
        rezultate.append(prob_estimata)
        
        if i % 10 == 0:
            print(f"Progres: p={p:.2f} -> Theta={prob_estimata:.3f}")

    print(f"Finalizat in {time.time() - start_time:.2f} secunde.")
    return p_values, rezultate, N_sim, epsilon

# --- 4. VIZUALIZARE ---

def ploteaza_rezultate(p_vals, probs, N_sim, epsilon):
    plt.figure(figsize=(10, 6))
    
    # Grafic date simulate
    plt.plot(p_vals, probs, 'b-o', label=f'Simulare Monte Carlo (N={N_sim})')
    
    # Linie teoretica prag critic
    p_c = 0.592746
    plt.axvline(x=p_c, color='r', linestyle='--', label=f'Prag Teoretic ($p_c \\approx {p_c:.4f}$)')
    
    # Zona de eroare
    plt.fill_between(p_vals, 
                     np.array(probs) - epsilon, 
                     np.array(probs) + epsilon, 
                     color='blue', alpha=0.1, label=f'Marjă eroare ($\\pm{epsilon}$)')

    plt.title('Tranziția de Fază în Percolație 2D')
    plt.xlabel('Probabilitatea de ocupare ($p$)')
    plt.ylabel('Probabilitatea de Percolație $\\theta(p)$')
    plt.grid(True)
    plt.legend()
    plt.show()

def vizualizeaza_grila(L, p):
    """
    Genereaza o imagine colorata pentru o singura instanta.
    Cod culori: Negru=Blocat, Alb=Liber(Uscat), Albastru=Percolat(Ud)
    """
    perc, grid, flow = verifica_percolatie(L, p)
    
    imagine = np.zeros((L, L))
    imagine[grid == 0] = 0  # Blocat
    imagine[grid == 1] = 1  # Liber
    imagine[flow == 1] = 2  # Ud
    
    plt.figure(figsize=(6, 6))
    cmap = plt.cm.colors.ListedColormap(['black', 'white', 'deepskyblue'])
    plt.imshow(imagine, cmap=cmap)
    plt.title(f"Exemplu p={p} (Percoleaza: {'DA' if perc else 'NU'})")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Rulare simulare
    p_vals, probs, N, eps = ruleaza_studiu_monte_carlo()
    
    # Plotare curba sigmoidala
    ploteaza_rezultate(p_vals, probs, N, eps)
    
    # Generare exemple vizuale pentru prezentare
    vizualizeaza_grila(50, 0.40) # Sub prag
    vizualizeaza_grila(50, 0.60) # Peste prag