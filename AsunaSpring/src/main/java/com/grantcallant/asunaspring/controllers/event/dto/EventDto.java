package com.grantcallant.asunaspring.controllers.event.dto;

import java.util.UUID;

/**
 * A DTO object for events.
 */
public class EventDto
{
  public UUID id;
  public String eventName;
  public UUID eventTypeId;
  public UUID guildId;
}
