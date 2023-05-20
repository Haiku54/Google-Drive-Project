# Google Drive Access Converter

Google Drive Access Converter is a project aimed at providing a solution for users with restricted internet access, specifically religious individuals with limited internet providers, by converting publicly shared Google Drive links into privately shared ones. This enables them to access content that might otherwise be inaccessible to them.

## How it works

The project was built using Google Cloud Platform and Python, which connects to Google Drive and Google Mail APIs. Users send an email containing a shared link in Google Drive for a file, and the system automatically uploads the content of the link to the Google Drive account and returns a private share link, sending it back to the user.

## Why it's necessary

Many religious people have limited ISPs with filtered access, allowing them to access only privately shared content. This restriction oppresses them, as they cannot access a lot of content meant for their consumption. Despite this limitation, they do not want to cancel internet filtering for religious reasons. This project helps them maintain their internet filtering while also accessing content shared on Google Drive by simply sending an email.

## Current status and future progress

Google Drive Access Converter is making consistent progress in its development. Initially, it operated on a local machine but has since transitioned to a more robust setup.

An important part of this progression was the enhancement of database management. Originally, a local SQL server was used for managing requests and the database. However, this aspect has now been successfully migrated to Microsoft Azure's MySQL cloud server, thereby improving efficiency and accessibility.

The most significant advancement has been the successful migration of the system to Google Cloud Functions. This development has automated the process, where the system triggers a file upload to the developer's Google Drive and generates a new link for the user upon receipt of an email. This upgrade has streamlined the operation and significantly enhanced the reliability and efficiency of the system.

The Google Drive Access Converter is already serving many users effectively. For those interested, a [simple registration form](https://docs.google.com/forms/d/e/1FAIpQLSenhwvdwOJKnqU12meJEKLcc_VsHz5KJ50UI6JbbOV-03vdOw/viewform?usp=sf_link) is available. Upon registration, users can start utilizing the service immediately.

Future plans for this project include further refinement and improvement, with the focus on maintaining its practical and manageable scale, while constantly increasing its effectiveness and value.


## Project Diagrams

This section contains visual representations of the project structure and database design, including an Entity Relationship Diagram (ERD) and a Unified Modeling Language (UML) diagram.

### Entity Relationship Diagram (ERD)

The ERD provides a detailed view of the database structure, including tables, fields, and the relationships between them. It serves as a blueprint for designing the database system.

![ERD diagram](https://github.com/Haiku54/Google-Drive-Project/assets/80857560/f8fbc968-34e8-418b-a390-a7a7bc16f359)


