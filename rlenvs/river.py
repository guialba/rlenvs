import numpy as np  


class River:
    def __init__(self, 
                 width=5, 
                 height=2,
                 river = [1,2,3],
                 S0 = [0],
                 G = [4]
                ):
        
        self.width = width
        self.height = height

        self.S0 = S0
        self.river = river
        self.G = G

        self.S = np.arange(width*height)
        self.A = np.arange(4)

        self.s = np.random.choice(self.S0)
        self.r = -1

    def T(self, s,a,s_):
        if s in self.G: # Meta é um estado absorvedor, portanto a prob de sair é 0
            return 0 if s!=s_ else 1
        
        m=None
        allowed_move = False
        try:
            # contrói grid e ações
            sx,sy = np.meshgrid(np.arange(self.width),np.arange(self.height))
            grid = np.vstack([sx.ravel(), sy.ravel()])
            acts = np.array([[0,0,1,-1], [1,-1,0,0]])
            m = grid[:,s] + acts[:,a]
            
            # valida movimento
            allowed_move = all(m == grid[:,s_])
            # move_s = np.where((grid[0] == m[0]) & (grid[1] == m[1]))[0][0]
        except:
            return 0 

        if not allowed_move: # Movimento não permitido 
            if s_ == 0 and s in self.river: 
                return .5 
            else: # Movimento no grid
                if 0<=m[0]<self.width and 0<=m[1]<self.height:
                    return 0
                else: # Movimento para fora do grid matem a posição
                    return 0 if s!=s_ else (1, .5)[s in self.river]
        else:
            if s_ == 0 and s in self.river:
                return 1
            else:
                return .5 if s in self.river else 1
                # return .5 if s in self.river or s_ in self.river else 1
    
    def R(self, s,a=None,s_=None):
        # return int(self.T(s,a,s_)>0 and s_ in self.G)-1
        return int(s in self.G)-1
        # return int(s in self.G)

    def reset(self):
        self.s = np.random.choice(self.S0)
        self.r = -1
    def last(self):
        return self.s, self.r, (self.s in self.G), None, None
    def step(self, s,a):
        self.r = self.R(s)
        if sum([self.T(s,a,s_) for s_ in self.S]) != 1:
            print("Err: ",s,a)
        self.s = np.random.choice(self.S, p=[self.T(s,a,s_) for s_ in self.S])
        return self.last()

    
    # def plot(self, func=None, mask=None):
    #     func = func or (lambda x: 'x' if x == self.s else ' ')
    #     mask = ['\u2191', '\u2193', '\u2192', '\u2190'] if mask else None
    #     x=self.width-1
    #     frame = ' '
    #     frame += '______'*self.width + '\b \n'
    #     i = 0
    #     for y in range(self.height-1, -1, -1):
    #         i = y * (x+1)
    #         for x in range(self.width-1, -1, -1):
    #             content = str(mask[func[i]]) if mask is not None else str(func[i])
    #             frame += f'|{content.center(5)}'
    #             i += 1
    #         frame += '|\n' 
    #         for x in range(self.width):
    #             frame += '|_____' 
    #         frame += '|\n' 
            
    #     print(frame)

    def plot(self, label=None, mask=None):
        '''
        
        '''
        mask = ['\u2191', '\u2193', '\u2192', '\u2190'] if mask else None
        x=self.width-1
        frame = ' '
        frame += '______'*self.width + '\b \n'
        i = 0
        for y in range(self.height-1, -1, -1):
            i = y * (x+1)
            for x in range(self.width-1, -1, -1):
                if label is None:
                    content = ''
                elif type(label) == type([]):
                    content = str(mask[label[i]]) if mask is not None else str(label[i])
                elif type(label) == type({}):
                    if i in label:
                        content = str(mask[label[i]]) if mask is not None else str(label[i])
                    else:
                        content = ' '

                elif label:
                    content = str(i)
                frame += f'|{content.center(5)}'
                i += 1
            frame += '|\n' 
            for x in range(self.width):
                frame += '|_____' 
            frame += '|\n' 
            
        print(frame)

