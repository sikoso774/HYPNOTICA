# test pour comprendre comment la fonction hasattr fonctionne...
class Test:
    def __init__(self, liste_mots):
        self.clear = True
        self.fail = False # (not True)
        self.max = 'Max Bellona'
        self.word_test = liste_mots
    
    def run_dynamic(self):
        print("--- Début du test dynamique ---")
        
        for word in self.word_test:
            # Etape 1 : On essaie de récupérer la valeur
            # Si 'word' n'existe pas, on récupère "Introuvable" (sans planter)
            valeur = getattr(self, word, "Introuvable")
            
            if valeur != "Introuvable":
                print(f"[LECTURE] L'attribut '{word}' existe. Valeur = {valeur}")
            else:
                # Etape 2 : Si ça n'existe pas, on le crée dynamiquement !
                print(f"[ECRITURE] '{word}' manque à l'appel. Je le crée...")
                setattr(self, word, f"Valeur générée pour {word}")

        print("--- Fin du test ---")
        
        # Vérification finale pour prouver que 'Excel' existe maintenant
        print(f"\nPreuve finale pour 'Excel' : {self.Excel}")

# --- Exécution ---
word_list = ['simple', 'clear', 'fail', 'max', 'Excel']
test = Test(word_list)
test.run_dynamic()

