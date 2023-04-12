import numpy as np
import matplotlib.pyplot as plt
import random as rnd
# import pycosat 


class Kid:
  def __init__(self, i: int, height: int) -> None:
    self.kid_name = i
    self.kid_height = height


class Adult:
  def __init__(self,i: int, height: int) -> None:
    self.adult_name = i
    self.adult_height = height


height_list_in_town = [4.9,5.0,5.1,5.2,5.3,5.4,5.5, 5.6, 5.7, 5.8]
numHeights = len(height_list_in_town)
p_ht_given_kid = [0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1, 0.1]
p_ht_given_adult = [0.02, 0.02, 0.02, 0.02, 0.02, 0.18, 0.18, 0.18, 0.18, 0.18]


p_height_given_kid_dictionary = dict()
for i in range(numHeights):
  # we can access the probability of height x, given kid
  p_height_given_kid_dictionary[height_list_in_town[i]] = p_ht_given_kid[i]

p_height_given_adult_dictionary = dict()
for i in range(numHeights):
  # we can access the probability of height x, given adult
  p_height_given_adult_dictionary[height_list_in_town[i]] = p_ht_given_adult[i]


# pKid is given to be 0.4
pKid = 0.4



def simulate_people(n: int, height_list_in_town: list, p_ht_given_kid: list, p_ht_given_adult: int, pKid: float ):
  # returns kid list and adult list

  kid_list  = []
  adult_list = []
  people_name_height = []
  # list containing tuple of name and height
  for i in range(n):
    kid_or_adult = rnd.choices(['kid','adult'], weights=[pKid,1-pKid], k=1)[0]
    # print(kid_or_adult)
    if kid_or_adult == 'kid':
      height_of_kid = rnd.choices(height_list_in_town, weights=p_ht_given_kid,k=1)[0]
      kid_list.append(Kid(i, height_of_kid))
      people_name_height.append((i,height_of_kid))
    else:
      height_of_adult = rnd.choices(height_list_in_town, weights=p_ht_given_adult,k=1)[0]
      adult_list.append(Adult(i, height_of_adult))
      people_name_height.append((i,height_of_adult))
  return kid_list, adult_list, people_name_height

# kid_objects, adult_objects = simulate_people(10000, height_list_in_town, p_ht_given_kid, p_ht_given_adult)
# the above is simulated for 10000 people

total_population = 1000

kid_objects, adult_objects, people_name_height_list = simulate_people(total_population, height_list_in_town, p_ht_given_kid, p_ht_given_adult,pKid)


# dictionary which represents who is kid and who is adult
people_type = dict()
for i in range(total_population):
  people_type[i] = ''
for kid in kid_objects:
  kid: Kid
  people_type[kid.kid_name] = 'kid'
for adult in adult_objects:
  adult: Adult
  people_type[adult.adult_name] = 'adult'





# height_freq_dictionary = dict()
# for height in height_list_in_town:
#   height_freq_dictionary[height] = [0,0]
# for kid in kid_objects:
#   kid: Kid
#   height_freq_dictionary[kid.kid_height][0]+=1
# for adult in adult_objects:
#   adult: Adult
#   height_freq_dictionary[adult.adult_height][1]+=1



# 2a

kid_heights = [isinstance(kid,Kid) and kid.kid_height for kid in kid_objects]
adult_heights = [isinstance(adult, Adult) and adult.adult_height for adult in adult_objects]

plt.hist(
  kid_heights,
  # bins=10,
  label='kids',
  alpha = 0.5,
  # color='b'
)
plt.hist(
  adult_heights,
  # bins=10,
  label='adults',
  alpha = 0.5,
  # color='g'
)
plt.legend(loc='upper right')

plt.show()


height_sample = (kid_heights.copy()).extend(adult_heights.copy())
# sample of all heights

# 2b
class Agent:
  def __init__(self, height_list_in_town: list, p_height_given_kid_dictionary: dict, p_height_given_adult_dictionary:dict, population: int ) -> None:
    self.possible_heights = height_list_in_town.copy()
    self.pHt_kid_dictionary = p_height_given_kid_dictionary.copy()
    self.pHt_adult_dictionary = p_height_given_adult_dictionary.copy()
    self.population_in_town = population

  def apply_bayes(self, sample: list, pKid: float, heights_in_town: list, pHtKid: list, pHtAdult: list):
    p_ht_kid_dictionary = dict()
    p_ht_adult_dictionary = dict()

    # sample is a list containing tuples as element
    # each tuple is of the form (person_name, height)
    for i in range(len(heights_in_town)):
      p_ht_kid_dictionary[heights_in_town[i]] = pHtKid[i]
      p_ht_adult_dictionary[heights_in_town[i]] = pHtAdult[i]
    

    
    # given a height we want to calculate the probability of whether the person is a kid 
    p_kid_height = dict()
    # the above dictionary stores the height X as 'key' and the probability whether the person is kid as 'value'
    p_adult_height = dict()
    for height in heights_in_town:
      z = p_ht_kid_dictionary[height] * pKid
      y = p_ht_adult_dictionary[height] * (1-pKid)
      prob_kid_height = z/(z+y)
      # print(z/(z+y))
      p_kid_height[height] = prob_kid_height
      p_adult_height[height]  = 1 - prob_kid_height
    


    predictions = dict()
    for i in range(self.population_in_town):
      predictions[i] = ''
    # for sample_element in sample:
    #   # sample element is a tuple of the form (name, height)
    #   name, height_given = sample_element

      name, height_given = sample[i]

      # print(name)
      # print([p_kid_height[height_given], p_adult_height[height_given]])
      # if kid, will give true
      prediction_kid_adult = rnd.choices(
        [True,False],
        weights=[p_kid_height[height_given], p_adult_height[height_given]],
        k=1
      )[0]
      # print(prediction_kid_adult)
      # print(name, height_given)

      # now we will store the prediction
      predictions[i] = 'kid' if prediction_kid_adult else 'adult'
    
    # now we will return this predictions dictionary
    return predictions
    

agent = Agent(height_list_in_town,p_height_given_kid_dictionary,p_height_given_adult_dictionary, total_population )
prediction_dictionary = agent.apply_bayes(people_name_height_list, pKid, height_list_in_town, p_ht_given_kid,p_ht_given_adult)

# actual information is stored in the dictionary named 'people_type'
correct_prediction = 0
total_count = total_population


for i in range(total_population):
  if prediction_dictionary[i] == people_type[i]:
    correct_prediction += 1


print(f'the number of correct predictions is {correct_prediction}')
print(f'The accuracy of the agent is {correct_prediction/total_count}')






