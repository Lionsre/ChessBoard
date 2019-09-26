import os
import re

mark_dict={"1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,
           "A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
pieceNumber_dict = {"Pawn": 1, "Rook": 2, "Knight": 3, "Bishop": 4, "Queen": 5, "King": 6}
pieceIcon_white_dict = {"Pawn": "♙", "Rook": "♖", "Knight": "♘", "Bishop": "♗", "Queen": "♕", "King": "♔"}
pieceIcon_black_dict = {"Pawn": "♟", "Rook": "♜", "Knight": "♞", "Bishop": "♝", "Queen": "♛", "King": "♚"}
initChessBoard = [[2,3,4,5,6,4,3,2],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,3,4,5,6,4,3,2]]
#initChessBoard = [[2,3,4,5,6,4,3,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[2,3,4,5,6,4,3,2]]


#白方为0，黑方为1，全选为其他值（默认-1）
class Piece:
    def __init__(self,camp):
        self.camp = camp
        self.predict = []
        self.class_name = self.__class__.__name__


class Pawn(Piece):
    def __init__(self,camp):
        Piece.__init__(self,camp)
        if camp == 0:
            self.name = pieceIcon_white_dict[self.class_name]
        else:
            self.name = pieceIcon_black_dict[self.class_name]
        self.number = pieceNumber_dict[self.class_name]
        self.isFirstStep = True
        self.attack = []


class Rook(Piece):
    def __init__(self, camp):
        Piece.__init__(self, camp)
        if camp == 0:
            self.name = pieceIcon_white_dict[self.class_name]
        else:
            self.name = pieceIcon_black_dict[self.class_name]
        self.number = pieceNumber_dict[self.class_name]


class Knight(Piece):
    def __init__(self, camp):
        Piece.__init__(self, camp)
        if camp == 0:
            self.name = pieceIcon_white_dict[self.class_name]
        else:
            self.name = pieceIcon_black_dict[self.class_name]
        self.number = pieceNumber_dict[self.class_name]


class Bishop(Piece):
    def __init__(self, camp):
        Piece.__init__(self, camp)
        if camp == 0:
            self.name = pieceIcon_white_dict[self.class_name]
        else:
            self.name = pieceIcon_black_dict[self.class_name]
        self.number = pieceNumber_dict[self.class_name]


class Queen(Piece):
    def __init__(self, camp):
        Piece.__init__(self, camp)
        if camp == 0:
            self.name = pieceIcon_white_dict[self.class_name]
        else:
            self.name = pieceIcon_black_dict[self.class_name]
        self.number = pieceNumber_dict[self.class_name]


class King(Piece):
    def __init__(self, camp):
        Piece.__init__(self, camp)
        if camp == 0:
            self.name = pieceIcon_white_dict[self.class_name]
        else:
            self.name = pieceIcon_black_dict[self.class_name]
        self.number = pieceNumber_dict[self.class_name]


