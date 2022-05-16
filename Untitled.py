#!/usr/bin/env python
# coding: utf-8

# # Identifying and Recommending Best Restaurants
# 
#  

# Project 1 
# 
# DESCRIPTION
# 
# Data Analysis is the process of creating a story using the data for easy and effective communication. It mostly utilizes visualization methods like plots, charts, and tables to convey what the data holds beyond the formal modeling or hypothesis testing task.
# 
#  
# 
#  Domain: Marketing
# 
# Read the information given below and also refer to the data dictionary provided separately in an excel file to build your understanding.
# 
# Problem Statement
# A restaurant consolidator is looking to revamp its B-to-C portal using intelligent automation tech. It is in search of different matrix to identify and recommend restaurants. To make sure an effective model can be achieved it is important to understand the behaviour of the data in hand.
# 
#  
# 
# 
# 

# Approach:
# 1. Data Preliminary analysis:
# 
# Perform preliminary data inspection and report the findings as the structure of the data, missing values, duplicates cleaning variable names etc.
# Based on the findings from the previous questions identify duplicates and remove them.
# 
# 2. Prepare a preliminary report of the given data by answering following questions.
# Expressing the results using graphs and plot will make it more appealing.
# 
# Explore the geographical distribution of the restaurants, finding out the cities with maximum / minimum number of restaurants.
# Explore how ratings are distributed overall.
# Restaurant franchise is a thriving venture. So, it becomes very important to explore the franchise with most national presence.
# What is the ratio between restaurants that allow table booking vs that do not allow table booking?
# What is the percentage of restaurants providing online delivery?
# Is there a difference in no. of votes for the restaurants that deliver and the restaurant that don’t?
# What are the top 10 cuisines served across cities?
# What is the maximum and minimum no. of cuisines that a restaurant serves? Also, what is the relationship between No. of cuisines served and Ratings
# Discuss the cost vs the other variables.
# Explain the factors in the data that may have an effect on ratings e.g. No. of cuisines, cost, delivery option etc.
# All the information gathered here will lead to a better understanding of the data and allow for a better implementation of ML models.
# 
#  
# 
# 

# Project Task: Week 1
# 
# Importing, Understanding, and Inspecting Data :
# 
# Perform preliminary data inspection and report the findings as the structure of the data, missing values, duplicates, etc.
# 
# Based on the findings from the previous questions, identify duplicates and remove them
# 
# Performing EDA:
# 
# Explore the geographical distribution of the restaurants and identify the cities with the maximum and minimum number of restaurants
# 
# Restaurant franchising is a thriving venture. So, it is very important to explore the franchise with most national presence
# 
# Find out the ratio between restaurants that allow table booking vs. those that do not allow table booking
# 
# Find out the percentage of restaurants providing online delivery
# 
# Calculate the difference in number of votes for the restaurants that deliver and the restaurants that do not deliver
# 
#  
# 
# 

# Project Task: Week 2
# 
# Performing EDA:
# 
# What are the top 10 cuisines served across cities?
# 
# What is the maximum and minimum number of cuisines that a restaurant serves? Also, which is the most served cuisine across the restaurant for each city?
# 
# What is the distribution cost across the restaurants? 
# 
# How ratings are distributed among the various factors?
# 
# Explain the factors in the data that may have an effect on ratings. For example, number of cuisines, cost, delivery option, etc.
# 
# 

# Dashboarding:
# 
# Visualize the variables using Tableau to help user explore the data and create a better understanding of the restaurants to identify the ‘’star’’ restaurant
# 
# Demonstrate  the variables associated with each other and factors to build a dashboard

# In[3]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[12]:


cc=pd.read_excel("Country-Code.xlsx")


# In[13]:


data=pd.read_excel("data.xlsx")


# In[14]:


variable=pd.read_excel("variable description.xlsx")


# In[15]:


cc.head()


# In[9]:


data.head()


# In[10]:


variable.head()


# In[11]:


data.info()


# In[16]:


