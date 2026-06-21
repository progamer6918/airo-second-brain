"""Google Calendar adapter placeholder.

No real calendar event is created in this phase.
"""

class GoogleCalendarAdapter:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def create_due_reminder(self, title: str, due_date: str) -> dict:
        return {
            "adapter": "calendar",
            "title": title,
            "due_date": due_date,
            "dry_run": self.dry_run,
            "status": "planned",
        }
