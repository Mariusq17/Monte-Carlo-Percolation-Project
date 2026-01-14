# Analiza Monte Carlo a Pragului de Percolație (2D)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

Acest proiect implementează o simulare **Monte Carlo** pentru studiul fenomenului de percolație pe o rețea pătratică bidimensională. Obiectivul principal este determinarea experimentală a **pragului critic de percolație ($p_c$)**, punctul în care sistemul suferă o tranziție de fază geometrică.

## 📌 Descrierea Fenomenului

Percolația este un model fundamental în fizica statistică, utilizat pentru a descrie comportamentul sistemelor dezordonate (ex: curgerea fluidelor prin roci poroase, răspândirea epidemiilor, conductivitatea în rețele).

Într-o grilă $L \times L$, fiecare celulă poate fi:
- **Deschisă** (probabilitate $p$): Permite trecerea fluidului.
- **Blocată** (probabilitate $1-p$): Oprește trecerea fluidului.

Sistemul **percolează** dacă există un drum continuu de celule deschise care conectează latura superioară de cea inferioară a grilei.

## 🧮 Fundament Teoretic

Pentru o rețea pătratică 2D, nu există o soluție analitică exactă pentru $p_c$. Valoarea acceptată în literatura de specialitate, determinată numeric, este:

$$p_c \approx 0.592746$$

Proiectul estimează probabilitatea de percolație $\theta(p)$ definită ca:
$$\theta(p) = \mathbb{E}[\Pi_p]$$
unde $\Pi_p$ este variabila indicator (1 dacă percolează, 0 altfel).

### Analiza Erorilor (Inegalitatea Hoeffding)
Pentru a asigura rigoarea științifică, numărul de simulări ($N$) a fost calculat folosind **Inegalitatea lui Hoeffding** pentru a garanta o marjă de eroare $\epsilon = 0.01$ cu un nivel de încredere de $95\%$:

$$P(|\hat{\theta}_N(p) - \theta(p)| \ge \epsilon) \le 2e^{-2N\epsilon^2}$$

Calculul rezultat impune un număr minim de **18.445 simulări** per punct de probabilitate.

## 🛠️ Metodologie și Algoritm

Simularea este scrisă în **Python** și urmează pașii:

1.  **Generare:** Se creează o matrice booleană $L \times L$ conform probabilității $p$.
2.  **Verificare (Flood Fill):** Se utilizează un algoritm de tip **Breadth-First Search (BFS)**.
    * Se inițializează o coadă cu toate celulele deschise de pe prima linie.
    * Se propagă "fluidul" către vecinii adiacenți (Sus, Jos, Stânga, Dreapta).
    * Dacă un "strop" ajunge pe ultima linie, grila este marcată ca percolantă.
3.  **Iterare:** Procesul se repetă de $N$ ori pentru fiecare valoare $p \in [0, 1]$.

## 🚀 Cum să rulezi proiectul

### Cerințe preliminare
Ai nevoie de Python 3 instalat. Bibliotecile necesare sunt `numpy` și `matplotlib`.

### Instalare
```bash
# Clonează repository-ul
git clone [https://github.com/userul-tau/nume-repo.git](https://github.com/userul-tau/nume-repo.git)

# Navighează în folder
cd nume-repo

# Instalează dependențele
pip install numpy matplotlib
```
RulareBashpython main.py
Scriptul va rula simularea (poate dura câteva minute datorită numărului mare de iterații pentru precizie) și va genera automat graficele.

📊 Rezultate
În urma simulării, se obține curba sigmoidă caracteristică tranziției de fază.

Graficul Probabilității
Vizualizare Grilă
Notă: Imaginile sunt generate automat la rularea scriptului.

📝 Concluzii
Simularea a confirmat că tranziția de fază are loc brusc în jurul valorii $0.59$. Sub acest prag, probabilitatea de percolație este nulă, iar deasupra lui tinde rapid către 1, validând comportamentul teoretic al sistemelor critice.