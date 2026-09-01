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
