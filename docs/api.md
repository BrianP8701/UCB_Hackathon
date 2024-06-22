## API Documentation

All PackageRows or PackageFormRows are to be displayed in the table in the frontend.

### POST /processPackage
**Request Parameters:**
- `files` (List[File])
- `name` (str)

**Response:**
- `packageRows` (List[PackageRow])

---------------------------------------------------------------------------------------------

### GET /getPackagesRows
**Request Parameters:**
- None

**Response:**
- `packageRows` (List[PackageRow])

---------------------------------------------------------------------------------------------

### GET /getPackage
**Request Parameters:**
- `packageId` (str)

**Response:**
- `package` (Package)

---------------------------------------------------------------------------------------------

### GET /getPackageStatus
**Request Parameters:**
- `packageId` (str)

**Response:**
- `packageStatus` (PackageStatus)

---------------------------------------------------------------------------------------------

### POST /createPackageForm
**Request Parameters:**
- `name` (str)
- `packageId` (str)

**Response:**
- `packageFormRows` (List[PackageFormRow])

---------------------------------------------------------------------------------------------

### GET /getPackageForm
**Request Parameters:**
- `packageFormId` (str): The ID of the package form.

**Response:**
- `packageForm`: The package form.

---------------------------------------------------------------------------------------------

### GET /getPackageFormRows
**Request Parameters:**
- `packageId` (str)

**Response:**
- `packageFormRows` (List[PackageFormRows]): A list of package forms with minimal details.

---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------

## Data Types

**type CreatePackageRequest**
- `packageName` (str)
- `rawFiles` (List[str])

---------------------------------------------------------------------------------------------

**type PackageRow**
- `packageId` (str)
- `packageName` (str)
- `packageStatus` (PackageStatus)

---------------------------------------------------------------------------------------------

**type Package**
- `packageId` (str)
- `packageName` (str)
- `packageStatus` (PackageStatus)
- `rawFiles` (List[str]) :          Paths to the images of initial files passed in.
- `filesWithBoxes` (List[str])      Paths to the images with boxes drawn on.
- `formFields` (List[FormField])    Form fields created by GPT for the final form

---------------------------------------------------------------------------------------------

**type PackageFormRow**
- `packageFormId` (str)
- `packageName` (str)
- `googleFormUrl` (str)
- `name` (str)

---------------------------------------------------------------------------------------------

**type PackageForm**
- `packageFormId` (str)
- `packageName` (str)
- `name` (str)
- `googleFormUrl` (str)
- `files` ([str]) : Paths to the filled out pdfs

---------------------------------------------------------------------------------------------

**enum PackageStatus**
- `detecting` : `Detecting Form Boxes with YOLO`
- `analyzing` : `Analyzing Form Boxes With GPT4o`
- `creating` : `Creating Form with GPT4o`
- `complete` : `Complete`

---------------------------------------------------------------------------------------------

**type FormField**
- `name` (str)
- `description` (str)
- `type` (FormFieldType)
