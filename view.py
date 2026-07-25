import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


BG_MAIN = "#6B4126"
BG_MENU = "#C9B49A"
BG_CARD = "#C9B49A"

COLLECTION = "#44523C"
RECHERCHE = "#44523C"
AJOUTER = "#44523C"
HOVER = "#995931"
GRIS = "#6E6E6E"

TEXT = "#ecf0f1"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 11, "bold")


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bibliothèque personnelle")
        self.configure(bg=BG_MAIN)
        self.state("zoomed")

        # ================= HEADER =================
        self.frame_header = tk.Frame(self, bg=BG_MAIN, height=60)
        self.frame_header.pack(fill="x")
        self.frame_header.pack_propagate(False)

        tk.Label(
            self.frame_header,
            text="📚 Gestion de la bibliothèque 📚",
            bg=BG_MAIN,
            fg="#DDD3B5",
            font=FONT_TITLE
        ).pack(pady=10)

        # ================= CONTAINER =================
        self.frame_container = tk.Frame(self, bg=BG_MAIN)
        self.frame_container.pack(fill="both", expand=True)



        # ================= MENU LATÉRAL =================
        self.frame_menu = tk.Frame(
            self.frame_container,
            bg=BG_MENU,
            width=250
        )
        self.frame_menu.pack(side="left", fill="y", padx=(20, 10), pady=20)
        self.frame_menu.pack_propagate(False)

        menu_content = tk.Frame(self.frame_menu, bg=BG_MENU)
        menu_content.pack(fill="both", expand=True)


        # --- Boutons en "cartes" ---
        self.menu_buttons = {}

        boutons_info = [
            ("📚 Afficher la collection", COLLECTION),
            ("🔎 Rechercher un livre", RECHERCHE),
            ("➕ Ajouter un livre", AJOUTER)
        ]

        for txt, color in boutons_info:
            card = tk.Frame(self.frame_menu, bg=BG_MENU, pady=10)
            card.pack(fill="x", padx=25, pady=40)


            b = tk.Button(
                card,
                text=txt,
                bg=color,
                fg="white",
                font=FONT_BUTTON,
                height=2,
                relief="ridge",
                activebackground=HOVER
            )
            b.pack(fill="x")

            self.menu_buttons[txt.split()[1]] = b  # clé simplifiée: "Afficher", "Rechercher", "Ajouter"

        # ================= ZONE PRINCIPALE =================
        self.frame_main = tk.Frame(
            self.frame_container,
            bg=BG_CARD
        )
        self.frame_main.pack(
            side="left",
            expand=True,
            fill="both",
            padx=(10, 20),
            pady=20
        )
        self.frame_main.pack_propagate(True)

        # ================= FOOTER =================
        self.frame_footer = tk.Frame(self, bg=BG_MAIN, height=50)
        self.frame_footer.pack(fill="x", side="bottom")
        self.frame_footer.pack_propagate(True)

        # Boutons Footer
        self.btn_help = tk.Button(
            self.frame_footer,
            text="? Aide",
            bg=RECHERCHE,
            fg="white",
            font=FONT_BUTTON,
            width=12
        )
        self.btn_help.pack(side="left", padx=10, pady=10)
        self.btn_help.config(command=self.ouvrir_aide)


        self.btn_quit = tk.Button(
            self.frame_footer,
            text="✖️ Quitter",
            bg="black",
            fg="white",
            font=FONT_BUTTON,
            width=14
        )
        self.btn_quit.pack(side="right", padx=10, pady=10)

        # Accueil au démarrage
        self.show_welcome()

    # ================= UTILITAIRES =================
    def clear_main(self):
        for widget in self.frame_main.winfo_children():
            widget.destroy()

    def subtitle(self, text):
        tk.Label(
            self.frame_main,
            text=text,
            bg=BG_CARD,
            fg=BG_MAIN,
            font=FONT_SUBTITLE
        ).pack(pady=20)

    def bouton_annuler(self, command):
        tk.Button(
            self.frame_main,
            text="⬅ Annuler",
            bg=GRIS,
            fg="white",
            font=FONT_BUTTON,
            width=14,
            command=command
        ).pack(pady=25)

    # ------------------ ACCUEIL ------------------
    def show_welcome(self):
        self.clear_main()
        container = tk.Frame(self.frame_main, bg=BG_CARD)
        container.pack(expand=True, fill="both", padx=20, pady=20)
        SliderLivres(container)

    def ouvrir_aide(self):
     aide = tk.Toplevel(self)
     aide.title("Aide")
     aide.geometry("700x600")
     aide.configure(bg=BG_CARD)

     text = tk.Text(
        aide,
        bg="#3A2010",
        fg="white",
        font=("Segoe UI", 11),
        wrap="word"
    )
     text.pack(fill="both", expand=True, padx=20, pady=20)

    # ------------- Message accueil --------------
     text.insert("end",
        "Cette bibliothèque est votre espace lecture.\n"
        "Organisez vos livres, explorez tranquillement 📚\n\n"
    )

    # ------------- Guide pratique ---------------
     text.insert("end", "Guide pratique :\n\n")

     text.insert("end",
        "📚 Afficher la collection\n"
        "En cliquant sur ce bouton vous pouvez voir tous les livres que vous avez ajoutés. "
        "Chaque livre affiche son titre, son auteur, son année et son genre. "
        "C’est le point de départ pour toutes vos actions : modifier, supprimer ou consulter les détails.\n\n"
    )

     text.insert("end",
        "🔎 Rechercher un livre\n"
        "En cliquant sur ce bouton vous pouvez chercher un livre précis en utilisant le titre, l'auteur, l'année ou le genre. "
        "Et saisir une valeur de recherche. " \
        "Pour de meilleurs résultats, utilisez des mots simples et évitez les fautes de frappe. "
        "La recherche est rapide et efficace pour trouver exactement ce que vous cherchez.\n\n"
    )

     text.insert("end",
        "➕ Ajouter un livre\n"
        "En cliquant sur ce bouton vous pouvez ajouter un nouveau livre"
        "Remplissez tous les champs du formulaire : titre, auteur, année et genre. "
        "Tous les champs sont obligatoires afin de garder votre bibliothèque complète et organisée. "
        "Vérifiez les informations avant de valider.\n\n"
    )

     text.insert("end",
        "✏ Modifier un livre\n"
        "Pour modifier les informations d'un livre vous devez selectionner un livre dans un tableau, soit celui de toute la collection ou celui du résultat de votre recherche."
        "Une fois séléctionné, cliquez sur le bouton Modifier."
        "Modifiez les informations du livre dans le formulaire pré-rempli par les anciennes informations, et enregistez. "
        "Cette fonction vous permet de corriger des erreurs ou de mettre à jour des détails comme l’année ou le genre.\n\n"
    )

     text.insert("end",
        "🗑 Supprimer un livre\n"
        "Pour supprimer un livre vous devez selectionner un livre dans un tableau, soit celui de toute la collection ou celui du résultat de votre recherche."
        "Une fois séléctionné, cliquez sur le bouton supprimer."
        "Confirmez la suppression du livre."
        "Cette fonction vous permet de supprimer des livre indisponibles, abimés, ou autre.\n\n"
    )

    # ----------------- Astuces et conseils --------------------
     text.insert("end", "💡 Astuces et conseils :\n\n")

     text.insert("end",
        "- Organisez régulièrement votre collection pour la garder claire et facile à parcourir.\n"
        "- Utilisez des mots-clés simples lors de la recherche pour trouver vos livres plus rapidement.\n"
        "- Vérifiez les informations avant d'ajouter ou modifier un livre pour éviter les doublons ou erreurs.\n"
        "- Profitez des sections détaillées pour garder une vue complète sur chaque livre.\n"
        "- Explorez la bibliothèque tranquillement et amusez-vous à redécouvrir vos lectures préférées !\n\n"
    )

     text.insert("end",
        "Merci d’utiliser l'application. 📖\n"
        "Organisez, explorez et profitez de vos lectures !\n"
    )

     text.config(state="disabled")

    


