# language: fr

@login
Fonctionnalité: Déconnecter un utilisateur

  *En tant qu'utilisateur identifié sur le Shopozor,  
  je veux pouvoir m'en déconnecter  
  de telle sorte que je doive à nouveau entrer mes identifiants pour m'y reconnecter.*  
  
  Le Shopozor utilise les JWTs pour gérer les sessions d'identification. De base, ceux-ci ne permettent pas 
  d'invalidation à la demande, comme indiqué [ici](https://medium.com/devgorilla/how-to-log-out-when-using-jwt-a8c7823e8a6). 
  Pour invalider un token, il faut implémenter un mécanisme supplémentaire qui n'est pas forcément requis par notre 
  application. 
  
  Scénario: L'utilisateur ferme sa session
    Etant donné un utilisateur identifié sur le Shopozor
    Lorsqu'il se déconnecte
    Alors son token d'identification est invalidé