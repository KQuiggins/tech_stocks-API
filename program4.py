import requests
import datetime
import wx
import sqlite3 as db


class myFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1000, 700))

        

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('#0d6a8f')

        self.lb1 = wx.StaticText(panel, -1, '', pos=(400, 50))
        self.lb2 = wx.StaticText(panel, -1, '', pos=(400, 75))
        self.lb1.SetForegroundColour('white')
        self.lb2.SetForegroundColour('white')

        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, pos=(110, 110), size=(723, 400))

        # Set up columns
        self.list.InsertColumn(1, 'Company', width=120)
        self.list.InsertColumn(2, 'Symbol', width=120)
        self.list.InsertColumn(3, 'Purchase Price', width=120)
        self.list.InsertColumn(4, 'Current Price', width=120)
        self.list.InsertColumn(5, 'Shares', width=120)
        self.list.InsertColumn(6, 'Gain/Loss', width=120)

        # set up buttons
        display = wx.Button(panel, -1, 'Display', size=(-1, 30), pos=(300, 550))
        cancel = wx.Button(panel, -1, 'Cancel', size=(-1, 30), pos=(620, 550))
        
        # Bind buttons to event handlers
        display.Bind(wx.EVT_BUTTON, self.OnDisplay)
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
           

    
    def getData(self):
        self.list.DeleteAllItems() # empty the list control
        con = db.connect('tech_stocks.db') # connect to database
        cur = con.cursor() # create a cursor

        cur.execute('SELECT company, symbol, purchase_price, shares  FROM dow_stocks') # Query the database 
        results = cur.fetchall() # Get the results 
        
        for row in results:  # Loop through results
            
            
            TOKEN = '&token=c8p71gqad3iajre6bjs0' # API Token key
            url = "https://finnhub.io/api/v1/quote?symbol=" + row[1] + TOKEN    # concatenate url, symbol, and token 
            
            response = requests.get(url)  # Make a request with url 

            if response.status_code == 200: # If ok then take info and perform calculations
                data = response.json()
                calc = row[3] * (data['c'] - row[2])
                r_calc = round(calc, 2)
                
           

                info =  [row[0], row[1], row[2], data['c'], row[3], r_calc ]  
            
                self.list.Append(info) # add record to list control
            
                x = datetime.datetime.now() # Get current date and time 
            
                date = x.strftime("%A %B %d, %Y : %H:%M")  # Format date and time
            
                self.lb1.SetLabel(date)   # Set formated date and time in label 1
            
                self.lb2.SetLabel("Net Gain/Loss: $" + str(r_calc)) # Set Gains/losses in Label 2

        cur.close()
        con.close()


    
    def OnDisplay(self, event):
        try:
            self.getData()
        
        except db.Error as error:
            dlg = wx.MessageDialog(self, str(error), 'Error occurred')
            dlg.ShowModal()


    
    
    def OnCancel(self, event):
        self.Close()

app = wx.App()
mf = myFrame(None, -1, 'Program 4')
mf.Show()
app.MainLoop()



 