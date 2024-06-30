#!/usr/bin/env python
# coding: utf-8

# # Inventory Management System

# ## Product Details:- <br>
# #### 1. Product ID<br>
# #### 2. Product Name<br>
# #### 3. Product Price<br>
# #### 4. Product Quantity

# ## Adding Products

# In[1]:


import os
import json
import datetime


# In[2]:


def newId(s):
    l=len(s)
    id_list=[False]*(l+1)
    
    for i in s:
        id_list[int(i)]=True
    
    for i in range(l+1):
        if(id_list[i]==False):
            break
    
    return i


# In[3]:


def addProduct(name,price,quantity):
    fd1=open(os.path.dirname(__file__)+"\Inventory.json","r")
    s=json.loads(fd1.read())
    c=newId(s.keys())
    fd1.close()
    
    fd2=open(os.path.dirname(__file__)+"\Inventory.json","w")
    s[c]={'name':name,'price':price,'quantity':quantity}
    fd2.write(json.dumps(s))
    fd2.close()


# ## Product Details

# In[4]:


def productDetails(id:str):
    fd=open(os.path.dirname(__file__)+"\Inventory.json","r")
    s=json.loads(fd.read())
    
    s2=""
    if id in s:
        s2=s[id]
    else:
        print("The product is not found.")
        
    fd.close()
    return s2


# ## Updating Inventory

# In[5]:


import pandas as pd
def updateInventory2(id:int,quantity:int):
    flag=False
    fd=pd.read_csv(os.path.dirname(__file__)+"\Inventory.csv")
    
    l=len(fd)
    for i in range(l):
        if(fd.loc[i,"ID"]==id):
            flag=True
            fd.loc[i,"Quantity"]=fd.loc[i,"Quantity"]+quantity
            break
    
    if(flag==True):
        fd.to_csv(os.path.dirname(__file__)+"\Inventory.csv",index=False)
    else:
        print("Product is not found.")


# In[6]:


