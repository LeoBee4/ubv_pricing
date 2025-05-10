import streamlit as st
import pandas as pd

arrangemnt_drinks = {
    "Stëlz": {"price": 17.50 / 2, "btw": 21},
    "Bier / Wijn / Fris": {"price": 9.00, "btw": 21},
    "Bier / Wijn / Fris EXTRA": {"price": 11, "btw": 21},
    "Kurkgeld": {"price": 2.5, "btw": 9},
}

arrangemnt_food = {
    # "Mediterraanse borrelplank": {"price": 30, "btw": 9, "veelvoud": 4},
    # "Hollandse borrelplank": {"price": 15, "btw": 9, "veelvoud": 4},
    "Mediterraanse borrelplank": {"price": 15, "btw": 9},
    "Hollandse borrelplank": {"price": 12.5, "btw": 9},
    "Warme hapjes": {"price": 20, "btw": 9}, 
    "Lunch - op basis van 2 uur": {"price": 20, "btw": 9},
}


class CalculatePrice:
    def __init__(self, hours, nr_people):
        self.hours = hours
        self.nr_people = nr_people
        pass

    def vaarkosten(self, night=False):
        vaarkosten = (
            max(450, 450 + (200 * (self.hours-2))) if not night else max(500, 500 + (200 * (self.hours-2)))
        )
        if self.nr_people > 20:
            vaarkosten = (
                vaarkosten + (self.nr_people - 20) * 10 * self.hours
                if not night
                else vaarkosten + (self.nr_people - 20) * 15 * self.hours
            )
        return vaarkosten, vaarkosten * 1.09

    def voorvaarkosten(self, voorvaarkosten):
        return voorvaarkosten, voorvaarkosten * 1.09

    def drankarrangement(self, arrangement):
        if arrangement in arrangemnt_drinks.keys():
            arrangement_price = (
                arrangemnt_drinks[arrangement]["price"] * self.nr_people * self.hours
            )
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangemnt_drinks[arrangement]
            )
        else:
            return 0, 0

    def etenarrangement(self, arrangement):
        if (
            arrangement == "Mediterraanse borrelplank"
            or arrangement == "Hollandse borrelplank"
        ):
            # veelvoud = arrangemnt_food[arrangement]["veelvoud"]
            # rest = self.nr_people - (self.nr_people // veelvoud * veelvoud)
            # if rest >= 2 or self.nr_people // veelvoud == 0:
            #     nr_arrangments = self.nr_people // veelvoud + 1
            # else:
            #     nr_arrangments = self.nr_people // veelvoud       
            # arrangement_price = (
            #     arrangemnt_food[arrangement]["price"]
            #     * nr_arrangments
            #     * self.hours
            # )
            arrangement_price = (
                arrangemnt_food[arrangement]["price"] * self.nr_people
            )
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangemnt_food[arrangement]
            )
        elif arrangement == 'Warme hapjes':
            arrangement_price = (
                arrangemnt_food[arrangement]["price"] * self.nr_people
            )
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangemnt_food[arrangement]
            )
        elif arrangement.startswith('Lunch'):
            arrangement_price = arrangemnt_food[arrangement]["price"] * self.nr_people
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangemnt_food[arrangement]
            )
        else:
            return 0, 0

    @staticmethod
    def calculate_prices_incld_btw(price_excl, item):
        return price_excl * (item["btw"] / 100 + 1)


# ✅ 1. Zorg ervoor dat alle sessievariabelen bestaan bij het starten van de app
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "hours" not in st.session_state:
    st.session_state.hours = 2
if "voorvaarkosten" not in st.session_state:
    st.session_state.voorvaarkosten = 0
if "nr_people" not in st.session_state:
    st.session_state.nr_people = 1
if "night" not in st.session_state:
    st.session_state.night = False
if "arrangement_drinks" not in st.session_state:
    st.session_state.arrangement_drinks = "Geen"
if "champagne" not in st.session_state:
    st.session_state.champagne = 0
if "arrangement_food" not in st.session_state:
    st.session_state.arrangement_food = "Geen"


# Functies om sessievariabelen bij te werken
def save_inputs():
    """Slaat de invoerwaarden op in de sessiestatus."""
    st.session_state.hours = hours
    st.session_state.voorvaarkosten = voorvaarkosten
    st.session_state.nr_people = nr_people
    st.session_state.night = night
    st.session_state.arrangement_drinks = arrangement_drinks
    st.session_state.champagne = champagne
    st.session_state.arrangement_food = arrangement_food
    st.session_state.clicked = True  # Verberg invoervelden


def reset_inputs():
    """Reset de sessiestatus en herlaad de invoervelden."""
    st.session_state.clicked = False


