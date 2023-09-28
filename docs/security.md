# SECURITY

A lot of emphasis has been put on security in this project, due to the private nature of the data contained in a 
medical report. Access to resources was properly limiyted to only those with the proper credentials and permissions.

## OVERVIEW

1. Authentication: JWT(JSON Web Token) was used as the default authentication mechanism. It provides a secure method
of authenticating each route. Once a user is authenticated, the data is encrypted using secured encryption algorithms 
and sent as a token. The tokens aren't stored on the database, because it is possible to decrypt the token, but only
with the proper encryption keys. The tokens are short lived and are only valid for a certain time period, therefore
preventing replay attacks.
2. Permission: Access to certain data and actions carried out, are controlled properly. There are two types of user roles
for this project namely: Patient and Doctor. A superadmin can also exists, without the need to pick a certain role.
Each user type has its own set of permissions, which are used to control access to certain resources.
During creation of medical records, doctor information is populated by presently logged in doctor.

### Patient Permissions

1. Patient view doctor profile data, and patient profile data.
2. A patient can view only their own medical report(s) and not others.
3. A patient can not delete, create or update a medical report
4. A patient can update and delete only their profile data

### Doctor Permissions
1. Doctor can view patient profile data and doctor profile data
2. A doctor can view medical report
3. A doctor can create medical report
4. A doctor can only update and delete medical records created by them.
5. A doctor can update and delete only their doctor data