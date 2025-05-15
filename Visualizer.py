import os
import sys
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
import json

from Generator import create_star_system
from StorageDataclasses import StarSystem, Star, Binary, Planet, Territory
import TextLists as TL


def format_star_system(system):
    lines = [f"System Name: {system.name}\n"]

    key_feature = system.keyFeature
    lines.append(f"Key Feature: {key_feature}")
    if key_feature in TL.SYSTEM_FEATURES:
        lines.append(f"Description: {TL.SYSTEM_FEATURES[key_feature]}")
    lines.append("")

    lines.append("Star:")
    if hasattr(system.star, 'starA'):
        lines.append("\tType: Binary Star System")
        for idx, star in enumerate([system.star.starA, system.star.starB], start=1):
            lines.append(f"\tStar {idx}:")
            lines.append(f"\tName: {star.name}")
            lines.append(f"\tType: {star.type}")
            if star.type in TL.STAR_TYPES:
                lines.append(f"    Description: {TL.STAR_TYPES[star.type]}")
            lines.append("")
    else:
        lines.append(f"\tName: {system.star.name}")
        lines.append(f"\tType: {system.star.type}")
        if system.star.type in TL.STAR_TYPES:
            lines.append(f"\tDescription: {TL.STAR_TYPES[system.star.type]}")
        lines.append("")

    def process_zone(zone_name, bodies):
        lines.append(f"{zone_name}:")
        for body in bodies:
            if isinstance(body, str):
                lines.append(f"\t{body}")
            elif hasattr(body, 'name'):
                lines.append(f"\tPlanet: {body.name}")
                lines.append(f"\t\tType: {body.type}")
                lines.append(f"\t\tBody: {body.body}")
                lines.append(f"\t\tGravity: {body.gravity}")
                lines.append(f"\t\tAtmosphere: {body.atmosphericPresence} ({body.atmosphericComposition})")
                lines.append(f"\t\tClimate: {body.climate}")
                lines.append(f"\t\tHabitability: {body.habitability}")
                for orbt in body.orbitalFeatures:
                    lines.append(f"\t\tOrbital: {orbt}")
                lines.append("\t\tTerritories:")
                for terr in body.territories:
                    lines.append(f"\t\tTerrain: {terr.baseTerrain},\nTrait: {terr.territoryTrait}")
                lines.append("")
        lines.append("")

    process_zone("Inner Zone", system.solarZoneInnerElements)
    process_zone("Middle Zone", system.solarZoneMiddleElements)
    process_zone("Outer Zone", system.solarZoneOuterElements)

    return "\n".join(lines)


