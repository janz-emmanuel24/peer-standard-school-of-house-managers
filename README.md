# Peer Standard School of Maids

A comprehensive Django web application for managing a professional training school for domestic services. This system provides complete management of students, courses, employers, certifications, and financial operations.

## Features

### 🎓 Training Management
- **Modular Course System**: Create and manage comprehensive training programs
- **Course Categories**: Organize courses by type (Cleaning, Cooking, Etiquette, Budgeting, Caregiving, Driving)
- **Assessment System**: Quizzes, practicals, attendance tracking, and evaluations
- **Instructor Management**: Assign instructors to courses with specialization tracking

### 👥 Student Management
- **Student Profiles**: Comprehensive student information and progress tracking
- **Enrollment System**: Digital and physical admission channels
- **Progress Reports**: Detailed tracking of student performance and attendance
- **Placement History**: Track job placements and career progression

### 🏢 Employer Portal
- **Job Posting System**: Employers can post job requirements and select candidates
- **Matching System**: Automated matching of certified graduates to job requirements
- **Background Verification**: Comprehensive safety checks for all parties
- **Feedback System**: Rating, review, and rehire capabilities

### 🏆 Certification System
- **Auto-Generated Certificates**: System generates certificates upon course completion
- **Verification System**: Public certificate verification with unique codes
- **Accreditation Management**: Track institutional accreditations and standards
- **Competency Assessments**: Continuous performance monitoring and re-training

### 💰 Financial Management
- **Tuition Tracking**: Comprehensive fee management per student
- **Placement Commissions**: Manage employer placement fees
- **Payroll System**: Instructor and staff salary management
- **Invoice Generation**: Automated billing and expense tracking
- **Financial Reports**: Detailed analytics and reporting

### 📊 Admin Dashboard
- **KPI Monitoring**: Placement rates, course completion rates, revenue tracking
- **System Analytics**: Comprehensive reporting for accreditation bodies
- **User Management**: Role-based access control for different user types
- **Audit Trail**: Complete system activity logging

## Technology Stack

- **Backend**: Django 5.2.7
- **API**: Django REST Framework (DRF) with JWT Authentication
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Tailwind CSS, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication with custom user model + JWT tokens
- **Admin Interface**: Django Admin with custom configurations
- **Forms**: Django Crispy Forms with Tailwind CSS styling
- **CORS**: django-cors-headers for cross-origin requests

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd peer-standard-school
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .env
   source .env/bin/activate  # On Windows: .env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers pillow python-decouple django-crispy-forms crispy-bootstrap5 django-widget-tweaks
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data (optional)**
   ```bash
   python manage.py populate_categories
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - API Documentation: http://127.0.0.1:8000/api/docs/
   - API Root: http://127.0.0.1:8000/api/

## Django REST Framework (DRF) API

### API Overview

The application provides a comprehensive REST API built with Django REST Framework, featuring JWT authentication and role-based permissions.

### API Endpoints

#### Authentication Endpoints
- `POST /api/token/` - Obtain JWT access token
- `POST /api/token/refresh/` - Refresh JWT access token

#### User Management
- `GET /api/accounts/users/` - List all users (admin only)
- `POST /api/accounts/users/` - Create new user
- `GET /api/accounts/users/{id}/` - Get user details
- `PUT /api/accounts/users/{id}/` - Update user
- `DELETE /api/accounts/users/{id}/` - Delete user

#### Course Management
- `GET /api/courses/courses/` - List all courses
- `POST /api/courses/courses/` - Create course (instructor/admin)
- `GET /api/courses/courses/{id}/` - Get course details
- `PUT /api/courses/courses/{id}/` - Update course
- `DELETE /api/courses/courses/{id}/` - Delete course
- `GET /api/courses/categories/` - List course categories

#### Student Management
- `GET /api/students/students/` - List students (admin/instructor)
- `POST /api/students/students/` - Create student profile
- `GET /api/students/students/{id}/` - Get student details
- `PUT /api/students/students/{id}/` - Update student
- `GET /api/students/enrollments/` - List enrollments

#### Employer Management
- `GET /api/employers/employers/` - List employers (admin)
- `POST /api/employers/employers/` - Create employer profile
- `GET /api/employers/employers/{id}/` - Get employer details
- `GET /api/employers/jobs/` - List job postings

#### Financial Management
- `GET /api/financials/payments/` - List payments (admin)
- `POST /api/financials/payments/` - Create payment record
- `GET /api/financials/reports/` - Financial reports (admin)

### Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. **Obtain Access Token**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "your-email@example.com", "password": "your-password"}'
   ```

2. **Use Token in Requests**
   ```bash
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://127.0.0.1:8000/api/courses/courses/
   ```

