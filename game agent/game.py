class gamer():
    def __init__(self):
        self.position=(80,80)
        self.face = 'S'
        self.stone_getable= []
        self.stone_ungetable=[]
        self.stones=[]
        self.have_stones=0
        self.graph=None
        self.tree =[]
        self.tree_ungetable =[]
        self.tree_getable =[]
        self.key =[]
        self.axe=[]
        self.door=[]
        self.have_raft = False
        self.treasure=None
        self.have_treasure=False
        self.have_key = False
        self.have_axe = False
    def total_stone(self):
        return self.stone_count+len(self.stone)
    # def have_key(self):
    #     return len(self.key)>0
    # def have_aex(self):
    #     return  len(self.aex)>0
    def total_tree(self):
        return len(self.tree)
    def get_node(self):
        return self.graph[self.position[0]][self.position[1]]
