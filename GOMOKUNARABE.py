import numpy as np
import tkinter
import tkinter.messagebox

"""定数宣言"""
#マスの状態
EMPTY=0
WHITE=-1
BLACK=1
WALL=2

#ボードのサイズ(オセロの大きさ)
BOARD_SIZE=8

#方向(２進数)
NONE=0
LEFT=2**0
UPPER_LEFT=2**1
UPPER=2**2
UPPER_RIGHT=2**3
RIGHT=2**4
LOWER_RIGHT=2**5
LOWER=2**6
LOWER_LEFT=2**7

#囲碁の大きさ用
"""
IN_ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
'p','q','r','s']
IN_NUMBER = ['A','B','C','D','E','F','G','H','I','J','K',
'L','M','N','O','P','Q','R','S']"""

#オセロの大きさ用
IN_ALPHABET = ['a','b','c','d','e','f','g','h']
IN_NUMBER = ['A','B','C','D','E','F','G','H']

# 手数の上限
MAX_TURNS = 361

"""ボードの再現"""
class Board:
    def __init__(self):
        #全マスを空きますに設定
        self.RawBoard=np.zeros((BOARD_SIZE+2,BOARD_SIZE+2),dtype=int)

        #壁を設定
        self.RawBoard[0,:]=WALL
        self.RawBoard[:,0]=WALL
        self.RawBoard[BOARD_SIZE+1,:]=WALL
        self.RawBoard[:,BOARD_SIZE+1]=WALL

        """ #初期配置
        self.RawBoard[4,4]=WHITE
        self.RawBoard[5,5]=WHITE
        self.RawBoard[4,5]=BLACK
        self.RawBoard[5,4]=BLACK """

        #手番
        self.Turns=0

        #現在の手番の色
        self.CurrentColor=BLACK

        #五個並んだかどうか（初期値ゼロの配列を作っている）
        self.CheckmatePos=np.zeros((BOARD_SIZE+2,BOARD_SIZE+2),dtype=int)

        #CheckmatePosの初期化
        self.initCheckmatePos()

        #終了したかどうかを判定する
        self.isFinished=False

        """五個並んだかどうかチェック"""
    def findCheckmatePos(self,x,y,color):
        #注目しているマスに置いたときに終局するかどうかの情報が入る（bool型）

        #既に石がある場合はダメ
        if(self.RawBoard[x,y]!=EMPTY):
            return False

        ##左
        if(self.RawBoard[x-1,y]==color):
            x_tmp=x-2
            y_tmp=y
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp-=1
                count+=1
            
            if(count>=5):
                return True

        ##左上
        if(self.RawBoard[x-1,y-1]==color):
            x_tmp=x-2
            y_tmp=y-2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp-=1
                y_tmp-=1
                count+=1
            
            if(count>=5):
                return True

        ##左上
        if(self.RawBoard[x-1,y-1]==color):
            x_tmp=x-2
            y_tmp=y-2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp-=1
                y_tmp-=1
                count+=1
            
            if(count>=5):
                return True
        
        ##上
        if(self.RawBoard[x,y-1]==color):
            x_tmp=x
            y_tmp=y-2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                y_tmp-=1
                count+=1
            
            if(count>=5):
                return True
        
        ##右上
        if(self.RawBoard[x+1,y-1]==color):
            x_tmp=x+2
            y_tmp=y-2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp+=1
                y_tmp-=1
                count+=1
            
            if(count>=5):
                return True

        ##右
        if(self.RawBoard[x+1,y]==color):
            x_tmp=x+2
            y_tmp=y
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp+=1
                count+=1
            
            if(count>=5):
                return True
        
        ##右下
        if(self.RawBoard[x+1,y+1]==color):
            x_tmp=x+2
            y_tmp=y+2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp+=1
                y_tmp+=1
                count+=1
            
            if(count>=5):
                return True

        ##下
        if(self.RawBoard[x,y+1]==color):
            x_tmp=x
            y_tmp=y+2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                y_tmp+=1
                count+=1
            
            if(count>=5):
                return True

        ##左下
        if(self.RawBoard[x-1,y+1]==color):
            x_tmp=x-2
            y_tmp=y+2
            count=1

            #自分の石が続いているだけループ
            while self.RawBoard[x_tmp,y_tmp]==color:
                x_tmp-=1
                y_tmp+=1
                count+=1
            
            if(count>=5):
                return True
        
        ##どの方向でも五個並んでなかったらFalse
        return False


    """手番での操作まとめ"""
    def setDiscs(self,x,y):
        #置く位置が正しいかチェック
        if x<1 or BOARD_SIZE<x:
            return False
        if y<1 or BOARD_SIZE<y:
            return False
        
        #石を置く
        #既に置かれていたらダメ
        if self.RawBoard[x,y]!=EMPTY:
            return False
        else:
            self.RawBoard[x,y]=self.CurrentColor

        return True

    def initCheckmatePos(self):
        self.CheckmatePos[:,:]=False

        #壁以外の全てのマスに対してループ
        for x in range(1,BOARD_SIZE+1):
            for y in range(1,BOARD_SIZE+1):

                if(self.findCheckmatePos(x,y,self.CurrentColor)):
                    self.CheckmatePos[x,y]=True
    
    """終局判定"""
    def isGameOver(self,x,y):
        #最大ターン数に到達したら終了
        if self.Turns>=MAX_TURNS:
            return True
        
        #五個並んだら終了
        if (self.CheckmatePos[:,:].any()):
            return True
        
        return False

    """表示用の関数"""
    def display(self):

        print(' abcdefgh')

        for y in range(1,BOARD_SIZE+1):
            print(IN_NUMBER[y-1],end="")

            for x in range(1,BOARD_SIZE+1):
                grid=self.RawBoard[x,y]
                if grid==EMPTY:
                    print('□',end="")
                if grid==WHITE:
                    print('×',end="")
                if grid==BLACK:
                    print('●',end="")
            print()

    def checkIN(self,IN):
        if not IN:
            return False
        
        if len(IN)<2:
            return False
        
        if IN[0] in IN_ALPHABET:
            if IN[1] in IN_NUMBER:
                return True
        return False
    

"""メインコード"""

#ボードインスタンスの作成
board=Board()

#手番ループ
while True:
    #盤面の表示
    board.display()
    
    """テスト用
    print("findCheckmatePosの表示")
    for y in range(1,20):
        for x in range(1,20):
            if(board.findCheckmatePos(x,y,board.CurrentColor)):
                print("T",end="")
            else:
                print("F",end="")
        print()"""

    #手番の表示
    if board.CurrentColor==BLACK:
        print("●の番です:",end="")
    else:
        print("×の番です:",end="")
        
    IN=input()
    print()

    if board.checkIN(IN):
        x=IN_ALPHABET.index(IN[0])+1
        y=IN_NUMBER.index(IN[1])+1
    else:
        print("正しい形式（例：aC）で入力してください")
        continue
    
    #手番を進める
    board.Turns+=1

    #手を打つ
    if not board.setDiscs(x,y):
        print("そこには置けません")
        continue

    #CheckmatePosの更新
    board.initCheckmatePos()

    #終局判定
    if (board.isGameOver(x,y)):
        board.display()
        print()
        print("終局")
        break

    #手番を交代する
    board.CurrentColor=-board.CurrentColor

#終局時の表示
print()
winner=board.CurrentColor

print(board.Turns,"手")

if winner==1:
    print("●の勝ちです")
else:
    print("×の勝ちです")
print()







        
        
            

    




            







        


