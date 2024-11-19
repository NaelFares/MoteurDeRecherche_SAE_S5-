def main():
    """
    Point d'entrée principal de l'application.
    """
    print("=== CONNEXION ===")
    login = input("Login : ")
    password = input("Password : ")

    # Vérifier les identifiants (fonction à implémenter)
    # verify_credentials(login, password)

    print("\n=== MENU PRINCIPAL ===")
    while True:
        print("\nMENU :")
        print("1. Rechercher un film")
        print("2. Voir la liste ou noter un film")
        print("3. Quitter")

        choice = input("\nChoisissez une option : ")
        if choice == "1":
            # recherche_film()
            print("\n=== Rechercher un film ===")
        elif choice == "2":
            # voir_ou_noter_film()
            print("\n=== voir_ou_noter_film ===")
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
