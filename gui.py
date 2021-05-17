from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from apicall import getDict,getData
from database import get_customer, update_name, update_pwd, get_transaction, insert_customer, buy_currency, sell_currency, verify_customer, delete_customer, connect, close
import re
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

# --------------------------------- Check for Number and Email Start ---------------------------------

def checkemail(email):
    if(re.search(regex, email)):
        return True
    else:
        return False

def numberCheck(input):
    try:
        float(input)
        if(float(input)>0):
            return True
        else:
            raise Exception("Value cannot by less than or equal to 0")
    except (Exception) :
        return False


# --------------------------------- Check for Number and Email End ---------------------------------

class Application(ttk.Frame):    
    def __init__(self, userid, master=None):
        super().__init__(master)
        self.master = master
        self.userid = userid
        self.pack(fill="both")
        self.checkconnect(self.page)
    
    # --------------------------------- Check Database Conncection Start ---------------------------------

    def checkconnect(self, func):
        e = connect()
        if e == True:
            func()
        else: 
            self.destroy_child(self.master)
            self.label = ttk.Label(self.master,text="Cannot connect to database")
            self.label.pack(pady=5,padx=10)
            self.btn = ttk.Button(self.master,text="Refresh",command=self.page_reset)
            self.btn.pack(pady=5,padx=10)
    
    def destroy_child(self,frame):
        for child in frame.winfo_children():
            # print(child,type(child))
            if(type(child)!=Authentication):
                # print(child,type(child))
                child.destroy()

    def page_reset(self):
        self.destroy_child(self.master)
        self.checkconnect(self.page)

    # --------------------------------- Check Database Conncection End ---------------------------------

    # --------------------------------- Logout Start ---------------------------------

    def logout(self):
        self.btn_logout.destroy()
        self.main_notebook.destroy()
        self.frame_main.destroy()
        self.destroy()
        del self
        Authentication(master=root)

    # --------------------------------- Logout End ---------------------------------

    # --------------------------------- Page Start ---------------------------------

    def page(self):
        self.frame_main=ttk.Frame(self.master)
        self.frame_main.pack(fill="both")
        self.btn_logout = ttk.Button(self.frame_main,text="Logout",command=self.logout)
        self.btn_logout.pack(fill="x",side="right",padx=10)
        self.createNoteBook()
           
    def createNoteBook(self):
        self.main_notebook = ttk.Notebook(self.master,width=500)
        # make fill y if width of search is not increased
        self.main_notebook.pack(fill="y",expand=1,padx=10)
        self.search_og_frame = ttk.Frame(self.main_notebook)    
        self.owned_og_frame = ttk.Frame(self.main_notebook)    
        self.customer_og_frame = ttk.Frame(self.main_notebook)    
        self.search_og_frame.pack(fill="both", expand=1,pady=10,padx=10)
        self.owned_og_frame.pack(fill="both", expand=1,pady=10,padx=10)
        self.customer_og_frame.pack(fill="both", expand=1,pady=10,padx=10)

        self.main_notebook.add(self.search_og_frame, text="Search Currency")
        self.main_notebook.add(self.owned_og_frame, text="Owned Currency")
        self.main_notebook.add(self.customer_og_frame, text="Customer Details")
        self.user = get_transaction(customer_id=self.userid)

        self.createSearchFrame()
        self.createOwnedFrame()
        self.createCustomerFrame()

        data = getData(limit=10)
        if(type(data)==ConnectionError or type(data)==Timeout or type(data)==TooManyRedirects): 
            ttk.Label(self.search_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
            ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=1,pady=5,padx=10,sticky="news")
            ttk.Label(self.owned_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
            ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")
        else:
            self.display(data)
            self.checkowned()

    # --------------------------------- Page End ---------------------------------

    # --------------------------------- Create Scrollbar Start ---------------------------------
    
    def create_scroll(self,init_frame):
        # create canvas for search frame
        canvas = tk.Canvas(init_frame,bg='#434343')
        
        canvas.pack(expand=1,side="left",fill="both")
        # scrollbar
        scrollbar = ttk.Scrollbar(init_frame,orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right",fill="y")
        
        # CONFIGURE CANVAS
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # create another frame
        frame = ttk.Frame(canvas)
        # add the new frame to a window in canvas

        canvas.create_window((0,0), window=frame,anchor="nw")
        # newframe=ttk.Frame(frame)
        # newframe.place(relx=0.5,rely=0.5,anchor="nw")
        return canvas, scrollbar, frame

    # --------------------------------- Create Scrollbar End ---------------------------------

    # --------------------------------- Refresh Search Tab Start ---------------------------------

    def search_frame_reset(self):
        self.search_init_frame.destroy()
        self.search_canvas.destroy()
        self.search_scrollbar.destroy()
        self.search_frame.destroy()
        self.createSearchFrame()

    # --------------------------------- Refresh Search Tab End ---------------------------------

    # --------------------------------- Refresh Owned Tab Start ---------------------------------

    def owned_frame_reset(self):
        self.user = get_transaction(customer_id=self.userid)
        self.owned_init_frame.destroy()
        self.owned_canvas.destroy()
        self.owned_scrollbar.destroy()
        self.owned_frame.destroy()
        self.createOwnedFrame()
    
    def owned_refresh(self):
        self.owned_frame_reset()
        self.checkowned()

    # --------------------------------- Refresh Owned Tab End ---------------------------------

    # --------------------------------- Refresh Customer Tab Start ---------------------------------

    def customer_frame_reset(self):
        self.user_details = get_customer(customer_id=self.userid)
        self.customer_frame.destroy()
        self.createCustomerFrame()

    # --------------------------------- Refresh Customer Tab End ---------------------------------

    # --------------------------------- Create Search Tab Start ---------------------------------

    def createSearchFrame(self):
        self.search_init_frame = ttk.Frame(self.search_og_frame)
        self.search_init_frame.pack(fill="both",expand=1)
        
        self.search_canvas, self.search_scrollbar, self.search_frame = self.create_scroll(init_frame=self.search_init_frame)

    # --------------------------------- Create Search Tab End ---------------------------------
    
    # --------------------------------- Create Owned Tab Start ---------------------------------

    def createOwnedFrame(self):
        self.owned_init_frame = ttk.Frame(self.owned_og_frame)
        self.owned_init_frame.pack(fill="both",expand=1)
        self.owned_canvas, self.owned_scrollbar, self.owned_frame = self.create_scroll(init_frame=self.owned_init_frame)
        ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")

    # --------------------------------- Create Owned Tab End ---------------------------------
    
    # --------------------------------- Create Customer Tab Start ---------------------------------
    def createCustomerFrame(self):
        self.customer_frame = ttk.Frame(self.customer_og_frame)
        self.customer_frame.pack(fill="both",expand=1)
        self.user_details = get_customer(customer_id=self.userid)
        self.customer()
        ttk.Button(self.customer_frame,text="Refresh",command=self.customer_frame_reset).grid(row=6,pady=5,padx=10,sticky="news")
    
    # --------------------------------- Create Customer Tab End ---------------------------------

    # --------------------------------- Search Tab Start ---------------------------------

    def display(self,data,count=2):
        self.search()
        ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=(count-1),pady=5,padx=10,sticky="news")
        if(type(data)==type([])):
            for i in range(len(data)):
                frame = ttk.Frame(self.search_frame)
                frame['borderwidth'] = 2
                frame['relief'] = 'sunken'
                frame.grid(row=(i+count), sticky="news", columnspan=2, padx=5,pady=5)
                self.card(frame,data[i]) 
        else:
            for i in data.keys():
                frame = ttk.Frame(self.search_frame)
                frame['borderwidth'] = 2
                frame['relief'] = 'sunken'
                frame.grid(row=count, sticky="ew", columnspan=2, padx=5,pady=5)
                count+=1
                # print(data[i])
                self.card(frame,data[i]) 

    # --------------------------------- Search Currency Start ---------------------------------
    
    def search(self):
        self.search_curr = ttk.Entry(self.search_frame)
        self.search_curr.grid(row=0, column=0,sticky="ew", padx=10,pady=10)
        # self.search_currency.bind("<Key>",self.search_currency)
        self.search_button = ttk.Button(self.search_frame, text="Search",command=self.search_currency)
        self.search_button.grid(row=0, column=1,sticky="ew",pady=10)

    def search_currency(self):
        dictslug = getDict("slug")
        if(type(dictslug)==ConnectionError or type(dictslug)==Timeout or type(dictslug)==TooManyRedirects):
            ttk.Label(self.search_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
            ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=1,pady=5,padx=10,sticky="news")
            ttk.Label(self.owned_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
            ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")  
        else:
            name=self.search_curr.get()
            id = next((id for id, slug in dictslug.items() if name.lower() == slug), None)

            self.search_frame_reset()         
            
            if(id==None):
                ttk.Label(self.search_frame,text="Not Found Currency: "+name).grid(row=1,pady=10)

                data = getData(limit=10)
                if(type(data)==ConnectionError or type(data)==Timeout or type(data)==TooManyRedirects):
                    ttk.Label(self.search_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
                    ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=1,pady=5,padx=10,sticky="news")
                    ttk.Label(self.owned_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
                    ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")  
                else:
                    self.display(data,3)
            else:
                data = getData(str(id),datatype="id")
                if(type(data)==ConnectionError or type(data)==Timeout or type(data)==TooManyRedirects):
                    ttk.Label(self.search_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
                    ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=1,pady=5,padx=10,sticky="news")
                    ttk.Label(self.owned_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
                    ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")  
                else:
                    self.display(data)

    # --------------------------------- Search Currency End ---------------------------------

    # --------------------------------- Search Refresh Start ---------------------------------

    def search_refresh(self):
        self.search_frame_reset()
        data = getData(limit=10)
        if(type(data)==ConnectionError or type(data)==Timeout or type(data)==TooManyRedirects):
            ttk.Label(self.search_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
            ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=1,pady=5,padx=10,sticky="news")
            ttk.Label(self.owned_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
            ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")          
        else:
            self.display(data)

    # --------------------------------- Search Refresh End ---------------------------------

    # --------------------------------- Search Card Start ---------------------------------

    def card(self, frame, data):
        ttk.Label(frame,text=(data['name']+"("+data['symbol']+")")).grid(row=0, column=0,sticky="ew", padx=10,pady=5)
        # ttk.Label(frame,text=("Market Capital: "+str(data['quote']['INR']['market_cap']))).grid(row=1, column=0)
        ttk.Label(frame,text=("last updated: "+str(data['quote']['INR']['last_updated']))).grid(row=2, column=0,sticky="ew", padx=10)
        ttk.Label(frame,text="").grid(row=1, column=0)
        ttk.Label(frame,text=("Change over last 7 days: "+str(data['quote']['INR']['percent_change_7d']))).grid(row=0, column=1,sticky="ew", padx=10,pady=5)
        ttk.Label(frame,text=("price: ₹"+str(data['quote']['INR']['price']))).grid(row=2, column=1, columnspan=2, sticky="nse", padx=10)
        ttk.Button(frame,text="Buy",command=lambda: self.buy(frame,data)).grid(row=3, column=1, sticky="e", padx=5)
    
    # --------------------------------- Search Card End ---------------------------------

    # --------------------------------- Search Buy Currency Start ---------------------------------

    def buy(self,frame,data):
        id=data['id']
        self.buy_curr = tk.Toplevel(self.master)
        
        style = ttk.Style(self.buy_curr)

        style.theme_use('clam')
        self.buy_curr['bg']="#434343"
        style.configure('TFrame', background= '#434343',foreground="#fff")
        style.configure('TLabel', background= '#434343',foreground="#fff")
        style.map("TButton",
            foreground=[('pressed', '#eee'), ('active', '#eee')],
            background=[('pressed', '#434343'), ('active', '#646365')]
            )
        style.configure('TButton', background='#434343',foreground="#fff")
        
        # data = getData(str(id),"id")[str(id)]
        self.buy_curr.title("Buy "+ data["name"])
        ttk.Label(self.buy_curr,text=(data['name']+"("+data['symbol']+")")).grid(row=0, column=0,sticky="ew", padx=10)        
        ttk.Label(self.buy_curr,text=("price: ₹"+str(data['quote']['INR']['price']))).grid(row=0, column=1, sticky="nse", padx=10)
        ttk.Label(self.buy_curr,text="Enter Amount: ").grid(row=1, column=0, pady=5, padx=10)
        self.buyamt=ttk.Entry(self.buy_curr)
        self.buyamt.grid(row=1, column=1,sticky="nse", padx=10, pady=5)
        ttk.Button(self.buy_curr,text="Buy",command=lambda: self.buy_calc(data['quote']['INR']['price'],id)).grid(row=2, column=1, padx=10, pady=5)

    def buy_calc(self,price,id):
        amount=self.buyamt.get()
        if(not numberCheck(amount)):
            messagebox.showerror("Invalid Input", "Amount must be in decimal")
            self.buyamt.delete(0, tk.END)
        else:
            amount = float(amount)
            own = amount/price
            response=messagebox.askokcancel("Confirm Amount", "Amount: "+str(amount)+" Owned: "+str(own))
            if(response==1):
                self.checkconnect(self.owned_refresh)
                self.buy_curr.destroy()
                self.search_refresh()
                buy_currency(id, own, amount, self.userid)
                self.owned_refresh()     
    
    # --------------------------------- Search Buy Currency Start ---------------------------------

    # --------------------------------- Search Tab End ---------------------------------
  
    # --------------------------------- Owned Tab Start ---------------------------------

    # --------------------------------- Owned Any Currency? Start ---------------------------------

    def checkowned(self):
        if(self.user!=[]):
            lst=list(map(lambda x: str(x['currency_id']) ,self.user))
            ids = ','.join(lst)

            data = getData(curr=ids,datatype="id")
            if(type(data)==ConnectionError or type(data)==Timeout or type(data)==TooManyRedirects):
                ttk.Label(self.search_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
                ttk.Button(self.search_frame,text="Refresh",command=self.search_refresh).grid(row=1,pady=5,padx=10,sticky="news")
                ttk.Label(self.owned_frame,text="Failed to establish API Connection").grid(row=0,pady=5,padx=10,sticky="news")
                ttk.Button(self.owned_frame,text="Refresh",command=lambda: self.checkconnect(self.owned_refresh)).grid(row=1,pady=5,padx=10,sticky="news")  
            else:
                self.owned(data,self.user)
        else:
            ttk.Label(self.owned_frame,text="You Don't Own any Currency",font=("Arial", 20)).grid(row=0,pady=5,padx=10,sticky="news")
    
    # --------------------------------- Owned Any Currency? End ---------------------------------
    
    # --------------------------------- Owned Currency Start ---------------------------------

    def owned(self,data,basedata):
        total_change=0
        for i in basedata:
            id=i["currency_id"]
            curr=data[str(id)]
            curr_val=round(round(float(i['total_bought']-i['total_sold']),4)*round(curr['quote']['INR']['price'],4),4)
            change=round(curr_val-(float(i['amount_bought']-i['amount_sold'])),4)
            total_change+=change

        if(total_change>0):
            text="Profit"
        elif(total_change<0):
            text="Loss"
            total_change*=-1
        else:
            text="No Profit/Loss"

        if(text=="No Profit/Loss"):
            ttk.Label(self.owned_frame,text=text,font=("Arial", 20)).grid(row=0,pady=5,padx=10,sticky="news")
        else:
            ttk.Label(self.owned_frame,text=text+" : "+str(round(total_change,4)),font=("Arial", 20)).grid(row=0,pady=5,padx=10,sticky="news")

        count=2
        for i in basedata:
            id=i["currency_id"]
            curr=data[str(id)]
            frame = ttk.Frame(self.owned_frame)
            frame['borderwidth'] = 2
            frame['relief'] = 'sunken'
            frame.grid(row=count, sticky="ew", columnspan=2, padx=5,pady=5)
            count+=1
            self.cardOwned(frame,i,curr)

    # --------------------------------- Owned Card Start ---------------------------------

    def cardOwned(self, frame, base, data):
        ttk.Label(frame,text=(data['name']+"("+data['symbol']+")")).grid(row=0, column=0,sticky="ew", padx=10,pady=5)
        # ttk.Label(frame,text=("Market Capital: "+str(data['quote']['INR']['market_cap']))).grid(row=1, column=0)
        ttk.Label(frame,text="Currency Price: ₹"+str( round(data['quote']['INR']['price'],4))).grid(row=1, column=0,sticky="ew", padx=10,pady=5)
        ttk.Label(frame,text=("last updated: "+str(data['quote']['INR']['last_updated']))).grid(row=0, column=1,sticky="ew", padx=10)
        curr_val=round(round(float(base['total_bought']-base['total_sold']),4)*data['quote']['INR']['price'],4)
        change=round(curr_val-(float(base['amount_bought']-base['amount_sold'])),4)
        if(change>0):
            text="Profit"
        elif(change<0):
            text="Loss"
            change*=-1
        else:
            text="No Profit/Loss"
        ttk.Label(frame,text=("Current Value: ₹"+str(curr_val))).grid(row=2, column=0, sticky="nse", padx=10)
        ttk.Label(frame,text=("Currency Owned : "+str(base['total_bought']-base['total_sold']))).grid(row=2, column=1, sticky="nse", padx=10)
        if(text=="No Profit/Loss"):
            ttk.Label(frame,text=text).grid(row=4, column=0,sticky="nsew", padx=10,pady=5,ipadx=5)
        else:
            ttk.Label(frame,text=(text + ": ₹"+str(change))).grid(row=4, column=0,sticky="nsew", padx=10,pady=5,ipadx=5)
        ttk.Button(frame,text="Sell",command=lambda: self.sell(frame,base,data)).grid(row=4, column=1, sticky="e", padx=5)
    
    # --------------------------------- Owned Card End ---------------------------------

    # --------------------------------- Currency Sell Start ---------------------------------

    def sell(self,frame,base,data):
        self.sell_curr = tk.Toplevel(self.master)

        style = ttk.Style(self.sell_curr)

        style.theme_use('clam')
        self.sell_curr['bg']="#434343"
        style.configure('TFrame', background= '#434343',foreground="#fff")
        style.configure('TLabel', background= '#434343',foreground="#fff")
        style.map("TButton",
            foreground=[('pressed', '#eee'), ('active', '#eee')],
            background=[('pressed', '#434343'), ('active', '#646365')]
            )
        style.configure('TButton', background='#434343',foreground="#fff")
        
        # data = getData(str(id),"id")[str(id)]
        curr_val=(float(base['total_bought']-base['total_sold']))*data['quote']['INR']['price']
        self.sell_curr.title("Sell "+ data["name"])
        ttk.Label(self.sell_curr,text=(data['name']+"("+data['symbol']+")")).grid(row=0, column=0,sticky="ew", padx=10,pady=5)        
        ttk.Label(self.sell_curr,text=("Current Value: ₹"+str(curr_val))).grid(row=0, column=1, sticky="nsew", padx=10)
        ttk.Label(self.sell_curr,text="Currency Owned: "+str(base['total_bought']-base['total_sold'])).grid(row=1, column=0, sticky="nsew", padx=10)
        ttk.Label(self.sell_curr,text="Enter Amount to Sell: ").grid(row=2, column=0, sticky="nsew", pady=5, padx=10)
        self.sellamt=ttk.Entry(self.sell_curr)
        self.sellamt.grid(row=2, column=1,sticky="nsew", padx=10, pady=5)
        ttk.Button(self.sell_curr,text="Sell",command=lambda: self.sell_calc(base,data['name'],data['quote']['INR']['price'])).grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

    def sell_calc(self,base,name,price):
        amount=self.sellamt.get()
        if(not numberCheck(amount)):
            messagebox.showerror("Invalid Input", "Amount must be in decimal")
            self.sellamt.delete(0, tk.END)
        elif(float(amount)>(base['total_bought']-base['total_sold'])):
            messagebox.showerror("Invalid Input", "Amount must be less than Owned Amount")
        else:
            amount = float(amount)
            sellingamt = amount*price
            response=messagebox.askokcancel("Confirm Amount", name + " Amount: " + str(amount) + " INR Value: " + str(sellingamt))
            if(response==1):
                self.sell_curr.destroy()
                self.checkconnect(self.owned_refresh)
                sell_currency(base['currency_id'], amount, sellingamt, self.userid)
                self.owned_refresh()
    
    # --------------------------------- Currency Sell End ---------------------------------
    
    # --------------------------------- Owned Currency End ---------------------------------

    # --------------------------------- Owned Tab End ---------------------------------

    # --------------------------------- Customer Tab Start ---------------------------------
    
    def customer(self):
        self.first_name = ttk.Label(self.customer_frame, text="First Name : "+self.user_details["first_name"])
        self.first_name.grid(row=0,column=0,sticky="w",padx=5,pady=5)
        self.last_name = ttk.Label(self.customer_frame, text="Last Name : "+self.user_details["last_name"])
        self.last_name.grid(row=0,column=1,sticky="w",padx=5,pady=5)
        self.namebtn = ttk.Button(self.customer_frame, text="Update Name", command=self.update_name)
        self.namebtn.grid(row=1,column=0,padx=5,pady=5,sticky="news") 
        self.email = ttk.Label(self.customer_frame, text="Email ID : "+self.user_details["email_id"])
        self.email.grid(row=2,column=0,sticky="w",padx=5,pady=5)
        self.username = ttk.Label(self.customer_frame, text="Username : "+self.user_details["username"])
        self.username.grid(row=3,column=0,sticky="w",padx=5,pady=5)
        self.passwordbtn = ttk.Button(self.customer_frame, text="Update Password", command=self.update_pwd)
        self.passwordbtn.grid(row=4,column=0,padx=5,pady=5,sticky="news")    
        # self.deletebtn = ttk.Button(self.customer_frame, text="Delete Account", command=self.delete_user)
        # self.deletebtn.grid(row=5,column=0,padx=5,pady=5,sticky="news")    

    # --------------------------------- Customer Delete Start ---------------------------------

    # def delete_user(self):
        # check_delete = delete_customer(self.userid)
        # if(check_delete==True):
            # messagebox.showinfo("Account Deleted","Account was Successfully Deleted")
            # self.main_notebook.destroy()
            # Authentication(master=root)
        # else:
            # messagebox.showerror("Cannot Delete user",check_delete)

    # --------------------------------- Customer Delete End ---------------------------------

    # --------------------------------- Customer Update Password Start ---------------------------------

    def update_pwd(self):
        self.pwd_update = tk.Toplevel(self.master)
        
        style = ttk.Style(self.pwd_update)
        style.theme_use('clam')
        self.pwd_update['bg']="#434343"
        style.configure('TFrame', background= '#434343',foreground="#fff")
        style.configure('TLabel', background= '#434343',foreground="#fff")
        style.map("TButton",
            foreground=[('pressed', '#eee'), ('active', '#eee')],
            background=[('pressed', '#434343'), ('active', '#646365')]
            )
        style.configure('TButton', background='#434343',foreground="#fff")
        
        ttk.Label(self.pwd_update,text="New Password").grid(row=0, column=0,sticky="ew", padx=10,pady=5)        
        ttk.Label(self.pwd_update,text="Re-Enter New Password").grid(row=1, column=0,sticky="ew", padx=10,pady=5)        
        self.new_pwd=ttk.Entry(self.pwd_update)
        self.new_pwd.grid(row=0, column=1,sticky="nsew", padx=10, pady=5)
        self.new_repwd=ttk.Entry(self.pwd_update)
        self.new_repwd.grid(row=1, column=1,sticky="nsew", padx=10, pady=5)
        ttk.Button(self.pwd_update,text="Update Password",command=self.pwd).grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

    def pwd(self):
        new_pass = self.new_pwd.get()
        new_repass = self.new_repwd.get()
        if(new_pass!=new_repass):
            messagebox.showerror("Cannot Update Password","Both Passwords Don't Match")
        else:
            check_update = update_pwd(new_pass, self.userid)
            if(check_update==True):
                messagebox.showinfo("Password Updated","Password was Successfully Updated")
                self.pwd_update.destroy()
                self.customer_frame_reset()
            else:
                messagebox.showerror("Cannot Update Password",check_update)
    
    # --------------------------------- Customer Update Password End ---------------------------------

    # --------------------------------- Customer Update Name Start ---------------------------------

    def update_name(self):
        self.name_update = tk.Toplevel(self.master)

        style = ttk.Style(self.name_update)
        style.theme_use('clam')
        self.name_update['bg']="#434343"
        style.configure('TFrame', background= '#434343',foreground="#fff")
        style.configure('TLabel', background= '#434343',foreground="#fff")
        style.map("TButton",
            foreground=[('pressed', '#eee'), ('active', '#eee')],
            background=[('pressed', '#434343'), ('active', '#646365')]
            )
        style.configure('TButton', background='#434343',foreground="#fff")
        
        ttk.Label(self.name_update,text="First Name").grid(row=0, column=0,sticky="ew", padx=10,pady=5)        
        ttk.Label(self.name_update,text="Last Name").grid(row=1, column=0,sticky="ew", padx=10,pady=5)        
        self.update_first=ttk.Entry(self.name_update)
        self.update_first.insert(0,self.user_details["first_name"])
        self.update_first.grid(row=0, column=1,sticky="nsew", padx=10, pady=5)
        self.update_last=ttk.Entry(self.name_update)
        self.update_last.insert(0,self.user_details["last_name"])
        self.update_last.grid(row=1, column=1,sticky="nsew", padx=10, pady=5)
        ttk.Button(self.name_update,text="Update Name",command= self.name).grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

    def name(self):
        first = self.update_first.get()
        last = self.update_last.get()
        check_update = update_name(first,last, self.userid)
        if(check_update==True):
            messagebox.showinfo("Name Updated","Name was Successfully Updated")
            self.name_update.destroy()
            self.customer_frame_reset()
        else:
            messagebox.showerror("Cannot Update Name",check_update)
    
    # --------------------------------- Customer Update Name End ---------------------------------

    # --------------------------------- Customer Tab End ---------------------------------

class Authentication(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.checkconnect(self.create_login_widgets)

    # --------------------------------- Check Database Connection Start ---------------------------------

    def checkconnect(self,func):
        e=connect()
        if(e == True):
            func()
        else: 
            self.destroy_child(self.master)
            self.label = ttk.Label(self.master,text="Cannot connect to database")
            self.label.pack(pady=5,padx=10)
            self.btn = ttk.Button(self.master,text="Refresh",command=self.login_reset)
            self.btn.pack(pady=5,padx=10)
    
    def destroy_child(self,frame):
        for child in frame.winfo_children():
            # print(child,type(child))
            if(type(child)!=Authentication):
                # print(child,type(child))
                child.destroy()

    def login_reset(self):
        self.destroy_child(self.master)
        self.checkconnect(self.create_login_widgets)

    # --------------------------------- Check Database Connection End ---------------------------------

    # --------------------------------- Create Widgets for Authentication Start ---------------------------------

    def create_login_widgets(self):
        self.login_notebook = ttk.Notebook(self.master)
        self.login_notebook.pack(expand=1)

        self.login_frame = ttk.Frame(self.login_notebook)    
        self.register_frame = ttk.Frame(self.login_notebook)    
        self.login_frame.pack(fill="both", expand=1, padx=10)
        self.register_frame.pack(fill="both", expand=1, padx=10)

        self.login_notebook.add(self.login_frame, text="Login")
        self.login_notebook.add(self.register_frame, text="Register")
        self.register()
        self.login()

    # --------------------------------- Create Widgets for Authentication End ---------------------------------

    # --------------------------------- Change Tab Start ---------------------------------

    def select_tab(self, notebook, num):
        notebook.select(num)

    # --------------------------------- Change Tab End ---------------------------------

    # --------------------------------- Register Start ---------------------------------

    def register(self):
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.email = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        
        ttk.Label(self.register_frame, text="Please enter details below").grid(row=0,column=0,columnspan=2, pady=15)
    
        self.first_name_lable = ttk.Label(self.register_frame, text="First Name : ")
        self.first_name_lable.grid(row=1,column=0, pady=5, padx=25)
        self.first_name_entry = ttk.Entry(self.register_frame, textvariable=self.first_name)
        self.first_name_entry.grid(row=1,column=1,sticky="e",padx=25)
        self.last_name_lable = ttk.Label(self.register_frame, text="Last Name : ")
        self.last_name_lable.grid(row=3,column=0, pady=5, padx=25)
        self.last_name_entry = ttk.Entry(self.register_frame, textvariable=self.last_name)
        self.last_name_entry.grid(row=3,column=1,sticky="e",padx=25)
        self.email_lable = ttk.Label(self.register_frame, text="Email ID : ")
        self.email_lable = ttk.Label(self.register_frame, text="Email ID : ")
        self.email_lable.grid(row=5,column=0)
        self.email_entry = ttk.Entry(self.register_frame, textvariable=self.email)
        self.email_entry.grid(row=5,column=1,sticky="e",padx=25)
        self.username_lable = ttk.Label(self.register_frame, text="Username : ")
        self.username_lable.grid(row=7,column=0, pady=5, padx=25)
        self.username_entry = ttk.Entry(self.register_frame, textvariable=self.username)
        self.username_entry.grid(row=7,column=1,sticky="e",padx=25)
        self.password_lable = ttk.Label(self.register_frame, text="Password : ")
        self.password_lable.grid(row=9,column=0, pady=5, padx=25)
        self.password_entry = ttk.Entry(self.register_frame, textvariable=self.password, show='*')
        self.password_entry.grid(row=9,column=1,sticky="e",padx=25)
        self.validate = []
        for i in range(2,11,2):
            x = ttk.Label(self.register_frame, text="")
            x.grid(row=i, columnspan=2,sticky="w",padx=10)
            self.validate.append(x)
    
        ttk.Button(self.register_frame, text="Register", command = self.validate_user).grid(row=11,column=0,columnspan=2)
        ttk.Label(self.register_frame,text="").grid(row=12)
        ttk.Button(self.register_frame, text="Already Have an account. Login", command = lambda: self.select_tab(self.login_notebook,0)).grid(row=13,column=0,columnspan=2,pady=10)

    # --------------------------------- Register Validation Start ---------------------------------

    def validate_user(self):
        flag=True
        first_name_len = len(self.first_name.get())
        last_name_len = len(self.last_name.get())
        username_len = len(self.username.get())
        password_len = len(self.password.get())
        email_info = self.email.get()
        style.configure("good.TLabel",foreground="#00a884")
        style.configure("bad.TLabel",foreground="#FF2027")
        
        if(first_name_len>=3 and first_name_len<=12):
            self.validate[0]["text"]="Looks Good"
            self.validate[0]["style"]="good.TLabel"
        else:
            self.validate[0]["text"]="First Name must be between 3 and 12 characters"
            self.validate[0]["style"]="bad.TLabel"
            flag=False

        if(last_name_len>=3 and last_name_len<=12):
            self.validate[1]["text"]="Looks Good"
            self.validate[1]["style"]='good.TLabel'
        else:
            self.validate[1]["text"]="Last Name must be between 3 and 12 characters"
            self.validate[1]["style"]="bad.TLabel"
            flag=False
    
        if(checkemail(email_info)):
            self.validate[2]["text"]="Looks Good"
            self.validate[2]["style"]='good.TLabel'
        else:
            self.validate[2]["text"]="Invalid Email"
            self.validate[2]["style"]="bad.TLabel"
            flag=False

        if(username_len>=5 and username_len<=15):
            self.validate[3]["text"]="Looks Good"
            self.validate[3]["style"]='good.TLabel'
        else:
            self.validate[3]["text"]="Username must be between 5 and 15 characters"
            self.validate[3]["style"]="bad.TLabel"
            flag=False
    
        if(password_len>=5 and password_len<=15):
            self.validate[4]["text"]="Looks Good"
            self.validate[4]["style"]='good.TLabel'
        else:
            self.validate[4]["text"]="Password must be between 5 and 15 characters"
            self.validate[4]["style"]="bad.TLabel"
            flag=False

        if(flag):
            self.checkconnect(self.register_user)
    
    # --------------------------------- Register Validation End ---------------------------------

    # --------------------------------- Register to Database Start ---------------------------------

    def register_user(self):
        self.first_name_info = self.first_name.get()
        self.last_name_info = self.last_name.get()
        self.username_info = self.username.get()
        self.password_info = self.password.get()
        self.email_info = self.email.get()

        self.flag = insert_customer(self.first_name_info,self.last_name_info,self.username_info,self.password_info,self.email_info)

        if(self.flag!=True):
            messagebox.showerror("Registration Failed", self.flag)
        else:
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            messagebox.showinfo("Registration Success", "User Successfully Registered")
            self.select_tab(self.login_notebook,0)

    # --------------------------------- Register to Database End ---------------------------------

    # --------------------------------- Register End ---------------------------------

    # --------------------------------- Login Start ---------------------------------

    def login(self):
        ttk.Label(self.login_frame, text="Please enter details below to login").grid(row=0,column=0,columnspan=2, pady=15)
        self.username_verify = tk.StringVar()
        self.password_verify = tk.StringVar()
    
        ttk.Label(self.login_frame, text="Username : ").grid(row=1,column=0,padx=25, pady=15)
        self.username_login_entry = ttk.Entry(self.login_frame, textvariable=self.username_verify)
        self.username_login_entry.grid(row=1,column=1,sticky="ew",padx=25)
        ttk.Label(self.login_frame, text="Password : ").grid(row=2,column=0,padx=25, pady=15)
        self.password_login_entry = ttk.Entry(self.login_frame, textvariable=self.password_verify, show= '*')
        self.password_login_entry.grid(row=2,column=1,sticky="ew",padx=25)

        ttk.Button(self.login_frame, text="Login", command = lambda: self.checkconnect(self.login_verify)).grid(row=3,column=0,columnspan=2)
        ttk.Label(self.login_frame,text="").grid(row=4)
        ttk.Button(self.login_frame, text="Don't Have an account. Register", command = lambda: self.select_tab(self.login_notebook,1)).grid(row=5,column=0,columnspan=2)

    # --------------------------------- Login Verification Start ---------------------------------

    def login_verify(self):
        self.username1 = self.username_verify.get()
        self.password1 = self.password_verify.get()
        self.username_login_entry.delete(0, tk.END)
        self.password_login_entry.delete(0, tk.END)
        
        userid = verify_customer(self.username1,self.password1)
        if(userid==False):
            messagebox.showerror("Login Failed","Username or Password invalid")
        else: 
            self.login_sucess(userid)
 
    # --------------------------------- Login Verification End ---------------------------------
    
    # --------------------------------- Successfull Login Start ---------------------------------

    def login_sucess(self,userid):
        self.login_notebook.destroy()
        self.destroy()
        del self
        Application(userid,master=root)
    
    # --------------------------------- Successfull Login End ---------------------------------
    
    # --------------------------------- Login End ---------------------------------
    
# --------------------------------- Dark Mode Default Start ---------------------------------

def dark(btn):
    # btn['text']="Light Mode"
    # btn['command']=lambda: light(btn)
    root['bg']="#434343"
    style.configure('normal.TLabel', background= '#eee')
    style.configure('normal.TButton', background= '#ddd')
    style.configure('TFrame', background= '#434343',foreground="#fff")
    style.configure('TLabel', background= '#434343',foreground="#fff")
    style.map("TButton",
        foreground=[('pressed', '#eee'), ('active', '#eee')],
        background=[('pressed', '#434343'), ('active', '#646365')]
        )
    style.configure('TButton', background='#434343',foreground="#fff")
    style.configure('TNotebook', background='#616365',foreground="#fff",border=0)
    # btn['style']='TButton'

# --------------------------------- Dark Mode Default End ---------------------------------

# --------------------------------- Light Mode Start ---------------------------------
    # --------------------------------- Can be Added ---------------------------------

# def light(btn):
#     btn['text']="Dark Mode"
#     btn['command']=lambda: dark(btn)
#     root['bg']="#bcbcbc"
#     style.configure('normal.TLabel', background= '#eee')
#     style.configure('normal.TButton', background= '#ddd')
#     style.configure('TFrame', background= '#bcbcbc',foreground="#000")
#     style.configure('TLabel', background= '#bcbcbc',foreground="#000")
#     style.map("TButton",
#         foreground=[('pressed', '#111'), ('active', '#111')],
#         background=[('pressed', '#bcbcbc'), ('active', '#9b9c9a')]
#         )
#     style.configure('TButton', background='#bcbcbc',foreground="#000")
#     style.configure('TNotebook', background='#9b9c9a',foreground="#000",border=0)
#     btn['style']='TButton'

# --------------------------------- Light Mode End ---------------------------------

root = tk.Tk()
root.title("CryptoCurrency Data Storage System")
root.geometry("550x500")

# --------------------------------- Styling Start ---------------------------------
style = ttk.Style(root)
style.theme_use('clam')
btn=None
dark(btn)
# --------------------------------- Styling End ---------------------------------

# --------------------------------- Authentication Object Create Start ---------------------------------
Authentication(master=root)
# --------------------------------- Authentication Object Create End ---------------------------------

# --------------------------------- End Database Connection on Application Close Start ---------------------------------
def close_window():
    close()
    root.destroy()
root.protocol('WM_DELETE_WINDOW', close_window)
# --------------------------------- End Database Connection on Application Close End ---------------------------------

root.mainloop()
