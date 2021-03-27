
import threading
import time
import math
import numpy as np

class Trader:
    
    """
    
    
    Implantez ici votre algorithme de trading. Le marche est accessible avec la
    variable Market. Les differentes fonctions disponibles sont disponibles dans
    le fichier API et expliquees dans le document de la competition
    """
    
    #Nom de l'equipe:
    equipe = ''

    def __init__(self, API):
        
        self.API = API
        self.API.setEquipe(self.equipe)
        
    """Function called at start of run"""
    def run(self):
        
        """You can add initialization code here"""
        self.current = None
        self.daycount = 0
        self.previous = []
        self.stocks = self.API.getListStocks()[:-1]
        
        
        self.t = threading.currentThread()
        while getattr(self.t, "run", True):
            try:
                self.trade()
            except Exception as err:
                print(err)
            time.sleep(0)
            
            
            
    """Your trading algorithm goes here!
        The function is called continuously"""
    def trade(self):
        time = self.API.getTime()
        if self.current == time:
            return
        else:
            self.daycount += 1

            if self.daycount > 2:
                self.previous = self.previous[1:] + [self.current]
            else:
                self.previous += [self.current]

            self.current = time

        print(self.daycount)
        if self.daycount > 2:
            change = []
            for stock in self.stocks:

                prices = self.API.getPastPrice(stock, self.previous[0], self.previous[1])
                change += [prices[self.previous[1]]/prices[self.previous[0]]]
            best = np.argmax(np.array(change))
            best_stock = self.stocks[best]

            print(change)

            self.sell_all()
            self.buy_max(best_stock)


    def sell_all(self):
        for stock in self.stocks:
            self.API.marketSell(stock, self.API.getUserStocks()[stock])

    def buy_max(self, stock):
        max_to_buy = math.floor(self.API.getUserCash()/self.API.getPrice(stock))
        self.API.marketBuy(stock, max_to_buy)

