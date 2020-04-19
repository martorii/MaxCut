# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OTlX00qy4Nu-waChkjOQJDcLApNe0lH6
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import time
import os
from scipy import stats

#%matplotlib notebook
# %matplotlib inline

# Max-cut functions
def InitializeGraph(n, min_weight, max_weight, dropout, seed = -1):
    # Randomness
    if seed == -1:
        W = np.random.uniform(low=min_weight, high=max_weight, size=(n,n))
    else:
        local_state = np.random.RandomState(seed)
        W = local_state.uniform(low=min_weight, high=max_weight, size=(n,n))
    # Dropout 
    if dropout>0:
        if seed == -1:
            D = np.random.choice([0,1], size=(n,n), replace=True, p=[dropout, 1-dropout])
        else:
            D = local_state.choice([0,1], size=(n,n), replace=True, p=[dropout, 1-dropout])
        W = np.multiply(W,D)
    # Copy upper diagonal to lower diagonal (only the upper perturbation counts)
    i_lower = np.tril_indices(n, -1)
    W[i_lower] = W.T[i_lower]
    # Make sure diagonal is empty
    np.fill_diagonal(W, 0)
    return W

def InitializeFlatGraph(n, min_weight, max_weight, dropout = 0, seed = -1):
    if seed == -1:
        W = np.random.uniform(low=min_weight, high=max_weight, size=n)
    else:
        local_state = np.random.RandomState(seed)
        W = local_state.uniform(low=min_weight, high=max_weight, size=n)
    if dropout>0:
        if seed == -1:
            D = np.random.choice([0,1], size=n, replace=True, p=[dropout, 1-dropout])
        else:
            D = local_state.choice([0,1], size=n, replace=True, p=[dropout, 1-dropout])
        W = np.multiply(W,D)  
    return W

def AdjacencyMatrixDegree(degseq):
    # n is number of vertices  
    n = len(degseq)
    mat = [[0] * n for i in range(n)] 
    for i in range(n): 
        for j in range(i + 1, n): 
            # For each pair of vertex decrement  
            # the degree of both vertex.  
            if (degseq[i] > 0 and degseq[j] > 0): 
                degseq[i] -= 1
                degseq[j] -= 1
                mat[i][j] = 1
                mat[j][i] = 1
    return mat

def GetKRandomPartition(n, k, seed = -1):
    partition = {}
    if seed == -1:
        for i in range(n):
            partition[i]=np.random.randint(low=0, high=k, size=1)[0]
    else:
        local_state = np.random.RandomState(seed)
        for i in range(n):
            partition[i]=local_state.randint(low=0, high=k, size=1)[0]
    return partition

def Get0Partition(n):
    partition = {}
    for i in range(n):
        partition[i]=0
    return partition

def Get1Partition(n):
    partition = {}
    for i in range(n):
        partition[i]=1
    return partition

def GetStupidPartition(n):
    partition = {}
    for i in range(n):
        partition[i]=-1
    return partition

def GetInitialPartition(n, k, initial_partition_type, seed = -1):
    if initial_partition_type == "random":
        initial_partition = GetKRandomPartition(n, k, seed)
    if initial_partition_type == "0":
        initial_partition = Get0Partition(n)
    if initial_partition_type == "1":
        initial_partition = Get1Partition(n)
    return initial_partition

def CutCost(W, partition, n, k):
    z = 0
    identity = np.identity(k)
    for i in range(n):
        for j in range(i, n):
            new_edge = (1-identity[partition[i], partition[j]])*W[i,j]
            z += new_edge
    return z
        
