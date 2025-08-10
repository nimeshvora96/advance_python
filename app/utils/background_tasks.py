import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_enrollment_email(student_email: str, teacher_name: str, student_name: str):
    """
    Simulate sending enrollment email
    In production, this would integrate with email service like SendGrid, AWS SES, etc.
    """
    logger.info(f"📧 EMAIL NOTIFICATION")
    logger.info(f"To: {student_email}")
    logger.info(f"Subject: Enrollment Confirmation")
    logger.info(f"Message: Dear {student_name}, you have been successfully enrolled with teacher {teacher_name}")
    logger.info(f"Sent at: {datetime.now()}")
    logger.info("=" * 50)