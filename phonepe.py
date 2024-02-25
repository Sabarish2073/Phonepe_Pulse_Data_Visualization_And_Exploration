import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json


#data frame creation
#sql connection
#aggr_insurance
mydb=psycopg2.connect(host="localhost",
                      port="5432",
                      user="postgres",
                      password="postgresql",
                      database="phonepe_data"
                     )
cursor=mydb.cursor()

cursor.execute("select * from aggr_insurance")
mydb.commit()
table1=cursor.fetchall()
aggr_insurance=pd.DataFrame(table1,columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggr_transaction
cursor.execute("select * from aggr_transaction")
mydb.commit()
table2=cursor.fetchall()
aggr_transaction=pd.DataFrame(table2,columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggr_user
cursor.execute("select * from aggr_user")
mydb.commit()
table3=cursor.fetchall()
aggr_user=pd.DataFrame(table3,columns=("State","Year","Quarter","Brand","Count","Percentage"))

#map_insurance
cursor.execute("select * from map_insurance")
mydb.commit()
table4=cursor.fetchall()
map_insurance=pd.DataFrame(table4,columns=("State","Year","Quarter","District","Transaction_count","Transaction_amount"))

#map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table5=cursor.fetchall()
map_transaction=pd.DataFrame(table5,columns=("State","Year","Quarter","District","Transaction_count","Transaction_amount"))

#map_user
cursor.execute("select * from map_user")
mydb.commit()
table6=cursor.fetchall()
map_user=pd.DataFrame(table6,columns=("State","Year","Quarter","District","RegisteredUsers","AppOpens"))

#top_insurance
cursor.execute("select * from top_insurance")
mydb.commit()
table7=cursor.fetchall()
top_insurance=pd.DataFrame(table7,columns=("State","Year","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table8=cursor.fetchall()
top_transaction=pd.DataFrame(table8,columns=("State","Year","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#top_user
cursor.execute("select * from top_user")
mydb.commit()
table9=cursor.fetchall()
top_user=pd.DataFrame(table9,columns=("State","Year","Quarter","Pincodes","RegisteredUsers"))



def Transaction_amount_count_Year(df, Year):
    
    tran_amount_count_year = df[df["Year"] == Year]
    tran_amount_count_year.reset_index(drop=True, inplace=True)

    # Group by state and calculate the sum of transaction count and transaction amount
    tran_amount_count_year_groupby = tran_amount_count_year.groupby("State")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    # Create a bar chart using Plotly Express

    col1, col2 = st.columns(2)  # Split the screen into two columns equally
    with col1:
        fig_amount = px.bar(
            tran_amount_count_year_groupby,
            x="State",
            y="Transaction_amount",
            title=f"<span style='color:#34eb34'>{Year} TRANSACTION AMOUNT</span>",
            color_discrete_sequence=px.colors.sequential.Bluered_r)  
        st.plotly_chart(fig_amount)  # Adjust chart width to fit the container
    with col2:
        fig_count = px.bar(
            tran_amount_count_year_groupby,
            x="State",
            y="Transaction_count",
            title=f"<span style='color:#dd45e6'>{Year} TRANSACTION COUNT</span>",
            color_discrete_sequence=px.colors.sequential.Blackbody_r)  
        st.plotly_chart(fig_count)  # Adjust chart width to fit the container
    col1,col2=st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        # Extract state names
        state_name = [feature["properties"]["ST_NM"] for feature in data1["features"]]
        state_name.sort()

        # Create choropleth map
        fig_india_1 = px.choropleth(
            tran_amount_count_year_groupby,
            geojson=data1,
            locations="State",
            featureidkey="properties.ST_NM",
            color="Transaction_amount",
            color_continuous_scale="tropic",
            range_color=(tran_amount_count_year_groupby["Transaction_amount"].min(), tran_amount_count_year_groupby["Transaction_amount"].max()),
            hover_name="State",
            title=f"<span style='color:#34eb34'>{Year} TRANSACTION AMOUNT</span>",
            fitbounds="locations",
            height=600,
            width=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(
            tran_amount_count_year_groupby,
            geojson=data1,
            locations="State",
            featureidkey="properties.ST_NM",
            color="Transaction_count",
            color_continuous_scale="tropic",
            range_color=(tran_amount_count_year_groupby["Transaction_count"].min(), tran_amount_count_year_groupby["Transaction_count"].max()),
            hover_name="State",
            title=f"<span style='color:#dd45e6'>{Year} TRANSACTION COUNT</span>",
            fitbounds="locations",
            height=600,
            width=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return tran_amount_count_year

def Transaction_amount_count_Quarter(df, Quarter):
    tran_amount_count_quarter = df[df['Quarter']==Quarter]
    tran_amount_count_quarter.reset_index(drop=True, inplace=True)

    # Group by state and calculate the sum of transaction count and transaction amount
    tran_amount_count_quarter_groupby = tran_amount_count_quarter.groupby("State")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    # Create bar charts
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(
            tran_amount_count_quarter_groupby,
            x="State",
            y="Transaction_amount",
            title=f"<span style='color:#34eb34'>{tran_amount_count_quarter['Year'].min()} Year {Quarter}Quarter TRANSACTION AMOUNT</span>",
            color_discrete_sequence=px.colors.sequential.Bluered_r,
            height=650, width=600)  
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(
            tran_amount_count_quarter_groupby,
            x="State",
            y="Transaction_count",
            title=f"<span style='color:#dd45e6'>{tran_amount_count_quarter['Year'].min()} Year {Quarter}Quarter TRANSACTION COUNT</span>",
            color_discrete_sequence=px.colors.sequential.Blackbody_r,
            height=650, width=600)  
        st.plotly_chart(fig_count)

    # Fetch Indian map data
    col1,col2=st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)

        # Extract state names
        state_name = [feature["properties"]["ST_NM"] for feature in data1["features"]]
        state_name.sort()

        # Create choropleth map
        fig_india_1 = px.choropleth(
            tran_amount_count_quarter_groupby,
            geojson=data1,
            locations="State",
            featureidkey="properties.ST_NM",
            color="Transaction_amount",
            color_continuous_scale="tropic",
            range_color=(tran_amount_count_quarter_groupby["Transaction_amount"].min(), tran_amount_count_quarter_groupby["Transaction_amount"].max()),
            hover_name="State",
            title=f"<span style='color:#34eb34'>{tran_amount_count_quarter['Year'].min()} Year {Quarter}Quarter TRANSACTION AMOUNT</span>",
            fitbounds="locations",
            height=600,
            width=600
        )
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(
            tran_amount_count_quarter_groupby,
            geojson=data1,
            locations="State",
            featureidkey="properties.ST_NM",
            color="Transaction_count",
            color_continuous_scale="tropic",
            range_color=(tran_amount_count_quarter_groupby["Transaction_count"].min(), tran_amount_count_quarter_groupby["Transaction_count"].max()),
            hover_name="State",
            title=f"<span style='color:#dd45e6'>{tran_amount_count_quarter['Year'].min()} Year {Quarter}Quarter TRANSACTION COUNT</span>",
            fitbounds="locations",
            height=600,
            width=600
        )
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return tran_amount_count_quarter
#aggr_transaction

def aggr_Transaction_type(df, State):
    aggr_transaction_state = df[df["State"] == State]
    aggr_transaction_state.reset_index(drop=True, inplace=True)

    # Group by state and calculate the sum of transaction count and transaction amount
    aggr_transaction_state_groupby = aggr_transaction_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum().reset_index()

    # Create bar charts
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(
            aggr_transaction_state_groupby,
            x="Transaction_type",
            y="Transaction_count",
            title=f"<span style='color:#34eb34'>{State} TRANSACTION TYPE AND TRANSACTION COUNT</span>",
            color_discrete_sequence=px.colors.sequential.Bluered_r,
            height=650, width=600)  

    #fig_amount.update_xaxes(tickangle=0)  # Rotate the x-axis labels by 90 degrees

        st.plotly_chart(fig_amount)
    with col2:

        fig_count = px.bar(
            aggr_transaction_state_groupby,
            x="Transaction_type",
            y="Transaction_amount",
            title=f"<span style='color:#ff5733'>{State}  TRANSACTION TYPE AND TRANSACTION AMOUNT</span>",
            color_discrete_sequence=px.colors.sequential.amp_r,
            height=650, width=600)  

        #fig_count.update_xaxes(tickangle=0)  # Rotate the x-axis labels by 90 degrees

        st.plotly_chart(fig_count)

#aggr_user_year

def aggr_user_1(df,Year):
    aggr_user_year = df[df["Year"] == Year]
    aggr_user_year.reset_index(drop=True,inplace=True)
    aggr_user_year_groupby=aggr_user_year.groupby("Brand")["Count"].sum().reset_index()

    fig_bar=px.bar(aggr_user_year_groupby,
                x="Brand",
                    y="Count",
                    title=f"<span style='color:#34eb34'>  {Year} BRANDS AND COUNT</span>",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,
                    height=650, width=600  
                )
    st.plotly_chart(fig_bar,use_container_width=True)
    return aggr_user_year

#aggr_user_quarter

def aggr_user_2(df,Quarter):
    aggr_user_quarter = df[df["Quarter"] == Quarter]
    aggr_user_quarter.reset_index(drop=True,inplace=True)
    aggr_user_quarter_groupby=aggr_user_quarter.groupby("Brand")["Count"].sum().reset_index()

    fig_pie=px.pie(aggr_user_quarter,
                names="Brand",
                values="Count",
                title=f"<span style='color:#34eb34'>  Quarter{Quarter} BRANDS AND COUNT </span>",
                hover_data="Percentage",
                color_discrete_sequence=px.colors.sequential.Bluered_r,
                #hole=0.5,
                height=650, width=600  
                )
    st.plotly_chart(fig_pie,use_container_width=True)
    return aggr_user_quarter

    

#aggr_user_state

def aggr_user_3(df,State):
    aggr_user_state = df[df["State"] == State]
    aggr_user_state.reset_index(drop=True,inplace=True)
    aggr_user_state_groupby=aggr_user_state.groupby("Brand")["Count"].sum().reset_index()

    fig_scatter=px.line(aggr_user_state_groupby,
                x="Brand",
                    y="Count",
                    title=f"<span style='color:#34eb34'>{State.upper()} BRANDS AND COUNT</span>",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,
                    markers="o",
                    height=650, width=600  
                )
    st.plotly_chart(fig_scatter,use_container_width=True)
    return aggr_user_state

#map_insure_count

def map_insure_district_1(df,State):
    map_district_1 = df[df["State"] == State]
    map_district_1_groupby=map_district_1.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    map_district_1_groupby.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_dist_pie_1=px.pie(map_district_1_groupby,
                    names="District",
                        values="Transaction_count",
                        title=f"<span style='color:#34eb34'>  {State.upper()} DISTRICT AND COUNT </span>",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height=650, width=600  
                    )
        st.plotly_chart(fig_dist_pie_1)
    with col2:
        fig_dist_pie_2=px.pie(map_district_1_groupby,
                    names="District",
                        values="Transaction_amount",
                        title=f"<span style='color:#dd45e6'>  {State.upper()} DISTRICT AND AMOUNT </span>",
                        color_discrete_sequence=px.colors.sequential.Mint_r,
                        height=650, width=600  
                    )
        st.plotly_chart(fig_dist_pie_2)
    return map_district_1

def map_insure_district_2(df,State):
    map_district_2= df[df["State"] == State]
    map_district_2_groupby=map_district_2.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    map_district_2_groupby.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_dist_pie_1=px.pie(map_district_2_groupby,
                    names="District",
                        values="Transaction_count",
                        title=f"<span style='color:#34eb34'>  {State.upper()} DISTRICT AND COUNT </span>",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height=650, width=600,hole=0.5
                    )
        st.plotly_chart(fig_dist_pie_1)
    with col2:
        fig_dist_pie_2=px.pie(map_district_2_groupby,
                    names="District",
                        values="Transaction_amount",
                        title=f"<span style='color:#dd45e6'>  {State.upper()} DISTRICT AND AMOUNT </span>",
                        color_discrete_sequence=px.colors.sequential.amp_r,
                        height=650, width=600,hole=0.5 
                    )
        st.plotly_chart(fig_dist_pie_2)
    return map_district_2
#map_user_year
def map_user_year(df,Year):
    map_user_year=map_user[map_user["Year"]==Year]
    map_user_year_groupby=map_user_year.groupby("State")[["RegisteredUsers","AppOpens"]].sum().reset_index()
    fig_scatter=px.line(map_user_year_groupby,
                    x="State",
                    y=["RegisteredUsers","AppOpens"],
                    title=f"<span style='color:#dd45e6'>  {Year} REGISTERED USERS and APPOPENS </span>",
                    markers=True,
                    color_discrete_sequence= px.colors.sequential.Bluered_r,
                    width=600,height=650)
    st.plotly_chart(fig_scatter)
    return map_user_year
def map_user_quarter(df,Quarter):
    map_user_quarter=map_user[map_user["Quarter"]==Quarter]
    map_user_quarter_groupby=map_user_quarter.groupby("State")[["RegisteredUsers","AppOpens"]].sum().reset_index()
    fig_pie=px.line(map_user_quarter_groupby,
                    x="State",
                    y=["RegisteredUsers","AppOpens"],
                    title=f"<span style='color:#34eb34'>{map_user_quarter["Year"].min()} Quarter{Quarter} REGISTERED USERS and APPOPENS </span>",
                    markers=True,
                    color_discrete_sequence= px.colors.sequential.Sunset_r,
                    width=600,height=650)
    st.plotly_chart(fig_pie)
    return map_user_quarter

def map_user_district(df,State):
    map_user_district=map_user[map_user["State"]==State]
    map_user_district_groupby=map_user_district.groupby("District")[["RegisteredUsers","AppOpens"]].sum().reset_index()
    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(map_user_district_groupby,
                        x="District",
                        y="RegisteredUsers",
                        title=f"<span style='color:#34eb34'>{State.upper()} REGISTERED USERS  </span>",
                        color_discrete_sequence= px.colors.sequential.Blackbody_r,
                        width=600,height=650)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(map_user_district_groupby,
                        x="District",
                        y="AppOpens",
                        title=f"<span style='color:#34eb34'>{State.upper()} APP OPENS  </span>",
                        color_discrete_sequence= px.colors.sequential.amp_r,
                        width=600,height=650)
        st.plotly_chart(fig_bar_2)
    return map_user_district
#top_user
def top_user_year(df,Year):
    top_user_y=df[df["Year"]==Year]
    top_user_y_groupby=top_user_y.groupby(["State","Quarter"])["RegisteredUsers"].sum().reset_index()
    fig_bar=px.bar(top_user_y_groupby,
                x="State",
                y="RegisteredUsers",
                barmode="group",
                color="Quarter",
                title=f"<span style='color:#34eb34'>Registered Users by State for {Year} -Quarterly (stacked)  </span>",
                color_discrete_sequence= px.colors.sequential.Rainbow_r,
                width=600,height=650)
    st.plotly_chart(fig_bar)
    return top_user_y

def top_user_year_state(df, State):
    top_user_y_s = df[df["State"] == State]
    top_user_y_s_groupby = top_user_y_s.groupby(["Quarter", "Pincodes"])["RegisteredUsers"].sum().reset_index()
    fig_bar = px.bar(top_user_y_s_groupby,
                     x="Quarter",
                     y="RegisteredUsers",
                     color="Pincodes",
                     barmode="stack",
                     title=f"<span style='color:#34eb34'>Registered Users by Quarter for {State} - Pincodes (stacked) </span>",
                     color_discrete_sequence=px.colors.sequential.Rainbow_r,
                     width=800, height=600)
    st.plotly_chart(fig_bar)
    return top_user_y_s

def ques1():
    Brand=aggr_user[["Brand","Count"]]
    Brand2=Brand.groupby("Brand")["Count"].sum().sort_values(ascending=False)
    Brand3=pd.DataFrame(Brand2).reset_index()

    fig_brand=px.pie(Brand3,
                    names="Brand",
                    values="Count",
                    title=f"<span style='color:#34eb34'>Top Mobile Brand Count </span>",
                    color_discrete_sequence= px.colors.sequential.Rainbow)
    return st.plotly_chart(fig_brand)

def ques2():
    Total_Trans_amount_1=aggr_insurance[["State","Transaction_amount"]]
    Total_Trans_amount_2=Total_Trans_amount_1.groupby("State")["Transaction_amount"].sum().sort_values(ascending=False)
    Total_Trans_amount_3=pd.DataFrame(Total_Trans_amount_2).reset_index()

    fig_amount=px.bar(Total_Trans_amount_3,
                    x="State",
                    y="Transaction_amount",
                    title=f"<span style='color:#f505e5'>Top 10 State of Transaction_amount in aggr_insurance  </span>",
                    color_discrete_sequence= px.colors.sequential.Aggrnyl_r)
    return st.plotly_chart(fig_amount)

def ques3():
    Total_Trans_amount_1=aggr_transaction[["State","Transaction_amount"]]
    Total_Trans_amount_2=Total_Trans_amount_1.groupby("State")["Transaction_amount"].sum().sort_values(ascending=False)
    Total_Trans_amount_3=pd.DataFrame(Total_Trans_amount_2).head(10).reset_index()

    fig_amount=px.bar(Total_Trans_amount_3,
                    x="State",
                    y="Transaction_amount",
                    title=f"<span style='color:#f505e5'>Top 10 State of Transaction_amount in aggr_transaction </span>",
                    color_discrete_sequence= px.colors.sequential.Aggrnyl_r)
    return st.plotly_chart(fig_amount)

def ques4():
    Total_map_amount_1=map_insurance[["State","Transaction_amount"]]
    Total_map_amount_2=Total_map_amount_1.groupby("State")["Transaction_amount"].sum().sort_values(ascending=False)
    Total_map_amount_3=pd.DataFrame(Total_map_amount_2).head(10).reset_index()

    fig_amount=px.bar(Total_map_amount_3,
                    x="State",
                    y="Transaction_amount",
                    title=f"<span style='color:#f505e5'>Top 10 States of Transaction_amount in MAP_insurance  </span>",
                    color_discrete_sequence= px.colors.sequential.Blackbody_r,
                    )
    

    return st.plotly_chart(fig_amount)

def ques5():
    Total_map_amount_1=map_insurance[["District","Transaction_amount"]]
    Total_map_amount_2=Total_map_amount_1.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    Total_map_amount_3=pd.DataFrame(Total_map_amount_2).head(10).reset_index()

    fig_amount=px.bar(Total_map_amount_3,
                    x="District",
                    y="Transaction_amount",
                    title=f"<span style='color:#f505e5'>Top 10 District of Transaction_amount in MAP_insurance  </span>",
                    color_discrete_sequence= px.colors.sequential.Blackbody_r,
                    )
    

    return st.plotly_chart(fig_amount)

def ques6():
    Total_map_amount_1=map_transaction[["State","Transaction_amount"]]
    Total_map_amount_2=Total_map_amount_1.groupby("State")["Transaction_amount"].sum().sort_values(ascending=False)
    Total_map_amount_3=pd.DataFrame(Total_map_amount_2).head(10).reset_index()

    fig_amount=px.bar(Total_map_amount_3,
                    x="State",
                    y="Transaction_amount",
                    title=f"<span style='color:#f505e5'>Top 10 States of Transaction_amount in MAP_transaction  </span>",
                    color_discrete_sequence= px.colors.sequential.Blackbody_r,
                    )
   
    return st.plotly_chart(fig_amount)

def ques7():
    Total_map_d_amount_1=map_transaction[["District","Transaction_amount"]]
    Total_map_d_amount_2=Total_map_d_amount_1.groupby("District")["Transaction_amount"].sum().sort_values(ascending=False)
    Total_map_d_amount_3=pd.DataFrame(Total_map_d_amount_2).head(10).reset_index()

    fig_amount=px.pie(Total_map_d_amount_3,
                    names="District",
                    values="Transaction_amount",
                    title=f"<span style='color:#f505e5'>Top 10 District of Transaction_amount in MAP_transaction  </span>",
                    color_discrete_sequence= px.colors.sequential.Aggrnyl_r,
                    hole=0.5)
    return st.plotly_chart(fig_amount)

def ques8():
    Total_map_user_1=map_user[["State","RegisteredUsers"]]
    Total_map_user_2=Total_map_user_1.groupby("State")["RegisteredUsers"].sum().sort_values(ascending=False)
    Total_map_user_3=pd.DataFrame(Total_map_user_2).head(10).reset_index()

    fig_register=px.pie(Total_map_user_3,
                    names="State",
                    values="RegisteredUsers",
                    title=f"<span style='color:#f505e5'>Top 10 State of Registered Users in MAP_Users  </span>",
                    color_discrete_sequence= px.colors.sequential.Rainbow_r,
                    )

    return st.plotly_chart(fig_register)

def ques9():
    Total_map_user_1=map_user[["District","RegisteredUsers"]]
    Total_map_user_2=Total_map_user_1.groupby("District")["RegisteredUsers"].sum().sort_values(ascending=False)
    Total_map_user_3=pd.DataFrame(Total_map_user_2).head(10).reset_index()

    fig_register=px.pie(Total_map_user_3,
                    names="District",
                    values="RegisteredUsers",
                    title=f"<span style='color:#f505e5'>Top 10 District of Registered Users in MAP_Users  </span>",
                    color_discrete_sequence= px.colors.sequential.Rainbow_r,
                    hole=0.5)
    return st.plotly_chart(fig_register)

def ques10():
    Total_map_user_1=map_user[["State","AppOpens"]]
    Total_map_user_2=Total_map_user_1.groupby("State")["AppOpens"].sum().sort_values(ascending=False)
    Total_map_user_3=pd.DataFrame(Total_map_user_2).head(10).reset_index()

    fig_app=px.pie(Total_map_user_3,
                    names="State",
                    values="AppOpens",
                    title=f"<span style='color:#f505e5'>Top 10 State of App Opens </span>",
                    color_discrete_sequence= px.colors.sequential.Bluered_r,
                    hole=0.5
                    )
    return st.plotly_chart(fig_app)

def ques11():
    Total_map_user_1=map_user[["District","AppOpens"]]
    Total_map_user_2=Total_map_user_1.groupby("District")["AppOpens"].sum().sort_values(ascending=False)
    Total_map_user_3=pd.DataFrame(Total_map_user_2).head(10).reset_index()

    fig_app=px.pie(Total_map_user_3,
                    names="District",
                    values="AppOpens",
                    title=f"<span style='color:#f505e5'>Top 10 District of App Opens </span>",
                    color_discrete_sequence= px.colors.sequential.algae_r,
                    hole=0.5
                    )
  
    return st.plotly_chart(fig_app)


class Homepage:
    def show(self):
        
        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button("Welcome"):
                st.balloons()
                st.write({"Name": "Sabarish"}, {"Batch No": "D104"}, {"Project": "Phonepe Data Visualization and Exploration"})

        with col2:
            
            st.title(":violet[PHONEPE DATA VISUALIZATION📊]")
            st.header("Simple, Fast & Secure")
            st.write("One app for all things money.")

            # Path to the video file
            video_path = "S:\\New folder (4)\\Phone Pe Ad(720P_HD).mp4"
            video_width = 600  
            st.video(video_path)
            st.markdown(f"""
                <style>
                    video {{
                        width: {video_width}px !important;
                    }}
                </style>
            """, unsafe_allow_html=True)


class DataExplorationpage:
    def show(self):
        tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
       
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                method1 = st.selectbox("Select the Method", ["Aggregated_Insurance", "Aggregated_Transaction", "Aggregated_User"])

            if method1 == "Aggregated_Insurance":
                col1, col2 = st.columns(2)
                with col1:
                    year_1 = st.radio("Select the year", range(aggr_insurance["Year"].min(),aggr_insurance["Year"].max()+1))

                aggr_insurance_year = Transaction_amount_count_Year(aggr_insurance,year_1)

                col1, col2 = st.columns(2)
                with col1:
                    quarter_1 = st.radio("Select the Quarter", range(int(aggr_insurance_year["Quarter"].min()), int(aggr_insurance_year["Quarter"].max()) + 1))

                Transaction_amount_count_Quarter(aggr_insurance_year,quarter_1)

            elif method1 == "Aggregated_Transaction":
                col1, col2 = st.columns(2)
                with col1:
                    year_2 = st.radio("Select the Year", range(aggr_transaction["Year"].min(), aggr_transaction["Year"].max() + 1))

                aggr_tran_year = Transaction_amount_count_Year(aggr_transaction, year_2)

                col1, col2 = st.columns(2)
                with col1:
                   quarter_2 = st.radio("Select the Quarter", range(int(aggr_tran_year["Quarter"].min()), int(aggr_tran_year["Quarter"].max()) + 1))
                aggr_tran_quarter = Transaction_amount_count_Quarter(aggr_tran_year, quarter_2)

                col1, col2 = st.columns(2)
                with col1:
                    state_1 = st.selectbox("Select the State", aggr_tran_quarter["State"].unique())
                aggr_Transaction_type(aggr_tran_quarter,state_1)

            elif method1 == "Aggregated_User":
                    year_3 = st.radio("Select the Year", range(aggr_user["Year"].min(),aggr_user["Year"].max()+1))
                    aggr_user_year = aggr_user_1(aggr_user,year_3)
                    

                    quarter_3 = st.radio("Select the Quarter", range(int(aggr_user_year["Quarter"].min()),int(aggr_user_year["Quarter"].max()+1)))
                    aggr_user_quarter = aggr_user_2(aggr_user_year, quarter_3)

                    state_2 = st.selectbox("Select the State", aggr_user_quarter["State"].unique())
                    aggr_user_3(aggr_user_quarter,state_2)

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                method2 = st.selectbox("Select the Method", ["Map_Insurance", "Map_Transaction", "Map_User"])
    
            if method2 == "Map_Insurance":
                col1, col2 = st.columns(2)
                with col1:
                    map_year_1 = st.radio("Select the Year", range(map_insurance["Year"].min(), map_insurance["Year"].max() + 1), key="map_insurance_year")
                map_insurance_year = Transaction_amount_count_Year(map_insurance, map_year_1)

                col1, col2 = st.columns(2)
                with col1:
                    map_state_1 = st.selectbox("Select the State", map_insurance_year["State"].unique(), key="map_insurance_state_1")
                map_insure_district_1(map_insurance_year, map_state_1)

                col1, col2 = st.columns(2)
                with col1:
                    map_quarter_1 = st.radio("Select the quarter", range(int(map_insurance_year["Quarter"].min()), int(map_insurance_year["Quarter"].max())), key="map_insurance_quarter_1")
                map_insurance_quarter = Transaction_amount_count_Quarter(map_insurance_year, map_quarter_1)

                col1, col2 = st.columns(2)
                with col1:
                    map_state_2 = st.selectbox("Select the State", map_insurance_quarter["State"].unique(), key="map_insurance_state_2")
                map_insure_district_2(map_insurance_quarter, map_state_2)

            elif method2 == "Map_Transaction":
                col1, col2 = st.columns(2)
                with col1:
                    map_year_1 = st.radio("Select the Year", range(map_transaction["Year"].min(), map_transaction["Year"].max() + 1), key="map_transaction_year")
                map_transaction_year = Transaction_amount_count_Year(map_transaction, map_year_1)

                col1, col2 = st.columns(2)
                with col1:
                    map_state_1 = st.selectbox("Select the State", map_transaction_year["State"].unique(), key="map_transaction_state")
                map_insure_district_1(map_transaction_year, map_state_1)

                col1, col2 = st.columns(2)
                with col1:
                    map_quarter_1 = st.radio("Select the Quarter", range(int(map_transaction_year["Quarter"].min()), int(map_transaction_year["Quarter"].max())), key="map_transaction_quarter")
                map_transaction_quarter = Transaction_amount_count_Quarter(map_transaction_year, map_quarter_1)

                col1, col2 = st.columns(2)
                with col1:
                    map_state_2 = st.selectbox("Select the State", map_transaction_quarter["State"].unique(), key="map_transaction_state_2")
                map_insure_district_2(map_transaction_quarter, map_state_2)

            elif method2 == "Map_User":
                col1, col2 = st.columns(2)
                with col1:
                    map_year = st.radio("Select the Year",range(map_user["Year"].min(),map_user["Year"].max() +1),key="map_user_year")
                map_user_y = map_user_year(map_user, map_year)
                col1,col2=st.columns(2)
                with col1:
                    map_quarter = st.radio("Select the Quarter", range(int(map_user_y["Quarter"].min()),int(map_user_y["Quarter"].max()+1)), key="map_user_quarter")
                map_user_q = map_user_quarter(map_user_y, map_quarter)
                
                col1, col2 = st.columns(2)
                with col1:
                    map_state = st.selectbox("Select the State", map_user_q["State"].unique(), key="map_user_state")
                map_user_state = map_user_district(map_user_q, map_state)
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                method3 = st.selectbox("Select the Method", ["Top_Insurance", "Top_Transaction", "Top_User"])

            if method3 == "Top_Insurance":
                col1, col2 = st.columns(2)
                with col1:
                    top_year_1 = st.radio("Select the Year", range(top_insurance["Year"].min(), top_insurance["Year"].max() + 1))
                top_insure_year = Transaction_amount_count_Year(top_insurance, top_year_1)
                col1, col2 = st.columns(2)
                with col1:
                    top_quarter_1 = st.radio("Select the Quarter", range(top_insure_year["Quarter"].min(), top_insure_year["Quarter"].max() + 1))
                top_insure_quarter = Transaction_amount_count_Quarter(top_insure_year, top_quarter_1)

            elif method3 == "Top_Transaction":
                col1, col2 = st.columns(2)
                with col1:
                    top_year_2 = st.radio("Select the Year", range(top_transaction["Year"].min(), top_transaction["Year"].max() + 1),key="top_year_radio")
                top_trans_year = Transaction_amount_count_Year(top_transaction, top_year_2)
                
                col1, col2 = st.columns(2)
                with col1:
                    top_quarter_2 = st.radio("Select the Quarter", range(top_trans_year["Quarter"].min(), top_trans_year["Quarter"].max() + 1),key="top_quarter_radio")
                top_trans_quarter = Transaction_amount_count_Quarter(top_trans_year, top_quarter_2)

            elif method3 == "Top_User":
                col1, col2 = st.columns(2)
                with col1:
                    top_year_3 = st.radio("Select the Year", range(top_user["Year"].min(), top_user["Year"].max() + 1))
                    user_year = top_user_year(top_user, top_year_3)  
                col1, col2 = st.columns(2)
                with col1:
                    state_3 = st.selectbox("Select the State", user_year["State"].unique(), key="state_selectbox")  
                user_quarter = top_user_year_state(user_year, state_3)

            
class TopChartspage:
    def show(self):
        ques=st.selectbox("Select the Query",("Top Brands of Mobile Used",
                                              "Top 10 State of Transaction_amount in aggr_insurance",
                                              "Top 10 State of Transaction_amount in aggr_transaction",
                                              "Top 10 States of Transaction_amount in MAP_insurance",
                                              "Top 10 District of Transaction_amount in MAP_insurance",
                                              "Top 10 States of Transaction_amount in MAP_transaction",
                                              "Top 10 District of Transaction_amount in MAP_transaction",
                                              "Top 10 State of Registered Users in MAP_Users",
                                              "Top 10 District of Registered Users in MAP_Users",
                                              "Top 10 State of App Opens ",
                                              "Top 10 District of App Opens"))
        if ques=="Top Brands of Mobile Used":
            ques1()
        elif ques=="Top 10 State of Transaction_amount in aggr_insurance":
            ques2()
        elif ques=="Top 10 State of Transaction_amount in aggr_transaction":
            ques3()
        elif ques=="Top 10 States of Transaction_amount in MAP_insurance":
            ques4()
        elif ques=="Top 10 District of Transaction_amount in MAP_insurance":
            ques5()
        elif ques=="Top 10 States of Transaction_amount in MAP_transaction":
            ques6()
        elif ques=="Top 10 District of Transaction_amount in MAP_transaction":
            ques7()
        elif ques=="Top 10 State of Registered Users in MAP_Users":
            ques8()
        elif ques=="Top 10 District of Registered Users in MAP_Users":
            ques9()
        elif ques=="Top 10 State of App Opens":
            ques10()
        elif ques=="Top 10 District of App Opens":
            ques10()

        # Add more logic for data exploration

class MultiPageApp:
    def __init__(self):
        self.pages = {
            "HOME": Homepage(),
            "DATA EXPLORATION": DataExplorationpage(),
            "TOP CHARTS":TopChartspage()
        }

    def run(self):
        with st.sidebar:
           
            select = option_menu(
                menu_title="Main Menu",
                options=["HOME", "DATA EXPLORATION", "TOP CHARTS"],
                menu_icon="chat-text-fill",
                icons=["house-fill","database","bar-chart"],
                styles={
                    "container":{"background-color":"black"},
                    "nav-link":{"color":"white","font-size":"25px"},
                    "nav-link-selected":{"background-color":"#f7611b"}},
                )
        
        # Display the selected page
        selected_page = self.pages.get(select, Homepage())
        selected_page.show()

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    phonepe = MultiPageApp()
    phonepe.run()