def CutGainAfterFlip(W, initial_partition, final_partition, n):
    # Vi: initial partition of the vertex v
    # Vj: final partition of the vertex v
    # z: current cut
    weights_to_add = 0
    weights_to_substract = 0
    
    diff_partition = {key: initial_partition[key] - final_partition.get(key, 0) for key in initial_partition}
    
    # v: vertex that flipped
    v = [key for key, val in diff_partition.items() if val!=0][0]
    v_old_partition = initial_partition[v]
    v_new_partition = final_partition[v]
    
    # Vertices belonging to the old group and the new group
    vertices_in_old_partition = [key  for (key, value) in initial_partition.items() if value == v_old_partition]
    vertices_in_new_partition = [key  for (key, value) in initial_partition.items() if value == v_new_partition]

    for vi in vertices_in_old_partition:
        if vi == v:
            continue
        else:
            weights_to_add += W[v, vi]
    for vj in vertices_in_new_partition:
        weights_to_substract += W[v, vj]
    z = weights_to_add - weights_to_substract
    return z

def DeleteTempResults(filename):
    if os.path.exists(filename):
        os.remove(filename)
    return
            
def SolveMaxCut(W, n, k, z, initial_partition, heuristic, seed = -1):
    tol = 1e-5
    maxIter = 100000
    it = 0
    
    zt1 = -10000
    zt2 = CutCost(W, initial_partition, n, k)
    
    # In case the cut is already optimal
    new_z = zt2
    
    # Store old and new partition
    old_partition = GetStupidPartition(n)
    new_partition = initial_partition
    
    start = time.time()
    if heuristic == "GBF":
        # Greedy Best Flip
        while(old_partition!=new_partition and it<maxIter):
            old_partition = new_partition
            new_partition, new_z = GreedyBestFlip(W, new_partition, n, k, zt2)
            zt1 = zt2
            zt2 = new_z
            it = it + 1
    elif heuristic == "RPF":
        # First Best Flip
         while(old_partition!=new_partition and it<maxIter):
            old_partition = new_partition
            new_partition, new_z = RandomPositiveFlip(W, new_partition, n, k, zt2, seed)
            zt1 = zt2
            zt2 = new_z
            it = it + 1
    elif heuristic == "WF":
        # Worst Flip
         while(old_partition!=new_partition and it<maxIter):
            old_partition = new_partition
            new_partition, new_z = WorstFlip(W, new_partition, n, k, zt2)
            zt1 = zt2
            zt2 = new_z
            it = it + 1
    elif heuristic == "FNF":
        # First Next Flip
        # Only for testing purposes
        iters_fnf = 3
        for i in range(iters_fnf):
            partition, new_z = FirstNextFlip(W, partition, n, k, zt2)
            zt1 = zt2
            zt2 = new_z
            it = it + 1
            
    end = time.time()
    elapsed_time = np.round(end - start, 4)
    # The last step would return the same partition, so it-1
    return new_partition, new_z, elapsed_time, it-1

def SymmetricMatrix(W):
    m = len(W)
    n = int((1+np.sqrt(1+4*2*m))/2)
    A = np.zeros(shape=(n, n))
    # k runs along W
    k = 0
    # Fill upper diagonal
    for i in range(n-1):
        for j in range(i+1, n):
            A[i,j]=W[k]
            k+=1
    # Fill lower diagonal
    i_lower = np.tril_indices(n, -1)
    A[i_lower] = A.T[i_lower]
    return A

def NumpyToCsv(array, filename):
    np.savetxt(str(filename) + ".csv", array, delimiter=";")

def CsvToNumpy(filename):
    return np.genfromtxt(str(filename) + ".csv", delimiter=";")

