# Google Drive Access Converter

Google Drive Access Converter is a project aimed at providing a solution for users with restricted internet access, specifically religious individuals with limited internet providers, by converting publicly shared Google Drive links into privately shared ones. This enables them to access content that might otherwise be inaccessible to them.

## How it works

The project was built using Google Cloud Platform and Python, which connects to Google Drive and Google Mail APIs. Users send an email containing a shared link in Google Drive for a file, and the system automatically uploads the content of the link to the Google Drive account and returns a private share link, sending it back to the user.

## Why it's necessary

Many religious people have limited ISPs with filtered access, allowing them to access only privately shared content. This restriction oppresses them, as they cannot access a lot of content meant for their consumption. Despite this limitation, they do not want to cancel internet filtering for religious reasons. This project helps them maintain their internet filtering while also accessing content shared on Google Drive by simply sending an email.

## Current status and future progress

Google Drive Access Converter is in ongoing development and already serving users, even while work continues. Currently, the system runs on the developer's local machine with main function in a temporary setup.

A significant advancement in the project has been in terms of database management. Initially, the documentation of the requests and database management was hosted on a local SQL server. However, it has now been successfully migrated to Microsoft Azure's MySQL cloud server, resulting in improved efficiency and accessibility.

The next step planned for the project is to migrate it to Google Cloud Functions. Upon completion of this step, the system will automatically trigger the file upload to the developer's Google Drive and return a new link to the user when an email is received.


## Project Diagrams

This section contains visual representations of the project structure and database design, including an Entity Relationship Diagram (ERD) and a Unified Modeling Language (UML) diagram.

### Entity Relationship Diagram (ERD)

The ERD provides a detailed view of the database structure, including tables, fields, and the relationships between them. It serves as a blueprint for designing the database system.

![ERD diagram](https://github.com/Haiku54/Google-Drive-Project/assets/80857560/f8fbc968-34e8-418b-a390-a7a7bc16f359)


