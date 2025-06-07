import json
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import ttkbootstrap as ttk

import TextLists as TL
from Generator import create_star_system
from StorageDataclasses import StarSystem, Star, Binary, Planet, Territory


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

        # root
        self.root = root
        self.root.title("Star System Generator")
        self.style = ttk.Style("superhero")
        self.root.minsize(800, 600)
        self.center_window(1600, 900)

        # Variables
        self.current_generated_system = None
        # Map of the tree to reference objects in the dataclass
        self.tree_map = {}

        # Save and Load Frame
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10, fill="x")

        self.save_btn = ttk.Button(self.button_frame, text="Save JSON", command=self.save_to_json)
        self.save_btn.pack(side="right", padx=5)

        self.load_btn = ttk.Button(self.button_frame, text="Load JSON", command=self.load_from_json)
        self.load_btn.pack(side="right", padx=5)

        # Notebook for different tabs
        tab_control = ttk.Notebook(root)
        self.browser_frame = ttk.Frame(tab_control)
        self.random_tab = ttk.Frame(tab_control)

        tab_control.add(self.browser_frame, text='Treeview')
        tab_control.add(self.random_tab, text='Text')
        tab_control.pack(expand=1, fill='both')

        self.setup_browser_frame()
        self.setup_text_tab()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_text_tab(self):
        self.random_gen_frame = ttk.Frame(self.random_tab, padding=20)
        self.random_gen_frame.pack(fill="both", expand=True)

        self.generate_btn = ttk.Button(self.button_frame, text="Generate Star System",
                                       command=self.generate_star_system)
        self.generate_btn.pack(side="left", padx=5)

        # Output Box
        self.output_text = tk.Text(self.random_gen_frame, wrap="word", height=40, width=100)
        self.output_text.pack(side="left", fill="both", expand=True)

    def setup_browser_frame(self):
        # Main horizontal layout frame
        self.browser_frame = ttk.Frame(self.browser_frame)
        self.browser_frame.pack(fill="both", expand=True)

        # Treeview on the left
        self.tree = ttk.Treeview(self.browser_frame)
        self.tree.column("#0", width=400)
        self.tree.heading("#0", text="Star System")
        self.tree.pack(side="left", fill="y", expand=False, padx=10, pady=10)

        # Event to prevent Star System node being closed
        def on_node_close(event):
            item_id = self.tree.focus()
            if "locked" in self.tree.item(item_id, "tags"):
                self.tree.item(item_id, open=True)

        self.tree.bind("<<TreeviewClose>>", on_node_close)

        # Description panel on the right
        self.detail_text = tk.Text(self.browser_frame, wrap="word", width=60)
        self.detail_text.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Bind tree selection
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select_get_description)

        def show_context_menu(event):
            # Check that you are selecting something and get the tree item
            item_id = self.tree.identify_row(event.y)
            if item_id:
                self.tree.selection_set(item_id)
                self.tree.focus(item_id)

            # Get current node tag to properly label the buttons
            current_tag = self.tree.item(item_id, "tags")
            label = "Edit"
            if "name" in current_tag:
                label = "Rename"

            # Build the context menu
            contextmenu = tk.Menu(self.browser_frame, tearoff=False)
            contextmenu.add_command(label=label, command=self.edit_node)
            contextmenu.add_separator()
            contextmenu.add_command(label="Generate New System", command=self.generate_star_system)

            # Try to open the menu
            try:
                contextmenu.tk_popup(event.x_root, event.y_root)
            finally:
                contextmenu.grab_release()

        self.tree.bind("<Button-3>", show_context_menu)

    def update_text_view(self,system):
        self.output_text['state'] = "normal"
        self.output_text.delete(1.0, tk.END)
        formatted = format_star_system(system)
        self.output_text.insert(tk.END, formatted)
        self.output_text['state'] = "disabled"

    def generate_star_system(self):
        system = create_star_system()
        self.update_text_view(system)
        self.display_star_system_tree(system)

    def display_star_system_tree(self, system):
        self.tree.delete(*self.tree.get_children())

        # Insert the Star System and map it
        system_id = self.tree.insert("", "end", text=f"Star System: {system.name}", open=True,
                                     tags=["system", "name", "locked"])
        self.tree.insert(system_id, "end", text=f"Key Feature: {system.keyFeature}", tags=["system", "feature"])
        self.tree_map[system_id] = system

        # Insert the Star and map it
        if hasattr(system.star, "starA"):  # Binary
            star_node = self.tree.insert(system_id, "end", text="Star: Binary System", open=True, tags=["system", "binary"])
            for i, star in enumerate([system.star.starA, system.star.starB], start=1):
                star_id = self.tree.insert(star_node, "end", text=f"Star {i}: {star.name}", open=True,
                                           tags=["star", "name", "binary"])
                self.tree.insert(star_id, "end", text=f"Star Type: {star.type}", tags=["star", "type"])
                self.tree_map[star_id] = star
        else:
            star = system.star
            star_id = self.tree.insert(system_id, "end", text=f"Star: {star.name}", open=True, tags=["star", "name"])
            self.tree.insert(star_id, "end", text=f"Star Type: {star.type}", tags=["star", "type"])
            self.tree_map[star_id] = star

        # Process the Zones
        def process_zone(title, bodies):
            zone_id = self.tree.insert(system_id, "end", text=title, open=True)
            for body in bodies:
                if isinstance(body, str):
                    element_id = self.tree.insert(zone_id, "end", text=f"{body}", open=True, tags=["system","system element"])
                    self.tree_map[element_id] = body
                else:
                    # Insert the planets and map them
                    planet_id = self.tree.insert(zone_id, "end", text=f"{body.type}: {body.name}", open=True,
                                                 tags=["planet", "name"])
                    self.tree.insert(planet_id, "end", text=f"Body: {body.body}", tags=["planet", "body"])
                    self.tree.insert(planet_id, "end", text=f"Gravity: {body.gravity}", tags=["planet", "gravity"])
                    self.tree.insert(planet_id, "end", text=f"Atmosphere: {body.atmosphericPresence}",
                                     tags=["planet", "atmosphericPresence"])
                    self.tree.insert(planet_id, "end", text=f"Atmosphere Compositions: {body.atmosphericComposition}",
                                     tags=["planet", "atmosphericCompositions"])
                    self.tree.insert(planet_id, "end", text=f"Climate: {body.climate}", tags=["planet", "climate"])
                    self.tree.insert(planet_id, "end", text=f"Habitability: {body.habitability}",
                                     tags=["planet", "habitability"])
                    self.tree_map[planet_id] = body

                    # Insert the orbitals and map them
                    orbital_id = self.tree.insert(planet_id, "end", text="Orbitals", open=True)
                    for orbital in body.orbitalFeatures:
                        if orbital != "No Features":
                            self.tree.insert(orbital_id, "end", text=f"{orbital}", tags=["planet","orbital"])
                            self.tree_map[orbital] = orbital

                    # Insert the territories
                    for terr in body.territories:
                        self.tree.insert(planet_id, "end",
                                         text=f"Territory: {terr.baseTerrain} / {terr.territoryTrait}",
                                         tags=["planet","territory"])

        process_zone("Inner Zone", system.solarZoneInnerElements)
        process_zone("Middle Zone", system.solarZoneMiddleElements)
        process_zone("Outer Zone", system.solarZoneOuterElements)

    def on_tree_select_get_description(self, event):
        selected_item = self.tree.focus()
        item_text = self.tree.item(selected_item, "text")
        item_tags = self.tree.item(selected_item, "tags")

        # Default fallback description
        description = "No description available."

        # Get the actual value
        try:
            label, key = item_text.split(": ")
        except:
            key = item_text

        # Get the tag that answers for the description value, ignore the first descriptor tag
        if len(item_tags) >= 2 and item_tags[0] in ("system", "star", "planet"):
            tag = item_tags[1]
        else:
            tag = item_tags

        # Check tag and check the proper TextList dict
        match tag:
            case "feature":
                description = TL.SYSTEM_FEATURES.get(key, description)
            case "system element":
                description = TL.SYSTEM_ELEMENTS.get(key, description)
            case "type":
                description = TL.STAR_TYPES.get(key, description)
            case "body":
                description = TL.PLANET_ROCKY_BODY_TYPES.get(key, TL.PLANET_GAS_BODY_TYPES.get(key, description))
            case "gravity":
                description = TL.PLANET_ROCKY_GRAVITY.get(key, TL.PLANET_GAS_GRAVITY.get(key, description))
            case "atmosphericPresence":
                if key == "Gas Giant":
                    description = "This planet is composed mostly of gas"
                else:
                    description = TL.PLANET_ATMOSPHERIC_PRESENCE.get(key, description)
            case "atmosphericCompositions":
                description = TL.PLANET_ATMOSPHERIC_COMPOSITION.get(key, TL.PLANET_GAS_CLASS.get(key, description))
            case "climate":
                if key == "None":
                    description = "This planet is composed mostly of gas, it does not have any climate."
                else:
                    description = TL.PLANET_CLIMATES.get(key, description)
            case "habitability":
                if key == "None":
                    description = "This planet is composed mostly of gas, therefore it is inhabitable"
                else:
                    description = TL.PLANET_HABITABILITY.get(key, description)
            case "orbital":
                description = TL.PLANET_ROCKY_ORBITALS.get(key, TL.PLANET_GAS_ORBITALS.get(key, description))
            case "territory":
                description = "TBA later"

        # Display the description
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, description)

    def edit_node(self):
        # Variables for system modification
        item_id = self.tree.focus()
        parent_id = self.tree.parent(item_id)
        current_text = self.tree.item(item_id, "text")
        current_tag = self.tree.item(item_id, "tags")
        text_label, current_value = self.tree.item(item_id, "text").split(": ")
        new_value = current_value
        obj = None

        # Check if the item has a tracked dataclass reference
        if item_id not in self.tree_map:
            # Send error message
            tk.messagebox.showerror("Error", "This item does not have a reference in item tree.")
        else:
            # Set current object and proceed with logic
            obj = self.tree_map[item_id]

            # Change  the name
            if "name" in current_tag:
                field = "name"
                new_value = tk.simpledialog.askstring("Edit", f"Enter new name for {text_label}:", initialvalue=current_value)
                if not new_value or new_value == current_value:
                    return


            # Check that we actually need to update Treeview and dataclass
            if new_value != current_value:
                try:
                    # Update Treeview display
                    self.tree.item(item_id, text=f"{text_label}: {new_value}")
                    # Set new value in dataclass
                    setattr(obj, field, new_value)
                    # Update Text View
                except:
                    tk.messagebox.showerror("Error", "Couldn't update {label}.")

        # Custom dialog window
        def open_edit_dialogue(label_text, values_list):
            # Dialog window itself
            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Node")
            dialog.grab_set()

            # Make appear at at the widnow

            main_x = self.root.winfo_rootx()
            main_y = self.root.winfo_rooty()
            dialog.geometry(f"+{main_x + 200}+{main_y + 80}")

            tk.Label(dialog, text=label_text).pack(padx=10, pady=(10, 0))

            # Combobox for selection
            combo = ttk.Combobox(dialog, values=values_list, state="readonly")
            combo.pack(padx=10, pady=5)
            combo.current(0)

            def submit():
                selected_value = combo.get()
                dialog.destroy()

            ttk.Button(dialog, text="Apply", command=submit).pack(pady=10)


    def save_to_json(self):
        if self.current_generated_system is None:
            tk.messagebox.showinfo("Info", "No star system generated yet.")
            return
        path = tk.filedialog.asksaveasfilename(initialdir=os.path.dirname(os.path.abspath(sys.argv[0])),
                                               defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, "w") as f:
                    json.dump(self.current_generated_system, f, indent=4, default=lambda o: o.__dict__)
                tk.messagebox.showinfo("Saved", f"Star system saved to:\n{path}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not save file:\n{e}")

    def load_from_json(self):
        path = tk.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(sys.argv[0])),
                                             filetypes=[("JSON Files", "*.json")])
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

                self.current_generated_system = system
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
