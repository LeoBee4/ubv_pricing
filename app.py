import streamlit as st

arrangemnt_drinks = {
    1 : {'name': 'Stëlz', 'price': 7.50, 'btw': 21},
    2 : {'name': 'Bier / Wijn / Fris / Stelzer', 'price': 12.00, 'btw': 21},
    3 : {'name': 'Onbeperkt drank', 'price': 11.94, 'btw': 21},
    7 : {'name': 'Kurkgeld', 'price': 1.25, 'btw': 9}
}
arrangemnt_food = {
    3 : {'name': 'Mediterraanse borrelplank', 'price': 6.50, 'btw': 9},
    4 : {'name': 'Matroos', 'price': 4.94, 'btw': 9},
    5 : {'name': 'Stuurman', 'price': 6.50, 'btw': 9},
    6 : {'name': 'Kapitein', 'price': 9.00, 'btw': 9}
}

def calculate_price(hours, voorvaarkosten, nr_people, arrangement_drinks, arrangement_food, company, night=False, custom_price=None):
    if custom_price:
        return custom_price
    # Price per hour
    sailing_price = max(400, 200 * hours) if not night else max(450, 200 * hours)
    if nr_people >= 20:
        sailing_price = sailing_price + (nr_people - 19) * 10 if not night else sailing_price + (nr_people - 19) * 15
    sailing_price = sailing_price * (1 + company * 0.09)

    # total price drinks
    total_price_drinks = 0
    for value in arrangemnt_drinks.values():
        if value['name'] == arrangement_drinks:
            ## Correct price for drinks incl and excl btw
            total_price_drinks = value['price'] * nr_people * (1 + (company * (1 + value['btw']/100)))
            break
    
    # total price food
    total_price_food = 0
    for value in arrangemnt_food.values():
        if value['name'] == arrangement_food:
            total_price_food = value['price'] * nr_people + (1 + company * (1 + value['btw']/100))
            break

    total_price = sailing_price + total_price_drinks + total_price_food + voorvaarkosten
    return total_price
    

def app():
    ## Create streamlit app to fill units and calculate the total price
    ## Add logo utrecht boot verhuur
    st.title('Prijsberekening Utrecht Boot Verhuur')
    st.write('Vul hieronder de gegevens van de vaartocht in om zo een prijs te berekenen.')

    ## Create form to fill in nr hours, people, night, arrangement drinks and food
    company = st.checkbox('Zakelijk tarief')
    custom_price = st.number_input('Eigen prijs:', min_value=0, value=None)
    hours = st.number_input('Aantal uren:', min_value=1, value=1)
    voorvaarkosten = st.number_input('Voorvaarkosten:', min_value=0, value=0)
    nr_people = st.number_input('Aantal personen:', min_value=1, value=1)
    night = st.checkbox('Avondtocht')
    drinks = ['Geen'] + [value['name'] for key, value in arrangemnt_drinks.items()]
    food = ['Geen'] + [value['name'] for key, value in arrangemnt_food.items()]
    arrangement_drinks = st.selectbox('Drank arrangement:', drinks, placeholder='Geen drank arrangement')
    arrangement_food = st.selectbox('Eten arrangement:', food, placeholder='Geen eet arrangement')

    ## Add button to calculate the total price
    if st.button('Bereken prijs'):
        ## Calculate the total price
        total_price = calculate_price(hours, voorvaarkosten, nr_people, arrangement_drinks, arrangement_food, company, night, custom_price)
        st.write('De totale prijs voor de vaartocht is: €', total_price)
        ## Split price into BTW and non BTW price


# Run the app
if __name__ == '__main__':
    app()
