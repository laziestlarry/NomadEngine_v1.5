from events.event_bus import EventBus

bus = EventBus()

bus.publish(
    "system_test",
    {"msg": "Nomad Test Event"},
    category="system",
)

print("Event emitted.")