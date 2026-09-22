import numpy as np
import matplotlib.pyplot as plt

def simulate_no_debt(N=500, M=5e5, steps=4e5, transaction_type='constant'):
    """
    Simulation without debt.
    N: number of agents
    M: total money
    steps: number of transactions
    transaction_type: 'constant' (exchange of 1 unit), 
                      'fraction_pair' (exchange of a random fraction of the average money of the pair),
                      'fraction_system' (exchange of a random fraction of the system-wide average money)
    """
    N = int(N)
    steps = int(steps)
    
    # Initialization: all agents start with equal amounts of money
    agents = np.ones(N) * M / N
    
    for t in range(steps):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        if i == j:
            continue
        
        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            mean_pair = (agents[i] + agents[j]) / 2
            delta = np.random.rand() * mean_pair
        elif transaction_type == 'fraction_system':
            mean_system = np.mean(agents)
            delta = np.random.rand() * mean_system
        else:
            delta = 1
        
        # Agent i pays agent j
        if agents[i] >= delta:
            agents[i] -= delta
            agents[j] += delta
        # If agent i doesn't have enough, skip the transaction
    
    return agents


def simulate_entropy(N=500, M=5e5, steps=2000, transaction_type='constant', bins=500, max_money=5000):
    """
    Simulate the evolution of entropy with different transaction types.
    
    Parameters:
    N : int
        Number of agents.
    M : float
        Total money in the system.
    steps : int
        Number of time steps.
    transaction_type : str
        Type of transaction ('constant', 'fraction_pair', 'fraction_system').
    bins : int
        Number of bins for the histogram.
    max_money : int
        Range for the histogram to compute the distribution.
        
    Returns:
    time : np.ndarray
        Time steps array.
    S_values : list
        Entropy values at each time step.
    """
    # Initialize agents with equal distribution of money
    agents = np.ones(N) * M / N

    # Compute initial entropy
    hist, _ = np.histogram(agents, bins=bins, range=(0, max_money), density=True)
    S_values = [-np.sum(hist[hist > 0] * np.log(hist[hist > 0]))]

    # Simulation loop
    for t in range(1, steps + 1):
        # Select two random agents
        i, j = np.random.choice(N, 2, replace=False)
        
        # Determine transaction amount based on type
        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            mean_pair = (agents[i] + agents[j]) / 2
            delta = np.random.rand() * mean_pair
        elif transaction_type == 'fraction_system':
            mean_system = np.mean(agents)
            delta = np.random.rand() * mean_system
        else:
            raise ValueError("Invalid transaction type.")

        # Perform the transaction if agent i has enough money
        if agents[i] >= delta:
            agents[i] -= delta
            agents[j] += delta
        
        # Compute entropy at each step
        hist, _ = np.histogram(agents, bins=bins, range=(0, max_money), density=True)
        S_values.append(-np.sum(hist[hist > 0] * np.log(hist[hist > 0])))

    time = np.arange(0, steps + 1)
    return time, S_values




def simulate_with_debt(N=500, M=5e5, steps=4e5, md=800, transaction_type='constant'):
    """
    Simulation with a maximum debt limit (md).
    """
    N = int(N)
    steps = int(steps)
    agents = np.ones(N) * M / N  # Initialize agents with equal money

    for t in range(steps):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        if i == j:
            continue

        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            mean_pair = (agents[i] + agents[j]) / 2
            delta = np.random.rand() * mean_pair
        elif transaction_type == 'fraction_system':
            mean_system = np.mean(agents)
            delta = np.random.rand() * mean_system
        else:
            delta = 1

        # Agent i pays agent j, can go into debt up to -md
        if agents[i] - delta >= -md:
            agents[i] -= delta
            agents[j] += delta
            
    return agents


def simulate_with_debt_shifted(N=500, M=5e5, steps=4e5, md=800, transaction_type='constant'):
    """
    Simulate money with a maximum debt limit using shifted wealth.

    The internal wealth variable is x = money + md, so x is always
    nonnegative. The returned array is converted back to actual money.
    """
    N = int(N)
    steps = int(steps)
    md = float(md)
    shifted_agents = np.ones(N) * (M / N + md)

    for _ in range(steps):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        if i == j:
            continue

        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            mean_pair = (shifted_agents[i] + shifted_agents[j]) / 2
            delta = np.random.rand() * mean_pair
        elif transaction_type == 'fraction_system':
            delta = np.random.rand() * np.mean(shifted_agents)
        else:
            raise ValueError("Invalid transaction type.")

        if shifted_agents[i] >= delta:
            shifted_agents[i] -= delta
            shifted_agents[j] += delta

    return shifted_agents - md


