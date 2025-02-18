import streamlit as st

arrangemnt_drinks = {
    "Stëlz": {"price": 17.50 / 2, "btw": 21},
    "Bier / Wijn / Fris": {"price": 11.00, "btw": 21},
    "Bier / Wijn / Fris EXTRA": {"price": 13, "btw": 21},
    "Onbeperkt drank": {"price": 11.94, "btw": 21},
    "Kurkgeld": {"price": 1.25, "btw": 9},
}

arrangement_extra = {
    "Fles champagne": {"price": 60, "btw": 21},
    "Jeux de borreldrank": {"price": 16, "btw": 21},
    "Lunch (3 broodjes)": {"price": 10, "btw": 9},
}

arrangemnt_food = {
    "Mediterraanse borrelplank": {"price": 22, "btw": 9, "veelvoud": 4},
    "Hollandse borrelplank": {"price": 12, "btw": 9, "veelvoud": 4},
    "Matroos": {"price": 4.94, "btw": 9},
    "Stuurman": {"price": 6.50, "btw": 9},
    "Kapitein": {"price": 9.00, "btw": 9},
    "Warme hapjes": {"price": 10, "btw": 9},
}


class CalculatePrice:
    def __init__(self, hours, nr_people):
        self.hours = hours
        self.nr_people = nr_people
        pass

    def vaarkosten(self, night=False):
        vaarkosten = (
            max(400, 200 * self.hours) if not night else max(450, 225 * self.hours)
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

    def extraarrangement(self, arrangement):
        if arrangement == "Fles champagne":
            return arrangement_extra[arrangement][
                "price"
            ], self.calculate_prices_incld_btw(
                arrangement_extra[arrangement]["price"], arrangement_extra[arrangement]
            )
        if arrangement == "Jeux de borreldrank":
            arrangement_price = arrangement_extra[arrangement]["price"] * self.nr_people
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangement_extra[arrangement]
            )
        if arrangement == "Lunch (3 broodjes)":
            arrangement_price = arrangement_extra[arrangement]["price"] * self.nr_people
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangement_extra[arrangement]
            )
        else:
            return 0, 0

    def etenarrangement(self, arrangement):
        if (
            arrangement == "Mediterraanse borrelplank"
            or arrangement == "Hollandse borrelplank"
        ):
            veelvoud = arrangemnt_food[arrangement]["veelvoud"]
            rest = self.nr_people - (self.nr_people // veelvoud * veelvoud)
            if rest > 2 or rest == 0:
                nr_arrangments = self.nr_people // veelvoud + 1
            else:
                nr_arrangments = self.nr_people // veelvoud       
            arrangement_price = (
                arrangemnt_food[arrangement]["price"]
                * nr_arrangments
                * self.hours
            )
            return arrangement_price, self.calculate_prices_incld_btw(
                arrangement_price, arrangemnt_food[arrangement]
            )
        elif arrangement in arrangemnt_food.keys():
            arrangement_price = (
                arrangemnt_food[arrangement]["price"] * self.nr_people * self.hours
            )
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
if "company" not in st.session_state:
    st.session_state.company = False
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
if "arrangement_extra" not in st.session_state:
    st.session_state.arrangement_extra = "Geen"
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
    st.session_state.arrangement_extra = arrangement_extra
    st.session_state.arrangement_food = arrangement_food
    st.session_state.clicked = True  # Verberg invoervelden


def reset_inputs():
    """Reset de sessiestatus en herlaad de invoervelden."""
    st.session_state.clicked = False


st.title("Prijsberekening Utrecht Boot Verhuur")
st.write("Vul hieronder de gegevens van de vaartocht in om zo een prijs te berekenen.")

# Toon invoervelden als er nog geen berekening is uitgevoerd
if not st.session_state.clicked:
    company = st.checkbox("Zakelijk tarief", value=st.session_state.company)
    hours = st.number_input("Aantal uren:", min_value=2, value=st.session_state.hours)
    voorvaarkosten = st.number_input(
        "Voorvaarkosten:", min_value=0, value=st.session_state.voorvaarkosten
    )
    nr_people = st.number_input(
        "Aantal personen:", min_value=1, value=st.session_state.nr_people
    )
    night = st.checkbox("Avondtocht", value=st.session_state.night)

    drinks = ["Geen"] + list(arrangemnt_drinks.keys())
    food = ["Geen"] + list(arrangemnt_food.keys())
    extra = ["Geen"] + list(arrangement_extra.keys())
    arrangement_drinks = st.selectbox(
        "Drank arrangement:",
        drinks,
        index=drinks.index(st.session_state.arrangement_drinks),
    )
    arrangement_extra = st.selectbox(
        "Extra arrangement:",
        extra,
        index=extra.index(st.session_state.arrangement_extra),
    )
    arrangement_food = st.selectbox(
        "Eten arrangement:", food, index=food.index(st.session_state.arrangement_food)
    )
    st.button("Bereken prijs", on_click=save_inputs)

# Berekening uitvoeren en tonen als de knop "Bereken prijs" is ingedrukt
if st.session_state.clicked:
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
    arrangement_extra, arrangement_extraBTW = priceCalculation.extraarrangement(
        st.session_state.arrangement_extra
    )
    arrangement_food, arrangement_foodBTW = priceCalculation.etenarrangement(
        st.session_state.arrangement_food
    )
    total_price, total_priceBTW = (
        (
            vaarkosten
            + voorvaarkosten
            + arrangement_drinks
            + arrangement_food
            + arrangement_extra
        ),
        vaarkostenBTW
        + voorvaarkostenBTW
        + arrangement_drinksBTW
        + arrangement_foodBTW
        + arrangement_extraBTW,
    )

    st.markdown(f"""
    |             | Bedrag (€)  | Bedrag incl. BTW (€) |
    |----------------------|-------------|---------------:|
    | Vaarkosten  | € {vaarkosten:,.2f} | € {vaarkostenBTW:,.2f} |
    | Voorvaarkosten   | € {voorvaarkosten:,.2f} | € {voorvaarkostenBTW:,.2f} |
    | Drank arrangement - {st.session_state.arrangement_drinks}| € {arrangement_drinks:,.2f} | € {arrangement_drinksBTW:,.2f} |
    | Extra arrangement - {st.session_state.arrangement_extra} | € {arrangement_extra:,.2f} | € {arrangement_extraBTW:,.2f} |
    | Eten arrangement - {st.session_state.arrangement_food}| € {arrangement_food:,.2f} | € {arrangement_foodBTW:,.2f} |
    | **Totaalprijs**     | **€ {total_price:,.2f}** | **€ {total_priceBTW:,.2f}** |
    """)

    st.button("Nieuwe prijs berekenen", on_click=reset_inputs)