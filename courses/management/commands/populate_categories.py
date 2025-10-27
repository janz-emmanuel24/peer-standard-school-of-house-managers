from django.core.management.base import BaseCommand
from courses.models import CourseCategory, Course
from accounts.models import User


class Command(BaseCommand):
    help = 'Populate course categories and sample courses for training programs'

    def handle(self, *args, **options):
        # Create course categories that match the training programs
        categories_data = [
            {
                'name': 'Cleaning & Maintenance',
                'description': 'Professional cleaning techniques, equipment handling, and maintenance protocols.'
            },
            {
                'name': 'Cooking & Nutrition',
                'description': 'Culinary skills, meal planning, dietary requirements, and kitchen management.'
            },
            {
                'name': 'Etiquette & Communication',
                'description': 'Professional communication, social etiquette, and client relationship management.'
            },
            {
                'name': 'Budgeting & Management',
                'description': 'Household budgeting, inventory management, and resource optimization.'
            },
            {
                'name': 'Caregiving',
                'description': 'Elderly care, child care, and specialized caregiving techniques.'
            },
            {
                'name': 'Driving & Transportation',
                'description': 'Safe driving practices, vehicle maintenance, and transportation services.'
            }
        ]

        # Create categories
        for cat_data in categories_data:
            category, created = CourseCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        # Create sample courses for each category
        sample_courses = [
            {
                'category': 'Cleaning & Maintenance',
                'courses': [
                    {
                        'title': 'Deep Cleaning Techniques',
                        'description': 'Master advanced cleaning methods for different surfaces and materials.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 2,
                        'total_hours': 20,
                        'tuition_fee': 150.00,
                        'learning_outcomes': 'Learn professional deep cleaning techniques, equipment usage, and safety protocols.'
                    },
                    {
                        'title': 'Eco-Friendly Cleaning',
                        'description': 'Sustainable cleaning practices using environmentally safe products.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 1,
                        'total_hours': 10,
                        'tuition_fee': 75.00,
                        'learning_outcomes': 'Understand eco-friendly cleaning products and sustainable practices.'
                    }
                ]
            },
            {
                'category': 'Cooking & Nutrition',
                'courses': [
                    {
                        'title': 'Basic Culinary Skills',
                        'description': 'Fundamental cooking techniques and kitchen safety.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 3,
                        'total_hours': 30,
                        'tuition_fee': 200.00,
                        'learning_outcomes': 'Master basic cooking techniques, knife skills, and kitchen safety.'
                    },
                    {
                        'title': 'Meal Planning & Nutrition',
                        'description': 'Plan balanced meals and understand nutritional requirements.',
                        'difficulty_level': 'intermediate',
                        'duration_weeks': 2,
                        'total_hours': 20,
                        'tuition_fee': 175.00,
                        'learning_outcomes': 'Learn meal planning, nutrition basics, and dietary considerations.'
                    }
                ]
            },
            {
                'category': 'Etiquette & Communication',
                'courses': [
                    {
                        'title': 'Professional Communication',
                        'description': 'Effective communication skills for domestic service professionals.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 2,
                        'total_hours': 16,
                        'tuition_fee': 120.00,
                        'learning_outcomes': 'Develop professional communication skills and client interaction techniques.'
                    },
                    {
                        'title': 'Social Etiquette',
                        'description': 'Proper etiquette for various social situations and formal events.',
                        'difficulty_level': 'intermediate',
                        'duration_weeks': 1,
                        'total_hours': 12,
                        'tuition_fee': 100.00,
                        'learning_outcomes': 'Master social etiquette and formal service protocols.'
                    }
                ]
            },
            {
                'category': 'Budgeting & Management',
                'courses': [
                    {
                        'title': 'Household Budgeting',
                        'description': 'Manage household finances and create effective budgets.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 2,
                        'total_hours': 16,
                        'tuition_fee': 125.00,
                        'learning_outcomes': 'Learn household budgeting, expense tracking, and financial planning.'
                    },
                    {
                        'title': 'Inventory Management',
                        'description': 'Efficiently manage household supplies and inventory systems.',
                        'difficulty_level': 'intermediate',
                        'duration_weeks': 1,
                        'total_hours': 10,
                        'tuition_fee': 80.00,
                        'learning_outcomes': 'Master inventory tracking, supply management, and cost optimization.'
                    }
                ]
            },
            {
                'category': 'Caregiving',
                'courses': [
                    {
                        'title': 'Elderly Care Basics',
                        'description': 'Essential care techniques for elderly family members.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 3,
                        'total_hours': 24,
                        'tuition_fee': 180.00,
                        'learning_outcomes': 'Learn elderly care techniques, safety protocols, and health monitoring.'
                    },
                    {
                        'title': 'Child Care & Safety',
                        'description': 'Safe and effective child care practices.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 2,
                        'total_hours': 20,
                        'tuition_fee': 160.00,
                        'learning_outcomes': 'Master child safety, developmental care, and emergency procedures.'
                    }
                ]
            },
            {
                'category': 'Driving & Transportation',
                'courses': [
                    {
                        'title': 'Defensive Driving',
                        'description': 'Safe driving practices and defensive driving techniques.',
                        'difficulty_level': 'beginner',
                        'duration_weeks': 1,
                        'total_hours': 8,
                        'tuition_fee': 100.00,
                        'learning_outcomes': 'Learn defensive driving techniques and safety protocols.'
                    },
                    {
                        'title': 'Vehicle Maintenance',
                        'description': 'Basic vehicle maintenance and troubleshooting.',
                        'difficulty_level': 'intermediate',
                        'duration_weeks': 1,
                        'total_hours': 12,
                        'tuition_fee': 120.00,
                        'learning_outcomes': 'Understand basic vehicle maintenance and common issues.'
                    }
                ]
            }
        ]

        # Get or create a default instructor user
        instructor_user, created = User.objects.get_or_create(
            username='instructor@example.com',
            defaults={
                'email': 'instructor@example.com',
                'first_name': 'Default',
                'last_name': 'Instructor',
                'user_type': 'instructor',
                'is_active': True
            }
        )
        if created:
            instructor_user.set_password('defaultpass123')
            instructor_user.save()

        # Create sample courses
        for category_data in sample_courses:
            try:
                category = CourseCategory.objects.get(name=category_data['category'])
                for course_data in category_data['courses']:
                    course, created = Course.objects.get_or_create(
                        title=course_data['title'],
                        category=category,
                        defaults={
                            'description': course_data['description'],
                            'difficulty_level': course_data['difficulty_level'],
                            'duration_weeks': course_data['duration_weeks'],
                            'total_hours': course_data['total_hours'],
                            'tuition_fee': course_data['tuition_fee'],
                            'status': 'active',
                            'learning_outcomes': course_data['learning_outcomes'],
                            'created_by': instructor_user
                        }
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Created course: {course.title}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Course already exists: {course.title}')
                        )
            except CourseCategory.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Category not found: {category_data["category"]}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated course categories and sample courses!')
        )
