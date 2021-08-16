# project3.py
# I would like you to:
# 1. Adapt this code to implement k-Approval.
# 2. Implement the Greedy Approximation to Chamberlin-Courant rule.
# 3. Run about 10 simulations each of these three, to get 
#       a feel for what they output.
# 4. For each of the three rules, run new simulations until you 
#       get an image that you believe is representative.
# 5. Save the images you selected, and caption them. 
#   Describe your findings, and comment on whether the results 
#   match the claimed goals of the rules. 

import numpy as np
import matplotlib.pyplot as plt

def euclid2d(x1, y1, x2, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def get_2d_gaussian_points(N):
    x = np.random.normal(loc=0.0, scale=1.0, size=N)
    y = np.random.normal(loc=0.0, scale=1.0, size=N)
    return x, y

def get_2d_gaussian_mixture_points(N):
    offset = 1.0
    stdev = 0.7

    x1 = np.random.normal(loc=-1*offset, scale=stdev, size=int(np.ceil(N/2)))
    y1 = np.random.normal(loc=-1*offset, scale=stdev, size=int(np.ceil(N/2)))

    x2 = np.random.normal(loc=offset, scale=stdev, size=int(np.floor(N/2)))
    y2 = np.random.normal(loc=offset, scale=stdev, size=int(np.floor(N/2)))

    x1.shape = (-1, 1)
    x2.shape = (-1, 1)

    y1.shape = (-1, 1)
    y2.shape = (-1, 1)

    x = np.vstack((x1, x2))
    y = np.vstack((y1, y2))

    return x, y

def k_borda_winners(x_cand, y_cand, x_vote, y_vote, k):
    '''
    Returns x_win, y_win; two parallel numpy arrays
    containing the coordinates of the candidates with 
    the top Borda scores.
    '''
    assert (len(x_cand) == len(y_cand) and len(x_vote) == len(y_vote))

    cand_scores = np.zeros_like(x_cand)
    # og_indicies = np.arange(0, len(x_cand))
    # og_indicies.shape = (-1,1)

    for i in range(len(x_vote)):
        distances = np.zeros_like(x_cand)
        distances.shape = (-1,1)
        for j in range(len(x_cand)):
            # Compute distances
            distances[j] = euclid2d(x_vote[i], y_vote[i], x_cand[j], y_cand[j])
            # sortable = np.hstack((og_indicies, distances))

        # Sort into preference order
        sorted_indicies = distances.argsort(axis=0) # This should be the same as sortable[:,0]
    
        # Assign points
        for l in range(len(cand_scores)):
            # Borda:
            cand_scores[sorted_indicies[l]] += len(cand_scores) - l - 1

    # Compute permutation that would sort cand_scores into ascending order,
    # but only select the last k elements of it. This returns the indicies 
    # of the k candidates with the highest borda scores.
    sorted_permutation = cand_scores.argsort()[:len(x_cand)-k-1:-1]

    # Extract those candidates using their indices.
    x_win = x_cand[sorted_permutation]
    y_win = y_cand[sorted_permutation]

    return x_win, y_win

def k_approval_winners(x_cand, y_cand, x_vote, y_vote, k):
    '''
    Returns x_win, y_win for k_approval
    '''
    assert (len(x_cand) == len(y_cand) and len(x_vote) == len(y_vote))

    cand_scores = np.zeros_like(x_cand)
    # og_indicies = np.arange(0, len(x_cand))
    # og_indicies.shape = (-1,1)

    for i in range(len(x_vote)):
        distances = np.zeros_like(x_cand)
        distances.shape = (-1,1)
        for j in range(len(x_cand)):
            # Compute distances
            distances[j] = euclid2d(x_vote[i], y_vote[i], x_cand[j], y_cand[j])
            # sortable = np.hstack((og_indicies, distances))

        # Sort into preference order
        sorted_indicies = distances.argsort(axis=0) # This should be the same as sortable[:,0]
    
        # Assign points
        for l in range(len(cand_scores)):
            # Borda:
            cand_scores[sorted_indicies[l]] += 1

    # Compute permutation that would sort cand_scores into ascending order,
    # but only select the last k elements of it. This returns the indicies 
    # of the k candidates with the highest borda scores.
    sorted_permutation = cand_scores.argsort()[:len(x_cand)-k-1:-1]

    # Extract those candidates using their indices.
    x_win = x_cand[sorted_permutation]
    y_win = y_cand[sorted_permutation]

    return x_win, y_win

def marginal_borda_scores(x_cand, y_cand, x_vote, y_vote, committee_indicies):
  assert (len(x_cand) == len(y_cand) and len(x_vote) == len(y_vote))
  marginals=np.zeros_like(x_cand)

  for i in range(len(x_vote)):
    distances = np.zeros_like(x_cand)
    for j in range(len(x_cand)):
      distances[j] = euclid2d(x_vote[i], y_vote[i], x_cand[j], y_cand[j])

    preference_order = distances.argsort()

    #find most preferred for i
    most_pref= len(x_cand)
    for committee_member in committee_indicies:
      position = np.where(preference_order == committee_member)[0][0]
      if position< most_pref:
        most_pref=position
    
    for p in range(1, most_pref+1):
      marginals[preference_order[most_pref-p]] += p
    
  return marginals
            

def greedy_CC(x_cand, y_cand, x_vote, y_vote, k):
    committee_indicies = []
    for i in range(k):  # For each seat on the committee
        marginals = marginal_borda_scores(x_vote, y_vote, x_cand, y_cand, committee_indicies)
        committee_indicies.append(np.argmax(marginals))

    x_win = x_vote[committee_indicies]
    y_win = y_vote[committee_indicies]

    return x_win, y_win


def main():      
    num_votes = 1000
    x_votes, y_votes = get_2d_gaussian_points(num_votes)
    #x_votes, y_votes = get_2d_gaussian_mixture_points(num_votes)

    num_cands = int(num_votes/10)
    x_cands, y_cands = get_2d_gaussian_points(num_cands)
    #x_cands, y_cands = get_2d_gaussian_mixture_points(num_cands)

    committee_size = 7
    
    # Compute borda winners:
    x_win, y_win = k_borda_winners(x_cands, y_cands, x_votes, y_votes, committee_size)
    x_win.shape = (-1, 1)
    y_win.shape = (-1, 1)

    # Plot setup
    fig = plt.figure()
    ax = fig.gca()  # Literally: get current axes
    sdvs = 3        # How many standard deviations in plot, larger "zooms out"
    ax.set_title('2D Gaussian Mixture')
    ax.set_xlim(left=-1*sdvs, right=sdvs)
    ax.set_ylim(bottom=-1*sdvs, top=sdvs)

    # Add voters to plot.
    plt.scatter(x_votes, y_votes, s=3, color='blue') # larger s increases point size

    # Add candidates to plot.
    plt.scatter(x_cands, y_cands, s=7, color='red') 

    # Add winners to plot.
    plt.scatter(x_win, y_win, s=128, color='green', marker='o')

    plt.show()

    # Compute k_approval winners:
    x_win, y_win = k_approval_winners(x_cands, y_cands, x_votes, y_votes, committee_size)
    x_win.shape = (-1, 1)
    y_win.shape = (-1, 1)

    # Plot setup
    fig = plt.figure()
    ax = fig.gca()  # Literally: get current axes
    sdvs = 3        # How many standard deviations in plot, larger "zooms out"
    ax.set_title('2D Gaussian Mixture')
    ax.set_xlim(left=-1*sdvs, right=sdvs)
    ax.set_ylim(bottom=-1*sdvs, top=sdvs)

    # Add voters to plot.
    plt.scatter(x_votes, y_votes, s=3, color='blue') # larger s increases point size

    # Add candidates to plot.
    plt.scatter(x_cands, y_cands, s=7, color='red') 

    # Add winners to plot.
    plt.scatter(x_win, y_win, s=128, color='green', marker='o')

    plt.show()

    # Compute greedy_cc:
    x_win, y_win = greedy_CC(x_cands, y_cands, x_votes, y_votes, committee_size)
    x_win.shape = (-1, 1)
    y_win.shape = (-1, 1)

    # Plot setup
    fig = plt.figure()
    ax = fig.gca()  # Literally: get current axes
    sdvs = 3        # How many standard deviations in plot, larger "zooms out"
    ax.set_title('2D Gaussian Mixture')
    ax.set_xlim(left=-1*sdvs, right=sdvs)
    ax.set_ylim(bottom=-1*sdvs, top=sdvs)

    # Add voters to plot.
    plt.scatter(x_votes, y_votes, s=3, color='blue') # larger s increases point size

    # Add candidates to plot.
    plt.scatter(x_cands, y_cands, s=7, color='red') 

    # Add winners to plot.
    plt.scatter(x_win, y_win, s=128, color='green', marker='o')

    plt.show()
    

main()