df_rest = pd.merge(data,cc,on='Country Code',how='left')
df_rest.head()


# In[17]:


df_rest.columns = df_rest.columns.str.replace(' ','_')
df_rest.columns


# In[18]:


df_rest.info()


# In[19]:


df_rest.isnull().sum() #total number of null entries per column


# In[20]:


df_rest[df_rest['Restaurant_Name'].isnull()]


# In[21]:


#Since the restaurant name is missing, we dropped the record and reset the index.
df_rest.dropna(axis=0,subset=['Restaurant_Name'],inplace=True)
df_rest.reset_index(drop=True,inplace=True)
df_rest[df_rest['Cuisines'].isnull()]


# In[22]:


#Since there were only 9 records without cuisines, we have replace the null values with Others.
df_rest['Cuisines'].fillna('Others',inplace=True)


# In[23]:


df_rest.isnull().sum()
df_rest.info()


# In[24]:


cntry_dist = df_rest.groupby(['Country_Code','Country']).agg( Count = ('Restaurant_ID','count'))
cntry_dist.sort_values(by='Count',ascending=False)
#We observe that India has then highest number of restaurants with 8651 restaurants and USA is number 2 with 434 restaurants


# In[25]:


cntry_dist.plot(kind='barh')


# In[26]:


city_dist = df_rest.groupby(['Country','City']).agg(Count = ('Restaurant_ID','count'))
city_dist.describe()
#city with max restaurant has count = 5473
#city with min restaurant has count = 1


# In[27]:


city_dist.sort_values(by='Count',ascending=False)
# we see that new Delhi has the maximum restaurant with 5473
# we observe that multiple cities have only one restaurant.


# In[28]:


min_cnt_rest = city_dist[city_dist['Count']==1]
min_cnt_rest.info()
min_cnt_rest
#There are 46 cities in 7 different countries with 1 restaurants


# In[29]:


max_rate = df_rest.sort_values(by='Aggregate_rating',ascending=False).groupby(['Country','City'],as_index=False).first()
#highest rating restaurants

min_rate = df_rest.sort_values(by='Aggregate_rating',ascending=False).groupby(['Country','City'],as_index=False).last()
#lowest rating restaurants


# In[30]:


df_max=max_rate[['Country','City','Restaurant_Name','Aggregate_rating']] #new dataframe created for high rated restaurants

df_min=min_rate[['Country','City','Restaurant_Name','Aggregate_rating']] #new dataframe created for low rated restaurants

rating_rest=df_max.merge(df_min,left_on='City',right_on='City',how='inner') #merge into single dataframe


# In[31]:


rating_rest


# In[32]:


rating_rest.drop(columns='Country_y',axis=1,inplace=True)
rating_rest.columns = ['Country','City','Highest Rated Restaurant','Rating Max','Lowest Rated Restaurant','Rating Min']
rating_rest


# In[33]:


#since India and USA has the most number of restaurants, 
#we will try to see the distribution of restaurants ratings for these two countries.

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import * 
init_notebook_mode()
import plotly.graph_objs as go #importing plotly or graphs


# In[34]:


rating_rest_city_india=rating_rest[rating_rest['Country']=='India'] #storing the dataframe only for country 'India'
rating_rest_city_india #In India
city=rating_rest_city_india['City'].tolist()#converting the series to list 
rate_max=rating_rest_city_india['Rating Max'].tolist()#converting the series to list
rate_min=rating_rest_city_india['Rating Min'].tolist()#converting the series to list
rest_name_high=rating_rest_city_india['Highest Rated Restaurant'].tolist()#converting the series to list
rest_name_low=rating_rest_city_india['Lowest Rated Restaurant'].tolist()


# In[35]:


