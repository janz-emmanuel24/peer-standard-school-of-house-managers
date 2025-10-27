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
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication with custom user model
- **Admin Interface**: Django Admin with custom configurations
- **Forms**: Django Crispy Forms with Bootstrap 5 styling

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
   pip install django djangorestframework pillow python-decouple django-crispy-forms crispy-bootstrap5
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

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Default admin credentials: admin / admin123

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

The system includes REST API endpoints for:
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