# =--------------------SLIDER -----------------------
class SliderLivres:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=BG_CARD)
        self.frame.pack(expand=True, fill="both")

        tk.Label(
            self.frame,
            text="  Les incontournables ! Les livres les plus empruntés 📚 ✨",
            bg=BG_CARD,
            fg="#6B4126",
            font=FONT_SUBTITLE
        ).pack(pady=10)

        self.canvas = tk.Canvas(
            self.frame,
            bg=BG_CARD,
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both", padx=40, pady=10)

        tk.Button(self.frame, text="◀", command=self.prev)\
            .place(relx=0.02, rely=0.5, anchor="w")
        tk.Button(self.frame, text="▶", command=self.next)\
            .place(relx=0.98, rely=0.5, anchor="e")

        self.livres = [
            {"image": "hp.jpg", "titre": "CANDIDE", "auteur": "Voltaire"},
            {"image": "lb.jpg", "titre": "BALTIMORE", "auteur": "Joel Dicker"},
            {"image": "as.jpg", "titre": "L'élegance du herisson", "auteur": "MURIEL BARBERY"}
        ]

        self.index = 0
        self.charger_images()
        self.afficher_image(initial=True)
        self.parent.after(4000, self.auto_slide)

    def charger_images(self):
        self.photos = []
        for livre in self.livres:
            img = Image.open(livre["image"])
            img = img.resize((300, 400))
            self.photos.append(ImageTk.PhotoImage(img))

    def afficher_image(self, initial=False):
        self.canvas.update_idletasks()
        self.canvas.delete("all")
        largeur = self.canvas.winfo_width() or 600
        hauteur = self.canvas.winfo_height() or 350
        self.current_img = self.canvas.create_image(largeur//2, hauteur//2-20, image=self.photos[self.index])
    
        if not initial:
            self.animation()

    def animation(self):
        self.canvas.update_idletasks()
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()
        next_img = self.canvas.create_image(largeur+200, hauteur//2-20, image=self.photos[self.index])
       
        for _ in range(50):
            self.canvas.move("all", -20, 0)
            self.canvas.update()
            self.canvas.after(10)
        self.canvas.coords(next_img, largeur//2, hauteur//2-20)
       
        if hasattr(self, "current_img"):
            self.canvas.delete(self.current_img)
            
        self.current_img = next_img
       

    def next(self):
        self.index = (self.index + 1) % len(self.photos)
        self.afficher_image()

    def prev(self):
        self.index = (self.index - 1) % len(self.photos)
        self.afficher_image()

    def auto_slide(self):
        self.next()
        self.parent.after(4000, self.auto_slide)


