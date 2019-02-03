# language: fr

@initial-release @login
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

  Plan du Scénario: L'utilisateur est enregistré mais entre un mot de passe erroné
    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail valide et un mot de passe invalide
    Alors il obtient un message d'erreur stipulant que ses identifiants sont incorrects

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | client               |
      | client         | administrateur       |
      | administrateur | administrateur       |

  Plan du Scénario: L'utilisateur peut s'identifier avec son identifiant et son mot de passe

    N'importe quel administrateur peut s'identifier en tant que client.

    Lorsqu'un <utilisateur> s'identifie en tant que <utilisateur prétendu> avec un e-mail et un mot de passe valides
    Alors il reçoit un token d'authentification

    Exemples:
      | utilisateur    | utilisateur prétendu |
      | client         | client               |
      | administrateur | administrateur       |
      | administrateur | client               |

  Scénario: Un client ne peut pas s'identifier en tant qu'administrateur
    Lorsqu'un client s'identifie en tant qu'administrateur avec un e-mail et un mot de passe valides
    Alors il obtient un message d'erreur stipulant que son compte n'a pas les droits d'administrateur

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

  Scénario: Définition des permissions du Responsable

    En plus de la gestion de ses données personnelles, le Responsable peut

    * accéder et modifier les produits publiés par les Producteurs affiliés à ses Shops
    * accéder à l'historique de ventes de tous ses Shops
    * verser le revenu des ventes à ses Producteurs
    
    Le Responsable est un administrateur.

    Lorsqu'un Responsable s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et il obtient les permissions suivantes:
      | permission       |
      | MANAGE_PRODUCERS |
    Et il est considéré comme un administrateur

  Scénario: Définition des permissions du Rex

    En plus de la gestion de ses données personnelles, le Rex peut

    * accéder et modifier les produits publiés par n'importe quel Producteur affilié au Shopozor
    * accéder à l'historique des ventes de tous les Shops du Shopozor
    * verser le revenu des ventes à ses Shops
    * changer les permissions des utilisateurs du Shopozor

    Le Rex est un administrateur.
    
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

  Scénario: Définition des permissions de Softozor

    En plus de la gestion de ses données personnelles, Softozor a tous les droits, pour des raisons de maintenance.
    C'est un super-utilisateur.

    Lorsque Softozor s'identifie avec un e-mail et un mot de passe valides
    Alors sa session s'ouvre pour 1 mois
    Et reste valide pendant 1 an
    Et il obtient les permissions suivantes:
      | permission       |
      | MANAGE_STAFF     |
      | MANAGE_USERS     |
      | MANAGE_PRODUCERS |
      | MANAGE_MANAGERS  |
      | MANAGE_REX       |
    Et il est considéré comme un administrateur
