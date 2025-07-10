import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

#  Create root window first
#root = tk.Tk()

# Then create StringVars, widgets, etc.
#my_var = tk.StringVar()


class SpongeLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Freshwater Sponge Logger")

        self.mode = tk.StringVar()
        self.sample_count = 1
        self.current_site_numb = ""

        self.build_mode_selection()

    def build_mode_selection(self):
        mode_frame = ttk.Frame(self.root, padding=20)
        mode_frame.pack()

        ttk.Label(mode_frame, text="Select Mode", font=("Arial", 14)).pack(pady=10)
        ttk.Radiobutton(mode_frame, text="🟩 Field Mode", variable=self.mode, value="field").pack(anchor='w')
        ttk.Radiobutton(mode_frame, text="🟦 Lab Mode", variable=self.mode, value="lab").pack(anchor='w')
        ttk.Button(mode_frame, text="Start", command=self.launch_interface).pack(pady=20)


# Field or Lab Mode
 
    def launch_interface(self):
        if not self.mode.get():
            messagebox.showerror("Mode Error", "Please select Field or Lab mode.")
            return
        for widget in self.root.winfo_children():
            widget.destroy()

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', expand=True)

        self.build_site_tab()
        self.build_water_tab()
        self.build_species_tab()
        self.build_sample_tab()
        if self.mode.get() == "lab":
            self.build_seq_tab()
            self.build_save_button()

# Site Info Tab

    def build_site_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Site Info")

        self.date_var = tk.StringVar()
        self.state_var = tk.StringVar()
        self.site_var = tk.StringVar()
        self.visit_var = tk.StringVar()
        self.lat_var = tk.StringVar()
        self.long_var = tk.StringVar()
        self.parish_var = tk.StringVar()
        self.sp_var = tk.StringVar()
        self.sp_col_var = tk.StringVar()

        entries = [
            ("Date (MM/DD/YYYY)", self.date_var),
            ("State", self.state_var),
            ("Site #", self.site_var),
            ("Visit #", self.visit_var),
            ("Latitude", self.lat_var),
            ("Longitude", self.long_var),
            ("Parish/County", self.parish_var),
            ("Sponges Found? (Y/N)", self.sp_var),
            ("Sponges Collected Count", self.sp_col_var)
        ]

        for i, (label, var) in enumerate(entries):
            ttk.Label(tab, text=label).grid(row=i, column=0, sticky='w')
            widget = ttk.Entry(tab, textvariable=var)
            widget.grid(row=i, column=1)
            if self.mode.get() == "lab":
                widget.state(['disabled'])

# Water Chemistry Tab

    def build_water_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Water Chemistry")

        self.water_field_vars = {}
        self.water_lab_vars = {}

        fields = [
            ("Flow (Len/Lo)", "flow"), ("pH", "ph"), ("Conductivity", "con"), ("Temperature", "temp"),
            ("Dissolved Oxygen", "do"), ("Turbidity", "turb"), ("Chlorine", "cl"),
            ("Nitrate", "no3"), ("Iron", "fe"), ("Ammonia", "nh"), ("Phosphate", "po4"),
            ("Nitrite", "no2"), ("Silica", "si"), ("Sulfate", "so4"), ("Calcium", "ca")
        ]

        for idx, (label, key) in enumerate(fields):
            ttk.Label(tab, text=f"{label} (Field)").grid(row=idx, column=0, sticky='w')
            if self.mode.get() == "field":
                var = tk.StringVar()
                self.water_field_vars[key] = var
                ttk.Entry(tab, textvariable=var).grid(row=idx, column=1)
            else:
                ttk.Label(tab, text="[Locked]", foreground='gray').grid(row=idx, column=1)
                var = tk.StringVar()
                self.water_field_vars[key] = var  # Placeholder for structure

            if self.mode.get() == "lab":
                ttk.Label(tab, text=f"{label} (Lab)").grid(row=idx, column=2, sticky='w')
                var_lab = tk.StringVar()
                self.water_lab_vars[key] = var_lab
                ttk.Entry(tab, textvariable=var_lab).grid(row=idx, column=3)
