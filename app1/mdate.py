from datetime import datetime,date

months={"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
def convertdate(inputdate):
    m=months.keys()
    d=inputdate.lower()
    for i in m:
        if i in d:
            #print(True)
            fdate=d.replace(i,str(months[i]))
    fdate=fdate.replace(" ","/")
    return fdate

#convertdate("10 Jan 2024")

def getdate(epoch):
    stringepoch=str(epoch)
    if len(stringepoch)>10:
        for i in range(len(stringepoch)-10):
            epoch=epoch//10
        
    dt_object = datetime.fromtimestamp(epoch)

    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

# print(getdate(1713965400))

def convertepoch(string):
    epoch=datetime.strptime(str(string),"%d/%m/%Y")
    convertedepoch=datetime.timestamp(epoch)

    #print(convertedepoch)

    return convertedepoch

def today():
    todaytime=datetime.strptime(str(date.today()),"%Y-%m-%d")
    todayepoch=datetime.timestamp(todaytime)

    #print(todaytime)

    return todayepoch

def todaydate():
    
    todaytime=datetime.strptime(str(date.today()),"%Y-%m-%d")
    today=str(todaytime).split(" ")[0].replace("-","")
    
    return today

def tillmaturity(mdate,tdate):
    #print(mdate)
    #print(tdate)
    if(int(tdate)>int(mdate)):
        return "Matured/Cancelled"
    else:
        epoch=int(mdate)-int(tdate)
        return epoch

def daystillmaturity(seconds):
    try:
        days=int(seconds)/86400
        return days
    except:
        return 0
