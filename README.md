# NSBM Super App System Backend

## Introduction

The NSBM Super App System Backend is a comprehensive Flask-based RESTful API designed to provide backend services for the NSBM Super App. This backend system facilitates user authentication, data management, event coordination, and system monitoring for the NSBM university community.

The system is built with a modular architecture using Flask and MongoDB, offering secure authentication via JWT, real-time system monitoring, and various data management capabilities. It provides specialized functionality for students, lecturers, staff, and administrators, enabling features such as event management, user registration, and administrative controls.

This backend serves as the central hub connecting different components of the NSBM Super App ecosystem, providing robust API endpoints for data storage, retrieval, and manipulation. The system includes advanced features like system monitoring, event cleanup services, and specialized access controls for different user types.

## User Manual

### System Requirements

- Python 3.7 or higher
- MongoDB 4.0 or higher
- Required Python packages (see requirements section)

### Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd nsbm_sa_system_backend
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file in the project root with the following variables:
   ```
   MONGO_URI="mongodb://localhost:27017/nsbm_sa"
   JWT_SECRET_KEY="your_secret_key_here"
   ```
   or do it directly in your terminal:
   ```
   export JWT_SECRET_KEY=a3f4e7b2c6d8e1f7a9b0c2d4e6f8a1b3c5d7e9f0a2c4e6d8b0a1c3e5f7a9d2
   ```
   Alternatively, you can export these variables directly:
   ```bash
   # For Windows CMD:
   set MONGO_URI=mongodb://localhost:27017/nsbm_sa
   set JWT_SECRET_KEY=your_secret_key_here

   # For Windows PowerShell:
   $env:MONGO_URI="mongodb://localhost:27017/nsbm_sa"
   $env:JWT_SECRET_KEY="your_secret_key_here"

   # For Linux/macOS:
   export MONGO_URI="mongodb://localhost:27017/nsbm_sa"
   export JWT_SECRET_KEY="your_secret_key_here"
   ```

4. **Start the server:**
   ```bash
   python run.py
   ```
   The server will start on `http://0.0.0.0:5000` by default.

### API Endpoints

#### Authentication Endpoints

1. **User Registration:**
   - Endpoint: `/auth/register`
   - Method: `POST`
   - Required Fields: full_name, email, password, phone_number, user_type, profile_picture, created_at, updated_at
   - Optional Fields: student_id, intake, degree, university, nic
   - Returns: JWT access token upon successful registration

2. **User Login:**
   - Endpoint: `/auth/login`
   - Method: `POST`
   - Required Fields: email, password
   - Returns: JWT access token and user details

3. **MIC (Society) Registration:**
   - Endpoint: `/auth/mic/register`
   - Method: `POST`
   - Required Fields: email, society_name, password
   - Returns: JWT access token

4. **MIC (Society) Login:**
   - Endpoint: `/auth/mic/login`
   - Method: `POST`
   - Required Fields: email, password
   - Returns: JWT access token and society details

5. **Admin Login:**
   - Endpoint: `/auth/admin`
   - Method: `POST`
   - Required Fields: email, password
   - Returns: JWT access token with admin privileges

#### Data Management Endpoints

1. **Store Data:**
   - Endpoint: `/data/<collection_name>/store`
   - Method: `POST`
   - Authorization: JWT required
   - Body: JSON data to store
   - Returns: Success message with document ID

2. **Create Document:**
   - Endpoint: `/data/<collection_name>/create`
   - Method: `POST`
   - Authorization: JWT required
   - Body: JSON data for document
   - Returns: Success message with document ID

3. **Fetch All Data:**
   - Endpoint: `/data/<collection_name>/fetch`
   - Method: `GET`
   - Authorization: JWT required
   - Returns: Array of documents from the collection

4. **Fetch Data by ID:**
   - Endpoint: `/data/<collection_name>/fetch/<record_id>`
   - Method: `GET`
   - Authorization: JWT required
   - Returns: Single document matching the ID

5. **Update Data:**
   - Endpoint: `/data/<collection_name>/update/<record_id>`
   - Method: `PUT`
   - Authorization: JWT required
   - Body: JSON data with fields to update
   - Returns: Success message

6. **Delete Event Request:**
   - Endpoint: `/data/<collection_name>/delete/<record_id>`
   - Method: `DELETE`
   - Authorization: JWT required
   - Returns: Success message

7. **Approve Event Request:**
   - Endpoint: `/data/<collection_name>/approve/<record_id>`
   - Method: `POST`
   - Authorization: JWT required
   - Returns: Success message

