import random
from itertools import combinations
m =30
n =128

def get_profile(n, m):
  profile= []
  ballot = list(range(m))
  for i in range(n):
    c_ballot= ballot.copy()
    random.shuffle(c_ballot)
    profile.append(c_ballot)
  return(profile)

def get_cWinnerPlurality(profile):
  counts=[]
  winner=0
  for count in range(m):
    counts.append(0)
  for ballot in profile:
    counts[ballot[0]]+=1
  max_score=counts[0]
  for a in range(1,len(counts)):
    if max_score < counts[a]:
      max_score=counts[a]
  for a in range(1, len(counts)-2):
    if max_score==counts[a]:
      return 0,0
  winner= counts.index(max_score)
  print("Plurality Winner is "+ str(winner))
  return 1, winner

def get_cWinnerCopeland(profile):
  counts=[]
  winner= 0
  m=len(profile[0])
  for count in range(m):
    counts.append(0)

  for comb in combinations(range(m), 2):
    counta=0
    countb=0
    for ballot in profile:
      if (ballot.index(comb[0])<ballot.index(comb[1])):
        counta+=1
      else:
        countb+=1
    if (counta > countb):
      counts[comb[0]]+=1
    else:
      counts[comb[1]]+=1
  max_score=max(counts)
  if max_score == m-1:
    winner= counts.index(max_score)
    print("Copeland Winner is " +str(winner))
    return 1, winner
  else: 
    return 0, 0
  

def get_cWinnerBorda(profile):
  counts=[]
  winner= 0
  for count in range(m):
    counts.append(0)

  for ballot in profile:
    for i in range(len(ballot)):
      counts[ballot[i]]+= m-1-i
  max_score=counts[0]

  for a in range(1,len(counts)):
    if max_score < counts[a]:
      max_score=counts[a] 
  for a in range(1, len(counts)-2):
    if max_score==counts[a]:
      return 0,0
  winner= counts.index(max_score)
  print("Borda Winner is " +str(winner))
  return 1, winner



def run_all():
  counts_plur=[]
  counts_copeland=[]
  counts_borda=[]
  count_same_condorcet= 0
  plurality_borda_samewinner =0
  plurality_copeland_samewinner = 0
  copeland_borda_samewinner=0
  total = 1000
  percentage_plurality =0
  percentage_copeland=0
  percentage_borda=0

  for i in range(total):
    profile= get_profile(n,m)
    winnerp, numberp=get_cWinnerPlurality(profile)
    winnerc, numberc=get_cWinnerCopeland(profile)
    winnerb, numberb = get_cWinnerBorda(profile)
    counts_plur.append(winnerp)
    counts_copeland.append(winnerc)
    counts_borda.append(winnerb)
    
    
    if(winnerp==winnerb):
      plurality_borda_samewinner+=1
    if(winnerp==winnerc):
      plurality_copeland_samewinner+=1
    if(winnerc==winnerb):
      copeland_borda_samewinner+=1
    if(winnerb==winnerc==winnerp):
      count_same_condorcet+=1

  for i in counts_plur:
    if (i==1):
      percentage_plurality+=1
  for j in counts_copeland:
    if(j==1):
      percentage_copeland+=1
  for l in counts_borda:
    if(l==1):
      percentage_borda+=1
  print ("Plurality percentage is "+ str(percentage_plurality/total))
  print("Copeland percentage is "+ str(percentage_copeland/total))
  print("Borda percentage is " + str(percentage_borda/total))
  print("Plurality and Borda chose the same Condorcet winner " + str(plurality_borda_samewinner/total))
  print("Plurality and Copeland chose the same Condorcet winner " + str(plurality_copeland_samewinner/total))
  print("Copeland and Borda chose the same Condorcet winner" + str(copeland_borda_samewinner/total))
  print("All functions choose the same Condorcet winner "+ str(count_same_condorcet/total))
  
def main():
  run_all()
main()