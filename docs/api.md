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
- None

**Response:**
- `packageFormRows` (List[PackageFormRows]): A list of package forms with minimal details.

---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------

## Data Types

**type CreatePackageRequest**
- `packageName` (str)
- `rawFiles` (List[File])

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
- `rawFiles` (List[File])
- `labeledFiles` (List[File]): If status is `complete`

---------------------------------------------------------------------------------------------

**type PackageFormRow**
- `packageFormId` (str)
- `packageName` (str)
- `name` (str)

---------------------------------------------------------------------------------------------

**type PackageForm**
- `packageFormId` (str)
- `packageName` (str)
- `name` (str)
- `typeformUrl` (str)
- `files` ([File]) : Filled out files from typeform

---------------------------------------------------------------------------------------------

**enum PackageStatus**
- `detecting` : `Detecting Form Boxes with YOLO`
- `analyzing` : `Analyzing Form Boxes With GPT4o`
- `creating` : `Creating Form with GPT4o`
- `complete` : `Complete`
