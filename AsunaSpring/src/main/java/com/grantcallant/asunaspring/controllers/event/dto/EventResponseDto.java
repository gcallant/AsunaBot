package com.grantcallant.asunaspring.controllers.event.dto;

import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.repository.event.model.EventType;
import com.grantcallant.asunaspring.repository.guild.model.Guild;

/**
 * A DTO object for events.
 */
public class EventResponseDto
{
  public Event event;
  public EventType eventType;
  public Guild guild;
}