stack0 = go.Bar( # GroupBarChart 1 (Highest Rated Resturant)
    x=city,#x axis label
    y=rate_max,# y axis label
    text=rest_name_high,# the value of the restaurant
    name='Highest Rated Restaurant',
     marker=dict(
        color='rgb(76,153,0)', #color of the bar graph's marker
        line=dict(
            color='rgb(76,153,0)', #color of the bar graph's line
            width=1.5, #width of the bar graph
        )
    ),
    opacity=1.0
)
stack1 = go.Bar( # GroupBarChart 2 (Lowest Rated Resturant)
    x=city,
    y=rate_min,
      text=rest_name_low,
    name='Lowest Rated Restaurant',
     marker=dict(
        color='rgb(255,0,0)',#color of the bar graph's marker
        line=dict(
            color='rgb(255,0,0)',#color of the bar graph's line
            width=1.5, #width of the bar graph
        )
    ),
    opacity=1.0
)

data = [stack0,stack1]
layout = go.Layout(
    legend=dict( #the layout of the graph( beautification)
        x=0,
        y=1,
        traceorder='normal',
        font=dict(
             family='sans-serif',
            size=12,
            color='#000'
        ),
        bgcolor='#E2E2E2',
        bordercolor='#FFFFFF',
        borderwidth=2
    ),
    autosize=False,
    width=1000, # size of the graph
    height=450,
    barmode='group',
    title="Graph 1.1: Restaurants rating of India <br>\
    <i>hover with cursor to see restaurant's name</i>", #title of the graph
    plot_bgcolor='rgba(245, 246, 249, 1)',
    xaxis=dict(tickangle=-45,title= 'City of India'), #making the graphs label inclined at 45 deg
    yaxis= {'title': 'Rating(scale of 5)'} #label of y-axis
    )
fig = go.Figure(data=data, layout=layout) #plotting the graph
iplot(fig, filename='style-barbar')


# In[36]:


#perform the same steps as above for Country='United States'
rating_rest_city_usa = rating_rest[rating_rest['Country']=='United States']
rating_rest_city_usa
cityu = rating_rest_city_usa['City'].tolist()
rate_maxu = rating_rest_city_usa['Rating Max'].tolist()
rate_minu = rating_rest_city_usa['Rating Min'].tolist()
rest_name_highu = rating_rest_city_usa['Highest Rated Restaurant'].tolist()
rest_name_lowu = rating_rest_city_usa['Lowest Rated Restaurant'].tolist()


# In[37]:


stack0 = go.Bar( # GroupBarChart 1 (Highest Rated Resturant)
    x=cityu,#x axis label
    y=rate_maxu,# y axis label
    text=rest_name_highu,# the value of the restaurant
    name='Highest Rated Restaurant',
     marker=dict(
        color='rgb(76,153,0)', #color of the bar graph's marker
        line=dict(
            color='rgb(76,153,0)', #color of the bar graph's line
            width=1.5, #width of the bar graph
        )
    ),
    opacity=1.0
)
stack1 = go.Bar( # GroupBarChart 2 (Lowest Rated Resturant)
    x=cityu,
    y=rate_minu,
    text=rest_name_lowu,
    name='Lowest Rated Restaurant',
     marker=dict(
          color='rgb(255,0,0)',#color of the bar graph's marker
        line=dict(
            color='rgb(255,0,0)',#color of the bar graph's line
            width=1.5, #width of the bar graph
        )
    ),
    opacity=1.0
)

data = [stack0,stack1]
layout = go.Layout(
    legend=dict( #the layout of the graph( beautification)
        x=0,
        y=1,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=12,
            color='#000'
        ),
         bgcolor='#E2E2E2',
        bordercolor='#FFFFFF',
        borderwidth=2
    ),
    autosize=False,
    width=1000, # size of the graph
    height=450,
    barmode='group',
    title="Graph 1.1: Restaurants rating of USA <br>\
    <i>hover with cursor to see restaurant's name</i>", #title of the graph
    plot_bgcolor='rgba(245, 246, 249, 1)',
    xaxis=dict(tickangle=-45,title= 'City of USA'), #making the graphs label inclined at 45 deg
    yaxis= {'title': 'Rating(scale of 5)'} #label of y-axis
)
fig = go.Figure(data=data, layout=layout) #plotting the graph
iplot(fig, filename='style-barbar')


