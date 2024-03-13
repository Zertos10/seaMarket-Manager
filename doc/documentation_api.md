# User

## **manage_user/** 

*Permission* : Admin
### *GET* : Liste des utilisateurs
#### Retour
**liste**
	**id**: int, identifiant de l'utilisateur dans la base de donnée
	**email**: string, courriel de l'utilisateur
	**lastName**: string ou null (si vide), nom de l'utilisateur 
	**firstName**: string ou null (si vide), prénom de l'utilisateur
**status**:200

### *POST*: Créer un utilisateur
#### Corps 
**email**: string, format : user@mail.ext ,*required*
**password** : string, mot de passe, *required*
**lastName**: string,nom de famille de l'utilisateur, *optional*
**firstName**: string,prénom de l'utilisateur, *optional*
#### Retour
**id** : int, identifiant de l'utilisateur dans la base de donnée
**status**: 201


#### Erreur
**errors**: object, message d'erreur 
**status**: 400

### PUT
#### Corps
**id**: int, identifiant de l'utilisateur dans la base de donnée,*required*
**lastName**: string, nom de famille de l'utilisateur, *optional*
**firstName**: string, prénom de l'utilisateur, *optional*
**email**: string, email de l'utilisateur, *format*:  user@mail.ext ,*optional*

#### Retour
**id**: int, identifiant de l'utilisateur dans la base de donnée
**email**: string, courriel de l'utilisateur
**lastName**: string ou null (si vide), nom de l'utilisateur 
**firstName**: string ou null (si vide), prénom de l'utilisateur
**status**: 200

#### Erreur
**status**:400
**error**: object, message d'erreur
### *DELETE*: Supprimer un utilisateur

#### Corps
**id**: int, identifiant de l'utilisateur dans la base de donnée

### Retour
**message**: string, *contenu* : "User deleted"
**status**: 200
# Product
## products/ 
### *GET*: Liste des produits mis en catalogue
*Permission*: User
#### Retour
**liste**
	**id**: int, identifiant du produit dans la base de donnée
	**productId**: identifiant du produit dans la base de donnée de Bateau Thibaut
	**prix**: decimal, prix unité de vente du produit
	**quantité**: int, quantité disponible en stock
	**percentSale**: int, pourcentage de promotion du produit (0 correspond au prix par défaut)
	**sellArticle** int, nombre de produit vendu
	**comments**: string, commentaire du produits
**status**: 200
## product/*id*/
*Permission*:User
### GET: Détail d'un produit
#### En-tête
**id**: int, identifiant du produit dans la base de donnée

#### Retour
**id**: int, identifiant du produit dans la base de donnée
**productId**: identifiant du produit dans la base de donnée de Bateau Thibaut
**prix**: decimal, prix unité de vente du produit
**quantité**: int, quantité disponible en stock
**percentSale**: int, pourcentage de promotion du produit (0 correspond au prix par défaut)
**sellArticle** int, nombre de produit vendu
**comments**: string, commentaire du produits
**status**: 200

## manage_product/
*Permission*: User
### POST: Ajouter un produit au catalogue
#### Corps
**productId**: identifiant du produit dans la base de donnée de Bateau Thibaut, *required*
**prix**: decimal, prix unité de vente du produit, 0 par défaut,*optional*
**quantité**: int, quantité disponible en stock,0 par défaut,*optional*
**percentSale**: int, pourcentage de promotion du produit (0 par défaut),*optional*
**sellArticle** int, nombre de produit vendu, 0 par défaut, *optional*
**comments**: string, commentaire du produits, vide par défaut, *optional*
**category**:liste de l'objet **Category**, liste des catégorie attaché au produit,par défaut catégory "tous", *optional*

#### Retour
**id**: int, identifiant du produit dans la base de donnée
**status**:201

### DELETE: Supprime un ou plusieurs produit du catalogue
*Supprime également l'historique liée au produit*
#### Corps
**liste**: 
	**id**:int, identifiant du produit dans la base de donnée
#### Retour
**message**: Message confirmant la suppression
**status**: 200

### PATCH: Modifier un produit

#### Corps
#### Retour


# Category



# Stat

## stats/revenues/
*Permission*: User

### GET: Historique du chiffre d'affaire
*Montant des produits vendus*
#### Paramètre
**category**: string, nom de la catégorie, *required*
**typeDate**: string, plage de donnée (ex : day,week,month,years,...),*required*
#### Retour
**liste**
	**date**:date
	**value**,decimal, prix en euro
	**quantity**: int, quantité vendu
**status**:200
## stats/margin/
*Permission*: User

### GET: Historique des marges

#### Paramètre

#### Retour

# Authentification

## login/
### POST: Authentification de l'utilisateur
#### Corps
**email**: string, email de l'utilisateur,*required*
**password**: string, mot de passe de l'utilisateur,*required*
#### Retour
**refresh**:string, Token de rafraichissement de la session
**access**: string, Token d'accès à la session
**refresh_exp**: date, Date d'expiration du token de rafraichissement
**access_exp**: date, Date d'expiration du token d'accès

## login/refresh/

### POST: Rafraichi le token d'accès
#### Corps
**refresh**:string, token de rafraichissement de la session, *required*

### Retour
**access**: string, token d'accès à la session

## logout/

### GET : Déconnecte la session
#### Retour
**status**: 200

