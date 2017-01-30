
# Users and Groups

A user should be able to register an incident anonymously. Each anonymous user should be coupled to a club.
We have 3 **categories of users**: the normal user, the administration user (AHot, safety manager), and the superusers: these are all defined by 3 groups :
* ato_user
* ato_admin
* ato_super
We use the standard user model that comes with django. Thus it needed to be extended. In the models.py file you will find the model **Ato_gebruiker**, which couples a user from django with a glider-club (model **Club**).
To reflect this extention, an **AToGebruiker** class had to be defined inlined in admin.py

So when you define a user, don't forget to select the correct club, and assign a group to the user. Only one group must be assigned to a user.

# Messages

One or more message can be put on the first page of the application, depending on the user or group of the user, logging in. The model reflecting this is called **Nieuws**. A message can be coupled to a user or a group (one of the 3 groups defined by app). Don't forget to put the message **online**!

# Voorval(incident/accident) & Maatregel(action)

The whole purpose of this app is to register incidents/accidents, but also the actions, which have been taken later on, as a measure on the incident.  
One incident/accident registration can have different actions.
To be able tio easy reference the number of actions on an incident, a database **trigger** has been defined, which updates the field **aantal_maatregelen**, when an action is added. On delete of an action, the field is decremented by 1.

## Export of Voorvallen/Maatregelen

A view has been defined to simplify this action. This is basically a join between the table  **Voorval** and the table **Maatregel**, but I also wanted to include the Voorval records with no action assigned to it (no record Maatregel present yet).  
I created a database **view** for this purpose, basically because I didn't know how to handle this with django ORM. The view is called **voorval_maatregel**. This view is also reflected in a model called **VoorvalMaatregel**. Be sure to keep this two in sync, especially when extending Voorval or Maatregel.