def simulate_double_sided_ratio(N=1000, M0=3000, r=0.6180339887498949, steps=1e6, transaction_type='constant'):
    """
    Simulate a two-sided money model where the fraction of positive agents is exactly r,
    and the fraction of negative/debt agents is 1-r.

    The positive pool has total M0 / r, while the debt pool has total
    M0 * (1-r) / r. This keeps the total net wealth equal to M0 while making the
    two populations match the chosen ratio.

    Choosing r = (sqrt(5)-1)/2 ~ 0.618 makes the two branches meet at m = 0.
    """
    N = int(N)
    steps = int(steps)
    M0 = float(M0)
    r = float(r)

    if N < 2:
        raise ValueError("N must be at least 2.")
    if M0 < 0:
        raise ValueError("M0 must be nonnegative.")
    if not 0 < r < 1:
        raise ValueError("r must be between 0 and 1 for a double-sided model.")

    # The two populations are sized according to the ratio r.
    N_positive = int(round(r * N))
    N_negative = N - N_positive

    if N_positive == 0:
        N_positive = 1
        N_negative = N - 1
    if N_negative == 0:
        N_negative = 1
        N_positive = N - 1

    positive_total = M0 / r
    debt_total = M0 * (1 - r) / r

    positive = np.full(N_positive, positive_total / N_positive)
    debt = np.full(N_negative, debt_total / N_negative)

    for _ in range(steps):
        pool = positive if np.random.rand() < r else debt
        i, j = np.random.choice(len(pool), size=2, replace=False)

        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            delta = np.random.rand() * (pool[i] + pool[j]) / 2
        elif transaction_type == 'fraction_system':
            delta = np.random.rand() * np.mean(pool)
        else:
            raise ValueError("Invalid transaction type.")

        if pool[i] >= delta:
            pool[i] -= delta
            pool[j] += delta

    return np.concatenate([positive, -debt])


def simulate_double_sided(N=1000, M0=3000, r=0.5, steps=1e6, transaction_type='constant'):
    """
    Simulate separately conserved positive-money and debt pools.

    The positive pool contains M0 / r and the debt pool contains
    M0 * (1 - r) / r. Returned balances are positive for the first pool
    and negative for the debt pool.
    """
    N = int(N)
    steps = int(steps)
    M0 = float(M0)
    r = float(r)

    if N < 2:
        raise ValueError("N must be at least 2.")
    if M0 < 0:
        raise ValueError("M0 must be nonnegative.")
    if not 0 < r < 1:
        raise ValueError("r must be between 0 and 1 for a double-sided model.")

    N_positive = N // 2
    N_negative = N - N_positive
    positive_total = M0 / r
    debt_total = M0 * (1 - r) / r

    positive = np.full(N_positive, positive_total / N_positive)
    debt = np.full(N_negative, debt_total / N_negative)

    for _ in range(steps):
        pool = positive if np.random.rand() < 0.5 else debt
        i, j = np.random.choice(len(pool), size=2, replace=False)

        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            delta = np.random.rand() * (pool[i] + pool[j]) / 2
        elif transaction_type == 'fraction_system':
            delta = np.random.rand() * np.mean(pool)
        else:
            raise ValueError("Invalid transaction type.")

        if pool[i] >= delta:
            pool[i] -= delta
            pool[j] += delta

    return np.concatenate([positive, -debt])


def simulate_entropy_with_debt(N=500, M=5e5, steps=2000, md=800, transaction_type='constant', bins=500, max_money=5000):
    """
    Simulate the evolution of entropy with a maximum debt limit (md).
    
    Parameters:
    N : int
        Number of agents.
    M : float
        Total money in the system.
    steps : int
        Number of time steps.
    md : float
        Maximum debt allowed.
    transaction_type : str
        Type of transaction ('constant', 'fraction_pair', 'fraction_system').
    bins : int
        Number of bins for the histogram.
    max_money : int
        Range for the histogram to compute the distribution.
        
    Returns:
    time : np.ndarray
        Time steps array.
    S_values : list
        Entropy values at each time step.
    """
    # Initialize agents with equal distribution of money
    agents = np.ones(N) * M / N

    # Compute initial entropy
    hist, _ = np.histogram(agents, bins=bins, range=(-md, max_money), density=True)
    S_values = [-np.sum(hist[hist > 0] * np.log(hist[hist > 0]))]

    # Simulation loop
    for t in range(1, steps + 1):
        # Select two random agents
        i, j = np.random.choice(N, 2, replace=False)
        
        # Determine transaction amount based on type
        if transaction_type == 'constant':
            delta = 1
        elif transaction_type == 'fraction_pair':
            mean_pair = (agents[i] + agents[j]) / 2
            delta = np.random.rand() * mean_pair
        elif transaction_type == 'fraction_system':
            mean_system = np.mean(agents)
            delta = np.random.rand() * mean_system
        else:
            raise ValueError("Invalid transaction type.")

        # Perform the transaction, allowing debt up to -md
        if agents[i] - delta >= -md:
            agents[i] -= delta
            agents[j] += delta
        
        # Compute entropy at each step
        hist, _ = np.histogram(agents, bins=bins, range=(-md, max_money), density=True)
        S_values.append(-np.sum(hist[hist > 0] * np.log(hist[hist > 0])))

    time = np.arange(0, steps + 1)
    return time, S_values


def simulate_proportional_money_transfer(
    N=500,
    M=5e5,
    steps=4e5,
    gamma=0.1,
):
    """
    Simulate a no-debt multiplicative asset-exchange model.

    In each transaction, a payer transfers the fixed fraction
    gamma of their current money to a randomly chosen receiver.
    """
    N = int(N)
    steps = int(steps)
    gamma = float(gamma)

    if N < 2:
        raise ValueError("N must be at least 2.")
    if M < 0:
        raise ValueError("M must be nonnegative.")
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be between 0 and 1.")

    agents = np.full(N, M / N, dtype=float)

    for _ in range(steps):
        payer, receiver = np.random.choice(N, size=2, replace=False)
        delta = gamma * agents[payer]

        agents[payer] -= delta
        agents[receiver] += delta

    return agents