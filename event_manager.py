"""Event Management System.

Author: Amar Patil
SRN: PES1UG24AM031
Course: Software Engineering (Lab 5: Static Code Analysis)
"""

from datetime import date
import json
import secrets
import subprocess  # nosec B404

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create a new event with specified venue, capacity, and guest list."""
    if guests is None:
        guests = []
    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": list(guests),
    }
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest for an event if seats are available."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of remaining seats available for an event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Determine whether an event date is upcoming or completed."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order="asc"):
    """Return a comma-separated string of registered guests sorted by order."""
    reverse = sort_order.lower() == "desc"
    names = sorted(events[event_name]["guests"], reverse=reverse)
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save all registered events to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


def load_events(file_name="events.json"):
    """Load event records from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


def print_badges(event_name):
    """Mock helper to print badges using a safe subprocess call."""
    cmd = ["/usr/bin/lp", f"badges_{event_name}.txt"]
    subprocess.run(cmd, check=False)  # nosec B603


def main():
    """Run the demonstration workflow for the event management system."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "asc"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = secrets.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events()  # reload to confirm the save worked
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])


if __name__ == "__main__":
    main()
