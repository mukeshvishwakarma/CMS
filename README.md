Setup Instructions

Clone the Repository:

:-git clone https://github.com/mukeshvishwakarma/CMS
 cd cms_app
Technologies Used

Django Django REST Framework rest_framework_simplejwt

APIs and Endpoints

Register User URL: /api/register/ Method: POST Description: Endpoint for registering a new user. Parameters: { "username": "testuser11", "email": "testuser11@example.com", "password": "TestPass123", "full_name": "Test User", "phone": "1234567890", "address": "123 Test St", "city": "Testville", "state": "Test State", "country": "Test Country", "pincode": "123456" }

User Login URL: /api/login/ Method: POST Description: Endpoint for user authentication and obtaining JWT tokens. Parameters: { "email": "testuser11@example.com", "password": "TestPass123", "username": "testuser11" }

Content Management List and Create Content Items URL: /api/contents/ Method: GET, POST Description: Endpoint for listing all content items or creating a new content item. Authentication: Required (JWT token) Retrieve, Update, and Delete Content Item

URL: /api/contents// Method: GET, PUT, DELETE Description: Endpoint for retrieving, updating, or deleting a specific content item. Authentication: Required (JWT token) Search Content Items

URL: /api/contents/search/ Method: GET Description: Endpoint for searching content items based on a query string. Parameters: query (string) Authentication: Required (JWT token)
