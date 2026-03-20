import os
import json
import customtkinter as ctk

class ProfileManager:
    """Manages loading and saving key bindings from/to a JSON file."""
    def __init__(self, profiles_file="profiles.json"):
        # Store profiles.json in the same directory as this script (src/app/)
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), profiles_file)
        self.data = {"profiles": {}, "active_profile": None}
        self.load()

    def load(self):
        """Load profiles from JSON file. Create default if it doesn't exist."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading profiles: {e}")
                self._create_default()
        else:
            self._create_default()

    def save(self):
        """Save current profiles to JSON file."""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving profiles: {e}")

    def _create_default(self):
        """Create a default racing/boxing profile."""
        self.data = {
            "profiles": {
                "Boxing (Default)": {
                    "left_punch": "left",
                    "right_punch": "right",
                    "block": "f",
                    "dodge_left": "q",
                    "dodge_right": "e",
                    "dodge_front": "w space",
                    "dodge_back": "s space",
                    "final_skill": "x"
                }
            },
            "active_profile": "Boxing (Default)"
        }
        self.save()

    def get_active_bindings(self):
        """Returns the dictionary of key bindings for the active profile."""
        active = self.data.get("active_profile")
        if active and active in self.data["profiles"]:
            return self.data["profiles"][active]
        return self.data["profiles"].get("Boxing (Default)", {})

    def get_profile_names(self):
        return list(self.data.get("profiles", {}).keys())

    def set_active_profile(self, name):
        if name in self.data["profiles"]:
            self.data["active_profile"] = name
            self.save()

    def update_profile(self, name, bindings):
        self.data["profiles"][name] = bindings
        self.save()


class SettingsUI(ctk.CTkToplevel):
    """A floating window for managing Profiles and Key Bindings."""
    def __init__(self, parent, on_profile_changed_callback=None):
        super().__init__(parent)
        
        self.title("Settings & Profiles")
        self.geometry("400x500")
        self.attributes("-topmost", True)
        
        self.profile_manager = ProfileManager()
        self.on_changed = on_profile_changed_callback
        
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        # Profile Selection Row
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self.top_frame, text="Active Profile:").pack(side="left", padx=(0, 10))
        
        self.profile_var = ctk.StringVar()
        self.profile_dropdown = ctk.CTkOptionMenu(
            self.top_frame, 
            variable=self.profile_var,
            command=self.on_profile_selected
        )
        self.profile_dropdown.pack(side="left", fill="x", expand=True)

        # Key Bindings Frame
        self.bindings_frame = ctk.CTkScrollableFrame(self, label_text="Key Bindings")
        self.bindings_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.binding_entries = {}
        # Actions we expect from the model
        actions = ["left_punch", "right_punch", "block", "dodge_left", "dodge_right", "dodge_front", "dodge_back", "final_skill"]
        
        for i, action in enumerate(actions):
            row = ctk.CTkFrame(self.bindings_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(row, text=action.replace("_", " ").title(), width=100, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, width=80)
            entry.pack(side="right")
            self.binding_entries[action] = entry

        # Save Button
        self.save_btn = ctk.CTkButton(self, text="Save Binding Changes", command=self.save_current_bindings, fg_color="green", hover_color="darkgreen")
        self.save_btn.pack(pady=(0, 20))

    def load_profile_data(self):
        """Populate the UI with data from ProfileManager."""
        names = self.profile_manager.get_profile_names()
        self.profile_dropdown.configure(values=names)
        
        active = self.profile_manager.data.get("active_profile")
        if active in names:
             self.profile_var.set(active)
             self.populate_fields(active)

    def populate_fields(self, profile_name):
        """Fill entry widgets with binding strings."""
        bindings = self.profile_manager.data["profiles"].get(profile_name, {})
        for action, entry in self.binding_entries.items():
            entry.delete(0, 'end')
            entry.insert(0, bindings.get(action, ""))

    def on_profile_selected(self, choice):
        """User selected a different profile from dropdown."""
        self.populate_fields(choice)
        self.profile_manager.set_active_profile(choice)
        if self.on_changed:
            self.on_changed(self.profile_manager.get_active_bindings())

    def save_current_bindings(self):
        """Save the entries back to the active profile."""
        active = self.profile_var.get()
        new_bindings = {}
        for action, entry in self.binding_entries.items():
            new_bindings[action] = entry.get().strip().lower()
            
        self.profile_manager.update_profile(active, new_bindings)
        
        if self.on_changed:
            self.on_changed(new_bindings)
        self.destroy()