# Meshgrid - No need to parallelize
def MeshGrid3dMaxCut(k, min_weight, max_weight, initial_partition_type, n_points_ax, n_iters, complexity, heuristic, sigma):
    weights_size = 3
    x = np.zeros(shape=(np.power(n_points_ax+1, 3), weights_size))
    f = np.zeros(np.power(n_points_ax+1, 3))
    # p runs over all points
    p = 0
    for i in range(n_points_ax+1):
        x_val = min_weight + (max_weight-min_weight)*i/n_points_ax
        for j in range(n_points_ax+1):
            y_val = min_weight + (max_weight-min_weight)*j/n_points_ax
            for l in range(n_points_ax+1):
                z_val = min_weight + (max_weight-min_weight)*l/n_points_ax
                w_flat = [x_val, y_val, z_val]
                w = SymmetricMatrix(w_flat)
                steps = np.zeros(n_iters)
                for it in range(n_iters):
                    initial_partition = GetInitialPartition(3, k, initial_partition_type)
                    initial_z = CutCost(w, initial_partition, 3, k)
                    if complexity == "average":
                        _p, _z, _t, steps[it] = SolveMaxCut(w, 3, k, initial_z, initial_partition, heuristic)
                    elif complexity == "smoothed":
                        # n_iters is also used for n_perturbations
                        steps[it] = SmoothedComplexity(w_flat, 3, k, initial_partition_type, 0, n_iters, heuristic, sigma)
                f[p] = np.mean(steps)
                x[p] = [x_val, y_val, z_val]
                p+=1
    return x, f

def PlotMeshGrid3d(x, f, title, colorsMap='jet'):
    cm = plt.get_cmap(colorsMap)
    cNorm = matcolors.Normalize(vmin=min(f), vmax=max(f))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x[:,0], x[:,1], x[:,2], c=scalarMap.to_rgba(f))
    plt.xticks(np.arange(min(x[:,0]), max(x[:,0])+1, 0.5))
    plt.yticks(np.arange(min(x[:,1]), max(x[:,1])+1, 0.5))
    scalarMap.set_array(f)
    fig.colorbar(scalarMap)
    if title:
        plt.title(title)
    plt.show()

# Plot results
def PlotGraph(G, partition = None):
    G = nx.from_numpy_matrix(np.round(G, 3))
    pos = nx.spring_layout(G)
    # Draw the graph according to node positions
    if partition is not None:
        colors= np.fromiter(partition.values(), dtype=int)+1
        nx.draw(G, pos, with_labels=True, node_color=colors)
    else:
        nx.draw(G, pos, with_labels=True)
    # Create edge labels
    labels = nx.get_edge_attributes(G, 'weight')

    # Draw edge labels according to node positions
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()
    return

def PlotRegressionResults(nodes, steps_mean, steps_sd, with_errorbars, r_var, r_var_label, method):
    
    # Convert X axis according to method
    x = nodes
    if method=="polynomial":
        x = np.log(x.reshape(-1, 1))
    if method == "quasipolynomial":
        x = np.log(x.reshape(-1, 1))*x.reshape(-1, 1)

    # t runs over all columns of steps_mean
    t=0
    slopes=[]
    intercepts=[]
    r_values=[]
    p_values=[]
    std_errs=[]

    # Create a new plot
    plt.figure(np.random.randint(501, 1000))
    
    for r_v in r_var:
        # Convert Y axis according to method
        y = steps_mean[:,t]
        if (method=="polynomial") or (method=="exponential") or (method=="quasipolynomial"):
            y = np.log(y)
        plt.scatter(x, y)
        if with_errorbars:
            y_sd = steps_sd[:, t]
            plt.errorbar(x,y,yerr=y_sd, linestyle="None")

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.mstats.linregress(x,y)

        # Store results
        slopes.append(slope)
        intercepts.append(intercept)
        r_values.append(r_value)
        p_values.append(p_value)
        std_errs.append(std_err)

        # Linear regression prediction
        y_reg = intercept + slope*x
        plt.plot(x, y_reg, label=str(r_var_label) + '=' + str(r_v))
        t+=1

    if method=="polynomial":
        plt.title('Polynomial behavior')     
        plt.xlabel('ln(Nodes)') 
        plt.ylabel('ln(Steps)')
    
    if method=="exponential":
        plt.title('Exponential behavior')     
        plt.xlabel('Nodes') 
        plt.ylabel('ln(Steps)')
        
    if method=="quasipolynomial":
        plt.title('Quasiplynomial behavior')     
        plt.xlabel('ln(Nodes)*Nodes') 
        plt.ylabel('ln(Steps)')
    
    plt.legend()        
    plt.show()

    # Print table
    print("Regression results:\n")
    print(tabulate(list(zip(*[r_var, slopes, intercepts, r_values])), headers=[r_var_label, 'slope', 'intercept', 'r_value'], floatfmt=".3f"))
    
    return slopes, intercepts
    
