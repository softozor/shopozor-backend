# language: fr

@initial-release @auth @wip
Fonctionnalité: Les mots de passe satisfont à la politique relative aux mots de passe 

  *En tant qu'Utilisateur,  
  j'ai besoin que mon mot de passe soit analysé  
  afin de minimiser les risques de piratage de mon compte.*  

  # Cette spécification correspond plus à un test unitaire de la fonction qui vérifie 
  # la conformité d'un mot de passe qu'à un test d'acceptance. Il est toutefois gardé 
  # en tant que tel à des fins de documentation pour les utilisateurs de la plateforme. 

  Plan du Scénario: Le mot de passe n'est pas conforme

    Un mot de passe est conforme à la politique relative aux mots de passe si, et 
    seulement si, il satisfait aux critères suivants: 

    - il contient au moins 8 caractères 
    - il mélange des chiffres et des lettres 
    - il contient au moins un caractère spécial
    - il n'a pas été compromis 

    Un mot de passe est **compromis** s'il est connu comme ayant fuité sur Internet, 
    i.e. si l'outil  
    
    https://haveibeenpwned.com/Passwords  
    
    le renseigne comme "pwned".

    Etant donné le <mot de passe non conforme>
    Alors il est non conforme

    Exemples:
      | mot de passe non conforme |
      | 1234                      |
      | 1l0v3y0u                  |
      | motdepassecompliqué       |
      | ufiDo_anCyx               |