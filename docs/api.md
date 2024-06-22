## API Documentation

All PackageRows or PackageFormRows are to be displayed in the table in the frontend.

### POST /createPackage
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

## Data Types

**type CreatePackageRequest**
- `packageName` (str)
- `pdfs` (List[str])

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
- `rawPdfs` (List[str]) :               Paths to the images of initial files passed in.
- `imagesWithBoxes` (List[str])         Paths to the images with boxes drawn on.
- `formFields` (List[FormField])        Form fields created by GPT for the final form
- `googleFormUrl` (str)
- `filledOutPackages` (List[str])    Paths to the filled out pdfs

---------------------------------------------------------------------------------------------

**type FilledOutPackage**
- `email` (str)
- `pdfs` (List[str])

---------------------------------------------------------------------------------------------

**enum PackageStatus**
- `DETECTING` : `Detecting Form Boxes with YOLO`
- `ANALYZING` : `Analyzing Form Boxes With GPT4o`
- `CREATING` : `Creating Form with GPT4o`
- `COMPLETE` : `Complete`

---------------------------------------------------------------------------------------------

**type FormField**
- `name` (str)
- `description` (str)
- `type` (FormFieldType)

---------------------------------------------------------------------------------------------

**enum FormFieldType**
- `TEXT` : `Text`
- `MULTIPLE_CHOICE` : `Multiple Choice`
- `CHECKBOX` : `Checkbox`
