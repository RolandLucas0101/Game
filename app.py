import math
import random
import streamlit as st

st.set_page_config(page_title="Class Tournament Brackets", layout="wide")

TOURNAMENTS = ["Mancala", "Chess"]
ROSTERS = {
    "First Class": [
        "Dorcas Abimbola", "Ebunoluwa Fowowe", "Edwin Amaya", "Elian Almanzar",
        "Emmanuel Tete", "Emmanuela Boateng", "Ethan Crecco", "Fanny Pena",
        "Fatiah Diekola", "Frederick Adewusi", "Gabriela Ramos", "Gabriella Meronuli",
        "Gabrielle Tyre", "Habeeblah Olatunji", "Hafiz Russell", "Hawa Kelleh",
        "Hawwa Diallo", "Hayleyn Angeles",
    ],
    "Second Class": [
        "Austin Rodriguez", "Autumn Cyrus-Mitchell", "Azorey Elam", "Brayan Estrella-Giron",
        "Brianna Chadan", "Bryniyah Neal", "Caio Lessa", "Celeste Benson",
        "Charlotte Tacuri", "Chase Davis", "Chidumebi Dike", "Christian Apple",
        "Dalaina Miller", "Daniel Onyebuchi", "David Agbovi", "David St. Phillippe",
        "David Takouezim", "Davon Carty", "Keily Morrocho", "John Santana",
    ],
    "Third Class": [
        "Ifedasola Salawu", "Inioluwa Ayoola-Oluwoye", "Isa Patterson", "Jackson Palchizaca",
        "Jaden Jackson", "Jaden Paschall", "Jarrel Smith", "Jayden Curry",
        "Jaylin Bouldin", "Jenna Williams", "John Cayamcela", "Jonathan McKinney",
        "Joseph Lane", "Josue Lopez-Reyes", "Joziah Mijangos", "Julian Ortiz",
        "Justin Logan", "Kabir Branch", "Konate Seydo", "Nykolas De Oliveria",
    ],
}

CLASS_ORDER = list(ROSTERS.keys())


def app_state():
    if "data" not in st.session_state:
        st.session_state.data = {}
    return st.session_state.data


def key_for(*parts):
    return "::".join(str(p) for p in parts)


def next_power_of_two(n):
    return 1 if n <= 1 else 2 ** math.ceil(math.log2(n))


def make_seed_slots(players):
    size = next_power_of_two(max(2, len(players)))
    slots = players[:] + ["BYE"] * (size - len(players))
    return slots


def get_tournament(tournament):
    data = app_state()
    if tournament not in data:
        data[tournament] = {
            "entrants": {c: ROSTERS[c][:] for c in CLASS_ORDER},
            "winners": {},
            "notes": {},
        }
    return data[tournament]


def match_winner(tdata, mid, p1, p2):
    if p1 == "BYE" and p2 == "BYE":
        return "BYE"
    if p1 == "BYE":
        return p2
    if p2 == "BYE":
        return p1
    return tdata["winners"].get(mid, "")


def unique_options(roster, current):
    opts = ["-- empty --"] + roster
    if current and current not in opts and current != "BYE":
        opts.append(current)
    return opts


def entrant_editor(tournament, class_name, tdata):
    st.subheader(f"{class_name} roster")
    roster = ROSTERS[class_name]
    entrants = tdata["entrants"].setdefault(class_name, roster[:])
    c1, c2 = st.columns([1, 1])
    with c1:
        active_count = st.number_input(
            "Active player slots",
            min_value=2,
            max_value=max(2, len(roster)),
            value=max(2, min(len(entrants), len(roster))),
            key=key_for(tournament, class_name, "active_count"),
            help="Use this when a smaller group is entering. Each slot can be changed with the dropdowns below.",
        )
    with c2:
        if st.button("Reset this class roster", key=key_for(tournament, class_name, "reset_roster")):
            tdata["entrants"][class_name] = roster[:]
            for k in list(tdata["winners"].keys()):
                if k.startswith(f"{class_name}|"):
                    del tdata["winners"][k]
            st.rerun()

    current = entrants[: int(active_count)]
    while len(current) < int(active_count):
        current.append(roster[len(current) % len(roster)])

    cols = st.columns(2)
    edited = []
    for i, name in enumerate(current):
        opts = unique_options(roster, name)
        default_index = opts.index(name) if name in opts else 0
        with cols[i % 2]:
            choice = st.selectbox(
                f"Seed {i + 1}",
                opts,
                index=default_index,
                key=key_for(tournament, class_name, "seed", i),
            )
        if choice != "-- empty --":
            edited.append(choice)
    tdata["entrants"][class_name] = edited
    return edited


