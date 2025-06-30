
# ff_surge_checklist.py
# (already defined in canvas, will be included)

diff --git a/ff_surge_checklist.py b/ff_surge_checklist.py
index 04e22ea..e1bfc0e 100644
--- a/ff_surge_checklist.py
+++ b/ff_surge_checklist.py
@@ -1,3 +1,150 @@
+import json
+import os
+
+import streamlit as st
+
+DATA_FILE = "surge_checklist.json"
+
+# Default data with a couple of sample cards and sets
+DEFAULT_DATA = {
+    "sets": ["Dawn of Heroes", "Rebellion's Call"],
+    "cards": [
+        {
+            "name": "Cloud Strife",
+            "set": "Dawn of Heroes",
+            "type": "Character",
+            "image": "https://via.placeholder.com/150",
+            "value": 15.0,
+            "owned": False,
+        },
+        {
+            "name": "Warrior of Light",
+            "set": "Dawn of Heroes",
+            "type": "Character",
+            "image": "https://via.placeholder.com/150",
+            "value": 10.0,
+            "owned": False,
+        },
+        {
+            "name": "Moogle's Gift",
+            "set": "Rebellion's Call",
+            "type": "Item/Spell",
+            "image": "https://via.placeholder.com/150",
+            "value": 5.0,
+            "owned": False,
+        },
+    ],
+}
+
+
+def load_data():
+    if os.path.exists(DATA_FILE):
+        with open(DATA_FILE, "r") as f:
+            return json.load(f)
+    return DEFAULT_DATA
+
+
+def save_data(data):
+    with open(DATA_FILE, "w") as f:
+        json.dump(data, f, indent=2)
+
+
+def main():
+    st.set_page_config(page_title="FF Surge Foil Checklist")
+    st.title("🧙‍♂️ FF Surge Foil Checklist")
+
+    data = load_data()
+
+    # Ensure session state for checkboxes
+    if "owned" not in st.session_state:
+        st.session_state["owned"] = {
+            idx: card.get("owned", False) for idx, card in enumerate(data["cards"])
+        }
+
+    # Filter by card types
+    card_types = sorted({card["type"] for card in data["cards"]})
+    selected_types = st.multiselect(
+        "Filter by card type",
+        options=card_types,
+        default=card_types,
+    )
+
+    st.write("### Cards")
+    for idx, card in enumerate(data["cards"]):
+        if card["type"] not in selected_types:
+            continue
+        cols = st.columns([1, 3])
+        with cols[0]:
+            if card.get("image"):
+                # use_container_width avoids deprecated use_column_width
+                st.image(card["image"], use_container_width=True)
+        with cols[1]:
+            owned = st.checkbox(
+                f"{card['name']} ({card['set']}) - ${card['value']:.2f}",
+                value=st.session_state["owned"].get(idx, False),
+                key=f"card_{idx}",
+            )
+            st.session_state["owned"][idx] = owned
+            card["owned"] = owned
+
+    # Stats
+    total_owned = sum(1 for c in data["cards"] if c.get("owned"))
+    total_cards = len(data["cards"])
+    total_value = sum(c["value"] for c in data["cards"] if c.get("owned"))
+
+    st.subheader("Collection Stats")
+    st.write(f"**Owned:** {total_owned}/{total_cards}")
+    st.write(f"**Estimated value:** ${total_value:.2f}")
+
+    # Forms to add new cards and sets
+    with st.expander("Add new card"):
+        with st.form("add_card_form"):
+            name = st.text_input("Name")
+            set_options = data["sets"] + ["<New set>"]
+            set_choice = st.selectbox("Set", options=set_options)
+            new_set = ""
+            if set_choice == "<New set>":
+                new_set = st.text_input("New set name")
+            card_type = st.selectbox(
+                "Type",
+                ["Character", "Basic Land", "Item/Spell", "Promo"],
+            )
+            image_url = st.text_input("Image URL")
+            value = st.number_input("Estimated value", min_value=0.0, step=0.5)
+            submitted = st.form_submit_button("Add card")
+            if submitted and name:
+                if new_set:
+                    set_name = new_set
+                    if set_name not in data["sets"]:
+                        data["sets"].append(set_name)
+                else:
+                    set_name = set_choice
+                new_card = {
+                    "name": name,
+                    "set": set_name,
+                    "type": card_type,
+                    "image": image_url,
+                    "value": value,
+                    "owned": False,
+                }
+                data["cards"].append(new_card)
+                st.session_state["owned"][len(data["cards"]) - 1] = False
+                save_data(data)
+                st.experimental_rerun()
+
+    with st.expander("Add new set"):
+        with st.form("add_set_form"):
+            set_name = st.text_input("Set name")
+            add_set = st.form_submit_button("Add set")
+            if add_set and set_name:
+                if set_name not in data["sets"]:
+                    data["sets"].append(set_name)
+                    save_data(data)
+                    st.experimental_rerun()
+
+    # Save progress when checkboxes change
+    save_data(data)
+
+
+if __name__ == "__main__":
+    main()