class StarSystemApp:
    def __init__(self, root):

        #root
        self.root = root
        self.root.title("Star System Generator")
        self.style = ttk.Style("superhero")
        self.root.minsize(800,600)
        self.center_window(1600,900)

        #Variables
        self.last_generated_system = None

        #Save and Load Frame
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10, fill="x")

        self.save_btn = ttk.Button(self.button_frame, text="Save JSON", command=self.save_to_json)
        self.save_btn.pack(side="right", padx=5)

        self.load_btn = ttk.Button(self.button_frame, text="Load JSON", command=self.load_from_json)
        self.load_btn.pack(side="right", padx=5)

        #Notebook for different tabs
        tab_control = ttk.Notebook(root)
        self.random_tab = ttk.Frame(tab_control)
        self.browser_frame = ttk.Frame(tab_control)

        tab_control.add(self.random_tab, text='Text')
        tab_control.add(self.browser_frame, text='Treeview')
        tab_control.pack(expand=1, fill='both')

        self.setup_random_tab()
        self.setup_browser_frame()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_random_tab(self):
        self.random_gen_frame = ttk.Frame(self.random_tab, padding=20)
        self.random_gen_frame.pack(fill="both", expand=True)

        self.generate_btn = ttk.Button(self.button_frame, text="Generate Star System", command=self.generate_star_system)
        self.generate_btn.pack(side="left", padx=5)

        # Output Box
        self.output_text = tk.Text(self.random_gen_frame, wrap="word", height=40, width=100)
        self.output_text.pack(side="left",fill="y", expand=False)

    def setup_browser_frame(self):
        # Main horizontal layout frame
        self.browser_frame = ttk.Frame(self.browser_frame)
        self.browser_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview on the left
        self.tree = ttk.Treeview(self.browser_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Description panel on the right
        self.detail_text = tk.Text(self.browser_frame, wrap="word", width=60)
        self.detail_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Bind tree selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Bind context menu
        contextmenu = tk.Menu(self.browser_frame, tearoff=False)
        contextmenu.add_command(label= "Edit", command = self.edit_tree)
        contextmenu.add_separator()
        contextmenu.add_command(label= "Generate New System", command = self.generate_star_system)

        def do_popup(event):
            selected_item = self.tree.identify_row(event.y)
            self.tree.selection_set(selected_item)
            self.tree.focus(selected_item)
            try:
                contextmenu.tk_popup(event.x_root, event.y_root)
            finally:
                contextmenu.grab_release()

        self.tree.bind("<Button-3>", do_popup)

    def generate_star_system(self):
        self.output_text['state'] = "normal"
        self.output_text.delete(1.0, tk.END)
        system = create_star_system()
        self.last_generated_system = system
        formatted = format_star_system(system)
        self.output_text.insert(tk.END, formatted)
        self.output_text['state'] = "disabled"
        self.display_star_system_tree(system)

    def display_star_system_tree(self, system):
        self.tree.delete(*self.tree.get_children())

        root_id = self.tree.insert("", "end", text=f"Star System: {system.name}", open=True)
        self.tree.insert(root_id, "end", text=f"Key Feature: {system.keyFeature}")

        # Star
        if hasattr(system.star, "starA"):  # Binary
            star_node = self.tree.insert(root_id, "end", text="Star: Binary System", open=True)
            for i, star in enumerate([system.star.starA, system.star.starB], start=1):
                sid = self.tree.insert(star_node, "end", text=f"Star {i}: {star.name}", open=True)
                self.tree.insert(sid, "end", text=f"Star Type: {star.type}")
        else:
            star = system.star
            sid = self.tree.insert(root_id, "end", text=f"Star: {star.name}", open=True)
            self.tree.insert(sid, "end", text=f"Star Type: {star.type}")

        # Zones
        def process_zone(title, bodies):
            zone_id = self.tree.insert(root_id, "end", text=title, open=True)
            for body in bodies:
                if isinstance(body, str):
                    self.tree.insert(zone_id, "end", text=f" {body}")
                else:
                    planet_id = self.tree.insert(zone_id, "end", text=f"{body.type}: {body.name}", open=True)
                    self.tree.insert(planet_id, "end", text=f"Body: {body.body}")
                    self.tree.insert(planet_id, "end", text=f"Gravity: {body.gravity}")
                    self.tree.insert(planet_id, "end", text=f"Atmosphere: {body.atmosphericPresence}")
                    self.tree.insert(planet_id, "end", text=f"Atmosphere Compositions: {body.atmosphericComposition}")
                    self.tree.insert(planet_id, "end", text=f"Climate: {body.climate}")
                    self.tree.insert(planet_id, "end", text=f"Habitability: {body.habitability}")
                    orbital_id = self.tree.insert(planet_id, "end", text="Orbitals", open=True)
                    for orbital in body.orbitalFeatures:
                        if orbital != "No Features":
                            self.tree.insert(orbital_id, "end", text=f"O: {orbital}")
                    for terr in body.territories:
                        self.tree.insert(planet_id, "end", text=f"Territory: {terr.baseTerrain} / {terr.territoryTrait}")

        process_zone("Inner Zone", system.solarZoneInnerElements)
        process_zone("Middle Zone", system.solarZoneMiddleElements)
        process_zone("Outer Zone", system.solarZoneOuterElements)

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        item_text = self.tree.item(selected_item, "text")

        # Default fallback
        description = "No description available."

        # Attempt matching by parsing known patterns
        if item_text.startswith("Key Feature: "):
            key = item_text.replace("Key Feature: ", "").strip()
            description = TL.SYSTEM_FEATURES.get(key, description)

        elif "Star Type: " in item_text:
            key = item_text.replace("Star Type: ", "").strip()
            description = TL.STAR_TYPES.get(key, description)

        elif "Body: " in item_text:
            key = item_text.replace("Body: ", "").strip()
            description = TL.PLANET_ROCKY_BODY_TYPES.get(key,
                                                         TL.PLANET_GAS_BODY_TYPES.get(key, description))

        elif "Gravity: " in item_text:
            key = item_text.replace("Gravity: ", "").strip()
            description = TL.PLANET_ROCKY_GRAVITY.get(key,
                                                      TL.PLANET_GAS_GRAVITY.get(key, description))

        elif "Atmosphere: " in item_text:
            start = item_text.find("(")
            end = item_text.find(")")
            if start != -1 and end != -1:
                comp_key = item_text[start + 1:end].strip()
                description = TL.PLANET_ATMOSPHERIC_COMPOSITION.get(comp_key,
                                                                    TL.PLANET_GAS_CLASS.get(comp_key, description))

        elif "Climate: " in item_text:
            key = item_text.replace("Climate: ", "").strip()
            description = TL.PLANET_CLIMATES.get(key, description)

        elif "Habitability: " in item_text:
            key = item_text.replace("Habitability: ", "").strip()
            description = TL.PLANET_HABITABILITY.get(key, description)

        elif " " in item_text:  # catch other entries like planets, features
            key = item_text.split(" ", 1)[1].strip()
            description = TL.SYSTEM_ELEMENTS.get(key, description)

        # Display the description
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, description)

    def edit_tree(self, event):
        selected_item = self.tree.focus()

    def save_to_json(self):
        if self.last_generated_system is None:
            tk.messagebox.showinfo("Info", "No star system generated yet.")
            return
        path = tk.filedialog.asksaveasfilename(initialdir=os.path.dirname(os.path.abspath(sys.argv[0])),defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, "w") as f:
                    json.dump(self.last_generated_system, f, indent=4, default=lambda o: o.__dict__)
                tk.messagebox.showinfo("Saved", f"Star system saved to:\n{path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not save file:\n{e}")

    def load_from_json(self):
        path = tk.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(sys.argv[0])), filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, "r") as f:
                    data = json.load(f)

                def make_star(data):
                    return Star(**data)

                def make_binary(data):
                    return Binary(
                        starA=Star(**data['starA']),
                        starB=Star(**data['starB'])
                    )

                def make_territories(data):
                    return [Territory(**t) for t in data]

                def make_planets(data):
                    return [Planet(**{**p, "territories": make_territories(p.get("territories", []))}) for p in data]

                star_obj = make_binary(data["star"]) if "starA" in data["star"] else make_star(data["star"])

                system = StarSystem(
                    name=data["name"],
                    keyFeature=data["keyFeature"],
                    star=star_obj,
                    solarZoneInnerElements=make_planets(data["solarZoneInnerElements"]),
                    solarZoneMiddleElements=make_planets(data["solarZoneMiddleElements"]),
                    solarZoneOuterElements=make_planets(data["solarZoneOuterElements"]),
                )

                self.last_generated_system = system
                formatted = format_star_system(system)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, formatted)
                tk.messagebox.showinfo("Loaded", f"Star system loaded from:\n{path}")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not load file:\n{e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = StarSystemApp(root)
    root.mainloop()
