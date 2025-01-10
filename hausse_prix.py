import pandas as pd
from pathlib import Path

def arrondir_prix(prix):
    """
    Fonction pour arrondir les prix selon les règles suivantes:
    - Si le dernier chiffre est 1,2,3,4 -> arrondir à 0
    - Si le dernier chiffre est 5 -> laisser tel quel
    - Si le dernier chiffre est 6,7,8,9 -> arrondir à la dizaine supérieure
    """
    try:
        prix = float(prix)
        # Multiplier par 100 pour travailler avec des entiers
        prix_cents = round(prix * 100)
        dernier_chiffre = prix_cents % 10
        
        if dernier_chiffre <= 4:
            # Arrondir vers le bas à la dizaine
            prix_cents = (prix_cents // 10) * 10
        elif dernier_chiffre > 5:
            # Arrondir vers le haut à la dizaine
            prix_cents = ((prix_cents // 10) + 1) * 10
        # Si c'est 5, on ne fait rien
        
        return prix_cents / 100
    except:
        return prix

def ajuster_prix(fichier_excel, pourcentage_augmentation):
    try:
        print("Lecture du fichier Excel...")
        df = pd.read_excel(fichier_excel)
        
        colonnes = list(df.columns)
        
        print("\nColonnes disponibles dans votre fichier:")
        for i, colonne in enumerate(colonnes, 1):
            print(f"{i}. {colonne}")
        
        choix = input("\nEntrez le numéro ou le nom de la colonne des prix unitaires: ")
        
        if choix.isdigit() and 1 <= int(choix) <= len(colonnes):
            colonne_prix = colonnes[int(choix)-1]
        else:
            colonne_prix = choix
        
        if colonne_prix not in colonnes:
            print(f"Erreur: Colonne '{colonne_prix}' introuvable")
            return
        
        # Calculer les nouveaux prix avec arrondi
        prix_avec_marge = df[colonne_prix].astype(float) * (1 + pourcentage_augmentation/100)
        df['Prix_final'] = prix_avec_marge.apply(arrondir_prix)
        df['Différence'] = df['Prix_final'] - df[colonne_prix]
        
        # Sauvegarder en CSV
        nom_fichier_sortie = str(Path(fichier_excel).stem) + '_modifie.csv'
        df.to_csv(nom_fichier_sortie, index=False, sep=';')
        
        print(f"\nFichier sauvegardé: {nom_fichier_sortie}")
        print("\nAperçu des modifications:")
        print(df[[colonne_prix, 'Prix_final', 'Différence']].head())
        
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")
        print("Type d'erreur:", type(e).__name__)

def main():
    print("Programme d'ajustement des prix avec arrondi personnalisé")
    print("------------------------------------------------------")
    
    fichier = input("Entrez le chemin du fichier Excel: ")
    
    while True:
        try:
            pourcentage = float(input("Entrez le pourcentage d'augmentation (ex: 10 pour 10%): "))
            break
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide")
    
    ajuster_prix(fichier, pourcentage)

if __name__ == "__main__":
    main()