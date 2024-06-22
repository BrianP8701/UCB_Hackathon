# Demo Plan

1. Explain the problem we are solving at a high level.
2. Explain backend design
3. Demo frontend
    (a) User uploads a file (single page)
    (b) Watch as the file undergoes phases until completion
    (c) Create a form from the package
    (d) Fill out the google form
    (e) Fetch the package form again to display the filled out file


/getPackageRows     to display inital page with all package rows

/processPackages    upload a list of files to be processed

/getPackage         click on the newly created package to view it

/getPackageStatus   poll this endpoint. whenever the package status changes call getPackage again

When the package is done processing we should display the images with the filled out boxes and beside it all the form fields

/createPackageForm  create the package form. it will return the list of package forms for this package

We then fill out the google form.

/getPackageForm     Display the returned pdf file names, and download the given final filled out file to show the end result