def PlotResults(nodes, steps_mean, steps_sd, with_errorbars, r_var, r_var_label, xlabel = "Nodes", ylabel = "Steps"):
    #r_var is running variable
    
    # Show results for each r_var
    x = nodes.reshape(-1, 1)

    # Legend
    r_var_labels=[]

    # t runs over all columns of steps_mean
    t=0

    # Create a new plot
    plt.figure(np.random.randint(0, 500))
    
    for r_v in r_var:
        run_steps = steps_mean[:,t]
        plt.scatter(x, run_steps)
        if with_errorbars:
            run_steps_sd = steps_sd[:, t]
            plt.errorbar(x,run_steps,yerr=run_steps_sd, linestyle="None")
        r_var_labels.append(str(r_var_label) + "=" + str(r_v))
        t+=1

    plt.title(str(xlabel) + " vs. " + str(ylabel)) 
    plt.xlabel(xlabel) 
    plt.ylabel(ylabel)
    plt.legend(r_var_labels)
    plt.show()
    
def PlotResultsSmoothed(nodes, steps_mean, steps_sd, with_errorbars, r_var, r_var_label, sigma, withUpperBound):
    #r_var is running variable
    
    # Show results for each r_var
    x = nodes.reshape(-1, 1)

    # Legend
    r_var_labels=[]

    # t runs over all columns of steps_mean
    t=0
    
    # Create a new plot
    plt.figure(np.random.randint(1001, 1500))

    for r_v in r_var:
        run_steps = steps_mean[:,t]
        plt.scatter(x, run_steps)
        if with_errorbars:
            run_steps_sd = steps_sd[:, t]
            plt.errorbar(x,run_steps,yerr=run_steps_sd, linestyle="None")
        r_var_labels.append(str(r_var_label) + "=" + str(r_v))
        t+=1
    # Assume gaussian
    if withUpperBound:
        phi = 1/np.sqrt(2*np.pi*sigma*sigma)
        upper_bound = phi*np.power(nodes, 7.83)
        plt.plot(nodes, upper_bound, color='red', linewidth=1.0, linestyle='--')
    plt.title('Steps vs. Nodes') 
    plt.xlabel('Nodes') 
    plt.ylabel('Steps')
    plt.legend(r_var_labels)
    plt.show()
    return

def GreedyBestFlip(W, partition, n, k, z):
    cut_costs = []
    partitions_flip = []
    # Permutate vertices so that we do not always start by the same one
    order = np.random.permutation(range(n))
    for i in order:
        for j in range(1, k):            
            new_partition = partition.copy()
            new_partition[i] = (new_partition[i]+j)%k
            partitions_flip.append(new_partition)
            cut_costs.append(CutGainAfterFlip(W, partition, new_partition, n))
      
    # Convert the list to a numpy array
    cut_costs = np.asarray(cut_costs)
    if np.any(cut_costs[cut_costs>0]):
        # New best partition was found
        best_index = np.argmax(cut_costs)
        best_partition = partitions_flip[best_index]
        new_cut_cost = z + cut_costs[best_index]
        return best_partition, new_cut_cost
    else:
        # We are in a local optimum
        return partition, z
    
def RandomPositiveFlip(W, partition, n, k, z, seed = -1):
    # Permutate vertices so that we do not always start by the same one
    # Randomness
    if seed == -1:
        order = np.random.permutation(range(n))
    else:
        local_state = np.random.RandomState(seed)
        order = local_state.permutation(range(n))
    for i in order:
        for j in range(1, k):            
            new_partition = partition.copy()
            new_partition[i] = (new_partition[i]+j)%k
            new_z = CutGainAfterFlip(W, partition, new_partition, n)
            if new_z > 0:
                return new_partition, z + new_z
      
    return partition, z

