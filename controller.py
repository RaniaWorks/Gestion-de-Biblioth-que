import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

MARRON = "#6B4126"
VERT = "#3C5330"
GRIS = "#6E6E6E"

class Controller:
    def __init__(self, model, view):
        self.m = model
        self.v = view
        self.dernier_crit = None  # pour mémoriser le dernier critère de recherche

        # Style Treeview
        self.personnaliser_tableau()

        # Lier les boutons menu
        self.v.menu_buttons["Afficher"].config(command=self.afficher)
        self.v.menu_buttons["Rechercher"].config(command=self.rechercher)
        self.v.menu_buttons["Ajouter"].config(command=self.ajouter)
        self.v.btn_quit.config(command=self.v.quit)

        # Page d'accueil
        self.accueil()

    # ================= ACCUEIL =================
    def accueil(self):
        self.v.clear_main()
        self.v.show_welcome()

    # ================= STYLE =================
    def personnaliser_tableau(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", background=MARRON, foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.configure("Treeview", background="#ffffff", foreground="black",
                        rowheight=28, fieldbackground="#ffffff", font=("Segoe UI", 11))
        style.map("Treeview", background=[("selected", "#44523C")], foreground=[("selected", "white")])

    # ================= VALIDATION =================
    def verifier_annee(self, annee_str):
        try:
            annee = int(annee_str)
        except ValueError:
            messagebox.showerror("Erreur", "L'année doit être un nombre")
            return False
        current_year = datetime.now().year
        if annee < 1000 or annee > current_year:
            messagebox.showerror("Erreur", f"L'année doit être entre 1000 et {current_year}")
            return False
        return True

    # ================= TABLEAU =================
    def tableau(self, parent, livres, show_actions=True):
        frame = tk.Frame(parent, bg=parent["bg"])
        frame.pack(fill="both", expand=True, pady=10)

        cols = ("Titre", "Auteur", "Année", "Genre")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=180)

        tree.tag_configure("even", background="#F3E7C2")
        tree.tag_configure("odd", background="white")

        for i, l in enumerate(livres):
            tree.insert("", "end", iid=l[0], values=l[1:], tags=("even" if i % 2 == 0 else "odd",))

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        tk.Label(self.v.frame_main,text="* Pour modifier ou supprimer un livre, sélectionnez d’abord un livre dans la liste.",fg="black",bg=self.v.frame_main["bg"],font=("Segoe UI", 10, "italic")).pack(pady=5)


        if show_actions:
           btn_frame = tk.Frame(parent, bg=parent["bg"])
        btn_frame.pack(pady=20)


        

         # Boutons alignés sur la même ligne
        tk.Button(btn_frame, text="Modifier", bg=VERT, fg="white", width=12,
          command=lambda: self.modifier_livre(tree)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Supprimer", bg=MARRON, fg="white", width=12,
          command=lambda: self.supprimer_livre(tree)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Annuler", bg=GRIS, fg="white", width=12,
          command=self.accueil).pack(side="left", padx=10)

        return tree

    # ================= AFFICHER =================
    def afficher(self):
        self.v.clear_main()
        self.v.subtitle("Toute notre collection de livres 📚")
        livres = self.m.tout_afficher()
        self.dernier_crit = None  # reset critère recherche
        if not livres:
            tk.Label(self.v.frame_main, text="Aucun livre dans la base", fg="white",
                     bg=self.v.frame_main["bg"], font=("Segoe UI", 12)).pack(pady=30)
            self.ajouter_bouton_annuler()
            return
        self.tableau(self.v.frame_main, livres)

        # Bouton annuler simple
        self.ajouter_bouton_annuler()

    # ================= RECHERCHER =================
    def rechercher(self):
        self.v.clear_main()
        self.v.subtitle("Rechercher un livre 🔍 📖")
        f = tk.Frame(self.v.frame_main, bg=self.v.frame_main["bg"])
        f.pack(pady=30, padx=240, anchor="w")

        f.grid_columnconfigure(0, weight=0, minsize=120)
        f.grid_columnconfigure(1, weight=1)

        def effacer_champs():
           crit.set("")
           val.delete(0, tk.END)


        tk.Label(f, text="Critère * :", fg="#502C17", bg=f["bg"], font=("bold italic", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        crit = ttk.Combobox(f, values=["Titre", "Auteur", "Année", "Genre"], width=43)
        crit.grid(row=0, column=1, pady=10, sticky="w")

        tk.Label(f, text="Recherche * :", fg="#502C17", bg=f["bg"], font=("bold italic", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        val = tk.Entry(f, width=30, font=("Segoe UI", 12))
        val.grid(row=1, column=1, pady=10, sticky="w")

        btn_frame = tk.Frame(f, bg=f["bg"])
        btn_frame.grid(row=2, column=0, columnspan=2,pady=15, padx=50, sticky="w")

        tk.Button(btn_frame, text="Rechercher", bg=VERT, fg="white", width=14,
                  command=lambda: self.lancer_recherche(crit, val)).pack(side="left", padx=10)
        tk.Button(btn_frame,text="Effacer tout", bg=MARRON, fg="white", width=12, command=effacer_champs).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Annuler", bg=GRIS, fg="white", width=14,
                  command=self.accueil).pack(side="left", padx=10)
        


        tk.Label(self.v.frame_main,text="* Champs obligatoires",fg=MARRON,
                 bg=self.v.frame_main["bg"],font=("Segoe UI", 10, "italic")).pack(pady=5)

                         #  LANCER RECHERCHE 
    def lancer_recherche(self, crit, val):
        if not crit or not crit.get() or not val.get():
            messagebox.showerror("Erreur", "Champs requis")
            return
        self.dernier_crit = (crit.get(), val.get())
        res = self.m.rechercher(crit.get(), val.get())
        self.v.clear_main()
        self.v.subtitle("Résultats de votre recherche 🔍 ")
        if not res:
            tk.Label(self.v.frame_main, text="Aucun résultat", fg="white", bg=self.v.frame_main["bg"]).pack(pady=20)
            self.ajouter_bouton_annuler()
            return
        self.tableau(self.v.frame_main, res)

        self.ajouter_bouton_annuler()

    # ================= AJOUTER =================
    def ajouter(self):
        self.v.clear_main()
        self.v.subtitle("Ajouter un livre 📖")
        self.formulaire()

    # ================= FORMULAIRE =================
    def formulaire(self, livre=None, retour_liste=None):
        f = tk.Frame(self.v.frame_main, bg=self.v.frame_main["bg"])
        f.pack(anchor="w", padx=240)

        labels = ["Titre * :", "Auteur * :", "Année * :"]
        champs = {}
        for i, l in enumerate(labels):
            tk.Label(f, text=l, fg="#502C17", bg=f["bg"], font=("bold italic", 12)).grid(row=i, column=0, padx=15, pady=12, sticky="e")
            e = tk.Entry(f, width=30, font=("Segoe UI", 12))   
            e.grid(row=i, column=1, pady=12)

            champs[l] = e

              # après la boucle
        tk.Label(f, text="Genre * : ", fg="#502C17", bg=f["bg"],
         font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="e")

        crit = ttk.Combobox(f, values=["Roman","Conte","BD","Historique", "Scientifique","Biographie","Manuels scolaires"], width=43)

        crit.grid(row=3, column=1, pady=10, sticky="w")
       
       
        if livre:
                for i, l in enumerate(labels):
                 champs[l].insert(0, livre[i+1])
                crit.set(livre[4])
           


        


        btn_frame = tk.Frame(self.v.frame_main, bg=self.v.frame_main["bg"])
        btn_frame.pack(pady=20, fill="x", padx=295)

        def effacer_champs():
            for entry in champs.values():
                entry.delete(0, tk.END)
                crit.set("")


        def enregistrer():
            data = [champs[l].get() for l in labels] + [crit.get()]
            if not all(data):
             messagebox.showerror("Erreur", "Champs requis")
             return

            if not self.verifier_annee(data[2]):
             return

            if livre:
                self.m.modifier(livre[0], *data)
                messagebox.showinfo("Succès", "Livre modifié avec succès !")
                if retour_liste:
                    retour_liste()
                else:
                    self.afficher()
            else:
                self.m.ajouter_livre(*data)
                messagebox.showinfo("Succès", "Livre ajouté avec succès !")
                for l in labels:
                    champs[l].delete(0, tk.END)
                crit.set("")    

        tk.Button(btn_frame, text="Enregistrer" if livre else "Valider", bg=VERT, fg="white", width=12, command=enregistrer).pack(side="left", padx=10)
        tk.Button(btn_frame,text="Effacer tout",bg=MARRON, fg="white", width=12,command=effacer_champs).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Annuler", bg=GRIS, fg="white", width=12, command=self.accueil).pack(side="left", padx=10)

        tk.Label(self.v.frame_main,text="* Champs obligatoires",fg=MARRON,
                 bg=self.v.frame_main["bg"],font=("Segoe UI", 10, "italic")).pack(pady=5)

    # ================= MODIFIER LIVRE =================
    def modifier_livre(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre")
            return
        livre = (int(sel[0]),) + tuple(tree.item(sel[0])["values"])
        self.v.clear_main()
        self.v.subtitle("Modifier un livre ✍️")
        self.formulaire(livre, retour_liste=self.afficher)

    # ================= SUPPRIMER LIVRE =================
    def supprimer_livre(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Attention", "Veuillez sélectionner un livre")
            return
        if messagebox.askyesno("Confirmation", "Supprimer ce livre ?"):
            self.m.supprimer(sel[0])
            self.afficher()

    