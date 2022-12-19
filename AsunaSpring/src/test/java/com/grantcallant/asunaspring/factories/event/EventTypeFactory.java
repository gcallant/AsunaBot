package com.grantcallant.asunaspring.factories.event;

import com.grantcallant.asunaspring.repository.event.model.EventType;

import java.util.Random;
import java.util.UUID;

/**
 * Factory for creating event types when testing.
 */
public record EventTypeFactory()
{
  private static final String[] eventTypeArray = {"Dungeon", "Trial", "Furniture", "Trivia"};

  public static EventType createEventType()
  {
    EventType eventType = new EventType();
    eventType.setId(UUID.randomUUID());
    eventType.setEventTypeName(eventTypeArray[new Random().nextInt(3)]);
    return eventType;
  }
}
