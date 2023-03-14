import queue
import csv

class Scientist:
  def __init__(self,name: str) -> None:
    self.name = name
    self.isVisited = False
    self.erdoNumber = -1
    self.collab_list = list()

  def __gt__(self, other):
    return isinstance(other, Scientist) and self.erdoNumber > other.erdoNumber
  def __lt__(self, other):
    return isinstance(other, Scientist) and self.erdoNumber < other.erdoNumber


class Graph:
  def __init__(self, n: int, m: int, scientist_name_list: list[str]) -> None:
    self.num_vertices = n
    self.num_edges = m
    self.vertices_list = [
      Scientist(scientist) for scientist in scientist_name_list
    ]
    self.vertices_dictionary = dict()
    for scientist in self.vertices_list:
      self.vertices_dictionary[scientist.name] = scientist
    

  def addEdge(self, name1: str, name2: str):
    try:
      scientist1 = self.vertices_dictionary[name1]
      scientist2 = self.vertices_dictionary[name2]
      scientist1: Scientist
      scientist2: Scientist
      scientist1.collab_list.append(scientist2)
      scientist2.collab_list.append(scientist1)
    except:
      print(f'one of the scientist name not found')


  def bfs(self,name: str):
    scientist_dictionary = self.vertices_dictionary
    for scientist in self.vertices_list:
      scientist.erdoNumber = -1
      scientist.isVisited = False
    
    try:
      source = scientist_dictionary[name]
      source: Scientist
      source.erdoNumber = 0
    except:
      print(f'The name {name} not found')
      return
    
    q = queue.Queue()
    q.put(source)
    while not q.qsize() == 0:
      current_scientist = q.get()
      current_scientist: Scientist
      current_scientist.isVisited = True
      for neighbour in current_scientist.collab_list:
        neighbour: Scientist
        if neighbour.isVisited == False:
          neighbour.erdoNumber = current_scientist.erdoNumber + 1
          q.put(neighbour)

  def printErdoNumber(self):
    for scientist in self.vertices_list:
      scientist: Scientist
      print(f'The erdo number of scientist {scientist.name} is {scientist.erdoNumber}')

    print()
    print()

    scientist_list = list(self.vertices_list)
    scientist_list.sort()

    erdo_number_dictionary = dict()
    for scientist in scientist_list:
      try:
        x = erdo_number_dictionary[scientist.erdoNumber]
        x: list
        x.append(scientist)
      except:
        erdo_number_dictionary[scientist.erdoNumber] = [scientist]

    for key in erdo_number_dictionary.keys():
      if key ==  -1:
        print('The scientist(s) having no erdo numbers are ')
        erdo_number_list = erdo_number_dictionary[key]
        erdo_number_list: list
        length = len(erdo_number_list)
        for i in range(length):
          scientist = erdo_number_list[i]
          if i == length - 1:
            print(scientist.name)
            print()
          else:
            print(scientist.name, end=', ')
            # print()
      
      else:
        print(f'The scientist having erdo number as {key} are')
        erdo_number_list = erdo_number_dictionary[key]
        erdo_number_list: list
        length = len(erdo_number_list)
        for i in range(length):
          scientist = erdo_number_list[i]
          scientist: Scientist
          if i == length - 1:
            print(scientist.name)
            print()
          else:
            print(scientist.name, end=', ')
            # print()
    del erdo_number_dictionary



with open('./collab.csv','r') as file:
  csvreader = csv.reader(file)
  unique_name_list = []
  file_content_list = []
  for row in csvreader:
    file_content_list.append(row)
    for name in row:
      if name not in unique_name_list:
        unique_name_list.append(name)


    
  graph = Graph(len(unique_name_list), 2*len(file_content_list), unique_name_list)
  for edge in file_content_list:
    graph.addEdge(edge[0],edge[1])
  # according to the question, we have to start with ERDOS
  graph.bfs('ERDOS')
  graph.printErdoNumber()


