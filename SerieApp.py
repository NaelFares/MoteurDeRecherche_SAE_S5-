import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
#Import des fonctions de requêtage de la bd 
from BD import requete

class SerieApp:
    def __init__(self, root):
        # === FENÊTRE PRINCIPALE ===
        self.root = root
        self.root.title("PyFlix")
        
        # === GESTION UTILISATEUR ===
        self.current_user_id = None
        
        # === STYLES ET THÈMES ===
        self.text_color = "#f4f4f4"  # Blanc
        self.font_title = ("Tahoma", 16, "bold")
        self.font_normal = ("Tahoma", 12)
        
        # === CHAMPS DE SAISIE ===
        # Login/Inscription
        self.login_entry = None
        self.password_entry = None
        self.new_login_entry = None
        self.new_password_entry = None
        # Recherche
        self.search_entry = None
        
        # === FRAMES DYNAMIQUES ===
        self.display_frame = None
        
        # === CONFIGURATION FENÊTRE ===
        # Thème
        self.root.configure(bg="#141414")
        
        # Dimensions et positionnement
        width, height = 500, 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # === INITIALISATION ===
        self.create_login_screen()
        
        # Index pour afficher les séries 10 par 10
        self.current_index = 0
        self.series = []
        self.total_series_count = 0
        self.search_performed = False  # État pour savoir si une recherche a été effectuée

    def create_login_screen(self):
        self.clear_screen()
        
        # Dimensions de la fenêtre
        width, height = 500, 300  # Ajuste les dimensions comme tu veux
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcul pour centrer la fenêtre
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Définir la géométrie
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Créer un Canvas pour dessiner un rectangle en fond
        canvas = tk.Canvas(self.root, width=400, height=400, bg="#141414", bd=0, highlightthickness=0)
        canvas.pack(expand=True)

        # Dessiner un rectangle dans le Canvas
        canvas.create_rectangle(60, 50, 350, 250, outline="#f4f4f4", width=2)

        # Créer un conteneur (Frame) pour le formulaire à l'intérieur du rectangle
        form_frame = tk.Frame(self.root, bg="#141414")
        canvas.create_window(205, 150, window=form_frame)  # Positionner le Frame au centre du Canvas (ajusté)

        # Titre centré en gros et blanc
        tk.Label(form_frame, text="S'identifier", font=("Tahoma", 24, "bold"), fg="white", bg="#141414").grid(row=0, column=0, columnspan=2, pady=20)

        # Ligne 1 : Login
        tk.Label(form_frame, text="Login:", font=self.font_normal, bg="#141414", fg=self.text_color).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.login_entry = tk.Entry(form_frame, bg="#313131", fg=self.text_color)
        self.login_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Ligne 2 : Password
        tk.Label(form_frame, text="Password:", font=self.font_normal, bg="#141414", fg=self.text_color).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(form_frame, show="*", bg="#313131", fg=self.text_color)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Bouton "Se connecter", centré sous le formulaire
        tk.Button(form_frame, text="Se connecter", bg="#e21219", font=("Tahoma", 13, "bold"), fg=self.text_color, command=self.check_login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Bouton "Créer un compte" en bas à gauche de la fenêtre principale
        tk.Button(self.root, 
                text="Créer un compte", 
                bg="#313131",  # Couleur grise
                font=("Tahoma", 10),  # Police plus petite
                fg=self.text_color, 
                command=self.create_account_screen).place(relx=0.02, rely=0.88)  # Position ajustée

    def check_login(self):
        # Récupérer les valeurs des champs
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Vérifier que les champs ne sont pas vides
        if not login or not password:
            messagebox.showerror("Erreur", "Veuillez remplir les champs Login et Password.")
            return

        # Vérifier les identifiants avec la fonction verify_user
        success, user_id = requete.verify_user(login, password)
        
        if success:
            # Stocker l'ID de l'utilisateur pour une utilisation ultérieure
            self.current_user_id = user_id
            # Redirection vers le menu principal
            self.create_main_menu()
        else:
            messagebox.showerror("Erreur", "Login ou mot de passe incorrect.")

    def logout(self):
        """Réinitialise l'application et ramène l'utilisateur à la page de connexion."""
        self.create_login_screen()

            
    # def check_login(self):
    #     # Récupérer les valeurs des champs
    #     login = self.login_entry.get()
    #     password = self.password_entry.get()

    #     # Exemple de logique de vérification (à adapter à vos besoins)
    #     if login == "admin" and password == "password123":
    #         print("Connexion réussie !")
    #         # Vous pouvez appeler une méthode pour changer d'écran ou afficher un message
    #     else:
    #         print("Login ou mot de passe incorrect")

    def create_main_menu(self):
        self.search_performed = False  # Réinitialiser l'état de recherche
        self.clear_screen()

        # Dimensions de la fenêtre
        width, height = 800, 600

        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer les coordonnées pour centrer la fenêtre
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Configurer la taille et la position de la fenêtre
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Ajouter les widgets du menu principal
        tk.Label(self.root, text="PyFlix", font=("Tahoma", 20, "bold"), fg="white", bg="#141414").pack(pady=20)

        # Frame pour les boutons "Noter", "Rechercher", "Déconnexion"
        button_frame = tk.Frame(self.root, bg="#141414")
        button_frame.pack(pady=10)

        # Boutons de navigation
        tk.Button(button_frame, text="Toutes les séries", font=("Tahoma", 14), fg="white", bg="#141414", command=self.create_list_screen).pack(side="left", padx=10)
        tk.Button(button_frame, text="Rechercher", font=("Tahoma", 14), fg="white", bg="#141414", command=self.create_search_screen).pack(side="left", padx=10)
        tk.Button(button_frame, text="Déconnexion", font=("Tahoma", 14), fg="white", bg="#e21219", command=self.logout).pack(side="left", padx=10)

        # Frame pour les séries recommandées
        recommendations_frame = tk.Frame(self.root, bg="#141414")
        recommendations_frame.pack(pady=20, fill="both", expand=True)

        tk.Label(
            recommendations_frame,
            text="Séries recommandées :",
            font=("Tahoma", 18, "bold"),
            fg="white",
            bg="#141414"
        ).pack(pady=10)

        # Obtenir les recommandations depuis la base de données
        recommended_series = requete.find_recommendations_from_favorites(self.current_user_id)
        
        if not recommended_series:
            # Afficher un message si aucune recommandation n'est disponible
            tk.Label(
                recommendations_frame,
                text="Notez des séries pour obtenir des recommandations personnalisées !",
                font=("Tahoma", 12),
                fg="white",
                bg="#141414"
            ).pack(pady=20)
            return

        # Canvas avec scrollbar pour les recommandations
        canvas = tk.Canvas(recommendations_frame, bg="#141414", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(recommendations_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Configuration du défilement avec la molette
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Met à jour les dimensions du conteneur pour que les séries s'affichent
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Frame pour contenir les séries recommandées
        series_container = tk.Frame(canvas, bg="#141414")
        canvas.create_window((0, 0), window=series_container, anchor="nw", width=canvas.winfo_width())
  

        # Configuration des colonnes
        for i in range(3):
            series_container.grid_columnconfigure(i, weight=1)

        # Affichage des séries recommandées
        for i, (title, score) in enumerate(recommended_series):
            try:
                # Créer un frame pour chaque série
                serie_frame = tk.Frame(series_container, bg="#141414")
                serie_frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

                # Construire le chemin de l'image
                image_path = f"img/{title.replace(' ', '').lower()}.png"

                # Image
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize((100, 150))
                    photo = ImageTk.PhotoImage(img)
                    img_label = tk.Label(serie_frame, image=photo, bg="#141414")
                    img_label.image = photo
                    img_label.pack(side="top")
                else:
                    # Label de remplacement si l'image n'existe pas
                    tk.Label(
                        serie_frame,
                        text="Image non disponible",
                        fg="white",
                        bg="#141414"
                    ).pack(side="top")

                # Titre
                tk.Label(
                    serie_frame,
                    text=title,
                    font=("Tahoma", 14),
                    fg="white",
                    bg="#141414"
                ).pack(side="top", pady=10)

            except Exception as e:
                print(f"Erreur lors du chargement de la série {title}: {e}")

        # Mettre à jour la zone de défilement
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        series_container.bind('<Configure>', configure_scroll_region)

    def create_search_screen(self):
        self.clear_screen()

        # Configurer l'arrière-plan principal
        self.root.configure(bg="#141414")

        # Frame pour le champ de recherche et le bouton
        search_frame = tk.Frame(self.root, bg="#141414")
        search_frame.pack(pady=20)

        tk.Label(
            search_frame,
            text="Rechercher une série :",
            font=("Tahoma", 14, "bold"),
            fg="white",
            bg="#141414"
        ).pack(side="left", padx=10)

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=10)

        tk.Button(
            search_frame,
            text="Rechercher",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=self.search_serie
        ).pack(side="left", padx=10)

        # Frame pour afficher les images et les titres
        self.display_frame = tk.Frame(self.root, bg="#141414")  # Sauvegardé comme attribut pour actualisation
        self.display_frame.pack(pady=20)

        # Frame pour le bouton de retour à l'accueil
        bottom_frame = tk.Frame(self.root, bg="#141414")
        bottom_frame.pack(pady=20)

        tk.Button(
            bottom_frame,
            text="Retour au menu principal",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=self.create_main_menu
        ).pack()

    
    def search_serie(self):
        # Effacer les anciens résultats
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Récupérer les mots-clés depuis l'entrée utilisateur
        motscles = self.search_entry.get().strip().lower()
        
        # Utiliser la fonction find_best_series importée de requete.py
        results_db = requete.find_best_series(motscles)
        
        # Vérifier la structure des résultats
        if not results_db:
            tk.Label(
                self.display_frame,
                text="Aucun résultat trouvé.",
                font=("Tahoma", 14),
                fg="white",
                bg="#141414"
            ).pack()
            return

        # Transformer les résultats de la BD en ne gardant que les id et les titres
        results_series = [{"id": row[0], "title": row[1]} for row in results_db]

        # Si aucun résultat trouvé
        if not results_series:
            tk.Label(
                self.display_frame,
                text="Aucun résultat trouvé.",
                font=("Tahoma", 14),
                fg="white",
                bg="#141414"
            ).pack()
            return

        # Hiérarchie des tailles pour le top 3
        sizes = [(200, 300), (150, 225), (100, 150)]  # Taille des images
        fonts = [("Tahoma", 14, "bold"), ("Tahoma", 12), ("Tahoma", 10)]  # Tailles des polices
        button_sizes = [("Tahoma", 12, "bold"), ("Tahoma", 10), ("Tahoma", 8)]  # Tailles pour les boutons

        # Afficher chaque résultat avec la hiérarchie visuelle
        for i, result in enumerate(results_series):
            # Créer un sous-frame pour chaque série
            image_frame = tk.Frame(self.display_frame, bg="#141414")
            image_frame.pack(side="left", padx=20)

            # Afficher le titre de la série
            title_label = tk.Label(
                image_frame,
                text=result["title"],
                font=fonts[i],
                fg="white",
                bg="#141414",
                anchor="center"
            )
            title_label.pack(pady=10)

            # Récupérer le titre du label pour construire le chemin de l'image
            serie_title = title_label.cget("text")  # Récupère le texte du label
            image_path = f"img/{serie_title.replace(' ', '').lower()}.png"  # Exemple : "Friends" -> "img/friends.png"

            # Charger et afficher l'image
            image_label = tk.Label(image_frame, bg="#141414")
            try:
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize(sizes[i])  # Ajuster la taille selon le classement
                    photo = ImageTk.PhotoImage(img)
                    image_label.config(image=photo)
                    image_label.image = photo
                else:
                    image_label.config(text="Image introuvable", fg="red")
            except Exception as e:
                image_label.config(text="Erreur lors du chargement", fg="red")
                print(f"Erreur : {e}")

            image_label.pack()

            # Ajouter le bouton Noter sous l'image
            noter_button = tk.Button(
                image_frame,
                text="Noter",
                font=button_sizes[i],
                fg="white",
                bg="#e21219",
                width=10,
                command=lambda s=result: self.open_rating_window(s)
            )
            noter_button.pack(pady=5)

    def create_list_screen(self):
        self.clear_screen()
        self.root.configure(bg="#141414")

        # Frame pour le titre et le bouton de retour
        title_frame = tk.Frame(self.root, bg="#141414")
        title_frame.pack(pady=10, fill="x")

        # Titre
        tk.Label(
            title_frame,
            text="Liste des séries",
            font=("Tahoma", 22, "bold"),
            fg="white",
            bg="#141414"
        ).pack(side="left", padx=20)

        # Bouton Retour au menu principal
        tk.Button(
            title_frame,
            text="Retour au menu principal",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=self.create_main_menu
        ).pack(side="right", padx=20)
        
        # Ajout de la barre de recherche sous le titre
        search_frame = tk.Frame(self.root, bg="#141414")
        search_frame.pack(pady=10, fill="x")
        
        search_label = tk.Label(
            search_frame,
            text="Rechercher une série par son titre :",
            font=("Tahoma", 12),
            fg="white",
            bg="#141414"
        )
        search_label.pack(side="left", padx=10)

        # Champ de texte pour la recherche
        self.list_search_entry = tk.Entry(
            search_frame,
            font=("Tahoma", 12),
            fg="black",
            bg="white",
            width=40
        )
        self.list_search_entry.pack(side="left", padx=10)

        # Bouton de recherche avec la commande liée
        search_button = tk.Button(
            search_frame,
            text="Rechercher",
            font=("Tahoma", 12),
            fg="white",
            bg="#e21219",
            command=self.filter_list_series  # Appel à filter_list_series
        )
        search_button.pack(side="left", padx=10)

        # Frame pour la liste des séries avec scrollbar
        container_frame = tk.Frame(self.root, bg="#141414")
        container_frame.pack(pady=20, fill="both", expand=True)

        # Si aucune recherche n'a été effectuée, récupérer toutes les séries
        if not self.search_performed:
            filtered_results = requete.filter_series("")  # Récupérer toutes les séries
            self.series = []
            for id_serie, titre, note in filtered_results:
                serie = {
                    "id": id_serie,
                    "title": titre,
                    "image_path": f"img/{titre.replace(' ', '').lower()}.png",
                    "rating": note if note is not None else 0
                }
                self.series.append(serie)

        # Si aucune série n'est trouvée, afficher un message
        if not self.series:
            tk.Label(
                container_frame,
                text="Aucune série trouvée",
                font=("Tahoma", 14),
                fg="white",
                bg="#141414"
            ).pack(pady=50)
            return

        # Canvas avec scrollbar
        canvas = tk.Canvas(container_frame, bg="#141414", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Toujours créer la scrollbar
        scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Configuration du défilement avec la molette
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Frame pour contenir toutes les séries
        series_frame = tk.Frame(canvas, bg="#141414")
        canvas_window = canvas.create_window((0, 0), window=series_frame, anchor="nw", width=canvas.winfo_width())

        # Ajuster la largeur du frame quand le canvas change de taille
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', on_canvas_configure)

        # Mettre à jour la région de scroll
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        series_frame.bind('<Configure>', update_scroll_region)
        
        # Appeler la méthode pour afficher les séries
        self.current_index = 0  # Réinitialiser l'index
        self.total_series_count = len(self.series)  # Mettre à jour le nombre total de séries
        self.display_series(series_frame)  # Afficher les séries initiales

        # Bouton pour charger plus de séries
        load_more_button = tk.Button(
            self.root,
            text="Charger plus de séries",
            font=("Tahoma", 14),
            fg="white",
            bg="#e21219",
            command=lambda: self.load_more_series(series_frame)  # Utiliser lambda pour passer le conteneur
        )
        load_more_button.pack(pady=20)

    def display_series(self, series_frame):
        """Affiche les séries à partir de l'index actuel dans le conteneur spécifié."""
        # Ne pas effacer les anciens résultats, juste ajouter les nouvelles séries
        # Affichage des séries par groupes de 10
        for i in range(self.current_index, min(self.current_index + 10, self.total_series_count)):
            serie = self.series[i]  # Utiliser l'index pour accéder à la série
            serie_frame = tk.Frame(series_frame, bg="#141414", bd=1, relief="solid")
            serie_frame.pack(fill="x", pady=5, padx=5)

            # Image
            img_label = tk.Label(serie_frame, bg="#141414")
            try:
                if os.path.exists(serie["image_path"]):
                    img = Image.open(serie["image_path"])
                    img = img.resize((50, 75))
                    photo = ImageTk.PhotoImage(img)
                    img_label.config(image=photo)
                    img_label.image = photo
                else:
                    img_label.config(text="Image introuvable", fg="red", font=("Tahoma", 10))
            except Exception as e:
                img_label.config(text="Erreur", fg="red", font=("Tahoma", 10))
                print(f"Erreur : {e}")
            img_label.pack(side="left", padx=10, pady=5)

            # Détails (titre et étoiles)
            details_frame = tk.Frame(serie_frame, bg="#141414")
            details_frame.pack(side="left", padx=10, pady=5, fill="x")

            # Titre
            tk.Label(
                details_frame,
                text=serie["title"],
                font=("Tahoma", 14),
                fg="white",
                bg="#141414",
                anchor="w"
            ).pack(anchor="w")

            # Étoiles pour la note
            stars = "★" * serie["rating"] + "☆" * (5 - serie["rating"])
            star_label = tk.Label(
                details_frame,
                text=stars,
                font=("Tahoma", 12),
                fg="yellow",
                bg="#141414",
                anchor="w"
            )
            star_label.pack(anchor="w", pady=5)

            # Bouton Noter
            tk.Button(
                serie_frame,
                text="Noter",
                font=("Tahoma", 12),
                fg="white",
                bg="#e21219",
                command=lambda s=serie, l=star_label: self.open_rating_window(s, l)
            ).pack(side="right", padx=10, pady=5)

    def load_more_series(self, series_frame):
        """Charge 10 séries supplémentaires."""
        if self.current_index < self.total_series_count:  # Vérifiez si plus de séries sont disponibles
            # Calculez combien de séries peuvent encore être chargées
            remaining_series = self.total_series_count - self.current_index
            # Chargez soit 10, soit le nombre de séries restantes
            load_count = min(10, remaining_series)
            self.current_index += load_count
            self.display_series(series_frame)  # Afficher les nouvelles séries
        else:
            messagebox.showinfo("Info", "Aucune série supplémentaire à charger.")  # Message si toutes les séries sont déjà affichées
            
    def filter_list_series(self):
        """Filtre et met à jour la liste des séries affichées"""
        search_text = self.list_search_entry.get().strip()
        filtered_results = requete.filter_series(search_text)
        
        # Mise à jour de la liste des séries avec gestion d'erreur
        try:
            self.series = []
            for id_serie, titre, note in filtered_results:  # Mettez à jour pour décomposer les résultats
                serie = {
                    "id": id_serie,  # Utilisez l'ID de la série
                    "title": titre,
                    "image_path": f"img/{titre.replace(' ', '').lower()}.png",
                    "rating": note if note is not None else 0  # Utilise 0 si pas de note
                }
                self.series.append(serie)
                
            # Indiquer qu'une recherche a été effectuée
            self.search_performed = True
                
            # Rafraîchir l'affichage de la liste
            self.create_list_screen()
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la liste : {e}")
        
            
    def open_rating_window(self, serie, star_label=None):
        """
        Ouvre une fenêtre pour noter une série.
        Args:
            serie (dict): La série à noter
            star_label (tk.Label, optional): Le label des étoiles à mettre à jour si présent
        """
        rating_window = tk.Toplevel(self.root)
        rating_window.title(f"Noter {serie['title']}")
        rating_window.configure(bg="#141414")
        
        # Dimensions de la fenêtre
        width, height = 300, 200
        
        # Obtenir les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculer les coordonnées x et y pour centrer la fenêtre
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Définir la géométrie de la fenêtre
        rating_window.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            rating_window,
            text=f"Attribuer une note à {serie['title']}",
            font=("Tahoma", 14),
            fg="white",
            bg="#141414"
        ).pack(pady=10)

        # Curseur pour attribuer une note
        initial_rating = serie.get("rating", 0)  # Utilise 0 si pas de rating existant
        note_var = tk.IntVar(value=initial_rating)
        slider = tk.Scale(
            rating_window,
            from_=0,
            to=5,
            orient="horizontal",
            bg="#141414",
            fg="white",
            highlightbackground="#141414",
            variable=note_var
        )
        slider.pack(pady=20)

        def save_rating():
            new_rating = note_var.get()
            serie["rating"] = new_rating
            
            if star_label:
                stars = "★" * new_rating + "☆" * (5 - new_rating)
                star_label.config(text=stars)

            # Appel de la fonction pour noter la série
            success = requete.rate_series(self.current_user_id, serie['id'], new_rating)
            if success:
                messagebox.showinfo("Succès", "Note enregistrée avec succès!")
            else:
                messagebox.showerror("Erreur", "Échec de l'enregistrement de la note.")
            
            rating_window.destroy()

        tk.Button(
            rating_window,
            text="Valider",
            font=("Tahoma", 12),
            fg="white",
            bg="#e21219",
            command=save_rating
        ).pack(pady=10)

    def choose_serie(self):
        serie = self.selected_serie.get()
        if serie:
            self.create_serie_screen(serie)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner une série.")

    def clear_screen(self):
        self.root.unbind_all("<MouseWheel>")  # Débinder l'événement de scroll
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_account_screen(self):
        self.clear_screen()
        
        # Dimensions de la fenêtre
        width, height = 500, 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcul pour centrer la fenêtre
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Définir la géométrie
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Créer un Canvas pour dessiner un rectangle en fond
        canvas = tk.Canvas(self.root, width=400, height=400, bg="#141414", bd=0, highlightthickness=0)
        canvas.pack(expand=True)

        # Dessiner un rectangle dans le Canvas
        canvas.create_rectangle(60, 50, 350, 250, outline="#f4f4f4", width=2)

        # Créer un conteneur (Frame) pour le formulaire
        form_frame = tk.Frame(self.root, bg="#141414")
        canvas.create_window(205, 150, window=form_frame)

        # Titre centré
        tk.Label(form_frame, text="Créer un compte", font=("Tahoma", 24, "bold"), fg="white", bg="#141414").grid(row=0, column=0, columnspan=2, pady=20)

        # Champ Login
        tk.Label(form_frame, text="Login:", font=self.font_normal, bg="#141414", fg=self.text_color).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.new_login_entry = tk.Entry(form_frame, bg="#313131", fg=self.text_color)
        self.new_login_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Champ Password
        tk.Label(form_frame, text="Password:", font=self.font_normal, bg="#141414", fg=self.text_color).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.new_password_entry = tk.Entry(form_frame, show="*", bg="#313131", fg=self.text_color)
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Bouton de création de compte
        tk.Button(form_frame, 
                text="Créer mon compte", 
                bg="#e21219", 
                font=("Tahoma", 13, "bold"), 
                fg=self.text_color, 
                command=self.validate_account_creation).grid(row=3, column=0, columnspan=2, pady=20)

        # Bouton retour
        tk.Button(self.root, 
                text="Retour", 
                bg="#313131", 
                font=("Tahoma", 10), 
                fg=self.text_color, 
                command=self.create_login_screen).place(relx=0.02, rely=0.88)

    def validate_account_creation(self):
        # Récupérer les valeurs des champs
        login = self.new_login_entry.get()
        password = self.new_password_entry.get()

        # Vérifier que les champs ne sont pas vides
        if not login or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Utiliser la fonction create_user de requete.py
        success = requete.create_user(login, password)
        
        if success:
            messagebox.showinfo("Succès", "Compte créé avec succès!")
            # Redirection vers la page de connexion
            self.create_login_screen()
        else:
            messagebox.showerror("Erreur", "La création du compte a échoué. Veuillez réessayer.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SerieApp(root)
    root.mainloop()
