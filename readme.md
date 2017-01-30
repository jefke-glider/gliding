#ATO safety incident/accident registrations

This project aims to implement the incident/accident registrations , 
which are required by the ATO EASA regulations. This is a typical 
website, where all registered clubs can login and enter incidents/accidents.

A club member can register and review a registration. The user accounts are anonymous (one or more per club). This way we hope that more incidents gets registered.
The responsible AhoT and the safety manager gets notified when a registration has occured in their club, they can review this registrations and make notes about the corrective actions.
The safety manager can query the database, and make reports in different formats.

#Requirements

* Python 3
* django 1.10
* bootstrap 3.0
* jQuery
* PostGresql 9.x

#ToDO
* send email to Ahot and safety manager OK
* corrective actions registration OK
* complete registration fields
* add some filtering possibilities e.g. only show records for the current year
* upload of all kinds of files (photo, document, etc..)
* 