def WorstFlip(W, partition, n, k, z):
    cut_costs = []
    partitions_flip = []
    # Permutate vertices so that we do not always start by the same one
    order = np.random.permutation(range(n))
    for i in order:
        for j in range(1, k):            
            new_partition = partition.copy()
            new_partition[i] = (new_partition[i]+j)%k
            partitions_flip.append(new_partition)
            cut_costs.append(CutGainAfterFlip(W, partition, new_partition, n))
      
    # Convert the list to a numpy array
    cut_costs = np.asarray(cut_costs)
    
    if np.any(cut_costs[cut_costs>0]):
        # A better partition was found
        min_val = min(c for c in cut_costs if c > 0)
        worst_index = np.argwhere(cut_costs==min_val)[0][0]
        worst_partition = partitions_flip[worst_index]
        new_cut_cost = z + cut_costs[worst_index]
        return worst_partition, new_cut_cost
    else:
        # We are in a local optimum
        return partition, z

def RunGridMaxCutAverageK(min_nodes, max_nodes, step_nodes, initial_partition_type, dropout, ks, min_weight, max_weight, iters_for_nk, heuristic, storeCSV=False):

    # Create nodes grid
    # nodes = np.linspace(min_nodes, max_nodes, num=step_nodes, dtype=int)
    nodes = np.logspace(np.log(min_nodes), np.log(max_nodes), num=step_nodes, base=np.exp(1))
    # Remove decimal part
    nodes = np.floor(nodes)
    # Convert to integer
    nodes = nodes.astype(int)

    steps_mean = np.zeros((len(nodes), len(ks)))
    steps_sd = np.zeros((len(nodes), len(ks)))
    
    # Save nodes
    if storeCSV:
        NumpyToCsv(nodes, "nodes")
    
    i = 0
    j = 0

    for ni in nodes:
        weights_size = int(ni*(ni-1)/2)
        for ki in ks:
            steps = np.zeros(iters_for_nk)
            for it in range(iters_for_nk):
                # Create graph and initial partition
                W_k_it = InitializeFlatGraph(weights_size, min_weight, max_weight, dropout)
                W_k_it = SymmetricMatrix(W_k_it)
                initial_partition = GetInitialPartition(ni, ki, initial_partition_type)
                # Get initial cost value
                initial_z = CutCost(W_k_it, initial_partition, ni, ki)
                # Get next local maximum
                partition, z, elapsed_time, n_steps = SolveMaxCut(W_k_it, ni, ki, initial_z, initial_partition, heuristic)
                # Save results for each iteration
                steps[it]=n_steps
             
            # Save results for a i,j combination    
            steps_mean[i,j] = np.mean(steps)
            steps_sd[i,j] = np.std(steps)/np.sqrt(iters_for_nk)
            if storeCSV:
                DeleteTempResults("average_complexities.csv")
                NumpyToCsv(steps_mean, "average_complexities")
                DeleteTempResults("average_complexities_sd.csv")
                NumpyToCsv(steps_sd, "average_complexities_sd")
            j = j + 1
        j = 0
        i = i + 1
    return steps_mean, steps_sd, nodes

## Define grid parameters
# Nodes
min_nodes = 5
max_nodes = 2000
num_nodes = 40

min_weight = -1
max_weight = 1

# Dropout assumed to be 0
dropout = 0

# K-cuts
ks=[2]

# Number of instances for each combination
iters_for_nk=1000

# Method
heuristic = "RPF"

# Initial partition
initial_partition_type = "0"

nodes, average_complexities, average_complexities_sd = RunGridMaxCutAverageK(min_nodes, max_nodes, num_nodes, initial_partition_type, dropout, ks, min_weight, max_weight, iters_for_nk, heuristic, True)

NumpyToCsv(nodes, "nodes")
NumpyToCsv(average_complexities, "average_complexities")
NumpyToCsv(average_complexities_sd, "average_complexities_sd")