# In[38]:


df_rest1 = df_rest.copy()
df_rest1.columns


# In[39]:


dummy = ['Has_Table_booking','Has_Online_delivery']
df_rest1 = pd.get_dummies(df_rest1,columns=dummy,drop_first=True)
df_rest1.head()
# 0 indicates 'NO'
# 1 indicates 'YES'


# In[40]:


#Ration between restaurants allowing table booking and those which dont
table_booking = df_rest1[df_rest1['Has_Table_booking_Yes']==1]['Restaurant_ID'].count()
table_nbooking =df_rest1[df_rest1['Has_Table_booking_Yes']==0]['Restaurant_ID'].count()
print('Ratio between restaurants that allow table booking vs. those that do not allow table booking: ',
      round((table_booking/table_nbooking),2))


# In[41]:


print(table_booking,table_nbooking)


# In[42]:


#Pie chart to show percentage of restaurants which allow table booking and those which don't
labels = 'Table Booking', 'No Table Booking'
sizes = [table_booking,table_nbooking]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots(figsize=(9,9))
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.set_title("Table Booking vs No Table Booking")
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()


# In[43]:


#Percentage of restaurant that has online delivery
rest_od = df_rest1[df_rest1['Has_Online_delivery_Yes'] == 1]['Restaurant_ID'].count()
rest_nod = df_rest1[df_rest1['Has_Online_delivery_Yes'] == 0]['Restaurant_ID'].count()
print('Percentage of restaurants providing online delivery : {} %'.format((round(rest_od/len(df_rest1),3)*100)))


# In[44]:


