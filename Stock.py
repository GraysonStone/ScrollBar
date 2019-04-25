import urllib2
from bs4 import BeautifulSoup
import socket
class Stock():
    ticker=''
    price=''
    percentchange=''
    totalString=''
    def __init__(self,ticker):
        check=self.getS(ticker)
        
        while check==False:
            print("Loop due to socket timeout")
            check=self.getS(ticker)
        
    def getS(self,ticker):
        self.ticker=ticker
        quote_page = 'https://finance.yahoo.com/quote/'+self.ticker
        
        try:
            page = urllib2.urlopen(quote_page,timeout = 5)
        except socket.timeout:
            print("socket timeoutcatch")
            return False
        soup = BeautifulSoup(page, 'html.parser')
        soup=str(soup)
        parsestart=soup.index("quote-header-info")
        soup=soup[parsestart+800:parsestart+1200]
        soup=soup[soup.index('data-reactid="14"'):len(soup)]
        self.price=soup[soup.index('>')+1:soup.index('<')]
        soup=soup[soup.index('data-reactid="16"'):len(soup)]
        self.percentchange=soup[soup.index('>')+1:soup.index('<')]
        self.totalString=self.ticker+" "+self.price+" "+self.percentchange
        return True



def main():
    Stock("AAPL")
if __name__ == '__main__':
    main()
