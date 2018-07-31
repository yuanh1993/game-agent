from map import *
from game import *
import time, math
import copy
class Strategy():
    def __init__(self):
        self.decision = "traversal"
        self.return_back=[]
        self.facing=''
        self.step_path =[]
        self.step=None
        self.on_water = False
        self.target = 'treasure'
        self.step_do=''

    def play(self,gamer,graph):
        #time.sleep(0.5)
        node = graph.graph[gamer.position[0]][gamer.position[1]]
        if self.decision == "water_traversal":
            return self.water_traversal(node,gamer)
        if self.decision == "traversal":
            if self.target =='back':
                self.decision = "Count"
            else:
                return self.traversal(node,gamer)
        if self.decision == "Count":
            print('I have Treasure ', gamer.have_treasure)
            if gamer.have_treasure == True :
                self.target = 'back'
            self.return_back=[]
            gamer.tree=[]
            gamer.stones=[]
            gamer.door=[]
            gamer.axe=[]
            for i in range(160):
                for j in range(160):
                    if graph.graph[i][j].get_material() =='T':
                        if (i,j) not in gamer.tree:
                            gamer.tree.append((i,j))
                    elif graph.graph[i][j].get_material() =='o':
                        if (i,j) not in gamer.stones:
                            gamer.stones.append((i,j))
                    elif graph.graph[i][j].get_material() =='$':
                        gamer.treasure=(i,j)
                    elif graph.graph[i][j].get_material() =='-':
                        if (i,j) not in gamer.door:
                            gamer.door.append((i,j))
                    elif graph.graph[i][j].get_material() =='a':
                        gamer.axe.append((i,j))
                    elif graph.graph[i][j].get_material() =='k':
                        gamer.key.append((i,j))
            print('PARMETER')
            print(self.target)
            print(gamer.have_key)
            print(len(gamer.door))
            if (self.target == 'treasure' or self.target == 'find_key')and len(gamer.door)>0:
                if gamer.have_key == True:
                    self.target ='open_door'
                else:self.target ='find_key'

            if self.on_water==True:
                visited_land=[]
                stone_land=[]
                if len(gamer.tree)>0:
                    for i in range(160):
                        for j in range(160):
                            #if graph.graph[i][j].get_material()!='~' and graph.graph[i][j].get_material()!=None and  graph.graph[i][j].get_material()!='.' and  graph.graph[i][j].get_material()!='*' and graph.graph[i][j].get_material()!='t' and graph.graph[i][j].get_material()!='-': #and graph.graph[i][j].get_visited()==False:
                            if  graph.graph[i][j].get_material()==' ' or graph.graph[i][j].get_material()=='o' :
                                if graph.graph[i][j].get_visited==True :
                                    visited_land.append (graph.graph[i][j])
                                if graph.graph[i][j].get_material()=='o':
                                    stone_land.append(graph.graph[i][j])
                                else:
                                    tree = self.if_have_tree(gamer,graph.graph,(i,j))
                                    print('I am tring to find land')
                                    print(tree)
                                    print(self.on_water)
                                    print(i,j)
                                    print( graph.graph[i][j].get_material())
                                    if len(tree)>0:
                                        path = self.A_Star(graph.graph, gamer.position, (i,j))
                                        path.reverse()
                                        if self.accessable_land(graph.graph,path,gamer ):
                                            print('the path that i know')
                                            print(path)
                                            self.decision='step'
                                            self.step_path = path[1:]
                                            self.step=(path[-1])
                                            self.step_do='on_bord'
                                            return ' '
                                        else:
                                            continue
                    next_option = stone_land+visited_land
                    for land in next_option:
                        tree = self.if_have_tree(gamer,graph.graph,(i,j))
                        print(tree)
                        print(self.on_water)
                        if len(tree)>0:
                            path = self.A_Star(graph.graph, gamer.position, (i,j))
                            path.reverse()
                            if self.accessable_land(graph.graph,path,gamer ):
                                print(path)
                                self.decision='step'
                                self.step_path = path[1:]
                                self.step=(path[-1])
                                self.step_do='on_bord'
                                return ' '
                            else:
                                continue
                if gamer.have_treasure ==False:
                    if len(gamer.key)>0 and len(gamer.door)>0:
                        path = self.A_Star(graph.graph, gamer.position, gamer.key[0])
                        path.reverse()
                        self.find_trouble(path,graph.graph,gamer)
                        return ' '
                    else:
                        path = self.A_Star(graph.graph, gamer.position, gamer.treasure)
                        print('here',path)
                        path.reverse()
                        self.find_trouble(path,graph.graph,gamer)
                        return ' '
                else:
                    path = self.A_Star(graph.graph, gamer.position, (80,80))
                    print('here',path)
                    path.reverse()
                    self.find_trouble(path,graph.graph,gamer)
                    return ' '
            else:
                if self.target =='open_door':
                    print('I am here to open the door')
                    if len(gamer.door)>0:
                        path = self.A_Star(graph.graph, gamer.position, gamer.door[0])
                        print(path)
                        path.reverse()
                        self.find_trouble(path,graph.graph,gamer)
                        return ' '
                    else:
                        self.target='treasure'
                        return ' '
                elif self.target == 'treasure':

                    if gamer.treasure!=None:
                        path=self.A_Star(graph.graph, gamer.position, gamer.treasure)
                        if path == 'Failure':
                            print('not find')
                            return ' '
                        else:
                            path.reverse()
                            print(path)
                            return self.find_trouble(path,graph.graph,gamer)
                    else:
                        print('No Treasure')
                        if len(gamer.stone_getable) ==0:
                            if gamer.have_raft == False:
                                self.get_trees ( graph.graph,gamer)
                                print('Cut tree')
                                if len(gamer.tree_getable)>0:
                                    self.target = 'Cut'
                                    return ' '
                            else:
                                if gamer.have_treasure==False:
                                    pos=self.find_river(graph.graph,gamer)
                                    path = self.A_Star(graph.graph, gamer.position, pos)
                                    path.reverse()
                                    self.target='treasure'
                                    self.decision='step'
                                    self.on_water=True
                                    self.step_path = path[1:]
                                    self.step=(path[-1])
                                    self.step_do='in_~'
                                    return ' '
                                else:
                                    if len(gamer.tree)>0:
                                        self.go_to_cut_tree(gamer,graph.graph,gamer.tree[0])
                                    else:
                                        self.decision ='Count'
                                        self.target = 'back'
                                    return ' '

                elif self.target == 'back':
                    self.get_trees( graph.graph,gamer)
                    if len(gamer.tree_getable) >0:
                        if gamer.have_axe==True:

                            path=self.A_Star(graph.graph, gamer.position,gamer.tree_getable[0])
                            path.reverse()
                            self.target='Cut'
                            #print('I am going to cut remain tree in the map')
                            #print(path)
                            return self.find_trouble(path,graph.graph,gamer)

                    self.get_stones(graph.graph,gamer)
                    if len(gamer.stone_getable)>0:
                        path=self.A_Star(graph.graph, gamer.position,gamer.stone_getable[0])
                        path.reverse()
                        return self.find_trouble(path,graph.graph,gamer)

                    path=self.A_Star(graph.graph, gamer.position, (80,80))
                    print(path)
                    path.reverse()
                #print(path)
                    return self.find_trouble(path,graph.graph,gamer)
                    # else:
                    #     self.get_stones(graph.graph,gamer)
                    #     if len(gamer.stone_getable)>0:
                    #         path=self.A_Star(graph.graph, gamer.position, gamer.stone_getable[0])
                    #         path.reverse()
                    #         self.decision='step'
                    #         self.step_do='o'
                    #         self.step_path=path[1:]
                    #         self.step=path[-1]
                    #         return ' '
                    #     else:
                    #         path=self.A_Star(graph.graph, gamer.position, (80,80))
                    #         path.reverse()
                    #         #print(path)
                    #         return self.find_trouble(path,graph.graph,gamer)

                elif self.target =='find_key' and self.on_water==False:
                    if len(gamer.key)>0:
                        path=self.A_Star(graph.graph, gamer.position, gamer.key[0])
                        if path !='Failure':
                            path.reverse()
                            return self.find_trouble(path,graph.graph,gamer)
                        else:
                            path=self.A_Star(graph.graph, gamer.position, gamer.treasure)
                            if path !='Failure':
                                path.reverse()
                                return self.find_trouble(path,graph.graph,gamer)
                    else:
                        if gamer.have_raft==False:
                            self.get_trees ( graph.graph,gamer)
                            print('Cut tree')
                            if len(gamer.tree_getable)>0:
                                self.target = 'Cut'
                                return ' '
                        else:
                            pos=self.find_river(graph.graph,gamer)
                            path = self.A_Star(graph.graph, gamer.position, pos)
                            path.reverse()
                            self.decision='step'
                            self.on_water=True
                            self.step_path = path[1:]
                            self.step=(path[-1])
                            self.step_do='in_~'
                            return ' '
                    if self.stone_get_new(path,graph.graph):
                        print('find the path without water')
                        path.reverse()
                        self.find_trouble(path,graph.graph,gamer)
                        return ' '
                    else:
                        if path == 'Failure':
                            print('fuck the game designer')
                        else:
                            print('find the path with water')
                            path.reverse()
                            self.find_trouble(path,graph.graph,gamer)
                            return ' '


                elif  self.target == 'Cut':
                    self.get_trees(graph.graph,gamer)
                    path=self.A_Star(graph.graph, gamer.position, gamer.tree_getable[0])
                    print(gamer.tree_getable[0])
                    print(path)
                    if path == 'Failure':
                        for tree in gamer.tree:
                            path=self.A_Star(graph.graph, gamer.position, gamer.tree[0])
                            path.reverse()
                            return self.find_trouble(path,graph.graph,gamer)
                        return ' '
                    else:
                        print(' here is my path to cut tree')
                        path.reverse()
                        print(path)
                        self.step_do='T'
                        return self.find_trouble(path,graph.graph,gamer)

                        # self.decision='step'
                        # self.step_path = path[1:]
                        # self.step=(path[-2])
                        # self.step_do='T'
                        # return ' '
        if self.decision=='find_axe':
            path=self.A_Star(graph.graph, gamer.position, gamer.axe[0])
            if path == 'Failure':
                print('fuck the game designer')
            else:
                path.reverse()
                return self.find_trouble(path,graph.graph,gamer)
        if self.decision=='find_key':
            path=self.A_Star(graph.graph, gamer.position, gamer.key[0])
            if self.stone_get_new(path,graph.graph):
                self.find_trouble(path,graph.gra,gamer)
            else:
                if path == 'Failure':
                    print('fuck the game designer')
                else:
                    path.reverse()
                    return self.find_trouble(path,graph.graph,gamer)
        if self.decision=='step':
            return self.step_front(graph.graph,gamer)

    def find_river(self,graph,gamer):
        k=[]
        k.append((gamer.position))
        while True:
            i,j=k.pop(0)
            if graph[i][j].get_material() == '~':
                return (i,j)
            if (i-1,j) not in k:
                k.append((i-1,j))
            if (i+1,j) not in k :
                k.append((i+1,j))
            if (i,j-1) not in k :
                k.append((i,j-1))
            if (i,j+1) not in k:
                k.append((i,j+1))

    def accessable_land(self,graph,path,gamer ):
        flag=True
        count = gamer.have_stones
        for i,j in path:
            if graph[i][j].get_material() =='~':
                if flag==True:
                    continue
                else:
                    count-=1
                    if count<0:
                        return False
            elif graph[i][j].get_material() =='-':
                if gamer.have_key==False:
                    return False
                else:
                    flag=False
            elif graph[i][j].get_material() =='o':
                count+=1
                flag=False
            else:
                flag=False
        return True

    def get_trees (self, graph,gamer):
        gamer.tree_getable=[]
        gamer.tree_ungetable=[]
        print(gamer.tree)
        for trees in gamer.tree:
            flag=True
            path=self.A_Star(graph, gamer.position, trees)
            if path != 'Failure':
                path.reverse()
                if path =='Failure':
                    gamer.tree_ungetable.append(trees)
                else:
                    for i in range(len(path)-1):
                         # weight=self.get_weight(graph[path[i][0]][path[i][1]],graph[path[i+1][0]][path[i+1][1]])
                         # if weight >1:
                         if graph[path[i][0]][path[i][1]].get_material()=='~':
                             if trees not in gamer.tree_ungetable:
                                 gamer.tree_ungetable.append(trees)
                                 flag=False
                         elif graph[path[i][0]][path[i][1]].get_material()=='-' and gamer.have_key==False:
                             if trees not in gamer.tree_ungetable:
                                 gamer.tree_ungetable.append(trees)
                                 flag=False
                    if flag==True:
                        if trees not in gamer.tree_getable:
                            gamer.tree_getable.append(trees)

        print('Tree that i can get',gamer.tree_getable)
        print('Tree that i cant get',gamer.tree_ungetable)
    def if_have_tree(self,gamer,graph,pos):
        print(pos)
        flag= False
        self.get_trees(graph,gamer)
        accessable = []
        for tree in gamer.tree:
            path=self.A_Star(graph, pos , tree)
            if path=='Failure':
                continue
            else:
                path.reverse()
                for i in path[:len(path)-1]:
                    if graph[i[0]][i[1]].get_material() =='-':
                        if gamer.have_key==True:
                            continue
                        else:
                            break
                    if graph[i[0]][i[1]].get_material() == '~':
                        break
                else:
                    accessable.append(tree)
        return accessable


    def find_trouble(self,path,graph,gamer):
        for i in range(len(path)-1):
            weight=self.get_weight(graph[path[i][0]][path[i][1]],graph[path[i+1][0]][path[i+1][1]])
            if self.on_water ==True:
                print('have been to the new function')
                if graph[path[i][0]][path[i][1]].get_material()=='-':
                    if gamer.have_key==False:
                        self.decision='find_key'
                        return ' '


            elif weight >1:
                if graph[path[i+1][0]][path[i+1][1]].get_material() =='~':
                    self.get_stones(graph,gamer)
                    water_length=self.find_total_water(path,graph)
                    print('water_length: ',water_length)
                    print('have_stones: ',gamer.have_stones)
                    if water_length <= gamer.have_stones:
                        print('put stone in river')
                        #gamer.have_stones=gamer.have_stones-water_length
                        self.decision='step'
                        self.step_path = path[1:]
                        self.step=(path[i+1][0],path[i+1][1])
                        self.step_do='~'
                        return ' '
                    else:
                        if water_length <= (len(gamer.stone_getable)+gamer.have_stones):
                            path = self.A_Star(graph, gamer.position, gamer.stone_getable[0])
                            path.reverse()
                            self.decision='step'
                            self.step_path = path[1:]
                            self.step=(path[-1])
                            self.step_do='o'
                            print('get stones')
                            return ' '
                        else:
                            if gamer.have_raft ==True:
                                if self.target !='back':
                                    if len(gamer.stones)>0:
                                        self.decision='step'
                                        self.step_path = path[1:]
                                        print('I am here to step in to water')
                                        print(self.step_path)
                                        print((path[i+1][0],path[i+1][1]))
                                        self.step=(path[i+1][0],path[i+1][1])
                                        self.step_do='in_~'
                                        return ' '
                                else:
                                    if self.if_get_stone(path,graph,gamer)==True:
                                        if len(gamer.stones)>0:
                                            path =  self.A_Star(graph, gamer.position, gamer.stones[0])
                                            path.reverse()
                                            print(path)
                                            self.decision='step'
                                            self.step_path = path[1:]
                                            self.step= path[-1]
                                            self.step_do='o'
                                            return ' '
                                    if len(gamer.tree)>0:
                                        self.target='Cut'
                                        print('I am going to cut remain tree in the map')
                                        self.go_to_cut_tree(gamer,graph,gamer.tree[0])
                                        return ' '
                                    else:
                                        path = self.A_Star(graph, gamer.position, (80,80))
                                        path.reverse()
                                        self.decision='step'
                                        self.step_path = path[1:]
                                        self.step=(80,80)
                                        return ' '
                            else:
                                if self.on_water ==True:
                                    self.decision='step'
                                    self.step_path = path[1:]
                                    self.step=(path[i+1][0],path[i+1][1])
                                    self.step_do='in_~'
                                self.get_tree( graph,gamer)
                                if len(gamer.tree)>0:
                                    path =  self.A_Star(graph, gamer.position, gamer.tree[0])
                                    path.reverse()
                                    self.decision='step'
                                    self.target='Cut'
                                    self.step_path = path[1:]
                                    self.step=(path[-2])
                                    self.step_do='T'
                                    return ' '
                                else:
                                    if len(gamer.stones)+gamer.have_stones>=water_length:
                                        if gamer.stone_getable != []:
                                            path = self.A_Star(graph, gamer.position, gamer.stone_getable[0])
                                            path.reverse()
                                            self.decision='step'
                                            self.step=path[-1]
                                            self.step_path = path[1:]
                                            self.step_do='o'
                                            print('get stones')
                                            return ' '
                                        else:
                                             pos,water_length=self.stone_chage(graph,gamer)
                                             path_1=self.choose_path(gamer,graph,pos)
                                             path_2=self.A_Star(graph, path_1[-1], pos)
                                             path_2.reverse()
                                             path = path_1[1:]+path_2[1:]
                                             print(path_2)
                                             print(path)
                                             print('put stone in river')
                                             #gamer.have_stones=gamer.have_stones-water_length
                                             self.decision='step'
                                             self.target ='treasure'
                                             self.step_path = path[:]
                                             self.step=path[-1]
                                             self.step_do='~'
                                             return ' '
                                    ###############
                                    #change stones#
                                    ###############
                else:
                    if graph[path[i+1][0]][path[i+1][1]].get_material() =='T':
                        if gamer.have_axe == True:
                            print(gamer.position)
                            print('I am going to cut the tree')
                            print(path[1:i+1])
                            self.decision='step'
                            self.step_path = path[1:i+1]
                            self.step=(path[i][0],path[i][1])
                            self.step_do='T'
                            return ' '
                        else:
                            print('find_axe')
                            self.decision='find_axe'
                            return' '
                    if graph[path[i+1][0]][path[i+1][1]].get_material() =='-':
                        if gamer.have_key == True:
                            print(gamer.position)
                            print('have keys')
                            self.decision='step'
                            print(path[1:i+1])
                            self.step_path = path[1:i+1]
                            print(self.step)
                            self.step=(path[i][0],path[i][1])
                            self.step_do='-'
                            return ' '
                        else:
                            if gamer.key ==[]:
                                if gamer.have_axe == True:
                                    if gamer.tree!=[]:
                                        path =  self.A_Star(graph, gamer.position, gamer.tree[0])
                                        path.reverse()
                                        self.decision='step'
                                        self.step_path = path[1:]
                                        self.step=(path[-2])
                                        self.step_do='T'
                                        self.decision='find_key'
                                        return ' '
                                else:
                                    print('find_axe')
                                    self.decision='find_axe'
                                    return' '
        else:
            if self.target =='Cut':
                self.decision='step'
                self.step_path = path[1:]
                self.step=(path[-2][0],path[-2][1])
                self.step_do='T'
                return ' '
            else:
                self.decision='step'
                self.step_path = path[1:]
                self.step=(path[-1][0],path[-1][1])
                self.step_do='o'
                return ' '
    def stone_get_new(self,path,graph):
        for i  in range(len(path)-1):
            weight=self.get_weight(graph[path[i][0]][path[i][1]],graph[path[i+1][0]][path[i+1][1]])
            if weight >1 and graph[path[i+1][0]][path[i+1][1]].get_material() == '~':
                return False
        return True


    def go_to_cut_tree(self,gamer,graph,tree):
        print('go_to_cut_tree')

        if graph[tree[0]][tree[1]].get_North().get_material()!= '~' and graph[tree[0]][tree[1]].get_North().get_material()!= '.' and graph[tree[0]][tree[1]].get_North().get_material()!= '*':
            path=self.A_Star(graph, gamer.position, (tree[0]-1,tree[1]))
            path.reverse()
            self.decision='step'
            self.step_path = path[1:]
            self.step=(path[-1])
            self.step_do='T'
        elif graph[tree[0]][tree[1]].get_East().get_material()!= '~' and graph[tree[0]][tree[1]].get_East().get_material()!= '.' and graph[tree[0]][tree[1]].get_East().get_material()!= '*':
            path=self.A_Star(graph, gamer.position, (tree[0],tree[1]+1))
            path.reverse()
            self.decision='step'
            self.step_path = path[1:]
            self.step=(path[-1])
            self.step_do='T'
        elif graph[tree[0]][tree[1]].get_West().get_material()!= '~' and graph[tree[0]][tree[1]].get_West().get_material()!= '.' and graph[tree[0]][tree[1]].get_West().get_material()!= '*':
            path=self.A_Star(graph, gamer.position, (tree[0],tree[1]-1))
            path.reverse()
            self.decision='step'
            self.step_path = path[1:]
            self.step=(path[-1])
            self.step_do='T'
        elif graph[tree[0]][tree[1]].get_South().get_material()!= '~' and graph[tree[0]][tree[1]].get_South().get_material()!= '.' and graph[tree[0]][tree[1]].get_South().get_material()!= '*':
            path=self.A_Star(graph, gamer.position, (tree[0]+1,tree[1]))
            path.reverse()
            self.decision='step'
            self.step_path = path[1:]
            self.step=(path[-1])
            self.step_do='T'
        else:
            return ' '
        print(path[1:])
        return ' '

    # def if_get_tree(self,path,graph,gamer):
    #     raft=gamer.have_raft
    #     in_water=False
    #     for (i,j) in path:
    #         if graph[i][j].get_material()=='~':
    #             if raft=False:
    #                 return

    def if_get_stone(self,path,graph,gamer):
        pass
        stone_count=gamer.have_stones
        raft=True
        in_water=False
        for (i,j) in path:
            if graph[i][j].get_material()=='~':
                if stone_count>0:
                    stone_count-=1
                else:
                    if in_water==True:
                        continue
                    else:
                        if raft==True:
                            raft=False
                        else:
                            return True
            else:
                if in_water ==True:
                    in_water=False


    def get_island(self,gamer,graph):
        island={}
        count =0
        object=[]
        for i in  list(set(gamer.tree)):
            object.append(i)
        for i in list(set(gamer.stones)):
            object.append(i)
        for i in list(set(gamer.door)):
            object.append(i)
        for i in list(set(gamer.key)):
            object.append(i)
        for i in list(set(gamer.axe)):
            object.append(i)
        object.append(gamer.treasure)
        object =list(set(object))
        print(object)
        for i in object:
            if len(island) ==0:
                island[count]=[]
                island[count].append(i)
            else:
                for key in island:
                    path = self.A_Star(graph, i, island[key][0])
                    if self.stone_get_new(path,graph):
                        island[key].append(i)
                        break
                else:
                    count+=1
                    island[count]=[i]
        return island

    def choose_path(self,gamer,graph,pos):
        landing_points = self.landing_point_BFS(graph,pos)
        print('I have this many landing_point ',landing_points)
        landing_points=list(set(landing_points))

        if len(landing_points) ==1:
            path_1=self.A_Star(graph, gamer.position, landing_points[0])
            path_1.reverse()
            path_2=self.A_Star(graph, landing_points[0], pos)
            path_2.reverse()
            return path_1[:]+path_2[1:]

        distance = math.inf
        closest_island =None
        island=self.get_island(gamer,graph)
        print(island)
        for landing_point in landing_points:
            path = self.A_Star(graph, gamer.position, landing_point)
            if self.stone_get_new(path,graph):
                landing_points.remove(landing_point)
        for land in island:
            if pos in island[land]:
                continue
            else:
                total=[0,0]
                for key in island[land]:
                    total[0]+=key[0]
                    total[1]+=key[1]
                total[0]=total[0]/len(island[land])
                total[1]=total[1]/len(island[land])
                temp_dis=self.Manhattan(pos, (total[0],total[1]))
                if temp_dis<distance:
                    closest_island=(total[0],total[1])
                    distance=temp_dis

        print('the choice that i have ',landing_points)
        distance = math.inf
        best_choice=None
        for choice in landing_points:
            temp_dis=self.Manhattan(choice,closest_island)
            if distance>temp_dis:
                best_choice=choice
                distance=temp_dis
        print('My choice is ',best_choice)
        path=self.A_Star(graph, gamer.position, best_choice)
        path.reverse()
        return path[:]

    def stone_chage(self,graph,gamer):
        self.get_stones (graph,gamer)
        for stone in gamer.stone_ungetable:
            path=self.A_Star(graph, gamer.position, stone)
            path.reverse()
            total_water=self.water_between(path,graph)
            print('get stone water len: ',total_water)
            print('stone that i can get ',gamer.stone_getable)
            print('All stone ',gamer.stones)
            print('stone that i cant get ',gamer.stone_ungetable)
            print('I have this much stones ',gamer.have_stones)
            print('This much water is in between ',total_water)
            print('The stone that i choose ',stone)
            if total_water<= len(gamer.stone_getable)+gamer.have_stones:
                count=1
                temp = gamer.stone_ungetable[:]
                temp.remove(stone)
                for s in temp:
                    path=self.A_Star(graph, stone, s)
                    if self.stone_get_new(path,graph):
                        count+=1
                if count>=total_water:
                    return stone,total_water

    def water_between(self,path,graph):
        count=0
        for i, j in path:
            if graph[i][j].get_material()=='~':
                count+=1
        return count
    def get_stones (self, graph,gamer):
        gamer.stone_ungetable=[]
        gamer.stone_getable=[]
        for stone in gamer.stones:
            path=self.A_Star(graph, gamer.position, stone)
            if path =='Failure':
                gamer.stone_ungetable.append(stone)
            else:
                for i in range(len(path)-1):
                     weight=self.get_weight(graph[path[i][0]][path[i][1]],graph[path[i+1][0]][path[i+1][1]])
                     if weight >1:
                         if stone not in gamer.stone_ungetable:
                             gamer.stone_ungetable.append(stone)
                         break
                else:
                    if stone not in gamer.stone_getable:
                        gamer.stone_getable.append(stone)

    def get_tree (self, graph,gamer):
        for tree in gamer.tree:
            path=self.A_Star(graph, gamer.position, tree)
            if path =='Failure':
                gamer.tree_ungetable.append(tree)
            else:
                for i in range(len(path)-1):
                     weight=self.get_weight(graph[path[i][0]][path[i][1]],graph[path[i+1][0]][path[i+1][1]])
                     if weight >1:
                         if tree not in gamer.tree_ungetable:
                             gamer.tree_ungetable.append(tree)
                         break
                else:
                    if tree not in gamer.tree_getable:
                        gamer.tree_getable.append(tree)

    def find_total_water(self,path,graph):
        count=0
        flag=False
        for i,j in path:
            if graph[i][j].get_material()=='~':
                if flag== False:
                    flag=True
                count+=1
            else:
                if flag==True:
                    return count
        return count

    def step_front(self,graph,gamer):
        if graph[gamer.position[0]][gamer.position[1]].get_material() == 'o':
            graph[gamer.position[0]][gamer.position[1]].set_material(' ')
            graph[gamer.position[0]][gamer.position[1]].set_visited(True)
            if gamer.position in gamer.stone_getable:
                gamer.stone_getable.remove(gamer.position)
            if gamer.position in gamer.stones:
                gamer.stones.remove(gamer.position)
            gamer.have_stones+=1
            print('game have stones: ',gamer.have_stones)
        if graph[gamer.position[0]][gamer.position[1]].get_material() == '~':
            if gamer.have_stones>0 and self.on_water ==False:
                graph[gamer.position[0]][gamer.position[1]].set_material(' ')
                graph[gamer.position[0]][gamer.position[1]].set_visited(True)
                gamer.have_stones-=1
            else:
                self.on_water=False

        if graph[gamer.position[0]][gamer.position[1]].get_material() == 'k':
            graph[gamer.position[0]][gamer.position[1]].set_material(' ')
            gamer.key.remove((gamer.position[0],gamer.position[1]))
            gamer.have_key=True
        if graph[gamer.position[0]][gamer.position[1]].get_material() == '$':
            graph[gamer.position[0]][gamer.position[1]].set_material(' ')
            gamer.have_treasure=True
            gamer.treasure=None
            gamer.target='back'
        if gamer.position != self.step:
            if graph[self.step_path[0][0]][self.step_path[0][1]] == graph[gamer.position[0]][gamer.position[1]].get_North():
                if gamer.face != 'N':
                    return self.turn_and_go(gamer,'N')
                else:
                    self.step_path.pop(0)
                    return 'F'
            if graph[self.step_path[0][0]][self.step_path[0][1]] == graph[gamer.position[0]][gamer.position[1]].get_West():
                if gamer.face != 'W':
                    return self.turn_and_go(gamer,'W')
                else:
                    self.step_path.pop(0)
                    return 'F'
            if graph[self.step_path[0][0]][self.step_path[0][1]] == graph[gamer.position[0]][gamer.position[1]].get_South():
                if gamer.face != 'S':
                    return self.turn_and_go(gamer,'S')
                else:
                    self.step_path.pop(0)
                    return 'F'
            if graph[self.step_path[0][0]][self.step_path[0][1]] == graph[gamer.position[0]][gamer.position[1]].get_East():
                if gamer.face != 'E':
                    return self.turn_and_go(gamer,'E')
                else:
                    self.step_path.pop(0)
                    return 'F'
        else:
            if 'on_bord' == self.step_do:
                self.decision='traversal'
                self.on_water=False
                self.target='Cut'
                return ' '
            if 'in_~' ==self.step_do:
                gamer.have_raft=False
                self.decision='water_traversal'
                self.on_water =True
                return ' '

            if 'o' == self.step_do:
                self.decision='Count'
                return ' '
            elif '~'==self.step_do:
                # if graph[gamer.position[0]][gamer.position[1]].get_material() =='~':
                #     gamer.have_stones-=1
                graph[gamer.position[0]][gamer.position[1]].set_material(' ')
                self.decision='traversal'
                return ' '
            else:
                if graph[gamer.position[0]][gamer.position[1]].get_North().get_material() == self.step_do:
                    graph[gamer.position[0]][gamer.position[1]].set_North_weight(1)
                    if self.step_do=='-':
                        if (gamer.position[0]-1,gamer.position[1]) in gamer.door:
                            gamer.door.remove((gamer.position[0]-1,gamer.position[1]))
                    elif self.step_do=='T':
                        if (gamer.position[0]-1,gamer.position[1]) in gamer.tree:
                            gamer.tree.remove((gamer.position[0]-1,gamer.position[1]))
                    face = 'N'
                elif graph[gamer.position[0]][gamer.position[1]].get_West().get_material() == self.step_do:
                    graph[gamer.position[0]][gamer.position[1]].set_West_weight(1)
                    if self.step_do=='-':
                        if (gamer.position[0],gamer.position[1]-1) in gamer.door:
                            gamer.door.remove((gamer.position[0],gamer.position[1]-1))
                    elif self.step_do=='T':
                        if (gamer.position[0],gamer.position[1]-1) in gamer.tree:
                            gamer.tree.remove((gamer.position[0],gamer.position[1]-1))
                    face = 'W'
                elif graph[gamer.position[0]][gamer.position[1]].get_South().get_material() == self.step_do:
                    graph[gamer.position[0]][gamer.position[1]].set_South_weight(1)
                    if self.step_do=='-':
                        if (gamer.position[0]+1,gamer.position[1]) in gamer.door:
                            gamer.door.remove((gamer.position[0]+1,gamer.position[1]))
                    elif self.step_do=='T':
                        if (gamer.position[0]+1,gamer.position[1]) in gamer.tree:
                            gamer.tree.remove((gamer.position[0]+1,gamer.position[1]))
                    face = 'S'
                else:
                    if self.step_do=='-':
                        if (gamer.position[0],gamer.position[1]+1) in gamer.door:
                            gamer.door.remove((gamer.position[0],gamer.position[1]+1))
                    elif self.step_do=='T':
                        if (gamer.position[0],gamer.position[1]+1) in gamer.tree:
                            gamer.tree.remove((gamer.position[0],gamer.position[1]+1))
                    graph[gamer.position[0]][gamer.position[1]].set_East_weight(1)
                    face = 'E'

                if gamer.face != face:
                    return self.turn_and_go(gamer,face)
                else:
                    if self.step_do=='-':
                        self.decision='traversal'
                        return 'U'
                    elif self.step_do=='T':
                        self.decision='traversal'
                        if self.target =='Cut':
                            self.target='treasure'
                        gamer.have_raft=True
                        return 'C'

    def get_weight(self,node_from,node_to):
        # if node_to.get_material=='T' or node_to.get_material=='-':
        #     return 6401
        # elif node_to.get_material()== '~':
        #     return 6500
        # elif node_to.get_material()=='*' or node_to.get_material()==None or node_to.get_material()=='.':
        #     return math.inf
        # else:
        #     return 1
        if node_to == node_from.get_North():
            return node_from.get_North_weight()
        elif node_to == node_from.get_West():
            return node_from.get_West_weight()
        elif node_to == node_from.get_South():
            return node_from.get_South_weight()
        elif node_to == node_from.get_East():
            return node_from.get_East_weight()

    def traversal(self,node,gamer):
        print(' get to traversal')
        node.set_visited(True)
        if node.get_material() =='$':
            gamer.have_treasure=True
            node.set_material(' ')
            gamer.treasure=None
            self.target='back'
        if node.get_material() =='k':
            gamer.have_key =True
        if node.get_material() =='a':
            gamer.have_axe =True
        if node.get_North_weight() ==1 and node.get_North().get_material() != 'o'and node.get_North().get_visited()==False:
            if gamer.face != 'N':
                return self.turn_and_go(gamer,'N')
            else:
                self.return_back.append('F')
                self.return_back.append('S')
                return 'F'

        if node.get_East_weight() ==1 and node.get_East().get_material() != 'o' and node.get_East().get_visited()==False:
            if gamer.face != 'E':
                return self.turn_and_go(gamer,'E')
            else:
                self.return_back.append('F')
                self.return_back.append('W')
                return 'F'
        print(node.get_South().get_material())
        if node.get_South_weight() ==1 and node.get_South().get_material() != 'o' and node.get_South().get_visited()==False:
            if gamer.face != 'S':
                return self.turn_and_go(gamer,'S')
            else:
                self.return_back.append('F')
                self.return_back.append('N')
                return 'F'

        if node.get_West_weight() ==1 and node.get_West().get_material() != 'o' and node.get_West().get_visited()==False:
            if gamer.face != 'W':
                return self.turn_and_go(gamer,'W')
            else:
                self.return_back.append('F')
                self.return_back.append('E')
                return 'F'
        if len(self.return_back) > 0:
            if self.return_back[-1] == 'F' :
                if self.facing !=gamer.face:
                    return self.turn_and_go(gamer,self.facing)
                else:
                    return self.return_back.pop(-1)
            else:
                self.facing=self.return_back.pop(-1)
                if self.facing == gamer.face:
                    return self.return_back.pop(-1)
                else:
                    return self.turn_and_go(gamer,self.facing)
        self.decision = "Count"
        return '  '

    def turn_and_go(self,game,want_face):
        if want_face == 'N':
            if game.face == 'E':
                return 'L'
            elif game.face == 'S':
                return 'R'
            elif game.face =='W':
                return 'R'
        if want_face == 'E':
            if game.face == 'N':
                return 'R'
            elif game.face == 'W':
                return 'R'
            elif game.face =='S':
                return 'L'
        if want_face == 'W':
            if game.face == 'E':
                return 'L'
            elif game.face == 'N':
                return 'L'
            elif game.face =='S':
                return 'R'
        if want_face == 'S':
            if game.face == 'E':
                return 'R'
            elif game.face == 'N':
                return 'R'
            elif game.face =='W':
                return 'L'

    def Manhattan(self, start, goal):
        return abs(start[0]-goal[0])+abs(start[1]-goal[1])

    def TrueDis(self, graph, start, goal):
        if self.on_water==True:
            if graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_North():
                if graph[goal[0]][goal[1]].get_material()=='~':
                    return 1
                else:
                    return (graph[start[0]][start[1]].get_North_weight()+6500)
            elif graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_South():
                if graph[goal[0]][goal[1]].get_material()=='~':
                    return 1
                else:
                    return (graph[start[0]][start[1]].get_South_weight()+6500)
            elif graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_West():
                if graph[goal[0]][goal[1]].get_material()=='~':
                    return 1
                else:
                    return (graph[start[0]][start[1]].get_West_weight()+6500)
            else:
                if graph[goal[0]][goal[1]].get_material()=='~':
                    return 1
                else:
                    return (graph[start[0]][start[1]].get_East_weight()+6500)

        else:
            if graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_North():
                return graph[start[0]][start[1]].get_North_weight()
            elif graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_South():
                return graph[start[0]][start[1]].get_South_weight()
            elif graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_West():
                return graph[start[0]][start[1]].get_West_weight()
            else:
                return graph[start[0]][start[1]].get_East_weight()

    def find_least(self, di, open):
        least = math.inf
        least_ele = None
        for ele in di:
            if ele in open:
                if di[ele] < least:
                    least = di[ele]
                    least_ele = ele
        return least_ele

    def path(self,come_from, current):
        total_path = [current]
        while current in come_from.keys():
            current = come_from[current]
            total_path.append(current)
        return total_path

    def neighbers(self,graph,node):
        neighbers=[]
        if graph[node[0]][node[1]].get_North_weight() != math.inf:
            neighbers.append((node[0]-1,node[1]))
        if graph[node[0]][node[1]].get_West_weight() != math.inf:
            neighbers.append((node[0],node[1]-1))
        if graph[node[0]][node[1]].get_South_weight() != math.inf:
            neighbers.append((node[0]+1,node[1]))
        if graph[node[0]][node[1]].get_East_weight() != math.inf:
            neighbers.append((node[0],node[1]+1))
        return neighbers

    def A_Star(self, graph, start, goal):
        closed = []
        open = [start]
        come_from = {}
        gx = {}
        hx = {}
        fx = {}
        gx[start] = 0
        hx[start] = self.Manhattan(start, goal)
        fx[start] = hx[start]
        while len(open) > 0:
            node  = self.find_least(fx, open)
            if node == goal:
                return self.path(come_from, goal)

            closed.append(node)
            while node in open:
                open.remove(node)

            neighbers = self.neighbers(graph,node)

            for neighber in neighbers:
                if neighber in closed:
                    continue
                if neighber not in open:
                    open.append(neighber)

                tempx = gx[node] + self.TrueDis(graph, node, neighber)
                try:
                    if tempx >= gx[neighber]:
                        continue
                except:
                    gx[neighber] = tempx
                come_from[neighber] = node
                gx[neighber] = tempx
                fx[neighber] = gx[neighber] + self.Manhattan(neighber, goal)

        return 'Failure'


    def stone_TrueDis(self, graph, start, goal):
        if graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_North():
            if graph[goal[0]][goal[1]].get_material() == ' ' or graph[goal[0]][goal[1]].get_material() == 'O' or graph[goal[0]][goal[1]].get_material() == 'o':
                return 0
            else:
                return graph[start[0]][start[1]].get_North_weight()
        elif graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_South():
            if graph[goal[0]][goal[1]].get_material() == ' ' or graph[goal[0]][goal[1]].get_material() == 'O' or graph[goal[0]][goal[1]].get_material() == 'o':
                return 0
            else:
                return graph[start[0]][start[1]].get_South_weight()
        elif graph[goal[0]][goal[1]] == graph[start[0]][start[1]].get_West():
            if graph[goal[0]][goal[1]].get_material() == ' ' or graph[goal[0]][goal[1]].get_material() == 'O' or graph[goal[0]][goal[1]].get_material() == 'o':
                return 0
            else:
                return graph[start[0]][start[1]].get_West_weight()
        else:
            if graph[goal[0]][goal[1]].get_material() == ' ' or graph[goal[0]][goal[1]].get_material() == 'O' or graph[goal[0]][goal[1]].get_material() == 'o':
                return 0
            else:
                return graph[start[0]][start[1]].get_East_weight()

    def landing_point_BFS(self, graph, start):
        print('!!!!!!!!!!!!!!!!!')
        print(start)
        print('!!!!!!!!!!!!!!!!!')
        search_list=[start]
        searched_list=[]
        min_landing_distance=math.inf
        landing_point = []
        while len(search_list)>0:
            node = search_list.pop(0)
            searched_list.append(node)
            print(search_list)
            neighbers = self.neighbers(graph,node)
            for neighber in neighbers:
                path=self.A_Star(graph, start, (neighber[0],neighber[1]))
                if graph[neighber[0]][neighber[1]].get_material() != '~' and ((neighber[0],neighber[1]) not in searched_list) and graph[neighber[0]][neighber[1]].get_visited() == True and ((neighber[0],neighber[1]) not in search_list):
                    if self.stone_get_new(path,graph)==True:
                        continue
                    else:
                        landing_distance=self.water_distance(path,graph)
                        if min_landing_distance>landing_distance:
                            landing_point=[(neighber[0],neighber[1])]
                            min_landing_distance=landing_distance
                        elif min_landing_distance==landing_distance:
                            landing_point.append((neighber[0],neighber[1]))
                else:
                    if self.water_distance(path,graph)<min_landing_distance and ((neighber[0],neighber[1]) not in searched_list) and ((neighber[0],neighber[1]) not in search_list):
                        search_list.append(neighber)
        water_return = []
        min_landing_distance=math.inf
        for i in landing_point:
            if graph[i[0]][i[1]].get_North().get_material()=='~' and (i[0]-1,i[1]) in searched_list:
                path=self.A_Star(graph, start, (i[0]-1,i[1]))
                landing_distance=self.water_distance(path,graph)

                if min_landing_distance>landing_distance:
                    water_return=[(i[0]-1,i[1])]
                    min_landing_distance=landing_distance
                elif min_landing_distance==landing_distance:
                    water_return.append((i[0]-1,i[1]))


            if graph[i[0]][i[1]].get_East().get_material()=='~' and (i[0],i[1]+1) in searched_list:
                path=self.A_Star(graph, start, (i[0],i[1]+1))
                landing_distance=self.water_distance(path,graph)
                if min_landing_distance>landing_distance:
                    water_return=[(i[0],i[1]+1)]
                    min_landing_distance=landing_distance
                elif min_landing_distance==landing_distance:
                    water_return.append((i[0],i[1]+1))
            if graph[i[0]][i[1]].get_South().get_material()=='~' and (i[0]+1,i[1]) in searched_list:
                path=self.A_Star(graph, start, (i[0]+1,i[1]))
                landing_distance=self.water_distance(path,graph)

                if min_landing_distance>landing_distance:
                    water_return=[(i[0]+1,i[1])]
                    min_landing_distance=landing_distance
                elif min_landing_distance==landing_distance:
                    water_return.append((i[0]+1,i[1]))
            if graph[i[0]][i[1]].get_West().get_material()=='~' and (i[0],i[1]-1) in searched_list:
                path=self.A_Star(graph, start, (i[0],i[1]-1))
                landing_distance=self.water_distance(path,graph)

                if min_landing_distance>landing_distance:
                    water_return=[(i[0],i[1]-1)]
                    min_landing_distance=landing_distance
                elif min_landing_distance==landing_distance:
                    water_return.append((i[0],i[1]-1))

        return water_return





    def water_distance(self, path, graph):
        count =0
        for i  in range(len(path)-1):
            weight=self.get_weight(graph[path[i][0]][path[i][1]],graph[path[i+1][0]][path[i+1][1]])
            if weight >1 and graph[path[i+1][0]][path[i+1][1]].get_material() == '~':
                count+=1
        return count



    def che_distance(self,start,goal):
        return max(abs(start[0]-goal[0]),abs(start[1]-goal[1]))
    def water_traversal(self,node,gamer):
        node.set_visited(True)
        if gamer.have_stones >0:
            print('set water on land')
            node.set_material==' '
            gamer.have_stones-=1

        if node.get_North().get_material() == '~'and node.get_North().get_visited()==False:
            if gamer.face != 'N':
                return self.turn_and_go(gamer,'N')
            else:
                self.return_back.append('F')
                self.return_back.append('S')
                return 'F'

        if node.get_East().get_material() == '~' and node.get_East().get_visited()==False:
            if gamer.face != 'E':
                return self.turn_and_go(gamer,'E')
            else:
                self.return_back.append('F')
                self.return_back.append('W')
                return 'F'
        if node.get_South().get_material() == '~' and node.get_South().get_visited()==False:
            if gamer.face != 'S':
                return self.turn_and_go(gamer,'S')
            else:
                self.return_back.append('F')
                self.return_back.append('N')
                return 'F'

        if node.get_West().get_material() == '~' and node.get_West().get_visited()==False:
            if gamer.face != 'W':
                return self.turn_and_go(gamer,'W')
            else:
                self.return_back.append('F')
                self.return_back.append('E')
                return 'F'
        if len(self.return_back) > 0:
            if self.return_back[-1] == 'F' :
                if self.facing !=gamer.face:
                    return self.turn_and_go(gamer,self.facing)
                else:
                    return self.return_back.pop(-1)
            else:
                self.facing=self.return_back.pop(-1)
                if self.facing == gamer.face:
                    return self.return_back.pop(-1)
                else:
                    return self.turn_and_go(gamer,self.facing)
        else:
            self.decision = "Count"
            return '  '