def build_winners_bracket(tournament, class_name, players, tdata):
    slots = make_seed_slots(players)
    rounds = []
    current = slots
    round_num = 1
    while len(current) > 1:
        next_round = []
        match_rows = []
        for i in range(0, len(current), 2):
            p1, p2 = current[i], current[i + 1]
            mid = f"{class_name}|WB|R{round_num}|M{i // 2 + 1}"
            winner = match_winner(tdata, mid, p1, p2)
            match_rows.append((mid, p1, p2, winner))
            next_round.append(winner if winner else f"Winner R{round_num}M{i // 2 + 1}")
        rounds.append(match_rows)
        current = next_round
        round_num += 1
    champion = current[0] if current else ""
    return rounds, champion


def draw_match(tournament, tdata, mid, p1, p2, title):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(f"{p1} vs {p2}")
        if p1 == "BYE" or p2 == "BYE":
            st.caption(f"Automatic winner: {match_winner(tdata, mid, p1, p2)}")
            return match_winner(tdata, mid, p1, p2)
        if p1.startswith("Winner") or p2.startswith("Winner"):
            st.caption("Complete earlier matches first.")
            return ""
        opts = ["", p1, p2]
        current = tdata["winners"].get(mid, "")
        idx = opts.index(current) if current in opts else 0
        winner = st.selectbox("Winner", opts, idx, key=key_for(tournament, mid, "winner"))
        if winner:
            tdata["winners"][mid] = winner
        elif mid in tdata["winners"]:
            del tdata["winners"][mid]
        loser = p2 if winner == p1 else p1 if winner == p2 else ""
        if loser:
            st.caption(f"Loser moves to losers bracket: {loser}")
        return winner


def draw_class_bracket(tournament, class_name, players, tdata):
    if len(players) < 2:
        st.warning("Select at least two players for this class.")
        return "", []
    rounds, champion = build_winners_bracket(tournament, class_name, players, tdata)
    st.subheader(f"{class_name} winners bracket")
    for r, matches in enumerate(rounds, start=1):
        st.markdown(f"### Round {r}")
        cols = st.columns(min(4, max(1, len(matches))))
        for idx, (mid, p1, p2, _) in enumerate(matches):
            with cols[idx % len(cols)]:
                draw_match(tournament, tdata, mid, p1, p2, f"Match {idx + 1}")

    losses = {p: 0 for p in players}
    for matches in rounds:
        for mid, p1, p2, winner in matches:
            if winner and p1 != "BYE" and p2 != "BYE" and not p1.startswith("Winner") and not p2.startswith("Winner"):
                if winner == p1:
                    losses[p2] = losses.get(p2, 0) + 1
                elif winner == p2:
                    losses[p1] = losses.get(p1, 0) + 1
    losers_alive = [p for p, l in losses.items() if l == 1]
    st.subheader(f"{class_name} losers bracket")
    st.info("This section tracks players with one loss. Use it to run consolation matches until one class runner-up remains.")
    if losers_alive:
        lb_key = f"{class_name}|LB|winner"
        opts = [""] + losers_alive
        idx = opts.index(tdata["winners"].get(lb_key, "")) if tdata["winners"].get(lb_key, "") in opts else 0
        lb_winner = st.selectbox("Losers bracket winner", opts, idx, key=key_for(tournament, lb_key))
        if lb_winner:
            tdata["winners"][lb_key] = lb_winner
        st.write("Players currently in losers bracket: " + ", ".join(losers_alive))
    else:
        st.caption("No players have moved into the losers bracket yet.")
    final_champion = champion if champion and not champion.startswith("Winner") and champion != "BYE" else ""
    if final_champion:
        st.success(f"Class champion: {final_champion}")
    return final_champion, losers_alive