#pie chart to show percentages of restaurants allowing online delivery vs those which do not have online delivery
labels = 'Online Delivery','No Online Delivery'
size = [rest_od,rest_nod]
explode = (0.1,0)
fig1,ax1 = plt.subplots(figsize=(9,9))
ax1.pie(size,explode=explode,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
ax1.set_title("Online Delivery vs No Online Delivery")
ax1.axis('equal')
plt.show()


# In[45]:


rest_deliver = df_rest1[df_rest1['Has_Table_booking_Yes'] == 1]['Votes'].sum()
rest_ndeliver = df_rest1[df_rest1['Has_Table_booking_Yes'] == 0]['Votes'].sum()
print('Difference in number of votes for restaurants that deliver and dont deliver: ',abs((rest_deliver - rest_ndeliver)))


# In[46]:


labels = 'Online Delivery','No Online Delivery'
size = [rest_ndeliver,rest_deliver]
explode = (0,0.1)
fig1,ax1 = plt.subplots(figsize=(9,9))
ax1.pie(size,explode=explode,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
ax1.set_title("Votes: Online Delivery vs Votes:No Online Delivery")
ax1.axis('equal')
plt.show()
#out of the total votes about 27.3% votes were given to restaurants that dont have online delivery option
#out of the total votes about 72.7% votes were given to restaurants that dont have online delivery option
#This clearly shows that restaurants that have online delivery are more likely to get a vote(feedback) 


# In[47]:


df_rest.columns
cuisines = df_rest['Cuisines'].apply(lambda x: pd.Series(x.split(',')))
cuisines.columns = ['Cuisine_1','Cuisine_2','Cuisine_3','Cuisine_4','Cuisine_5','Cuisine_6','Cuisine_7','Cuisine_8']
cuisines.tail()


# In[48]:


df_cuisines = pd.concat([df_rest,cuisines],axis=1)
df_cuisines.head()


# In[49]:


cuisine_loc = pd.DataFrame(df_cuisines[['Country','City','Locality_Verbose','Cuisine_1','Cuisine_2','Cuisine_3',
                                        'Cuisine_4','Cuisine_5','Cuisine_6','Cuisine_7','Cuisine_8']])
cuisine_loc_stack=pd.DataFrame(cuisine_loc.stack()) #stacking the columns 
cuisine_loc.head()


# In[50]:


keys = [c for c in cuisine_loc  if c.startswith('Cuisine')]
a=pd.melt(cuisine_loc, id_vars='Locality_Verbose', value_vars=keys, value_name='Cuisines') 
#melting the stack into one row
max_rate=pd.DataFrame(a.groupby(by=['Locality_Verbose','variable','Cuisines']).size().reset_index())
#find the highest restuarant in the city
max_rate
del max_rate['variable']
max_rate.columns=['Locality_Verbose','Cuisines','Count']
max_rate.head()


# In[51]:


#find the highest restuarant in the city
loc=max_rate.sort_values('Count', ascending=False).groupby(by=['Locality_Verbose'],as_index=False).first()
loc.head()


# In[52]:


rating_res=loc.merge(df_rest,left_on='Locality_Verbose',right_on='Locality_Verbose',how='inner') 
#inner join to merge the two dataframe
df=pd.DataFrame(rating_res[['Country','City','Locality_Verbose','Cuisines_x','Count']]) 
#making a dataframe of rating restaurant
country=rating_res.sort_values('Count', ascending=False).groupby(by=['Country'],as_index=False).first()
#grouping the data by country code
con=pd.DataFrame(country[['Country','City','Locality','Cuisines_x','Count']])
con.columns=['Country','City','Locality','Cuisines','Number of restaurants in the country']
#renaming the columns
con1=con.sort_values('Number of restaurants in the country', ascending=False) 
#sorting the restaurants on the basis of the number of restaurants in the country
con1[:10]
final_con=con1.drop(con1.index[[7,10]])


# In[53]:


final_con


# In[54]:


loc_list=final_con['City'] #converting the series to dataframe
a_list=loc_list.tolist()

cui_list=final_con['Cuisines']# converting the series to dataframe
b_list=cui_list.tolist()

count_list=final_con['Number of restaurants in the country']# converting the series to dataframe
c_list=count_list.tolist()
trace0 = go.Bar(# BarChart 1 (Popular cuisines of the country)
    x=b_list, #x axis label
    y=c_list, # y axis label
    text=loc_list, # location of the cuisine
    name='Popular Cuisine',
     marker=dict(
        color=['rgb(255,69,0)',
                'rgb(255,140,0)',
                'rgb(165,42,42)',
                'rgb(220,20,60)',
                'rgb(255,0,0)',
                'rgb(255,99,71)',
                'rgb(255,127,80)',
                'rgb(205,92,92)',
                'rgb(240,128,128)',
                'rgb(233,150,122)',
                'rgb(250,128,114)',
                'rgb(255,160,122)'],
        line=dict(
            color='rgb(255,0,0)',#color of the bar graph's line
            width=1.5, #width of the bar graph
        )
    ),
    opacity=1.0
)
data = [trace0] 
layout = go.Layout(

    legend=dict( #the layout of the graph( beautification)
        x=0,
        y=1,
        traceorder='normal',
        font=dict(
            family='sans-serif',
            size=12,
            color='#000'
        ),
        bgcolor='#E2E2E2',
        bordercolor='#FFFFFF',
        borderwidth=20,
    ),
    autosize=False,
    width=1000, # size of the graph
    height=450,
    margin=Margin(r=20, l=300,
                  b=75, t=125),
    title="Graph 2.1 : Most popular cuisines in the World<br>\
    <i>hover with cursor to see location in the country where they are most popular </i>", #title of the graph
    plot_bgcolor='rgba(245, 246, 249, 1)',
    xaxis=dict(tickangle=-45,title= '<br>Cuisine<br>',mirror=True,showticklabels=True), 
    #making the graphs label inclined at 45 deg
    yaxis= {'title': 'Number of restaurants offering<br> cuisine in the location'},#label of y-axis
)
fig = go.Figure(data=data, layout=layout)#plotting the graph
iplot(fig)


# In[55]:


rest_cuisine = pd.DataFrame(df_cuisines[['Restaurant_Name','City','Cuisine_1','Cuisine_2','Cuisine_3','Cuisine_4',
                                         'Cuisine_5','Cuisine_6','Cuisine_7','Cuisine_8']])
rest_cuisine_stack=pd.DataFrame(rest_cuisine.stack()) #stacking the columns 
rest_cuisine.head()


# In[56]:


keys1 = [c for c in rest_cuisine  if c.startswith('Cuisine')]
b=pd.melt(rest_cuisine, id_vars='Restaurant_Name', value_vars=keys, value_name='Cuisines') 
#melting the stack into one row
max_rate1=pd.DataFrame(b.groupby(by=['Restaurant_Name','variable','Cuisines']).size().reset_index()) 
#find the highest restuarant in the city
max_rate1
del max_rate1['variable']
max_rate1.columns=['Restaurant_Name','Cuisines','Count']
max_rate1.head(20)


# In[57]:


max_rate1.sort_values('Count',ascending=False)
#Cafe Coffee Day has the max number of cuisines and The least number of cuisines in a resaurant is 1.


# In[58]:



Restaurant_Name	Cuisines	Count
2479	Cafe Coffee Day	Cafe	83
4596	Domino's Pizza	Pizza	79
4597	Domino's Pizza	Fast Food	78
12984	Subway	Salad	63
12985	Subway	Healthy Food	63
...	...	...	...
5568	Gabbar's Bar & Kitchen	Chinese	1
5569	Gabbar's Bar & Kitchen	Mexican	1
5570	Gabbar's Bar & Kitchen	Italian	1
5571	Gaga Manjero	World Cuisine	1
15963	Ìàukura€Ùa Sofras€±	Izgara	1
15964 rows × 3 columns

rating = df_rest1[['Restaurant_ID','Restaurant_Name','Country','City','Aggregate_rating','Average_Cost_for_two','Votes','Price_range','Has_Table_booking_Yes','Has_Online_delivery_Yes']]
rating = rating.merge(max_rate1,left_on='Restaurant_Name',right_on='Restaurant_Name',how='left')
rating


# In[59]:


rating = df_rest1[['Restaurant_ID','Restaurant_Name','Country','City','Aggregate_rating','Average_Cost_for_two','Votes','Price_range','Has_Table_booking_Yes','Has_Online_delivery_Yes']]


# In[60]:


rating = rating.merge(max_rate1,left_on='Restaurant_Name',right_on='Restaurant_Name',how='left')
rating


# In[61]:


sns.regplot(x='Count',y='Aggregate_rating',data=rating)
rating[["Count", "Aggregate_rating"]].corr()
#Number of cuisines is not a good factor to decide the rating of a restaurant


# In[62]:


sns.regplot(x='Average_Cost_for_two',y='Aggregate_rating',data=rating)
rating[["Average_Cost_for_two", "Aggregate_rating"]].corr()
#Average cost for two is a weak positive factor to decide the rating of a restaurant


# In[63]:


sns.regplot(x='Votes',y='Aggregate_rating',data=rating)
rating[['Votes','Aggregate_rating']].corr()
##Average cost for two can be a factor to decide the rating of a restaurant


# In[64]:


abc = df_rest1[df_rest1['Has_Online_delivery_Yes'] == 1]['Aggregate_rating'].mean()
xyz = df_rest1[df_rest1['Has_Online_delivery_Yes'] == 0]['Aggregate_rating'].mean()
sns.regplot(x='Price_range',y='Aggregate_rating',data=rating)
rating[['Price_range','Aggregate_rating']].corr()
##Price range can be a factor to decide the rating of a restaurant


# In[65]:


sns.regplot(x='Has_Table_booking_Yes',y='Aggregate_rating',data=rating)
rating[['Has_Table_booking_Yes','Aggregate_rating']].corr()
##Table booking can be a factor to decide the rating of a restaurant


# In[ ]:




