import streamlit as st

arrangemnt_drinks = {
    'Stëlz':  {'price': 7.50, 'btw': 21},
    'Bier / Wijn / Fris / Stelzer':  {'price': 12.00, 'btw': 21},
    'Onbeperkt drank': {'price': 11.94, 'btw': 21},
    'Kurkgeld': {'price': 1.25, 'btw': 9}
}

arrangemnt_food = {
    'Mediterraanse borrelplank': {'price': 6.50, 'btw': 9},
    'Matroos': {'price': 4.94, 'btw': 9},
    'Stuurman': {'price': 6.50, 'btw': 9},
    'Kapitein': {'price': 9.00, 'btw': 9}
}

class CalculatePrice():
    def __init__(self, hours, nr_people):
        self.hours = hours
        self.nr_people = nr_people
        pass

    def vaarkosten(self, night=False):
        vaarkosten = max(400, 200 * self.hours) if not night else max(450, 200 * self.hours)
        if self.nr_people >= 20:
            vaarkosten = vaarkosten + (self.nr_people - 19) * 10 if not night else vaarkosten + (self.nr_people - 19) * 15
        return vaarkosten

    def voorvaarkosten(self, voorvaarkosten):
        return voorvaarkosten

    def drankarrangement(self, arrangement):
        if arrangement in arrangemnt_drinks.keys():
            return arrangemnt_drinks[arrangement]['price'] * self.nr_people * self.hours
        else:
            return 0
        
    def etenarrangement(self, arrangement):
        if arrangement in arrangemnt_food.keys():
            return arrangemnt_food[arrangement]['price'] * self.nr_people * self.hours
        else:
            return 0
        
    @staticmethod
    def calculate_prices_incld_btw(price_excl, btw_percentage):
        return price_excl * btw_percentage


# ✅ 1. Zorg ervoor dat alle sessievariabelen bestaan bij het starten van de app
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "company" not in st.session_state:
    st.session_state.company = False
if "hours" not in st.session_state:
    st.session_state.hours = 1
if "voorvaarkosten" not in st.session_state:
    st.session_state.voorvaarkosten = 0
if "nr_people" not in st.session_state:
    st.session_state.nr_people = 1
if "night" not in st.session_state:
    st.session_state.night = False
if "arrangement_drinks" not in st.session_state:
    st.session_state.arrangement_drinks = "Geen"
if "arrangement_food" not in st.session_state:
    st.session_state.arrangement_food = "Geen"

# Functies om sessievariabelen bij te werken
def save_inputs():
    """Slaat de invoerwaarden op in de sessiestatus."""
    st.session_state.company = company
    st.session_state.hours = hours
    st.session_state.voorvaarkosten = voorvaarkosten
    st.session_state.nr_people = nr_people
    st.session_state.night = night
    st.session_state.arrangement_drinks = arrangement_drinks
    st.session_state.arrangement_food = arrangement_food
    st.session_state.clicked = True  # Verberg invoervelden

def reset_inputs():
    """Reset de sessiestatus en herlaad de invoervelden."""
    st.session_state.clicked = False

st.title('Prijsberekening Utrecht Boot Verhuur')
st.write('Vul hieronder de gegevens van de vaartocht in om zo een prijs te berekenen.')

# Toon invoervelden als er nog geen berekening is uitgevoerd
if not st.session_state.clicked:
    company = st.checkbox('Zakelijk tarief', value=st.session_state.company)
    hours = st.number_input('Aantal uren:', min_value=1, value=st.session_state.hours)
    voorvaarkosten = st.number_input('Voorvaarkosten:', min_value=0, value=st.session_state.voorvaarkosten)
    nr_people = st.number_input('Aantal personen:', min_value=1, value=st.session_state.nr_people)
    night = st.checkbox('Avondtocht', value=st.session_state.night)

    drinks = ['Geen'] + list(arrangemnt_drinks.keys())
    food = ['Geen'] + list(arrangemnt_food.keys())
    arrangement_drinks = st.selectbox('Drank arrangement:', drinks, index=drinks.index(st.session_state.arrangement_drinks))
    arrangement_food = st.selectbox('Eten arrangement:', food, index=food.index(st.session_state.arrangement_food))
    st.button('Bereken prijs', on_click=save_inputs)

# Berekening uitvoeren en tonen als de knop "Bereken prijs" is ingedrukt
if st.session_state.clicked:
    priceCalculation = CalculatePrice(
        st.session_state.hours, 
        st.session_state.nr_people, 
    )
    vaarkosten = priceCalculation.vaarkosten(st.session_state.night)
    voorvaarkosten = priceCalculation.voorvaarkosten(st.session_state.voorvaarkosten)
    arrangement_drinks = priceCalculation.drankarrangement(st.session_state.arrangement_drinks)
    arrangement_food = priceCalculation.etenarrangement(st.session_state.arrangement_food)
    total_price = vaarkosten + voorvaarkosten + arrangement_drinks + arrangement_food

    st.markdown(f"""
    |             | Bedrag (€)  |
    |----------------------|------------:|
    | Vaarkosten    | € {vaarkosten:,.2f} |
    | Voorvaarkosten   | € {voorvaarkosten:,.2f} |
    | Drank arrangement| € {arrangement_drinks:,.2f} |
    | Eten arrangement | € {arrangement_food:,.2f} |
    | **Totaalprijs**     | **€ {total_price:,.2f}** |
    """)

    st.button('Nieuwe prijs berekenen', on_click=reset_inputs)
