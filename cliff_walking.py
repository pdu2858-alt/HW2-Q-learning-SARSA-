class CliffWalkingEnv:
    def __init__(self, width=12, height=4):
        self.width = width
        self.height = height
        self.start_state = (height - 1, 0) # (3, 0)
        self.goal_state = (height - 1, width - 1) # (3, 11)
        # cliff is bottom row from col 1 to 10
        self.cliff = [(height - 1, i) for i in range(1, width - 1)]
        self.current_state = self.start_state

        # actions: 0: up, 1: right, 2: down, 3: left
        self.actions = [0, 1, 2, 3]

    def reset(self):
        self.current_state = self.start_state
        return self.current_state

    def step(self, action):
        r, c = self.current_state
        
        if action == 0:   # up
            r = max(0, r - 1)
        elif action == 1: # right
            c = min(self.width - 1, c + 1)
        elif action == 2: # down
            r = min(self.height - 1, r + 1)
        elif action == 3: # left
            c = max(0, c - 1)
            
        next_state = (r, c)
        
        # Check if in cliff
        if next_state in self.cliff:
            reward = -100
            next_state = self.start_state
            done = False
        elif next_state == self.goal_state:
            reward = -1
            done = True
        else:
            reward = -1
            done = False
            
        self.current_state = next_state
        return next_state, reward, done
