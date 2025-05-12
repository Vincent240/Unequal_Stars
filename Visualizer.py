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
        self.manual_tab = ttk.Frame(tab_control)

        tab_control.add(self.random_tab, text='Random Generator')
        tab_control.add(self.manual_tab, text='Manual Creator')
        tab_control.pack(expand=1, fill='both')

        self.setup_random_tab()
        self.setup_manual_tab()

    def setup_random_tab(self):
        # Button Frame
        self.button_frame = ttk.Frame(self.random_tab)
        self.button_frame.pack(pady=10, fill="x")

        self.random_gen_frame = ttk.Frame(self.random_tab, padding=20)
        self.random_gen_frame.pack(fill="both", expand=True)

        self.generate_btn = ttk.Button(self.button_frame, text="Generate Star System", command=self.generate_star_system)
        self.generate_btn.pack(side="left", padx=5)

        # Output Box
        self.output_text = tk.Text(self.random_gen_frame, wrap="word", height=40, width=100)
        self.output_text.pack(side="left",fill="y", expand=False)

    def setup_manual_tab(self):

        self.description_frame = ttk.Frame(self.manual_tab)
        self.description_frame.pack(fill="both", expand=True)

        string_test = tk.StringVar()

        self.combobox = ttk.Combobox(self.description_frame, textvariable=string_test,values=list(TL.SYSTEM_ELEMENTS.keys()))
        self.combobox.current(0)
        self.combobox.pack()

        self.info_box = ttk.Label(self.description_frame, text=TL.SYSTEM_ELEMENTS[string_test.get()])
        self.info_box.pack()

    def generate_star_system(self):
        self.output_text['state'] = "normal"
        self.output_text.delete(1.0, tk.END)
        system = create_star_system()
        self.last_generated_system = system
        formatted = format_star_system(system)
        self.output_text.insert(tk.END, formatted)
        self.output_text['state'] = "disabled"

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