8. **Count Field Occurrences:**
   - Endpoint: `/data/<collection_name>/count`
   - Method: `GET`
   - Authorization: JWT required
   - Query Parameters: field, value, event_data_get
   - Returns: Count of matching documents

#### Administrative Endpoints

1. **Execute MongoDB Query:**
   - Endpoint: `/data/mongodb/query`
   - Method: `POST`
   - Authorization: JWT required (admin only)
   - Body: JSON with collection, query, sort, page, limit
   - Returns: Query results with pagination info

2. **Create Collection:**
   - Endpoint: `/data/create-collection`
   - Method: `POST`
   - Authorization: JWT required (admin only)
   - Body: JSON with collection name
   - Returns: Success message

3. **Password Hashing:**
   - Endpoint: `/custom/hash-password`
   - Method: `POST`
   - Authorization: JWT required (admin only)
   - Body: JSON with plaintext password
   - Returns: Hashed password

4. **Custom Function Execution:**
   - Endpoint: `/custom/execute`
   - Method: `POST`
   - Authorization: JWT required
   - Body: JSON with input parameters
   - Returns: Function result

### Security Features

1. **JWT Authentication:**
   - All protected endpoints require a valid JWT token
   - Tokens include role-based claims for authorization
   - Different user types have different access levels

2. **Password Security:**
   - Passwords are hashed using bcrypt before storage
   - Password verification is secure and leak-resistant

3. **Role-Based Access Control:**
   - Admin endpoints are restricted to superuser accounts
   - MIC users have access to their society's events only
   - Regular users have standard permissions

### System Monitoring

The backend includes automatic system monitoring that collects:
- CPU usage
- RAM usage
- Network I/O statistics
- Storage usage

This data is stored in the `admin_sys_stats` collection and can be accessed by administrators for system health analysis. Old monitoring data is automatically pruned to prevent database bloat.

### Logging System

The system uses a comprehensive logging service that:
- Logs operations with timestamp and severity level
- Uses color-coded console output for better visibility
- Stores logs in `~/.nsbm-sa-logs/log.txt`
- Captures info, warnings, errors, and success messages

### Automated Maintenance

1. **System Status Monitoring:**
   - Runs in the background to collect system metrics
   - Stores metrics in MongoDB for analysis
   - Auto-prunes data older than 1 day

2. **Event Cleanup:**
   - Automatically removes invalid or corrupt events
   - Validates event data integrity periodically
   - Maintains database health

### Example API Usage

1. **Register a new user:**
   ```bash
   curl -X POST http://127.0.0.1:5000/auth/register -H "Content-Type: application/json" \
   -d '{
     "full_name": "John Doe",
     "email": "john@example.com",
     "password": "securepassword",
     "phone_number": "+94123456789",
     "user_type": "student",
     "student_id": "S12345",
     "intake": "2023",
     "degree": "Computer Science",
     "university": "NSBM",
     "nic": "123456789X",
     "profile_picture": "https://example.com/profile.jpg",
     "created_at": "2023-05-15T10:00:00Z",
     "updated_at": "2023-05-15T10:00:00Z"
   }'
   ```

2. **Login and get token:**
   ```bash
   curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" \
   -d '{
     "email": "john@example.com",
     "password": "securepassword"
   }'
   ```

3. **Create a new event request:**
   ```bash
   curl -X POST http://127.0.0.1:5000/data/event_requests/store \
   -H "Authorization: Bearer YOUR_JWT_TOKEN" \
   -H "Content-Type: application/json" \
   -d '{
     "event_name": "Tech Conference",
     "event_description": "Annual technology conference",
     "event_venue": "Main Auditorium",
     "selectedDate": "2023-12-15",
     "selectedTime": "10:00",
     "event_held_by": "Computing Society",
     "organizer_email": "john@example.com",
     "created_at": "2023-05-15T10:00:00Z"
   }'
   ```

4. **Fetch all events:**
   ```bash
   curl -X GET http://127.0.0.1:5000/data/events/fetch \
   -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

### Troubleshooting

1. **Connection Issues:**
   - Verify MongoDB is running and accessible
   - Check the MONGO_URI environment variable
   - Ensure network settings allow connections to MongoDB port

2. **Authentication Errors:**
   - Verify JWT_SECRET_KEY is set correctly
   - Check if token is expired or malformed
   - Ensure user credentials are correct

3. **Permission Denied:**
   - Verify user role has proper permissions
   - Check if JWT token includes necessary claims
   - Admin endpoints require superuser role

4. **Data Not Found:**
   - Verify collection name and document ID
   - Check if data was actually saved to database
   - MongoDB queries are case-sensitive

For additional support, check the log files in `~/.nsbm-sa-logs/log.txt` for detailed error information.
