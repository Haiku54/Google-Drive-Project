# Google Drive Access Converter

Google Drive Access Converter is a project aimed at providing a solution for users with restricted internet access, specifically religious individuals with limited internet providers, by converting publicly shared Google Drive links into privately shared ones. This enables them to access content that might otherwise be inaccessible to them.

## How it works

The project was built using Google Cloud Platform and Python, which connects to Google Drive and Google Mail APIs. Users send an email containing a shared link in Google Drive for a file, and the system automatically uploads the content of the link to the Google Drive account and returns a private share link, sending it back to the user.

## Why it's necessary

Many religious people have limited ISPs with filtered access, allowing them to access only privately shared content. This restriction oppresses them, as they cannot access a lot of content meant for their consumption. Despite this limitation, they do not want to cancel internet filtering for religious reasons. This project helps them maintain their internet filtering while also accessing content shared on Google Drive by simply sending an email.

## Current status and future progress

GDrive Access Converter is still a work in progress, but people are already using it. The current run is only on the developer's local computer, where the existing main function is temporary. Later, the project will be transferred to Google Cloud Functions which, upon receiving an email from the user, will automatically activate the upload of the file to the developer's Google Drive and return the new link to the user.

In addition, the current documentation of the requests and database management is hosted on a local SQL server. Later, it will be ported to Google SQL to improve efficiency.