class ChessBoard: # 以棋盘为参照，横坐标（等效直角坐标系中的X轴）为j，纵坐标（等效直角坐标系中的Y轴）为i
    chess_round = 0
    king_position = [[],[]]
    step_record = []
    isSurround = False
    isStepEnd = False
    def __init__(self):
        self.column = 8
        self.raw = 8
        self.board = []
        for i in range(self.column):
            self.board.append([])
            if i <= 3: camp = 0
            else: camp = 1
            for j in range(self.raw):
                if initChessBoard[i][j] == pieceNumber_dict["Pawn"]:
                    self.board[i].append(Pawn(camp))
                elif initChessBoard[i][j] == pieceNumber_dict["Rook"]:
                    self.board[i].append(Rook(camp))
                elif initChessBoard[i][j] == pieceNumber_dict["Knight"]:
                    self.board[i].append(Knight(camp))
                elif initChessBoard[i][j] == pieceNumber_dict["Bishop"]:
                    self.board[i].append(Bishop(camp))
                elif initChessBoard[i][j] == pieceNumber_dict["Queen"]:
                    self.board[i].append(Queen(camp))
                elif initChessBoard[i][j] == pieceNumber_dict["King"]:
                    self.board[i].append(King(camp))
                    ChessBoard.king_position[camp] = [i,j]
                else:self.board[i].append(None)

    def Pawn_Predict(self,i,j): # 主要思路：直进斜吃，排除法
        if self.board[i][j].camp == 0:  # 判断黑白方士兵前进方向
            piece_step = 1
        else: piece_step = -1
        if self.board[i][j].isFirstStep:
            firstStep = [[i + piece_step * 2, j], [i + piece_step, j]]
            if piece_step == -1: return (firstStep,[])
            else:
                firstStep[0],firstStep[1] = firstStep[1],firstStep[0]
                return (firstStep,[])
        pawn_predict = [[i + piece_step, j-1],[i + piece_step, j],[i + piece_step, j+1]]
        pawn_attack = []
        for number in range(len(pawn_predict)-1,-1,-1):
            if pawn_predict[number][1] < 0 or pawn_predict[number][1] > 7:
                pawn_predict.remove(pawn_predict[number])
                continue
            if self.board[pawn_predict[number][0]][pawn_predict[number][1]] and pawn_predict[number][1] == j:
                pawn_predict.remove(pawn_predict[number])
            elif not self.board[pawn_predict[number][0]][pawn_predict[number][1]] and pawn_predict[number][1] != j:
                pawn_predict.remove(pawn_predict[number])
            else:
                if self.board[pawn_predict[number][0]][pawn_predict[number][1]]:
                    if self.board[pawn_predict[number][0]][pawn_predict[number][1]].camp == self.board[i][j].camp:
                        pawn_predict.remove(pawn_predict[number])
                    else:pawn_attack.append(pawn_predict[number])
        return (pawn_predict,pawn_attack)

    def Rook_Predict(self, i, j):# 主要思路：针对四个方向进行判断，遇到棋子在判断敌我后返回坐标退出循环
        rook_predict = []
        for rook_N in range(i, 8): # 上
            if rook_N == i: continue
            if not self.board[rook_N][j]:
                rook_predict.append([rook_N, j])
            elif self.board[rook_N][j].camp != self.board[i][j].camp:
                rook_predict.append([rook_N, j])
                break
            else: break
        for rook_S in range(i, -1, -1): # 下
            if rook_S == i: continue
            if not self.board[rook_S][j]:
                rook_predict.append([rook_S, j])
            elif self.board[rook_S][j].camp != self.board[i][j].camp:
                rook_predict.append([rook_S, j])
                break
            else: break
        for rook_E in range(j, 8): # 右
            if rook_E == j: continue
            if not self.board[i][rook_E]:
                rook_predict.append([i, rook_E])
            elif self.board[i][rook_E].camp != self.board[i][j].camp:
                rook_predict.append([i, rook_E])
                break
            else: break
        for rook_W in range(j, -1, -1): # 左
            if rook_W == j: continue
            if not self.board[i][rook_W]:
                rook_predict.append([i, rook_W])
            elif self.board[i][rook_W].camp != self.board[i][j].camp:
                rook_predict.append([i, rook_W])
                break
            else: break
        return rook_predict

    def Knight_Predict(self, i, j): # 主要思路：八个固定走位，排除法
        knight_predict = [[i + 1, j - 2], [i + 2, j - 1], [i + 2, j + 1], [i + 1, j + 2], [i - 1, j + 2],
                          [i - 2, j + 1], [i - 1, j - 2], [i - 2, j - 1]]
        for number in range(len(knight_predict) - 1, -1, -1):
            if knight_predict[number][0] < 0 or knight_predict[number][0] > 7 or knight_predict[number][1] < 0 or \
                    knight_predict[number][1] > 7:
                knight_predict.remove(knight_predict[number])
                continue
        for number in range(len(knight_predict) - 1, -1, -1):
            if self.board[knight_predict[number][0]][knight_predict[number][1]]:
                if self.board[knight_predict[number][0]][knight_predict[number][1]].camp == self.board[i][j].camp:
                    knight_predict.remove(knight_predict[number])
        return knight_predict

    def Bishop_Predict(self, i, j): # 主要思路：四方斜进，同战车思路
        bishop_predict = []
        for bishop_NE in range(1,8):
            x = j + bishop_NE
            y = i + bishop_NE
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j < 7 and i < 7: #右上
                if not self.board[y][x]:bishop_predict.append([y,x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    bishop_predict.append([y,x])
                    break
                else: break
        for bishop_SE in range(1, 8):
            x = j + bishop_SE
            y = i - bishop_SE
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j < 7 and i > 0: #右下
                if not self.board[y][x]:bishop_predict.append([y,x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    bishop_predict.append([y,x])
                    break
                else: break
        for bishop_NW in range(1, 8):
            x = j - bishop_NW
            y = i + bishop_NW
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j > 0 and i < 7: #左上
                if not self.board[y][x]:bishop_predict.append([y,x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    bishop_predict.append([y,x])
                    break
                else: break
        for bishop_SW in range(1, 8):
            x = j - bishop_SW
            y = i - bishop_SW
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j > 0 and i > 0: #左下
                if not self.board[y][x]:bishop_predict.append([y,x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    bishop_predict.append([y,x])
                    break
                else: break
        return bishop_predict

    def Queen_Predict(self, i, j): # 主要思路：皇后 = 战车 + 主教
        queen_predict = []
        for queen_N in range(i, 8):
            if queen_N == i: continue
            if not self.board[queen_N][j]:
                queen_predict.append([queen_N, j])
            elif self.board[queen_N][j].camp != self.board[i][j].camp:
                queen_predict.append([queen_N, j])
                break
            else: break
        for queen_S in range(i, -1, -1):
            if queen_S == i: continue
            if not self.board[queen_S][j]:
                queen_predict.append([queen_S, j])
            elif self.board[queen_S][j].camp != self.board[i][j].camp:
                queen_predict.append([queen_S, j])
                break
            else: break
        for queen_E in range(j, 8):
            if queen_E == j: continue
            if not self.board[i][queen_E]:
                queen_predict.append([i, queen_E])
            elif self.board[i][queen_E].camp != self.board[i][j].camp:
                queen_predict.append([i, queen_E])
                break
            else: break
        for queen_W in range(j, -1, -1):
            if queen_W == j: continue
            if not self.board[i][queen_W]:
                queen_predict.append([i, queen_W])
            elif self.board[i][queen_W].camp != self.board[i][j].camp:
                queen_predict.append([i, queen_W])
                break
            else: break
        for queen_NE in range(1, 8):
            x = j + queen_NE
            y = i + queen_NE
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j < 7 and i < 7:  # 右上
                if not self.board[y][x]:
                    queen_predict.append([y, x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    queen_predict.append([y, x])
                    break
                else: break
        for queen_SE in range(1, 8):
            x = j + queen_SE
            y = i - queen_SE
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j < 7 and i > 0:  # 右下
                if not self.board[y][x]:
                    queen_predict.append([y, x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    queen_predict.append([y, x])
                    break
                else: break
        for queen_NW in range(1, 8):
            x = j - queen_NW
            y = i + queen_NW
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j > 0 and i < 7:  # 左上
                if not self.board[y][x]:
                    queen_predict.append([y, x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    queen_predict.append([y, x])
                    break
                else: break
        for queen_SW in range(1, 8):
            x = j - queen_SW
            y = i - queen_SW
            if x < 0 or x > 7 or y < 0 or y > 7: break
            if j > 0 and i > 0:  # 左下
                if not self.board[y][x]:
                    queen_predict.append([y, x])
                elif self.board[y][x].camp != self.board[i][j].camp:
                    queen_predict.append([y, x])
                    break
                else: break
        return queen_predict

    def King_Predict(self, i, j): # 主要思路：八个固定走位，先排除不合法，再排除己方，最后根据对方可吃路线排除送子区域
        king_predict = []
        for a in range(i - 1,i + 2):
            for b in range(j - 1,j + 2):
                if a >= 0 and b >= 0 and a <= 7 and b <=7 :
                    if a != i or b != j:
                        king_predict.append([a,b])
        if king_predict:
            for number in range(len(king_predict)-1,-1,-1):
                if self.board[king_predict[number][0]][king_predict[number][1]]:
                    if self.board[king_predict[number][0]][king_predict[number][1]].camp == self.board[i][j].camp:
                        king_predict.remove(king_predict[number])
        if king_predict:
            self.PredictAll(1 - self.board[i][j].camp) #使用PredictAll
            for column in self.board:
                for element in column:
                    if element:
                        if element.camp != self.board[i][j].camp:
                            for number in range(len(king_predict) - 1, -1, -1):
                                if element.number == pieceNumber_dict["Pawn"]:
                                    if king_predict[number] in element.attack:
                                        king_predict.remove(king_predict[number])
                                else:
                                    if king_predict[number] in element.predict:
                                        king_predict.remove(king_predict[number])
        return king_predict

    def King_Predicted(self, i, j): # 对方王棋走位预测
        king_predicted = []
        for a in range(i - 1,i + 2):
            for b in range(j - 1,j + 2):
                if a >= 0 and b >= 0 and a <= 7 and b <=7 and (a != i or b != j):
                    king_predicted.append([a,b])
        if king_predicted:
            for number in range(len(king_predicted)-1,-1,-1):
                if self.board[king_predicted[number][0]][king_predicted[number][1]]:
                    if self.board[king_predicted[number][0]][king_predicted[number][1]].camp == self.board[i][j].camp:
                        king_predicted.remove(king_predicted[number])
        if king_predicted:
            self.PredictKing(1 - self.board[i][j].camp) #使用PredictKing
            for column in self.board:
                for element in column:
                    if element:
                        if element.camp != self.board[i][j]:
                            for number in range(len(king_predicted) - 1, -1, -1):
                                if element.number == pieceNumber_dict["Pawn"] and (king_predicted[number] in element.attack):
                                    king_predicted.remove(king_predicted[number])
                                elif king_predicted[number] in element.predict:
                                    king_predicted.remove(king_predicted[number])
        return king_predicted

    def Predict(self,i,j):
        predict_result = []
        if self.board[i][j] != None:
            if self.board[i][j].number == pieceNumber_dict["Pawn"]:#"Pawn"
                (self.board[i][j].predict,self.board[i][j].attack) = self.Pawn_Predict(i, j)
            elif self.board[i][j].number == pieceNumber_dict["Rook"]: #"Rook"
                self.board[i][j].predict = self.Rook_Predict(i, j)
            elif self.board[i][j].number == pieceNumber_dict["Knight"]: #"Knight"
                self.board[i][j].predict = self.Knight_Predict(i, j)
            elif self.board[i][j].number == pieceNumber_dict["Bishop"]: #"Bishop"
                self.board[i][j].predict = self.Bishop_Predict(i, j)
            elif self.board[i][j].number == pieceNumber_dict["Queen"]: #"Queen"
                self.board[i][j].predict = self.Queen_Predict(i, j)
            elif self.board[i][j].number == pieceNumber_dict["King"]: #"King"
                self.board[i][j].predict = self.King_Predict(i, j)
            predict_result = self.board[i][j].predict
        return predict_result

    def PredictAll(self, camp):#白方为0，黑方为1，全选为其他值（默认-1），我方王棋预测用
        for i in range(self.column):
            for j in range(self.raw):  # """
                if self.board[i][j] != None:
                    if self.board[i][j].camp != camp and (camp == 0 or camp == 1):continue
                    if self.board[i][j].number == pieceNumber_dict["Pawn"]:  # "Pawn"
                        (self.board[i][j].predict, self.board[i][j].attack) = self.Pawn_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Rook"]:  # "Rook"
                        self.board[i][j].predict = self.Rook_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Knight"]:  # "Knight"
                        self.board[i][j].predict = self.Knight_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Bishop"]:  # "Bishop"
                        self.board[i][j].predict = self.Bishop_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Queen"]:  # "Queen"
                        self.board[i][j].predict = self.Queen_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["King"]:  # "King"
                        self.board[i][j].predict = self.King_Predicted(i, j)

    def PredictKing(self, camp):#白方为0，黑方为1，全选为其他值（默认-1），对方王棋预测用
        for i in range(self.column):
            for j in range(self.raw):  # """
                if self.board[i][j] != None:
                    if self.board[i][j].camp != camp and (camp == 0 or camp == 1):continue
                    if self.board[i][j].number == pieceNumber_dict["Pawn"]:  # "Pawn"
                        (self.board[i][j].predict, self.board[i][j].attack) = self.Pawn_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Rook"]:  # "Rook"
                        self.board[i][j].predict = self.Rook_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Knight"]:  # "Knight"
                        self.board[i][j].predict = self.Knight_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Bishop"]:  # "Bishop"
                        self.board[i][j].predict = self.Bishop_Predict(i, j)
                    elif self.board[i][j].number == pieceNumber_dict["Queen"]:  # "Queen"
                        self.board[i][j].predict = self.Queen_Predict(i, j)

    def PredictFixedDisplay(self, chessboard_get, i, j): # 预测走位状态并返回修改后的棋盘显示
        predict_result = self.Predict(i, j)
        for element in predict_result:
            if self.board[element[0]][element[1]]:
                chessboard_get[element[0]][element[1]] = "×"
            else:
                chessboard_get[element[0]][element[1]] = "■"
        return chessboard_get

    def GetCurrentChessboard(self): # 获取当前棋盘状态
        chessboard = []
        for i in range(self.column):
            chessboard.append([])
            for j in range(self.raw):
                if self.board[i][j]:chessboard[i].append(self.board[i][j].name)
                else:chessboard[i].append("〇")
        return chessboard

    def PrintChessboard(self,chessboard): # 控制台输出棋盘
        for line in range(8,0,-1):
            print(line.__str__(),end='')
            print(chessboard[line-1],end="\n\n")
        print("   ",end="")
        print("A     B     C     D     E     F     G     H",end="\n\n")
        return chessboard

    def Move(self,src:list,dst:list): # 行子
        if not self.board[src[0]][src[1]]:return False
        else:
            if self.board[dst[0]][dst[1]]:pass
            self.board[dst[0]][dst[1]] = self.board[src[0]][src[1]]
            self.board[src[0]][src[1]] = None
            if self.board[dst[0]][dst[1]].number == pieceNumber_dict["Pawn"]:
                self.board[dst[0]][dst[1]].isFirstStep = False
            if self.board[dst[0]][dst[1]].number == pieceNumber_dict["King"]:
                ChessBoard.king_position[self.board[dst[0]][dst[1]].camp] = [dst[0],dst[1]]
            return True

    def CheckMate(self):# 将军
        for column in self.board:
            for element in column:
                if element:
                    if element.camp != self.board[ChessBoard.king_position[ChessBoard.chess_round][0]][ChessBoard.king_position[ChessBoard.chess_round][1]].camp and ([ChessBoard.king_position[ChessBoard.chess_round][0], ChessBoard.king_position[ChessBoard.chess_round][1]] in element.predict):
                        return True
        return False


if __name__ == "__main__":
    chessboard = ChessBoard()
    chessboard_get = chessboard.GetCurrentChessboard()
    while True: # 以棋盘为参照，横坐标（等效直角坐标系中的X轴，棋盘中的字母部分）为j，纵坐标（等效直角坐标系中的Y轴，棋盘中的数字部分）为i
        ChessBoard.isStepEnd = False
        campstr = ["白方","黑方"]
        while True: # 选子
            if chessboard.isSurround: break
            os.system("cls")
            chessboard_get = chessboard.GetCurrentChessboard()
            chessboard.PrintChessboard(chessboard_get) #输出正常棋盘
            if chessboard.CheckMate():
                print("Check Mate Attention！！！\n{}的国王面临危机！（如不应将则判输）".format(campstr[ChessBoard.chess_round]))
            piece_select = input("请{}选择棋子（字母在先数字在后，不区分大小写）：".format(campstr[ChessBoard.chess_round])).upper()
            if piece_select == "GG": chessboard.isSurround = True
            if len(piece_select) == 2 and re.match("^[A-H][1-8]$",piece_select):
                i,j= mark_dict[piece_select[1]],mark_dict[piece_select[0]]
                if chessboard.board[i][j]:
                    if chessboard.board[i][j].camp == ChessBoard.chess_round:
                        chessboard_predict = chessboard.PredictFixedDisplay(chessboard_get, i, j)
                        break
                    else:
                        print("不可以抢对方的棋子！")
                        os.system("pause")
        while True: # 落子
            if chessboard.isSurround:break
            if chessboard.board[i][j].predict:
                os.system("cls")
                chessboard.PrintChessboard(chessboard_predict) #输出预测棋盘
                move_select = input("请{}选择落子区域（字母在先数字在后，不区分大小写）：".format(campstr[ChessBoard.chess_round])).upper()
                if move_select == "GG": chessboard.isSurround = True
                if len(move_select) == 2 and re.match("^[A-H][1-8]$", move_select):
                    a,b = mark_dict[move_select[1]],mark_dict[move_select[0]]
                    if [a,b] in chessboard.board[i][j].predict:
                        chessboard.Move([i,j],[a,b])
                        ChessBoard.isStepEnd = True
                        break
                elif move_select == "":break
            else:break
        if ChessBoard.isStepEnd == True:
            ChessBoard.step_record.append([i,j,a,b])
            chessboard.Predict(ChessBoard.king_position[ChessBoard.chess_round][0], ChessBoard.king_position[ChessBoard.chess_round][1])
            if chessboard.CheckMate():
                if chessboard.board[ChessBoard.king_position[ChessBoard.chess_round][0]][ChessBoard.king_position[ChessBoard.chess_round][1]].predict:
                    print("{}没能主动应将，故此判输。".format(campstr[ChessBoard.chess_round]))
                else:print("{}无法应将，故此判输。".format(campstr[ChessBoard.chess_round]))
                ChessBoard.chess_round = 1 - ChessBoard.chess_round
                break
        ChessBoard.chess_round = 1 - ChessBoard.chess_round
        if chessboard.isSurround:
            print("{}投降了！".format(campstr[1 - ChessBoard.chess_round]))
            break
    print("{}获得了胜利！".format(campstr[ChessBoard.chess_round]))