def updateInventory(id:str,quantity:int):
    fd=open(os.path.dirname(__file__)+"\Inventory.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    if id in s:
        if quantity<0 and s[id]["quantity"]<abs(quantity):
            print("Enough quantity is not present.")
            return False
        else:
            s[id]["quantity"]+=quantity
            fd=open(os.path.dirname(__file__)+"\Inventory.json","w")
            fd.write(json.dumps(s))
            return True
    else:
        print("The product is not found.")
        return False


# ## Updating The Unit Price

# In[7]:


def updatePrice(id:str,price:int):
    fd=open(os.path.dirname(__file__)+"\Inventory.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    if id in s:
        s[id]["price"]=price
        fd=open(os.path.dirname(__file__)+"\Inventory.json","w")
        fd.write(json.dumps(s))
        fd.close()
        return True
    else:
        print("The product is not found.")
        return False


# ## Deleting Products

# In[8]:


def deleteProduct(id:str):
    fd=open(os.path.dirname(__file__)+"\Inventory.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    if id in s:
        s.pop(id)
        fd=open(os.path.dirname(__file__)+"\Inventory.json","w")
        fd.write(json.dumps(s))
        fd.close()
        return True
    else:
        return False


# ## Generating Purchase and Sales Records

# #### Purchase Details:- <br>
# #### 1. Merchant Name<br>
# #### 2. Contact Details of the merchant<br>
# #### 3. Product ID<br>
# #### 4. Quantity <br>
# #### 5. Total Cost<br>
# #### 6. Purchase Time

# {"merchant_name1":{"time1":{"contacts":contact,"id":id1,"quantity":100,"total cost":10000},
#                   "time2":{"contacts":contact,"id":id2,"quantity":1000,"total cost":10000}},
# "merchant_name2":{"time2":{"contacts":contact,"id":id2,"quantity":100,"total cost":10000},
#                   "time4":{"contacts":contact,"id":id4,"quantity":1000,"total cost":10000}}}

# In[9]:


def purchase():
    fd=open(os.path.dirname(__file__)+"\Purchasings.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    
    
    merchant=input("Please enter the merchant name:- ")
    contact=input("Please enter the contact details of the merchant:- ")
    timeArray=[]
    
    while(True):
        id=input("Please enter the product id:- ")
        q=int(input("Please enter the quantity:-"))
        
        if(updateInventory(id,q)==True):
            details=productDetails(id)
            p=details["price"]
            
            
            d=str(datetime.datetime.now())
            
            if merchant in s:
                s[merchant][d]={"contacts":contact,"id":id,"quantity":q,"total cost":(p*q)}
            else:
                s[merchant]={d:{"contacts":contact,"id":id,"quantity":q,"total cost":(p*q)}}
            
            timeArray.append([d,details["name"],details["price"]])
            
            
            
        flag=input("Do you want to purchase more from the current merchant(Yes:- 1 or No:- 0)?:- ")
        if(flag=="0"):
            break
    
    fd=open(os.path.dirname(__file__)+"\Purchasings.json","w")
    fd.write(json.dumps(s))
    fd.close()
    
    
    d=datetime.datetime.now()
    filepath=os.path.dirname(__file__)+"\Purchasing Receipts\\"+merchant+" "+str(d.date())+" "+d.strftime("%H-%M-%S.%f")+".csv"
    fd=open(filepath,"a")
    print("_"*200)
    print("Purchasing Receipt on ",datetime.datetime.now(),":- ",sep="")
    fd.write("Purchasing Receipt on:-,"+str(datetime.datetime.now())+"\n")
    print("Merchant Name:- "+merchant,sep="")
    fd.write("Merchant Name:-,"+merchant+"\n")
    print("Merchant Contact:- "+contact)
    fd.write("Merchant Contact:-,"+contact+"\n")
    print("_"*200)
    print("Serial Number\tProduct ID\tProduct Name\tUnit Price\t\tQuantity Purchased\tTotal Price")
    fd.write("Serial Number,Product ID,Product Name,Unit Price,Quantity Purchased,Total Price\n")
    print("_"*200)
    
    t=0
    for i in range(len(timeArray)):
        print((i+1),"\t",s[merchant][timeArray[i][0]]["id"],timeArray[i][1],timeArray[i][2],"\t",s[merchant][timeArray[i][0]]["quantity"],"\t",s[merchant][timeArray[i][0]]["total cost"],sep="\t")
        fd.write(str(i+1)+","+s[merchant][timeArray[i][0]]["id"]+","+timeArray[i][1]+","+str(timeArray[i][2])+","+str(s[merchant][timeArray[i][0]]["quantity"])+","+str(s[merchant][timeArray[i][0]]["total cost"])+"\n")
        t+=s[merchant][timeArray[i][0]]["total cost"]
        
        
    print("\t\t\t\t\t\t\t\t\tTotal Amount\t",t,sep="\t")
    print("_"*200)
    fd.write(",,,,Total Amount,"+str(t))
    fd.close()


# #### Sales Details:- <br>
# #### 1. User Name<br>
# #### 2. Contact Details of the user<br>
# #### 3. Product ID<br>
# #### 4. Quantity <br>
# #### 5. Total Price<br>
# #### 6. Sales Time

# {"username1":{"time1":{"contacts":contact,"id":id1,"quantity":100,"total cost":10000},
#               "time2":{"contacts":contact,"id":id2,"quantity":1000,"total cost":10000}}, 
# "username2":{"time2":{"contacts":contact,"id":id2,"quantity":100,"total cost":10000},
#              "time4":{"contacts":contact,"id":id4,"quantity":1000,"total cost":10000}}}

# In[12]:


def sales():
    fd=open(os.path.dirname(__file__)+"\Sales.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    
    
    un=input("Please enter your user name:- ")
    contact=input("Please enter your contact details:- ")
    timeArray=[]
    totalCost=0
    
    while(True):
        id=input("Please enter the product id:- ")
        q=int(input("Please enter the quantity:-"))
        
        if(updateInventory(id,q)==True):
            details=productDetails(id)
            p=details["price"]
            
            
            d=str(datetime.datetime.now())
            totalCost+=p*q
            
            if un in s:
                s[un][d]={"contacts":contact,"id":id,"quantity":q,"total cost":(p*q)}
            else:
                s[un]={d:{"contacts":contact,"id":id,"quantity":q,"total cost":(p*q)}}
            
            timeArray.append([d,details["name"],details["price"]])
            
            
            
        flag=input("Do you want to buy more(Yes:- 1 or No:- 0)?:- ")
        if(flag=="0"):
            break
    
    t=totalCost
    if totalCost>=10000:
        t=totalCost*0.8
        for i in timeArray:
            s[un][i[0]]["total cost"]=s[un][i[0]]["total cost"]*0.8
    
        
    fd=open(os.path.dirname(__file__)+"\Sales.json","w")
    fd.write(json.dumps(s))
    fd.close()
    
    
    d=datetime.datetime.now()
    filepath=os.path.dirname(__file__)+"\Sales Receipts\\"+un+" "+str(d.date())+" "+d.strftime("%H-%M-%S.%f")+".csv"
    fd=open(filepath,"a")
    print("_"*200)
    print("Sales Receipt on ",datetime.datetime.now(),":- ",sep="")
    fd.write("Sales Receipt on:-,"+str(datetime.datetime.now())+"\n")
    print("User Name:- "+un,sep="")
    fd.write("User Name:-,"+un+"\n")
    print("User Contact:- "+contact)
    fd.write("User Contact:-,"+contact+"\n")
    print("_"*200)
    print("Serial Number\tProduct ID\tProduct Name\tUnit Price\t\tQuantity Purchased\tTotal Price")
    fd.write("Serial Number,Product ID,Product Name,Unit Price,Quantity Purchased,Total Price\n")
    print("_"*200)
    
    for i in range(len(timeArray)):
        if t==totalCost:
            print((i+1),"\t",s[un][timeArray[i][0]]["id"],timeArray[i][1],timeArray[i][2],"\t",s[un][timeArray[i][0]]["quantity"],"\t",s[un][timeArray[i][0]]["total cost"],sep="\t")
            fd.write(str(i+1)+","+s[un][timeArray[i][0]]["id"]+","+timeArray[i][1]+","+str(timeArray[i][2])+","+str(s[un][timeArray[i][0]]["quantity"])+","+str(s[un][timeArray[i][0]]["total cost"])+"\n")
        else:
            print((i+1),"\t",s[un][timeArray[i][0]]["id"],timeArray[i][1],timeArray[i][2],"\t",s[un][timeArray[i][0]]["quantity"],"\t",s[un][timeArray[i][0]]["total cost"]*1.25,sep="\t")
            fd.write(str(i+1)+","+s[un][timeArray[i][0]]["id"]+","+timeArray[i][1]+","+str(timeArray[i][2])+","+str(s[un][timeArray[i][0]]["quantity"])+","+str(s[un][timeArray[i][0]]["total cost"]*1.25)+"\n")
        
        
    print("\t\t\t\t\t\t\t\t\tSubtotal Amount\t",totalCost,sep="\t")
    print("\t\t\t\t\t\t\t\t\tTotal Amount\t",t,sep="\t")
    
    print("_"*200)
    fd.write(",,,,Subtotal Amount,"+str(totalCost)+"\n")
    fd.write(",,,,Total Amount,"+str(t)+"\n")
    fd.close()


# In[11]:


sales()


# ## Displaying Purchasings and Sales records 

# ## Purchasings Records 

# In[ ]:


def displayPurchasings():
    fd=open(os.path.dirname(__file__)+"\Purchasings.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    timeDict={}
    for i in s.keys():#i=merchant names
        for j in s[i].keys():#j=timestamps
            timeDict[j+"|"+i]=s[i][j]
    
    print("Serial number\t\tTime of the purchase\t\t\tMerchant Name\tMerchant Contact\t\tProduct id\tQuantity Purchased\tTotal Cost")
    timeArray=sorted(timeDict.keys())
    for i in range(len(timeArray)):
        c=timeArray[i].split("|")
        print((i+1),"\t\t\t",c[0],"\t\t",c[1],"\t",timeDict[timeArray[i]]["contacts"],"\t",timeDict[timeArray[i]]["id"],"\t\t",timeDict[timeArray[i]]["quantity"],"\t\t\t",timeDict[timeArray[i]]["total cost"],sep="")


# ## Sales Records

# In[ ]:


def displaySales():
    fd=open(os.path.dirname(__file__)+"\Sales.json","r")
    s=json.loads(fd.read())
    fd.close()
    
    timeDict={}
    for i in s.keys():#i=user names
        for j in s[i].keys():#j=timestamps
            timeDict[j+"|"+i]=s[i][j]
    
    print("Serial number\t\tTime of the buying\t\t\tUser Name\tUser Contact\t\tProduct id\t\tQuantity Bought\t\tTotal Cost")
    timeArray=sorted(timeDict.keys())
    for i in range(len(timeArray)):
        c=timeArray[i].split("|")
        print((i+1),"\t\t\t",c[0],"\t\t",c[1],"\t\t",timeDict[timeArray[i]]["contacts"],"\t\t",timeDict[timeArray[i]]["id"],"\t\t\t",timeDict[timeArray[i]]["quantity"],"\t\t\t",timeDict[timeArray[i]]["total cost"],sep="")


# ## Integrating all functions together

# In[ ]:


while(True):
    print("Please enter you choice by entering the corresponding numbers associated with the choices:- ")
    print("1. Adding Products")
    print("2. Deleting products")
    print("3. Displaying Product details")
    print("4. Updating Inventory")
    print("5. Updating Price")
    print("6. Purchasing Items")
    print("7. Selling Items")
    print("8. Display Purchasings")
    print("9. Display Sales")
    print("10. Exiting Options")
    choice=input("Please enter your choice:- ")
    
    match choice:
        case "1":
            name=input("Please enter product name:- ")
            p=int(input("Please enter unit price:- "))
            q=int(input("Please enter available quantity:- "))
            addProduct(name,p,q)
        
        case "2":
            id=input("Please enter id of the product to be deleted:- ")
            deleteProduct(id)

        case "3":
            id=input("Please enter product id:- ")
            print("ID\tName\tUnit Price\tQuantity Available")
            s=productDetails(id)
            print(id,s["name"],s["price"],s["quantity"],sep="\t")
            
        case "4":
            id=input("Please enter product id:- ")
            q=input("Please enter quantity to be added:- ")
            updateInventory(id,int(q))

        case "5":
            id=input("Please enter id of the product whose unit price is to be updated:- ")
            price=int(input("Please enter the new unit price of the product:- "))
            updatePrice(id,price)
        
        case "6":
            purchase()
            
        case "7":
            sales()
        
        case "8":
            displayPurchasings()
        case "9":
            displaySales()
        case "10":
            break
        case _:
            print("You have entered an invalid choice. You may please try again.")


# In[ ]:




