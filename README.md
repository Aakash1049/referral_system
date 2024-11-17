API Endpoints
1. User Registration
Endpoint: POST /api/register/

Description: Register a new user and generate a referral code.

Request Body:

json
Copy code
{
  "email": "user@example.com",
  "name": "John Doe",
  "mobile_number": "1234567890",
  "city": "New York",
  "referral_code": "xPEQ1pyj3f",  // Optional, if provided, must be valid
  "password": "password123"
}
Response:

Success (201 Created):
json
Copy code
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "mobile_number": "1234567890",
  "city": "New York",
  "referral_code": "ABCD1234",
  "referrer": null
}
Error (400 Bad Request):
json
Copy code
{
  "email": ["This field is required."],
  "name": ["This field is required."],
  "mobile_number": ["This field is required."],
  "city": ["This field is required."],
  "password": ["This field is required."]
}
2. User Login
Endpoint: POST /api/login/

Description: Login a user using email and password.

Request Body:

json
Copy code
{
  "email": "user@example.com",
  "password": "password123"
}
Response:

Success (200 OK):
json
Copy code
{
  "message": "Login successful",
  "user_id": 1,
  "email": "user@example.com"
}
Error (400 Bad Request):
json
Copy code
{
  "error": "Invalid credentials"
}
3. Referral List
Endpoint: GET /api/referral/

Description: Get the list of users who registered using your referral code.

Headers:

Authorization: Bearer <JWT_TOKEN> (You need to authenticate as a logged-in user)
Response:

Success (200 OK):
json
Copy code
[
  {
    "id": 2,
    "email": "referee1@example.com",
    "name": "Referee One",
    "registration_date": "2024-11-10T14:23:00"
  },
  {
    "id": 3,
    "email": "referee2@example.com",
    "name": "Referee Two",
    "registration_date": "2024-11-11T16:30:00"
  }
]
Error (Unauthorized - 401):
json
Copy code
{
  "error": "Authentication credentials were not provided."
}
Authentication
Login provides an API that returns a successful login message and a user_id.
Use the user_id and email to authenticate requests for the Referral API via a JWT Token or session management.
Make sure to include Authorization: Bearer <JWT_TOKEN> in the headers when calling the Referral List API.
Additional Notes
Referral Code: The referral code is optional during registration, but if provided, it must be valid (i.e., it should match a referral code of an existing user).
Password: Make sure the password is sufficiently strong. The password is hashed using Django's default password hashing algorithm before storing it in the database.
Testing the API
1. Test the Register API
Use Postman to test the registration API:

Set the request type to POST.
Use the URL: http://localhost:8000/api/register/.
Include the appropriate request body (as shown above) in JSON format.
2. Test the Login API
Use Postman to test the login API:

Set the request type to POST.
Use the URL: http://localhost:8000/api/login/.
Include the appropriate request body (as shown above) in JSON format.
3. Test the Referral API
Once logged in, test the referral API:

Set the request type to GET.
Use the URL: http://localhost:8000/api/referral/.
Add the Authorization header with the JWT token you received after logging in.
Future Improvements
JWT Authentication: Implement JWT token authentication for better security and session management.
Enhanced Error Handling: Improve error messages and validation for better user experience.
Admin Panel: Set up an admin panel to manage users and referral codes.
License
This project is licensed under the MIT License - see the LICENSE file for details.

