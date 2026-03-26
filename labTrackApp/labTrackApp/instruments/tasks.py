# labTrackApp/instruments/tasks.py
import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)

@shared_task
def process_maintenance_reminder(instrument_model, due_date):
    """
    Simulates a long-running task, like generating a reminder email
    or updating a status based on a due date.
    """
    now = timezone.now()
    logger.info(f"--- CELERY TASK STARTED ---")
    logger.info(f"Processing reminder for {instrument_model} due on {due_date}")

    # In a real app, this would be where:
    # Look up user emails
    # Connect to an external API
    # Perform a complex calculation

    logger.info(f"Task finished at {now}. Reminder processed.")
    return f"Reminder for {instrument_model} processed successfully."