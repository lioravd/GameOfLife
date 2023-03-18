#import game_of_life_interface
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2


class GameOfLife():  # This is the way you construct a class that inherits properties
    def __init__(self, size_of_board, board_start_mode, rules, rle="", pattern_position=(0,0)):

        self.size_of_board = size_of_board
        self.board_start_mode = board_start_mode
        self.rules = rules
        self.rle = rle
        self.pattern_position = pattern_position
        self.board = [[0 for i in range(size_of_board)] for j in range(size_of_board)]
        self.start_mode()




    def start_mode(self):
        if type(self.pattern_position) != tuple:
            self.pattern_position = (0,0)
        if self.rle!="":
            self.board=self.transform_rle_to_matrix(self.rle)
        else:
            if self.board_start_mode == 4:
              self.pattern_position = (10, 10)
              self.board = self.transform_rle_to_matrix("24bo11b$22bobo11b$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o14b$2o8bo3bob2o4bobo11b$10bo5bo7bo11b$11bo3bo20b$12b2o!")
            elif self.board_start_mode == 1:
               self.board=np.random.choice([0,255], [self.size_of_board, self.size_of_board] , p=[0.5,0.5])
            elif  self.board_start_mode == 2:
               self.board = np.random.choice([0, 255], [self.size_of_board, self.size_of_board], p=[0.2, 0.8])
            elif  self.board_start_mode == 3:
               self.board = np.random.choice([0, 255], [self.size_of_board, self.size_of_board], p=[0.8, 0.2])
            else:
                self.board = np.random.choice([0, 255], [self.size_of_board, self.size_of_board], p=[0.5, 0.5])


    def B_rules(self):
        B=[]
        c=self.rules.index("/")
        for i in range(len(self.rules)):
            if self.rules[i].isnumeric():
                if i<c:
                    B.append(self.rules[i])
        return B

    def S_rules(self):
        S = []
        c = self.rules.index("/")
        for i in range(len(self.rules)):
            if self.rules[i].isnumeric():
                if i > c:
                    S.append(self.rules[i])
        return S


    def update(self):

        a = self.size_of_board
        b=  self.size_of_board
        board = self.board
        B=self.B_rules()
        S=self.S_rules()


        newboard= [[0 for k in range(self.size_of_board)] for l in range(self.size_of_board)]

        for i in range(a):
            for j in range(b):
                neighbors=0
                if board[i%self.size_of_board][(j+1)%self.size_of_board] == 255:
                   neighbors +=1
                if board[(i-1)%self.size_of_board][(j+1)%self.size_of_board] == 255:
                    neighbors += 1
                if board[(i+1)%self.size_of_board][(j+1)%self.size_of_board] == 255:
                   neighbors +=1
                if board[(i-1)%self.size_of_board][j%self.size_of_board] == 255:
                   neighbors += 1
                if board[(i+1)%self.size_of_board][j%self.size_of_board] == 255:
                   neighbors +=1
                if board[(i+1)%self.size_of_board][(j-1)%self.size_of_board] == 255:
                   neighbors += 1
                if board[i%self.size_of_board][(j-1)%self.size_of_board] == 255:
                   neighbors +=1
                if board[(i-1)%self.size_of_board][(j-1)%self.size_of_board] == 255:
                   neighbors += 1

                for y in B:
                    if int(y)==neighbors:
                        if board[i][j]==0:
                            newboard[i][j]=255
                for u in S:
                    if int(u)==neighbors:
                         if board[i][j] == 255:
                              newboard[i][j] = 255


        self.board=newboard


    def save_board_to_file(self, file_name):
        plt.imsave(file_name , self.board)



    def display_board(self):
        plt.imshow(self.board)
        plt.pause(0.6)
        plt.close()
        plt.show()


    def run(self, num_of_iterations):
        self.start_mode()
        self.display_board()
        for i in range(num_of_iterations):
            self.update()
            self.display_board()



    def return_board(self):
        if not(isinstance(self.board, list)):
            return self.board.tolist()
        return self.board

    def decrement_line(self, i, num_of_dec):
        #return (i%self.size_of_board) + num_of_dec
        i+=num_of_dec
        return i

    def init_dead_cell(self, i, j, num_of_deadcells):
        for k in range(0, num_of_deadcells):
            self.board[i% self.size_of_board][j % self.size_of_board] = 0
            j += 1

        return j % self.size_of_board

    def init_live_cell(self, i, j, num_of_livecells):
        for k in range(0, num_of_livecells):
            self.board[i% self.size_of_board][j % self.size_of_board] = 255
            j += 1
        return j % self.size_of_board


    def transform_rle_to_matrix(self, rle):
        i = self.pattern_position[0]
        j = self.pattern_position[1]
        num_of_ops = 1
        seen_number = False
        for char in rle:
            if char == 'b':
                j = self.init_dead_cell(i, j, num_of_ops)
                num_of_ops = 1
                seen_number = False
            elif char == 'o':
                j = self.init_live_cell(i, j, num_of_ops)
                num_of_ops = 1
                seen_number = False
            elif char == '$':
                i = self.decrement_line(i, num_of_ops)
                j=self.pattern_position[1]
                num_of_ops = 1
                seen_number = False
                if i>self.size_of_board:
                    i=0
            elif char.isdigit():
                if seen_number:
                    num_of_ops = num_of_ops * 10 + int(char)
                else:
                    num_of_ops = int(char)
                    seen_number = True
            elif char == '!':
                break
        return self.board



if __name__ == '__main__':# You should keep this line for our auto-grading code.
#    a=GameOfLife(100,4,"B3/S23",  "5b3o11b3o5b$4bo3bo9bo3bo4b$3b2o4bo7bo4b2o3b$2bobob2ob2o5b2ob2obobo2b$b2obo4bob2ob2obo4bob2ob$o4bo3bo2bobo2bo3bo4bo$12bobo12b$2o7b2obobob2o7b2o$12bobo12b$6b3o9b3o6b$6bo3bo9bo6b$6bobo4b3o11b$12bo2bo4b2o5b$15bo11b$11bo3bo11b$11bo3bo11b$15bo11b$12bobo!",(40,40))
    b=GameOfLife(100,4,"B3/S23")
    b.run(270)
    b.display_board()












