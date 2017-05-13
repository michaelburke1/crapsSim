from random import randint
import sys

board = [0, 0, 0, 0, 0, 0, 0, 0]
odds  = [0, 0, 0, 0, 0, 0, 0]

class Game():
    def __init__(self):
        self.amount = 100
        self.bet    = 5
        self.rolls  = [0, 0, 0, 0, 0, 0, 0]
        self.comes  = 0
        self.comeLimit = 3
        self.comePlace = 7
        self.point = 0
        self.curr = 0

    def roll(self):
        die1 = randint(1,6)
        die2 = randint(1,6)
        self.rolls[0] += 2
        self.rolls[die1] += 1
        self.rolls[die2] += 1
        roll = "1: " + str(die1) + "\n2: " + str(die2)
        print(roll)

        roll = die1 + die2

        return roll

    def makeBet(self):
        if self.amount < self.bet:
            print("game over")
            sys.exit(0)

        if board[0] == 0:
            self.initBet()
        else:
            self.comeBet()

    def initBet(self):
        board[0] += self.bet
        self.amount -= self.bet

    def comeBet(self):
        if self.comes > self.comeLimit:
            print("Have 3 comes placed, no more set")
            return 0

        if odds[0] == 0:
            if self.amount >= 2*self.bet:
                odds[0] += 2*self.bet
                self.amount -= 2*self.bet
        if board[self.comePlace] == 0:
            board[self.comePlace] += self.bet
            self.amount -= self.bet
        for i in range (1, 7):
            if self.amount >= 2*self.bet:
                if board[i] > 0 and odds[i] == 0:
                    odds[i] += 2*self.bet
                    self.amount -= 2*self.bet

    def resetCome(self):
        board[self.comePlace] = 0

    def odds(self, point, amount):
        if point == 4 or point == 10:
            return 2* amount + amount
        elif point == 5 or point == 9:
            return 3 * amount / 2. + amount
        elif point == 6 or point == 8:
            return 6 * amount / 5. + amount

    def rollConvert(self, roll):
        if roll >= 4 and roll <= 6:
            roll -= 3
        elif roll >= 8 and roll <= 10:
            roll -= 4

        return roll

    def settle(self, roll):
        iroll = self.rollConvert(roll)
        if self.curr == 1:
            if roll == 7:
                print("7 was rolled. Crap!")
                self.point = 0
                self.curr = 0
                for i in range (0, 7):
                    board[i] = 0
                    odds[i] = 0
                self.comeLimit = 0
                if board[self.comePlace] > 0:
                    self.amount += 2*board[self.comePlace]
                    self.resetCome()

            elif roll == 11:
                if board[self.comePlace] > 0: 
                    self.amount += board[self.comePlace]
                    self.resetCome()
            
            elif roll == 2 or roll == 3 or roll == 12:
                self.resetCome()
            
            else:
                if self.point == roll:
                    print("Point scored at %d" % roll)
                    self.amount += 2*board[0]
                    self.amount += self.odds(roll, odds[0])
                    board[0] = 0
                    odds[0] = 0
                    board[iroll] = board[self.comePlace]
                    self.comeLimit += 1
                    self.resetCome()
                    self.point = 0

                elif board[iroll] > 0:
                    self.amount += 2*board[iroll]
                    self.amount += self.odds(roll, odds[roll])
                
                else:
                    board[iroll] += self.bet
                    self.amount -= self.bet
                    self.resetCome()
                    self.comeLimit += 1

        else:
            if roll == 7 or roll == 11:
                print("%d rolled, you won %d" % (roll, board[0]))
                self.amount += 2*board[0]
                board[0] = 0

            elif roll == 2 or roll == 3 or roll == 12:
                print("Crap! %d rolled, you lose your pass line bet of %d" %(roll, board[0]))
                board[0] = 0

            else:
                print("Point is set at " + str(roll))
                self.point = roll
                self.amount += 2*board[iroll]
                self.amount += odds[iroll]
                board[iroll] = 0
                odds[iroll] = 0
                #odds[0] += 2*self.bet
                #self.amount -= 2*self.bet
                self.comeBet()
                self.curr = 1
                

    def printStats(self):
        print("Amount: %d\nCurrent Bets: %d\nBetting: %d" %(self.amount, board[0], self.bet))

    def printBoard(self):
        print("  Points:     4           5           6           8           9          10          Point")
        #print("  B/O:     $%d , $%d     $% , $%     $% , $%     $% , $%     $% , $%     $% , $%")
        print("Bet/Odds:  ", end=""),
        for i in range (1,7):
            print("$%d , $%d     " % (board[i], odds[i]),end=""),
        if self.curr == 0:
            print("None")
        else:
            print("Point: %d, $%d , $%d" % (self.point, board[0], odds[0]))
#        print("%d  ,  $%d" % ())
        print("\n\nCome:                                  $%d" % board[self.comePlace])

    def play(self):
        while True:
            self.printStats()
            self.makeBet()
            result = self.roll()
            
            if curr == 1:
                print("point is set at %d, roll was %d" %(self.point, result))
            else:
                print("Point not set, roll is %d" % result)
                
            self.settle(result)
            self.printStats()
            self.printBoard()
            n = input("Roll again? ")
            if n.strip() == 'r':
                continue
            else:
                break
curr = Game()

curr.play()
