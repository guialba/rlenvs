import numpy as np  


class Hunting:
    def __init__(self, 
                 width=15, 
                 height=15
                ):
        
        self.width = width
        self.height = height

        self.S = np.arange((width*height)**2)
        self.A = np.arange(4)

        self.reset()
    
    def reset(self):
        self.c = np.random.randint(0,4)
        self.pray = np.random.randint(0,self.width) + (self.height-5)*self.width
        self.agent = self.width//2 + 4*self.width
        self.r = -1
        self.s = self.compose_state(self.agent, self.pray)

    def last(self):
        return self.s, self.r, (self.agent == self.pray), None, None
    def step(self, s,a):
        self.r = self.R(s)
        self.agent, self.pray = self.grid_move(s,a)
        self.s = self.compose_state(self.agent, self.pray)
        # self.s = np.random.choice(self.S, p=[self.T(s,a,s_) for s_ in self.S])
        return self.last()

    def compose_state(self, agent, pray):
        size = self.height * self.width
        sx,sy = np.meshgrid(np.arange(size),np.arange(size))
        grid = np.vstack([sx.ravel(), sy.ravel()])
        return np.argwhere([p==(agent, pray) for p in zip(*grid)])[0][0]
    def factor_state(self, s):
        size = self.height * self.width
        sx,sy = np.meshgrid(np.arange(size),np.arange(size))
        grid = np.vstack([sx.ravel(), sy.ravel()])
        return tuple(grid[:,s])
    def grid_move(self, s, a):
        agent, pray = self.factor_state(s)
        # contrói grid
        sx,sy = np.meshgrid(np.arange(self.width),np.arange(self.height))
        grid = np.vstack([sx.ravel(), sy.ravel()])
        # contrói ações
        acts = np.array([[0,0,1,-1], [1,-1,0,0]])
        # aplica ações no grid
        aM = grid[:,agent] + acts[:,a]
        pM = grid[:,pray] + acts[:,self.c]

        # aplica regras de torus
        limits = (self.width, self.height)
        agentM = tuple([v%l for v,l in zip(aM,limits)])
        prayM = tuple([v%l for v,l in zip(pM,limits)])

        # extrai a posicao enumerada
        agent = np.argwhere([p==agentM for p in zip(*grid)])[0][0]
        pray = np.argwhere([p==prayM for p in zip(*grid)])[0][0]
        return agent, pray

    def T(self, s,a,s_):
        agent, pray = self.factor_state(s)
        if agent == pray: # agente pegou a presa, portanto a prob de sair é 0
            return 0 if s!=s_ else 1
    
        agent, pray = self.grid_move(s,a)    
        if s_ == self.compose_state(agent, pray):
            return 1
        else: 
            return 0
    
    def R(self, s,a=None,s_=None):
        agent, pray = self.factor_state(s)
        return int(pray == agent)-1
    
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
                    if i == self.pray:
                        content = 'o'
                    if i == self.agent:
                        content = '^.^'                    
                elif type(label) == type([]):
                    content = str(mask[label[i]]) if mask is not None else str(label[i])
                elif type(label) == type({}):
                    if i in label:
                        content = str(mask[label[i]]) if mask is not None else str(label[i])
                    else:
                        content = ' '

                elif label:
                    content = str(i+1)
                frame += f'|{content.center(5)}'
                i += 1
            frame += '|\n' 
            for x in range(self.width):
                frame += '|_____' 
            frame += '|\n' 
            
        print(frame)