st.title("Prijsberekening Utrecht Boot Verhuur")
st.write("Vul hieronder de gegevens van de vaartocht en druk op de bereken knop.")

# Toon invoervelden als er nog geen berekening is uitgevoerd
if not st.session_state.clicked:
    st.write("Details van vaartocht:")
    night = st.checkbox("Avondtocht", value=st.session_state.night)
    hours = st.number_input("Aantal uren:", min_value=2, value=st.session_state.hours)
    voorvaarkosten = st.number_input(
        "Voorvaarkosten:", min_value=0, value=st.session_state.voorvaarkosten
    )
    nr_people = st.number_input(
        "Aantal personen:", min_value=1, value=st.session_state.nr_people
    )

    st.write("Arrangementen:")
    drinks = ["Geen"] + list(arrangemnt_drinks.keys())
    food = ["Geen"] + list(arrangemnt_food.keys())
    arrangement_drinks = st.selectbox(
        "Drank arrangement:",
        drinks,
        index=drinks.index(st.session_state.arrangement_drinks),
    )
    champagne = st.number_input(
        "Aantal flessen champagne:", min_value=0, value=st.session_state.champagne
    )
    arrangement_food = st.selectbox(
        "Eten arrangement:", food, index=food.index(st.session_state.arrangement_food)
    )
    st.button("Bereken prijs", on_click=save_inputs)

# Berekening uitvoeren en tonen als de knop "Bereken prijs" is ingedrukt
if st.session_state.clicked:
    df = pd.DataFrame()
    priceCalculation = CalculatePrice(
        st.session_state.hours,
        st.session_state.nr_people,
    )
    vaarkosten, vaarkostenBTW = priceCalculation.vaarkosten(st.session_state.night)
    voorvaarkosten, voorvaarkostenBTW = priceCalculation.voorvaarkosten(
        st.session_state.voorvaarkosten
    )
    arrangement_drinks, arrangement_drinksBTW = priceCalculation.drankarrangement(
        st.session_state.arrangement_drinks
    )
    champagne_price, champagne_priceBTW = st.session_state.champagne * 60, st.session_state.champagne * 60 * 1.21
    arrangement_food, arrangement_foodBTW = priceCalculation.etenarrangement(
        st.session_state.arrangement_food
    )
    total_price, total_priceBTW = (
        (
            vaarkosten
            + voorvaarkosten
            + arrangement_drinks
            + arrangement_food
        ),
        vaarkostenBTW
        + voorvaarkostenBTW
        + arrangement_drinksBTW
        + arrangement_foodBTW
    )

    # df["Details"] = [
    #     "Vaarkosten",
    #     "Voorvaarkosten",
    #     f"Drank arrangement - {st.session_state.arrangement_drinks}",
    #     f"Champagne - {st.session_state.champagne} flessen",
    #     f"Eten arrangement - {st.session_state.arrangement_food}",
    #     "Totaalprijs",
    # ]

    # df["Bedrag - particulier (€)"] = [
    #     vaarkosten,
    #     voorvaarkosten,
    #     arrangement_drinks,
    #     champagne_price,
    #     arrangement_food,
    #     total_price,
    # ]
    # df["Bedrag - zakelijk (bedrijf) (€)"] = [
    #     vaarkostenBTW,
    #     voorvaarkostenBTW,
    #     arrangement_drinksBTW,
    #     champagne_priceBTW,
    #     arrangement_foodBTW,
    #     total_priceBTW,
    # ]

    # st.write(df)


    st.markdown(f"""
    |             | Bedrag - particulier (€)  | Bedrag - zakelijk (bedrijf) (€) |
    |------------------------------------------|-------------------:|---------------------:|
    | Vaarkosten  | € {vaarkosten:,.2f} | € {vaarkostenBTW:,.2f} |
    | Voorvaarkosten   | € {voorvaarkosten:,.2f} | € {voorvaarkostenBTW:,.2f} |
    | Drank arrangement - {st.session_state.arrangement_drinks}| € {arrangement_drinks:,.2f} | € {arrangement_drinksBTW:,.2f} |
    | Champagne - {st.session_state.champagne} flessen | € {champagne_price:,.2f} | € {champagne_priceBTW:,.2f} |
    | Eten arrangement - {st.session_state.arrangement_food}| € {arrangement_food:,.2f} | € {arrangement_foodBTW:,.2f} |
    | **Totaalprijs**     | **€ {total_price:,.2f}** | **€ {total_priceBTW:,.2f}** |
    """)

    st.button("Nieuwe prijs berekenen", on_click=reset_inputs)
