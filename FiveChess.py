class fiveChess:

    size = 15

    def __init__(self):
        self.checkerboard = [[0 for _ in range(15)] for _ in range(15)]
        self.ks = [(0,1),(1,1),(1,0),(1,-1)]
        self.color = 1
        self.order = []

    def set_in(self, position: tuple, color: int):
        x = position[0]
        y = position[1]
        self.checkerboard[y][x] = color
        self.color = color
        self.order.append((x,y))

    def remove(self):
        if self.order:
            position = self.order.pop()
            self.checkerboard[position[1]][position[0]] = 0
            self.color *= -1
            return True
        else:
            return False
    
    def clear(self):
        for j in range(15):
            for i in range(15):
                self.checkerboard[j][i] = 0
        self.order.clear()
        self.color = 1
    
    def is_void(self, position: tuple):
        if self.checkerboard[position[1]][position[0]] == 0:
            return True
        else:
            return False

    def is_win(self, position:tuple):
        for k in self.ks:
            k_r = (k[0]*(-1), k[1]*(-1))
            num = self.count_k(k, 1, position)
            num = self.count_k(k_r, num, position)
            if num >= 5:
                return True
        else:
            return False
            
    def count_k(self, k, num, position: tuple):
        p_n = [position[0]+k[0], position[1]+k[1]]
        if 0 <= p_n[1] <= 14 and 0 <= p_n[0] <= 14:
            if self.checkerboard[p_n[1]][p_n[0]] == self.color:
                num += 1
                num = self.count_k(k, num, p_n)
        return num
