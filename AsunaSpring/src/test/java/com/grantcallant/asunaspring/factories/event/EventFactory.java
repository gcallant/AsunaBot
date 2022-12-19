package com.grantcallant.asunaspring.factories.event;

import com.grantcallant.asunaspring.factories.guild.GuildFactory;
import com.grantcallant.asunaspring.repository.event.model.Event;
import net.bytebuddy.utility.RandomString;

import java.util.UUID;

/**
 * Creates Events for testing.
 */
public record EventFactory()
{
  public static Event createEvent()
  {
    Event event = new Event();
    event.setId(UUID.randomUUID());
    event.setEventName(RandomString.make());
    event.setEventType(EventTypeFactory.createEventType());
    event.setGuild(GuildFactory.createGuild());
    return event;
  }
}
