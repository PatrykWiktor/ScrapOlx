import backend 
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models.layouts import Row
from datetime import datetime



def graph():
    dates = sorted([datetime.combine(i, datetime.min.time()) for i in backend.Acces_Data_Table("date")])
    items = backend.Acces_Data_Table("number_of_items")
    prices = backend.Acces_Data_Table("median_price")
    min_price = backend.Acces_Data_Table("min_price")
    max_price = backend.Acces_Data_Table("max_price")
    high_price = backend.Acces_Data_Table("high_price")
    low_price = backend.Acces_Data_Table("low_price")
    
    # compare price to price from next day
    increse = []
    for i in range(0,len(prices)):
        try:
            increse.append(f'{(prices[i]-prices[i+1])/prices[i]:.3f}')
        except:
            increse.append(0)
    print (increse)

    #First Figure
    s1=figure(width = 1000, height = 600,x_axis_type="datetime",title="Prices",toolbar_location="above",x_axis_label="Date", y_axis_label="Price")
    s1.title.text_font_size = "25px"
    #prices
    s1.dash(dates, prices, size = 50)
    s1.text(dates, prices,text=prices,x_offset=30,y_offset=5)
    #min price
    s1.dash(dates, min_price, size = 50)
    s1.text(dates, min_price,text=min_price,x_offset=30,y_offset=5)
    #max price
    s1.dash(dates, max_price, size = 50)
    s1.text(dates, max_price,text=max_price,x_offset=30,y_offset=5)
    #min to max price
    s1.segment(dates,min_price,dates,max_price,line_width=5)
    #high price
    s1.dash(dates, high_price, size = 50)
    s1.text(dates, high_price,text=high_price,x_offset=30,y_offset=5)
    #low price
    s1.dash(dates, low_price, size = 50)
    s1.text(dates, low_price,text=low_price,x_offset=30,y_offset=5)
    #low to high price
    s1.segment(dates,low_price,dates,high_price,line_width=20)

    #Second Figure
    s2 = figure(width=800, height=600, title="Number of items", x_axis_type="datetime",toolbar_location="above",x_axis_label="Date", y_axis_label="Number of items")
    s2.title.text_font_size = "25px"
    #price
    s2.line(dates,items)
    s2.asterisk(dates,items)
    s2.text(dates,items,text=items,x_offset=10,y_offset=5)


    p = Row(s1, s2)
    show(p)


graph()

