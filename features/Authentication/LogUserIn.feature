# language: fr

@initial-release @auth @login
Fonctionnalité: Identifier un utilisateur

  *En tant qu'utilisateur enregistré dans le Shopozor,  
  je veux pouvoir m'identifier avec un e-mail et un mot de passe  
  afin de pouvoir faire mes achats ou accéder aux outils de gestion liés à mon compte.*
  
  Contexte: L'utilisateur n'est pas identifié
    Etant donné un utilisateur non identifié sur le Shopozor
    
  Plan du Scénario: L'utilisateur n'est pas encore enregistré
    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail et un mot de passe invalides
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | client               |
      | client         | administrateur       |
      | administrateur | administrateur       |

  @user-accounts
  Plan du Scénario: L'utilisateur est enregistré mais entre un mot de passe erroné
    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail valide et un mot de passe invalide
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | client               |
      | client         | administrateur       |
      | administrateur | administrateur       |

  @user-accounts
  Plan du Scénario: L'utilisateur peut s'identifier avec son identifiant et son mot de passe

    N'importe quel administrateur peut s'identifier en tant que client.
    Si l'identification est réussie, alors la session s'ouvre pour 1 mois.
    Durant cette période, la session doit être rafraîchie.  

    - Si la session n'est pas rafraîchie dans les temps, alors elle se ferme automatiquement et l'utilisateur doit s'identifier à nouveau.  
    
    - Si la session est rafraîchie dans les temps, alors elle reste valide 1 mois de plus, et ainsi de suite, tant qu'elle est rafraîchie dans les temps. 
      La session se ferme alors automatiquement après 1 année. Après 1 année de rafraîchissement de session, l'utilisateur est forcé de s'identifier à nouveau.

    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | administrateur       |
      | administrateur | client               |

  @user-accounts
  Scénario: Un client ne peut pas s'identifier en tant qu'administrateur
    Lorsqu'un client s'identifie en tant qu'administrateur avec un e-mail et un mot de passe valides
    Alors il obtient un message d'erreur stipulant que son compte n'a pas les droits d'administrateur

  @user-accounts
  Plan du Scénario: Définition des permissions du Consommateur et du Producteur

    Le Consommateur et le Producteur n'ont aucune permission particulière.
    Ils peuvent accéder et modifier leurs données personnelles.
    Les produits font partie des données personnelles du Producteur. 
    Le Consommateur est un client. Le Producteur est un administrateur. 

    Lorsqu'un <persona> s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et il n'obtient pas de permissions
    Et il est considéré comme un <type d'utilisateur>

    Exemples:
      | persona      | type d'utilisateur |
      | Consommateur | client             |
      | Producteur   | administrateur     |

  @user-accounts
  Scénario: Définition des permissions du Responsable

    Le Responsable est un administrateur. En plus de la gestion de ses données personnelles, le Responsable peut  
    
    - accéder et modifier les produits publiés par les Producteurs affiliés à ses Shops
    - accéder à l'historique de ventes de tous ses Shops
    - verser le revenu des ventes à ses Producteurs

    Lorsqu'un Responsable s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et il obtient les permissions suivantes:
      | permission       |
      | MANAGE_PRODUCERS |
    Et il est considéré comme un administrateur

  @user-accounts
  Scénario: Définition des permissions du Rex

    Le Rex est un administrateur. En plus de la gestion de ses données personnelles, le Rex peut  

    - accéder et modifier les produits publiés par n'importe quel Producteur affilié au Shopozor
    - accéder à l'historique des ventes de tous les Shops du Shopozor
    - verser le revenu des ventes à ses Shops
    - changer les permissions des utilisateurs du Shopozor  
    
    Lorsqu'un Rex s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et il obtient les permissions suivantes:
      | permission       |
      | MANAGE_STAFF     |
      | MANAGE_USERS     |
      | MANAGE_PRODUCERS |
      | MANAGE_MANAGERS  |
    Et il est considéré comme un administrateur

  @user-accounts
  Scénario: Définition des permissions de Softozor

    En plus de la gestion de ses données personnelles, Softozor a tous les droits, pour des raisons de maintenance.
    C'est un super-utilisateur.

    Lorsqu'un Softozor s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et c'est un super-utilisateur
    Et il est considéré comme un administrateur
    

  @HackerAbuse
  Plan du Scénario: Un utilisateur qui n'a pas encore défini de mot de passe ne peut pas s'identifier
    Etant donné un utilisateur <état> et sans mot de passe
    Lorsqu'il s'identifie
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects
    
    Exemples:
      | état    |
      | actif   |
      | inactif |

    
  @HackerAbuse 
  Scénario: Un utilisateur inactif qui a défini un mot de passe ne peut pas s'identifier
    Etant donné un utilisateur inactif et avec mot de passe
    Lorsqu'il s'identifie
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects