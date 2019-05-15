#language: fr

@initial-release @auth @signup @wip
Fonctionnalité: Enregistrer un nouveau client

  *En tant que nouveau client du Shopozor,  
  je veux pouvoir y créer un compte avec un e-mail et un mot de passe,  
  afin d'avoir accès à toutes ses fonctionnalités.*  

  ![Processus d'enregistrement](UserRegistration-fr.png)
  
  # Nous avons deux possibilités : 
  # - soit nous enregistrons l'e-mail de l'utilisateur qui définit ensuite son mot de passe au moment
  #   de l'activation du compte
  # - soit nous enregistrons l'e-mail et le mot de passe de l'utilisateur qui valide ensuite son compte 
  #   en suivant le lien d'activation du compte
  # Nous nous sommes décidés pour le dernier choix car il respecte le principe de séparation des préoccupations. 
  # En effet, pour implémenter le premier choix, il faut coupler la définition du mot de passe à l'activation 
  # du compte. La création du compte avec un identifiant et un mot de passe est plus compréhensible comme opération 
  # de notre API que l'activation d'un compte en définissant un mot de passe. De plus, dans le premier cas, il n'est pas 
  # possible d'extraire proprement la fonctionnalité de réinitialisation du mot de passe d'un utilisateur, autant 
  # pour l'application client que pour le serveur ainsi qu'en termes de tests. Le premier cas implique l'usage 
  # de la méthode setPassword de l'API qu'il est plus judicieux de tester en temps que fonctionnalité en tant que telle 
  # sans qu'elle ne soit couplée à quoi que ce soit d'autre. 
  
  Scénario: Un nouveau client s'enregistre avec un mot de passe conforme

    Le client potentiel commence par donner un e-mail et un mot de passe. Il devra ensuite 
    valider son e-mail en visitant un lien de confirmation qui lui y aura été envoyé. Dans 
    l'intervalle, un compte inactif protégé par son mot de passe lui est créé.  
    
    Le lien est du type 
  
    <pre>http://www.shopozor.ch/activate/encodedUserId/token</pre>

    # Il faudrait se débarrasser de sendActivationEmail: true dans la mutation customerCreate
    
    Lorsqu'un client inconnu fait une demande d'enregistrement avec un mot de passe conforme
    Alors il reçoit un e-mail avec un lien d'activation de compte
    Et son compte est créé
    Et son mot de passe est sauvegardé
    Mais son compte est inactif

  Scénario: Un nouveau client s'enregistre avec un mot de passe non conforme

    Lorsqu'un client inconnu fait une demande d'enregistrement avec un mot de passe non conforme
    Alors il obtient un message d'erreur stipulant que son mot de passe n'est pas conforme à la politique des mots de passe
    Et son compte n'est pas créé
    Et il ne reçoit pas d'e-mail d'activation de compte
    
  @user-accounts  
  Scénario: Le client a déjà un compte inactif et propose un mot de passe conforme
    
    Le client qui a déjà enregistré son e-mail et son mot de passe mais n'a pas réussi à 
    consulter son lien de confirmation dans les temps conserve un compte inactif. Il peut alors
    refaire une demande d'enregistrement et obtenir un nouveau lien d'activation de compte. 
    Il peut spécifier un mot de passe différent lors de cette nouvelle demande.
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte inactif et un mot de passe conforme
    Alors il reçoit un e-mail avec un lien d'activation de compte    
    Et son mot de passe est sauvegardé
    Et son compte reste inactif

  @user-accounts
  Scénario: Le client a déjà un compte inactif et propose un mot de passe non conforme
    
    Si l'utilisateur propose un mot de passe non conforme, alors son compte ne s'active pas. 
    Quoi qu'il arrive avec le mot de passe n'est pas vraiment important. Il peut être sauvé ou 
    pas, il sera redéfini au moment où l'utilisateur entre un mot de passe conforme. 
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte inactif et un mot de passe non conforme
    Alors il obtient un message d'erreur stipulant que son mot de passe n'est pas conforme à la politique des mots de passe
    Et son mot de passe n'est pas sauvegardé
    Et son compte reste inactif  
    Et il ne reçoit pas d'e-mail d'activation de compte
    
  @HackerAbuse @user-accounts
  Scénario: Un utilisateur s'enregistre avec l'e-mail d'un compte actif

    Si un utilisateur tente de s'enregistrer avec un e-mail lié à un compte déjà actif, 
    il faut notifier le client correspondant à cet e-mail et inscrire l'incident 
    dans un journal car il se peut que ce client soit en train de se faire pirater 
    son compte. La notification est envoyée que le pirate potentiel ait entré un mot de 
    passe conforme ou non.
    
    Aucun message d'erreur n'est retourné afin de donner le moins d'information possible 
    à un potentiel pirate. 
    
    Lorsqu'un utilisateur fait une demande d'enregistrement avec l'e-mail d'un compte actif et un mot de passe conforme
    Alors il n'obtient aucun message d'erreur
    Alors un message d'avertissement est envoyé à cet e-mail
    Et l'incident est enregistré dans un journal

  Scénario: Le nouveau client active son compte dans les temps
    
    Au moment où l'utilisateur suit son lien d'activation, il s'invalide et son compte 
    est activé.
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte au plus tard 1 jour après sa réception
    Alors son compte est activé
    Et son lien d'activation est invalidé
    Mais il n'est pas identifié
    
  Scénario: Le nouveau client active son compte une deuxième fois
  
    Le lien d'activation de compte ne peut être utilisé qu'une seule fois, 
    dans un certain laps de temps. 
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Et qui a déjà activé son compte
    Lorsqu'il l'active pour la deuxième fois avant l'expiration du lien
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    
  Scénario: Le nouveau client active son compte trop tard 
    
    En plus de n'être utilisable qu'une seule fois, le lien expire après un certain temps. 
    Dans ce cas, l'utilisateur reste inactif avec un mot de passe, i.e. son compte n'est pas supprimé.
    Il a toujours la possibilité d'activer son compte en refaisant une demande d'enregistrement pour 
    obtenir un nouveau lien, auquel cas il aura même la possibilité de spécifier un mot de passe différent.
    
    Etant donné un nouveau client qui a reçu un lien d'activation de compte
    Lorsqu'il active son compte 2 jours après sa réception
    Alors il obtient un message d'erreur stipulant que le lien a expiré
    Et son compte reste inactif