#Species Observed Tab
    def build_species_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Species Observed")

        species = [
            "aa", "cb", "dm", "dr", "efl", "efr", "hb", "ht", "rce", "rcr", "rr", "sa", "sl", "th", "tl", "tp"
        ]
        self.species_vars = {}

        for i, code in enumerate(species):
            var = tk.BooleanVar()
            self.species_vars[code] = var
            chk = ttk.Checkbutton(tab, text=code, variable=var)
            chk.grid(row=i % 8, column=i // 8)
            if self.mode.get() == "lab":
                chk.state(["disabled"])
 #Sample ID tab
    def build_sample_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Sample ID")

        self.sam_numb_var = tk.StringVar()
        ttk.Label(tab, text="Sample Number (sam.numb)").grid(row=0, column=0, sticky='w')
        ttk.Label(tab, textvariable=self.sam_numb_var, foreground='blue').grid(row=0, column=1)

        def update_sam_numb(*args):
            try:
                base = f"{int(self.site_var.get())}.{int(self.visit_var.get())}"
                self.current_site_numb = base
                self.sam_numb_var.set(f"{base}.{self.sample_count}")
            except:
                self.sam_numb_var.set("Invalid")
        self.site_var.trace_add("write", update_sam_numb)
        self.visit_var.trace_add("write", update_sam_numb)

        self.substrate_var = tk.StringVar()
        ttk.Label(tab, text="Substrate").grid(row=1, column=0, sticky='w')
        ttk.Combobox(tab, textvariable=self.substrate_var, values=[
            "A: Trash", "B: Rock", "C: Concrete", "D: Brick", "E: Plants/roots", "F: Log/branch",
            "G: Metal", "H: Tree", "I: Wood piling"
        ], state='readonly').grid(row=1, column=1)

        self.id_type_var = tk.StringVar()
        ttk.Label(tab, text="ID Type").grid(row=2, column=0, sticky='w')
        for i, txt in enumerate(["spicule", "DNA", "not sponge"]):
            ttk.Radiobutton(tab, text=txt, variable=self.id_type_var, value=txt).grid(row=2, column=1+i)

        self.mixed_var = tk.StringVar()
        ttk.Label(tab, text="Mixed?").grid(row=3, column=0)
        ttk.Combobox(tab, textvariable=self.mixed_var, values=["Y", "N"], state='readonly').grid(row=3, column=1)

        self.unknown_var = tk.StringVar()
        ttk.Label(tab, text="Unknown?").grid(row=4, column=0)
        ttk.Combobox(tab, textvariable=self.unknown_var, values=["x", ""], state='readonly').grid(row=4, column=1)

        self.megasclere_var = tk.StringVar()
        ttk.Label(tab, text="Megasclere Type").grid(row=5, column=0)
        ttk.Combobox(tab, textvariable=self.megasclere_var, values=[
            "smooth", "lightly spined", "dense spined", "trochospongilla type"
        ], state='readonly').grid(row=5, column=1)

        self.species_id_var = tk.StringVar()
        ttk.Label(tab, text="Identified Species").grid(row=6, column=0)
        ttk.Combobox(tab, textvariable=self.species_id_var, values=[
            "aa", "cb", "dm", "dr", "efl", "efr", "hb", "ht", "rce", "rcr", "rr", "sa", "sl", "th", "tl", "tp"
        ], state='readonly').grid(row=6, column=1)

#Sequencing Tab

    def build_seq_tab(self):
         tab = ttk.Frame(self.tabs)
         self.tabs.add(tab, text="Sequencing Info")

         self.seq_type_var = tk.StringVar()
         ttk.Label(tab, text="Gene Type").grid(row=0, column=0, sticky='w')
         self.seq_type_combo = ttk.Combobox(
         tab, textvariable=self.seq_type_var,
         values=["COI", "CO2", "ITS", "D3"],
         state='readonly'
    )
         self.seq_type_combo.grid(row=0, column=1)

         self.genbank_var = tk.StringVar()
         ttk.Label(tab, text="GenBank Deposit (Y/N)").grid(row=1, column=0, sticky='w')
         self.genbank_combo = ttk.Combobox(
        tab, textvariable=self.genbank_var,
        values=["Y", "N"],
        state='readonly'
    )
         self.genbank_combo.grid(row=1, column=1)

         self.acc_num_var = tk.StringVar()
         ttk.Label(tab, text="Accession Number").grid(row=2, column=0, sticky='w')
         self.acc_num_entry = ttk.Entry(tab, textvariable=self.acc_num_var)
         self.acc_num_entry.grid(row=2, column=1)

    # Lock widgets unless ID.TYPE is DNA
         def toggle_seq_tab(*args):
             is_dna = self.id_type_var.get() == "DNA"
             state = "normal" if is_dna else "disabled"
             for widget in [self.seq_type_combo, self.genbank_combo, self.acc_num_entry]:
                 widget.config(state=state)

         self.id_type_var.trace_add("write", toggle_seq_tab)
    


    # Save to CSV
    def build_save_button(self):
     ttk.Button(self.root, text="💾 Save Entry", command=self.save_all_data).pack(pady=10)

    def save_all_data(self):
        data = {
        "DATE": self.date_var.get(),
        "STATE": self.state_var.get(),
        "SITE": self.site_var.get(),
        "VISIT": self.visit_var.get(),
        "SITE.NUMBER": self.current_site_numb,
        "LAT": self.lat_var.get(),
        "LONG": self.long_var.get(),
        "PARISH": self.parish_var.get(),
        "SPONGES_FOUND": self.sp_var.get(),
        "SPONGES_COLLECTED": self.sp_col_var.get(),
        "SAM.NUMB": self.sam_numb_var.get(),
        "SUBSTRATE": self.substrate_var.get().split(":")[0],
        "ID.TYPE": self.id_type_var.get(),
        "MIXED": self.mixed_var.get(),
        "UNK": self.unknown_var.get(),
        "MEGASCLERE": self.megasclere_var.get(),
        "SPECIES": self.species_id_var.get(),
        "FIELD_LOCKED": "TRUE" if self.mode.get() == "field" else "FALSE"
        }

        # Water chemistry
        if self.mode.get() == "field":
            for k, v in self.water_field_vars.items():
                data[f"{k.upper()}_FIELD"] = v.get()
        else:
            for k, v in self.water_lab_vars.items():
                data[f"{k.upper()}_LAB"] = v.get()

        # Species observed
        for k, var in self.species_vars.items():
            data[k] = "X" if var.get() else ""
    
        # DNA sequencing
        if self.mode.get() == "lab" and self.id_type_var.get() == "DNA":
            data["SEQ.TYPE"] = self.seq_type_var.get()
            data["GEN.DEP"] = self.genbank_var.get()
            data["ACC"] = self.acc_num_var.get()
    
        # Save to CSV
        file_exists = os.path.exists("field_data.csv")
        try:
            with open("field_data.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
            messagebox.showinfo("Saved", f"✅ Sample {data['SAM.NUMB']} saved.")
            self.sample_count += 1
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save: {e}")


# Startup
if __name__ == "__main__":
    root = tk.Tk()
    app = SpongeLoggerApp(root)
    root.mainloop()

