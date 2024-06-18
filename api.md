## API Documentation

### POST /signup
**Description:** Register a new user.

**Request Parameters:**
- `username` (str): The username of the new user.
- `password` (str): The password of the new user.

**Response:**
- JWT Token (user_id encoded)


### POST /login
**Description:** Authenticate an existing user.

**Request Parameters:**
- `username` (str): The username of the user.
- `password` (str): The password of the user.

**Response:**
- JWT Token (user_id encoded)


### POST /processPackage
**Description:** User uploads a file/files to be processed.

**Request Parameters:**
- `files` (List): A list of files to be processed.

**Response:**
- No response


### GET /getUsersPackages
**Description:** Retrieve a list of packages with packageId, packageName and status. Use this endpoint to show the user all the packages they have, in like a table or something. You can poll this so the user can see statuses update in real time.

**Request Parameters:**
- None (uses user id in JWT token)

**Response:**
- `List[Package]`: A list of packages.


### GET /getPackageRows
**Description:** Retrieve details of a specific package. This will return the original file URLs and the 

**Request Parameters:**
- `packageId` (str): The ID of the package.

**Response:**
- `Package`: The details of the package with just id, name and status.


### GET /getPackage
**Description:** Retrieve the complete details of a specific package.

**Request Parameters:**
- `packageId` (str): The ID of the package.

**Response:**
- `Package`: The complete details of the package including id, name, status, raw files, labeled files, and form fields. When the user is viewing this page, continuously poll this. Rerender the data when the PackageStatus changes.


### POST /createPackageForm
**Description:** Create a new package form.

**Request Parameters:**
- `name` (str): The name of the package form.
- `packageId` (str): The ID of the package being used.

**Response:**
- `packageForm` (PackageForm): The created package form.


### GET /getPackageForm
**Description:** Retrieve details of a specific package form. Poll this when the user is viewing a package form. 

**Request Parameters:**
- `packageFormId` (str): The ID of the package form.

**Response:**
- `PackageForm`: The package form.


### GET /getUsersPackageForms
**Description:** Retrieve a list of package forms for the authenticated user. Poll this when the user is on this page.

**Request Parameters:**
- None (uses user id in JWT token)

**Response:**
- `List[PackageForm]`: A list of package forms with minimal details.



## Data Types

**Package**
- `packageId` (str): The ID of the package.
- `packageName` (str): The name of the package.
- `packageStatus` (PackageStatus): The status of the package.
- `rawFiles` (List[str]): URLs to the original files
- `labeledFiles` (List[str]): URLs to files with labels
- `formFields` (List[formField]): List of form fields found in the files.

**PackageStatus**
- `Finding Forms`
- `Reading`
- `Completed`
- ...

**FormField**
- `description` (str)
- `name` (str)
- `fieldType` (FieldType)

**PackageForm**
- `packageFormId` (str): The ID of the package form.
- `name` (str): The name of the package form.
- `typeformUrls` (List[str]): A list of Typeform URLs.
- `formFields` ([FormField]): A list of form fields.
- `filledOutFileUrls` ([str]): A list of URLs to the filled out files.
