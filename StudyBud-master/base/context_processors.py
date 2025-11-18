from datetime import date
from django.db.models import Q
from .models import Announcement

def upcoming_events(request):
    if request.user.is_authenticated:
        today = date.today()
        # Get events from today onwards
        upcoming = Announcement.objects.filter(
            event_date__gte=today
        ).order_by('event_date')[:5]  # Show next 5 events
        return {'upcoming_events': upcoming}
    return {'upcoming_events': []}