3. **Refresh Token**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
   ```

### API Usage Examples

#### Get All Courses (Public)
```bash
curl http://127.0.0.1:8000/api/courses/courses/
```

#### Create a New Course (Authenticated)
```bash
curl -X POST http://127.0.0.1:8000/api/courses/courses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Cleaning Techniques",
    "description": "Learn advanced cleaning methods",
    "difficulty_level": "intermediate",
    "duration_weeks": 4,
    "total_hours": 40,
    "tuition_fee": "300.00",
    "status": "active"
  }'
```

#### Get Student Details
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/students/students/1/
```

#### List Job Postings
```bash
curl http://127.0.0.1:8000/api/employers/jobs/
```

### API Response Format

All API responses follow a consistent format:

#### Success Response
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/courses/courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Course Title",
      "description": "Course description",
      "difficulty_level": "beginner",
      "duration_weeks": 4,
      "total_hours": 40,
      "tuition_fee": "250.00",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Error Response
```json
{
  "error": "Authentication credentials were not provided.",
  "detail": "Authentication credentials were not provided."
}
```

### Rate Limiting

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Admin users**: Unlimited requests

### CORS Configuration

The API supports cross-origin requests from:
- `http://localhost:3000` (React development)
- `http://127.0.0.1:3000`
- `http://localhost:8080` (Vue development)
- `http://127.0.0.1:8080`

### Testing the API

#### Using curl
```bash
# Test authentication
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Test protected endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/courses/courses/
```

#### Using Python requests
```python
import requests

# Get token
response = requests.post('http://127.0.0.1:8000/api/token/', json={
    'email': 'admin@example.com',
    'password': 'admin123'
})
token = response.json()['access']

# Use token
headers = {'Authorization': f'Bearer {token}'}
courses = requests.get('http://127.0.0.1:8000/api/courses/courses/', headers=headers)
print(courses.json())
```

#### Using JavaScript/Fetch
```javascript
// Get token
const tokenResponse = await fetch('http://127.0.0.1:8000/api/token/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'admin@example.com',
    password: 'admin123'
  })
});
const { access } = await tokenResponse.json();

// Use token
const coursesResponse = await fetch('http://127.0.0.1:8000/api/courses/courses/', {
  headers: {
    'Authorization': `Bearer ${access}`
  }
});
const courses = await coursesResponse.json();
```

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/docs/redoc/

### Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## User Types

### 👨‍💼 Administrator
- Full system access
- User management
- Financial oversight
- System configuration
- Reports and analytics

### 👨‍🏫 Instructor
- Course management
- Student progress tracking
- Assessment grading
- Attendance management

### 👩‍🎓 Student
- Course enrollment
- Progress tracking
- Certificate access
- Job application

### 🏢 Employer
- Job posting
- Candidate selection
- Feedback submission
- Rehire requests

## Database Schema

### Core Models
- **User**: Extended user model with role-based permissions
- **Student**: Student profiles and academic information
- **Course**: Training programs and modules
- **Employer**: Company profiles and job postings
- **Certificate**: Generated certifications and verification
- **Payment**: Financial transactions and billing

### Key Relationships
- Students enroll in Courses
- Courses have multiple Modules and Assessments
- Employers post Jobs and hire Students
- Students receive Certificates upon completion
- All activities are tracked for audit purposes

## API Endpoints

The system includes comprehensive REST API endpoints built with Django REST Framework. See the [Django REST Framework (DRF) API](#django-rest-framework-drf-api) section above for detailed documentation, authentication, and usage examples.

Key API areas include:
- User authentication and management
- Course enrollment and progress
- Job posting and applications
- Certificate generation and verification
- Financial reporting and analytics

## Security Features

- **Role-based Access Control**: Different permissions for different user types
- **Background Verification**: Comprehensive safety checks
- **Audit Logging**: Complete activity tracking
- **Data Encryption**: Sensitive information protection
- **Session Management**: Secure user sessions

## Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email settings
5. Set up SSL/HTTPS
6. Configure proper logging

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@peerstandardschool.com
- Documentation: [Link to documentation]
- Issues: [GitHub Issues]

## Roadmap

### Phase 1 (Current)
- ✅ Core system implementation
- ✅ User management and authentication
- ✅ Course and student management
- ✅ Basic employer portal

### Phase 2 (Planned)
- 📱 Mobile application
- 🔔 Advanced notification system
- 📈 Enhanced analytics dashboard
- 🌐 Multi-language support

### Phase 3 (Future)
- 🤖 AI-powered job matching
- 📊 Advanced reporting and BI
- 🔗 Third-party integrations
- ☁️ Cloud deployment options

---

**Peer Standard School of Maids** - Professional training for domestic excellence.
