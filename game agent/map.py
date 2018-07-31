import math
class Node():
    def __init__(self,North = None,East=None, West = None, South =None,location = None,material=None):
        self.North=North
        self.East=East
        self.West=West
        self.South=South
        self.location=location
        self.material = material
        self.North_weight =math.inf
        self.East_weight =math.inf
        self.West_weight =math.inf
        self.South_weight =math.inf
        self.visited = False

    ###########################
    #     getter and setter   #
    ###########################
    def get_visited(self):
        return self.visited
    def set_visited(self,Key):
        self.visited=Key

    def set_North(self,North):
        self.North=North
    def set_East(self,East):
        self.East=East
    def set_West(self,West):
        self.West=West
    def set_South(self,South):
        self.South=South
    def get_North(self):
        return self.North
    def get_East(self):
        return self.East
    def get_West(self):
        return self.West
    def get_South(self):
        return self.South

    def set_location(self,location):
        self.location=location
    def get_location(self):
        return self.location
    def get_material (self):
        return self.material
    def set_material (self,material):
        self.material = material

    def set_North_weight(self,weight):
        self.North_weight=weight
    def set_East_weight(self,weight):
        self.East_weight=weight
    def set_West_weight(self,weight):
        self.West_weight=weight
    def set_South_weight(self,weight):
        self.South_weight=weight

    def get_North_weight(self):
        return self.North_weight
    def get_East_weight(self):
        return self.East_weight
    def get_West_weight(self):
        return self.West_weight
    def get_South_weight(self):
        return self.South_weight