def overall_finals(tournament, tdata, class_champions):
    st.header("Overall finals: class champions")
    available = {c: p for c, p in class_champions.items() if p}
    if len(available) < 3:
        st.warning("Complete each class bracket to unlock the 1st/2nd/3rd overall finals.")
        return
    names = list(available.values())
    st.write("Overall finalists: " + ", ".join(f"{c}: {p}" for c, p in available.items()))
    pairs = [(names[0], names[1]), (names[0], names[2]), (names[1], names[2])]
    wins = {n: 0 for n in names}
    for i, (p1, p2) in enumerate(pairs, start=1):
        mid = f"OVERALL|{i}"
        with st.container(border=True):
            st.markdown(f"**Finals Match {i}**")
            st.write(f"{p1} vs {p2}")
            opts = ["", p1, p2]
            current = tdata["winners"].get(mid, "")
            idx = opts.index(current) if current in opts else 0
            w = st.selectbox("Winner", opts, idx, key=key_for(tournament, mid))
            if w:
                tdata["winners"][mid] = w
                wins[w] += 1
    manual = st.checkbox("Use manual overall placements", key=key_for(tournament, "manual_places"))
    if manual:
        remaining = names[:]
        first = st.selectbox("1st place", [""] + remaining, key=key_for(tournament, "place1"))
        second_opts = [n for n in remaining if n != first]
        second = st.selectbox("2nd place", [""] + second_opts, key=key_for(tournament, "place2"))
        third_opts = [n for n in remaining if n not in [first, second]]
        third = st.selectbox("3rd place", [""] + third_opts, key=key_for(tournament, "place3"))
        placements = [first, second, third]
    else:
        placements = [p for p, _ in sorted(wins.items(), key=lambda x: (-x[1], x[0]))]
    if all(placements):
        st.success(f"1st: {placements[0]}  |  2nd: {placements[1]}  |  3rd: {placements[2]}")


def main():
    st.title("Mancala and Chess Tournament Brackets")
    st.caption("Toggle between tournaments, adjust entrants with dropdowns, run class brackets, then finish with overall finals.")
    tournament = st.sidebar.radio("Tournament", TOURNAMENTS)
    tdata = get_tournament(tournament)

    with st.sidebar:
        st.header("Controls")
        if st.button("Shuffle current tournament seeds"):
            for c in CLASS_ORDER:
                random.shuffle(tdata["entrants"][c])
            tdata["winners"].clear()
            st.rerun()
        if st.button("Clear all winners for this tournament"):
            tdata["winners"].clear()
            st.rerun()

    tab_rosters, tab_brackets, tab_finals = st.tabs(["Player dropdowns", "Class brackets", "Overall finals"])
    with tab_rosters:
        for c in CLASS_ORDER:
            entrant_editor(tournament, c, tdata)
            st.divider()

    class_champions = {}
    with tab_brackets:
        for c in CLASS_ORDER:
            with st.expander(c, expanded=True):
                champ, _ = draw_class_bracket(tournament, c, tdata["entrants"].get(c, []), tdata)
                class_champions[c] = champ
    with tab_finals:
        # Recalculate champions after bracket interactions.
        class_champions = {}
        for c in CLASS_ORDER:
            _, champ = build_winners_bracket(tournament, c, tdata["entrants"].get(c, []), tdata)
            class_champions[c] = champ if champ and not str(champ).startswith("Winner") and champ != "BYE" else ""
        overall_finals(tournament, tdata, class_champions)


if __name__ == "__main__":
    main()
