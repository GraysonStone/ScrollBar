import Stock
import threading
from Tkinter import *
import datetime
from time import sleep
class labels():
    lab = ''
    x = 0
    info = ''
    def __init__(self,x,info):
        if info.find("+") !=-1:
                    self.lab = Label(text = info, bg="grey8",fg="green", font=("Calibri",11))
        else:
                    self.lab = Label(text = info, bg="grey8",fg="red", font=("Calibri",11))
        self.info = info
        self.x = x
    def info_update(self,info):
        if info.find("+") !=-1:
                    self.lab.config(fg="green")# = Label(text = info, bg="grey8",fg="green", font=("Calibri",11))
        else:
                    self.lab.config(fg="red") #= Label(text = info, bg="grey8",fg="red", font=("Calibri",11))
        self.lab.config(text=info)
class bar():
    b = Tk()
    stocks = []
    labels = []
    stock_lock = threading.Lock()
    display_lock = threading.Lock()
    stockList = []
    end=False
    t1 = threading.Thread() 
    t2 = threading.Thread() 
    def __init__(self):
        self.t1 = threading.Thread(target=self.updater) 
        self.t1.start()
        self.scroll()
        self.end = True
        self.t1.join()
      
        
    def updater(self):
        self.display_lock.acquire()
        first = True
        while not self.end:
            self.read()
            self.write()
            if first:
                self.display_lock.release()
            first = False
            sleep(40)
             
    def scroll(self):
        self.display_lock.acquire()
        for i in range(0,4):
            self.stock_lock.acquire()
            self.labels.append(labels(i*200,self.stocks[i]))
            self.stock_lock.release()
        self.b.overrideredirect(True)
        self.b.geometry("400x20+1279+0")
        self.b.config(bg="grey8")
        self.b.update()
        stock_count = 0
        count_lim=len(self.stocks)
        while 1==1:
            for i in range(0,4):
                self.labels[i].lab.place(x=self.labels[i].x)
                self.labels[i].x-=1
                if self.labels[i].x <=-200:
                    self.labels[i].x = 600
                    self.stock_lock.acquire()
                    self.labels[i].info_update(self.stocks[stock_count])
                    self.stock_lock.release()
                    stock_count+=1
                    if stock_count == count_lim:
                        stock_count = 0
                    

            self.b.update()



    def internetError(self):
        print("go sleep 5 min")
        sleep(300)
        self.read()
    def write(self):
        self.stock_lock.acquire()
        self.stocks = []
        for i in range(0,len(self.stockList)):
            self.stocks.append(self.stockList[i])
        self.stock_lock.release()
        print("Write")
    def read(self):
        print("read")
        file=open("/Users/Gray/Desktop/ScrollBar/StockWatchList.txt",'r')
        line=file.readlines()
        file.close()
        self.stockList=[]
        woopseCount=0
        while 1==1:
            try:
                for i in range(0,len(line)):
                    self.stockList.append(Stock.Stock(line[i][0:len(line[i])-1]).totalString)
                break
            except:
                woopseCount+=1
                print("woopsie")
                sleep(10)
                if woopseCount>12:
                    self.internetError()
                    break
        print("readStop")



if __name__ == '__main__':
   bar()
        
