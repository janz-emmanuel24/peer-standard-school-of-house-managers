from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    API Root - Overview of all available endpoints
    """
    return Response({
        'message': 'Welcome to Peer Standard School of Maids API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'login': reverse('token_obtain_pair', request=request, format=format),
                'refresh': reverse('token_refresh', request=request, format=format),
            },
            'accounts': {
                'users': reverse('user-list', request=request, format=format),
                'background_checks': reverse('backgroundcheck-list', request=request, format=format),
            },
            'courses': {
                'categories': reverse('coursecategory-list', request=request, format=format),
                'courses': reverse('course-list', request=request, format=format),
                'modules': reverse('coursemodule-list', request=request, format=format),
                'instructors': reverse('instructor-list', request=request, format=format),
                'assessments': reverse('assessment-list', request=request, format=format),
            },
            'students': {
                'students': reverse('student-list', request=request, format=format),
                'enrollments': reverse('enrollment-list', request=request, format=format),
                'attendance': reverse('attendance-list', request=request, format=format),
                'assessment_results': reverse('assessmentresult-list', request=request, format=format),
                'progress_reports': reverse('progressreport-list', request=request, format=format),
                'placements': reverse('placement-list', request=request, format=format),
            },
            'employers': {
                'employers': reverse('employer-list', request=request, format=format),
                'job_postings': reverse('jobposting-list', request=request, format=format),
                'job_applications': reverse('jobapplication-list', request=request, format=format),
                'feedback': reverse('employerfeedback-list', request=request, format=format),
                'rehire_requests': reverse('rehirerequest-list', request=request, format=format),
            },
            'certifications': {
                'templates': reverse('certificatetemplate-list', request=request, format=format),
                'certificates': reverse('certificate-list', request=request, format=format),
                'verifications': reverse('certificateverification-list', request=request, format=format),
                'accreditations': reverse('accreditation-list', request=request, format=format),
                'course_accreditations': reverse('courseaccreditation-list', request=request, format=format),
                'competency_assessments': reverse('competencyassessment-list', request=request, format=format),
            },
            'financials': {
                'tuition_fees': reverse('tuitionfee-list', request=request, format=format),
                'payments': reverse('payment-list', request=request, format=format),
                'placement_fees': reverse('placementfee-list', request=request, format=format),
                'payroll': reverse('payroll-list', request=request, format=format),
                'expenses': reverse('expense-list', request=request, format=format),
                'invoices': reverse('invoice-list', request=request, format=format),
                'reports': reverse('financialreport-list', request=request, format=format),
            }
        },
        'documentation': {
            'browsable_api': 'Add ?format=json to any endpoint for JSON response',
            'authentication': 'Use JWT tokens for authenticated requests',
            'pagination': 'All list endpoints support pagination with ?page=N',
            'filtering': 'Most endpoints support filtering and search parameters',
        }
    })
