## User Stories
> As a researcher, I would like to be able to create Imaging pipelines by linking predefined components together
* Users should be able to drag and drop components onto a canvas
* Users should be able to directionally link components together; showing a flow of data

---
> As a researcher, I  would like to be able to add too add to the list of components.
* Users should be able to upload an algorithm they have created to be used in the pipelines.
* This process should be language and requirements agnostic.

---
> As a researcher, I  would like to save the pipelines I have created
* User should be able to save the pipelines they have created into the database.
* Users should be able to edit, modify, and delete the pipelines they have created

---
> As a researcher, I would like to have a dashboard to view the status of my pipelines


---
> As an admin, I would like ensure that all routes are protected behind a login page.
* Due to the  sensitive nature of clinical data, all routes will require and authorization token to be access
* Only users with specific privilege levels will be able to access certain resources

---
> As an user, I would like to use the same credentials to login as I use to login to my work computer.
* Users will be asked to login with their bccrc credentials.
* Authentication will be handled by the bccrc ldap server
* Upon successful login, an api token  will be given to the user which will enable them to access the app.

---
> As an admin, I would like to control which users have access to specific parts of the app.

---
> As an admin, I would like to view and control about how users are using the application
* The admin should be able to view an admin dashboard which will display all relevant information about the app and its users.
* The admin should be able to to make changes to any and all parts of the application (including created pipelines).

## Definitions
| Term | Definition |
| ---- | ---------- |
Component | All components should had a well defined input and output. Terminal components should have only an input or output. Algorithms are examples of non-terminal components while scanners and databases are examples of terminal components.