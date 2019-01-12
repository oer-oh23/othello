# -*- coding:utf-8 -*-
import datetime
import random
import csv
import time

time.sleep(0.5)

timestamp = ("{0:%Y%m%d%H%M%S%f}".format(datetime.datetime.now()))
timestamp = (timestamp[2:-4])
csv_file1 = csv.writer(open("./result/{}.csv".format(timestamp), 'w'))
csv_file1.writerow(["No.","color","position"])

csv_file2 = csv.writer(open("./result/all.csv".format(datetime.datetime.now()), 'a'))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Configs
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
TABLE_SIZE = 8
WHITE = 0
BLACK = 1
# human:0
# computer:1~
PLAYER_FLG_B = 0
PLAYER_FLG_W = 0
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# alphabet -> array
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
def div_alpnum(chars):
  alp=0
  num=0

  if chars ==None:
    return None
  else:
    for i in list(chars):
        #print("{} :{}".format(i,ord(i)))
#a-z
        if 97<=ord(i) & ord(i)<=122:
          alp += int(ord(i))
          alp = alp-96
#A-Z -> a-z
        if 65<=ord(i) & ord(i)<=90:
          alp += int(ord(i)+32)
          alp = alp-96
#0-9
        if 48<=ord(i) & ord(i)<=57:
          if num>0:
            num = num*10
          num += int(i)

  #print("----debug-----")
  #print("num :{}".format(num))
  #print("alp :{}".format(alp))
  #print("--------------")
  
  if (alp<=0) | (num<=0) | (alp-1>=TABLE_SIZE) | (num-1>=TABLE_SIZE):
    return None
  else:
    return [alp-1,num-1]
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# array -> alphabet
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
def list_readable(cellslist):
  choice=[]
  if cellslist != None:
    for i in cellslist:
      tmp=""
      tmp+=chr(int(i[0])+97)
      tmp+=chr(int(i[1]+1+48))

      choice.append(tmp)
  return choice
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 1:BLACK  2:WHITE
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
def const_to_char(const):
  if const == WHITE:
    return ("WHITE")
  elif const == BLACK:
    return ("BLACK")
  else:
    return None
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Game Board
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
class GameBoard(object):

  player_flg=BLACK

  def __init__(self):
    self.cells = []
    for i in range(TABLE_SIZE):
      self.cells.append([None for i in range(TABLE_SIZE)])

    self.cells[int(TABLE_SIZE/2-1)][int(TABLE_SIZE/2-1)] = WHITE
    self.cells[int(TABLE_SIZE/2-1)][int(TABLE_SIZE/2  )] = BLACK
    self.cells[int(TABLE_SIZE/2  )][int(TABLE_SIZE/2-1)] = BLACK
    self.cells[int(TABLE_SIZE/2  )][int(TABLE_SIZE/2  )] = WHITE

  def put_stone(self, x, y, player_stone):
    if self.cells[y][x] != None:
      return False

    reversible = self.list_rev_able(x,y,player_stone)
    if reversible == []:
      return False

    self.cells[y][x] = player_stone
    for x,y in reversible:
      self.cells[y][x] = player_stone

    return True

  def list_rev_able(self, x, y, player_stone):
    ANGLE = [-1, 0, 1]
    reversible = []

    for dir_x in ANGLE: 
      for dir_y in ANGLE:
        if (dir_x == 0) & (dir_y == 0):
          continue
        tmp = []
        dist = 0
        while(True):
          dist += 1
          rx = x + (dir_x * dist)
          ry = y + (dir_y * dist)
          if (0 <= rx < TABLE_SIZE) & (0 <= ry < TABLE_SIZE):
            request = self.cells[ry][rx]
            if request == None:
              break
            if request == player_stone:
              if tmp != []:
                reversible.extend(tmp)
            else:
              tmp.append([rx, ry])
          else:
            break
    return reversible

  def list_can_put(self, player_stone):
    possible = []
    for x in range(TABLE_SIZE):
      for y in range(TABLE_SIZE):
        if self.cells[y][x] != None:
          continue
        if self.list_rev_able(x, y, player_stone) == []:
          continue
        else:
          possible.append([x,y])
    return possible


  def show_board(self):
    print("\\ ",end="")

    for k in range(TABLE_SIZE):
      print("{} ".format(chr(ord("a")+k)),end="")
    print()

    for i in range(TABLE_SIZE):
      print("{} ".format(i+1),end="")

      for j in range(TABLE_SIZE):
        if self.cells[i][j]==None:
          print("-",end="")
        elif self.cells[i][j]==BLACK:
          print("b",end="")
        elif self.cells[i][j]==WHITE:
          print("w",end="")
        print(" ",end="")
      print()

    return self.cells
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Judgement
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Judgement():

  c_play_no=1

  score_b=0
  score_w=0

  pass_b = 0
  pass_w = 0

  def __init__(self):
    pass

  def calc_score(self,tableinfo):
    i = 0
    j = 0
    for i in range(len(tableinfo)):
      for j in range(len(tableinfo[0])):
        if tableinfo[i][j] == None:
          pass
        elif tableinfo[i][j] == WHITE:
          self.score_w += 1
        elif tableinfo[i][j] == BLACK:
          self.score_b += 1

  def winner_is(self):
    if self.score_b == self.score_w:
      return ("draw")
    if self.score_b < self.score_w:
      return ("white")
    if self.score_b > self.score_w:
      return ("black")

  def score_b_is(self):
    return (self.score_b)

  def score_w_is(self):
    return (self.score_w)

  def add_play_no(self):
    self.c_play_no += 1
  
  def ret_play_no(self):
    return self.c_play_no

  def c_player(self):
    return int(self.c_play_no % 2)

  def player_pass(self,player_color):
    if player_color == WHITE:
      self.pass_w += 1
    if player_color == BLACK:
      self.pass_b += 1

  def init_pass(self,player_color):
    if player_color == WHITE:
      self.pass_w = 0
    if player_color == BLACK:
      self.pass_b = 0

  def game_status(self):
    if (self.pass_b > 2) & (self.pass_w > 2):
      return 1 #finished
    else:
      return 0 #continue
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Player's Info
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PlayerInfo():
  # human:0
  # computer:1~
  type_w = 0
  type_b = 0

  i_choose = None

  def __init__(self):
    self.type_w = PLAYER_FLG_W
    self.type_b = PLAYER_FLG_B
    pass

  def init_player(self, color, player_type):
    if player_color == WHITE:
      self.type_w = player_type
    if player_color == BLACK:
      self.type_b = player_type

  def ret_player_type(self, color):
    if player_color == WHITE:
      return self.type_w
    if player_color == BLACK:
      return self.type_b
    
  def ret_player_type(self, player):
    if(player == WHITE):
      return self.type_w
    if(player == BLACK):
      return self.type_b

  def select_choices(self, player_type, choices_list):
    if player_type == 0:
      self.i_choose = input()
      if self.i_choose=="" :
        self.i_choose=None
    elif player_type == 1:
      self.i_choose = choices_list[0]
      print(self.i_choose)
    elif player_type == 2:
      rl = choices_list
      out_rl = random.sample(rl,len(rl))
      self.i_choose = out_rl[0]
      print(self.i_choose)
    else:
      self.i_choose = None

    print()
    return self.i_choose
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Main function
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":

  board = GameBoard()
  player = PlayerInfo()
  judgement = Judgement()
  player_color = None
  continue_to_put = None

  print ("table size : {}".format(TABLE_SIZE))
  print ()

  while (True):
    if(judgement.game_status() == 1):
      break

    player_color = judgement.c_player()

    print("\n\nNo.{}+++++++++++++++++++++++++++++++++++++++++++++++++++++++".format(judgement.ret_play_no()))
    board.show_board()

    print("you can choose from:{}".format(list_readable(board.list_can_put(player_color))))
    print("{} >> ".format(const_to_char(player_color)), end="")

    if board.list_can_put(player_color)==[]:
      print("pass")
      judgement.player_pass(player_color)
      judgement.add_play_no()
      continue
    else:
      judgement.init_pass(player_color)

      selected_position = div_alpnum(
        player.select_choices(
          player.ret_player_type(player_color), 
          list_readable(board.list_can_put(player_color))
        )
      )

    if selected_position == None:
      pass
    else:
      #board.put_stone(x,y,player_color)
      continue_to_put = board.put_stone(selected_position[0],selected_position[1],player_color)
      if(continue_to_put == True):
        csv_file1.writerow(
          [
            judgement.ret_play_no(),
            const_to_char(player_color),
            list_readable([selected_position])[0]
          ]
        )
        judgement.add_play_no()

    player_color = None
    continue_to_put = None

    #print("----debug-----")
    #print("(player_color) :{}".format(player_color))
    #print("--------------")

  print("\n\n\n\n\n\nResult +++++++++++++++++++++++++++++++++++++++++++++++++++++")
  print()
  print("No.{}".format(judgement.ret_play_no()-7))
  score_calc_tmp = board.show_board()
  judgement.calc_score(score_calc_tmp)
  print()
  print("White : {}, Black : {}".format(judgement.score_w_is(),judgement.score_b_is()))
  print("Winner is :{}".format(judgement.winner_is()))
  csv_file2.writerow(
    [
      timestamp,
      TABLE_SIZE,
      judgement.winner_is(),
      judgement.score_b_is(),
      judgement.score_w_is(),
      player.ret_player_type(BLACK),
      player.ret_player_type(WHITE),
    ]
  )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++
