class map():
    def __init__(self):
        self.graph=[]
        for i in range (160):
            temp = []
            for j in range (160):
                temp.append(Node())
            self.graph.append(temp)
        for i in range(160):
            for j in range(160):
                if i>0:
                    self.graph[i][j].set_North(self.graph[i-1][j])
                if i<159:
                    self.graph[i][j].set_South(self.graph[i+1][j])
                if j >0:
                    self.graph[i][j].set_West(self.graph[i][j-1])
                if j<159:
                    self.graph[i][j].set_East(self.graph[i][j+1])
                self.graph[i][j].set_location((i,j))
                # if i > 77 and i<83 and j>77 and j<77:
                #     if view[i][j] =='^' or view[i][j] =='<' or view[i][j] =='>' or view[i][j] =='v':
                #         Graph[i][j].set_material(' ')
                #     else:
                #         Graph[i][j].set_material(view[i][j])

    def refrsh_map(self,view,face,pos,action=None):
        Graph = self.graph
        if action == None:
            for i in range(5):
                for j in range(5):
                    if view[i][j] =='^' or view[i][j] =='<' or view[i][j] =='>' or view[i][j] =='v':
                        Graph[i+78][j+78].set_material(' ')
                    else:
                        Graph[i+78][j+78].set_material(view[i][j])

            for i in range(5):
                for j in range(5):
                    if Graph[i+78][j+78].North.get_material() == 'T' or Graph[i+78][j+78].North.get_material() == '-' :
                        Graph[i+78][j+78].set_North_weight(6401)
                    elif Graph[i+78][j+78].North.get_material() == '~':
                        Graph[i+78][j+78].set_North_weight(6500)
                    elif Graph[i+78][j+78].North.get_material()=='*' or Graph[i+78][j+78].North.get_material()==None or Graph[i+78][j+78].North.get_material()=='.':
                        Graph[i+78][j+78].set_North_weight(math.inf)
                    else:
                        Graph[i+78][j+78].set_North_weight(1)

                    if Graph[i+78][j+78].East.get_material() == 'T' or Graph[i+78][j+78].East.get_material() == '-' :
                        Graph[i+78][j+78].set_East_weight(6401)
                    elif  Graph[i+78][j+78].East.get_material() == '~':
                        Graph[i+78][j+78].set_East_weight(6500)
                    elif Graph[i+78][j+78].East.get_material()=='*' or Graph[i+78][j+78].East.get_material()==None or Graph[i+78][j+78].East.get_material()=='.':
                        Graph[i+78][j+78].set_East_weight(math.inf)
                    else:
                        Graph[i+78][j+78].set_East_weight(1)

                    if Graph[i+78][j+78].West.get_material() == 'T' or Graph[i+78][j+78].West.get_material() == '-' :
                        Graph[i+78][j+78].set_West_weight(6401)
                    elif  Graph[i+78][j+78].West.get_material() == '~':
                        Graph[i+78][j+78].set_West_weight(6500)
                    elif Graph[i+78][j+78].West.get_material()=='*' or Graph[i+78][j+78].West.get_material()==None or Graph[i+78][j+78].West.get_material()=='.':
                        Graph[i+78][j+78].set_West_weight(math.inf)
                    else:
                        Graph[i+78][j+78].set_West_weight(1)

                    if Graph[i+78][j+78].South.get_material() == 'T' or Graph[i+78][j+78].South.get_material() == '-' :
                        Graph[i+78][j+78].set_South_weight(6401)
                    elif  Graph[i+78][j+78].South.get_material() == '~':
                        Graph[i+78][j+78].set_South_weight(6500)
                    elif Graph[i+78][j+78].South.get_material()=='*' or Graph[i+78][j+78].South.get_material()==None or Graph[i+78][j+78].South.get_material()=='.':
                        Graph[i+78][j+78].set_South_weight(math.inf)
                    else:
                        Graph[i+78][j+78].set_South_weight(1)
        elif action == 'F':
            if face =='N':
                Graph[pos[0]+1][pos[1]].set_material(view[3][2])
                for i in range (5):
                    Graph[pos[0]-2][pos[1]+i-2].set_material(view[0][i])
            elif face =='E':
                Graph[pos[0]][pos[1]-1].set_material(view[2][1])
                for i in range (5):
                    Graph[pos[0]-2+i][pos[1]+2].set_material(view[i][4])
            elif face == 'W':
                Graph[pos[0]][pos[1]+1].set_material(view[2][3])
                for i in range (5):
                    Graph[pos[0]+i-2][pos[1]-2].set_material(view[i][0])
            elif face == 'S':
                Graph[pos[0]-1][pos[1]].set_material(view[1][2])
                for i in range (5):
                    Graph[pos[0]+2][pos[1]-2+i].set_material(view[4][i])
            # Graph[pos[0]][pos[1]].set_material(view[2][2])

            for i in range(160):
                for j in range(160):
                    if Graph[i][j].get_North()!=None:
                        self.weight_setter(Graph[i][j].get_North(),Graph[i][j].set_North_weight)
                    if Graph[i][j].get_West()!=None:
                        self.weight_setter(Graph[i][j].get_West(),Graph[i][j].set_West_weight)
                    if Graph[i][j].get_South()!=None:
                        self.weight_setter(Graph[i][j].get_South(),Graph[i][j].set_South_weight)
                    if Graph[i][j].get_East()!=None:
                        self.weight_setter(Graph[i][j].get_East(),Graph[i][j].set_East_weight)

    def weight_setter(self,graph_from,graph_from_weight):
        if graph_from.get_material() =='T' or graph_from.get_material() =='-':
            graph_from_weight(6401)
        elif  graph_from.get_material()== '~':
            graph_from_weight(6500)
        elif graph_from.get_material()=='*' or graph_from.get_material()==None or graph_from.get_material()=='.':
            graph_from_weight(math.inf)
        else:
            graph_from_weight(1)


    def map_printer(self):
        graph = self.graph
        for i in range(65,95):
            print_matrix=''
            for j in range(65,95):
                if graph[i][j].get_material() == None:
                    print_matrix +='N'
                else:
                    print_matrix= print_matrix+(graph[i][j].get_material())
            if len(print_matrix)>0:
                print(print_matrix)
