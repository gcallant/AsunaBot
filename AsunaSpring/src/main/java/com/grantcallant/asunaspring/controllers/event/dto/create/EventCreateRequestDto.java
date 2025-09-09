package com.grantcallant.asunaspring.controllers.event.dto.create;

import java.util.Map;
import java.util.UUID;

public class EventCreateRequestDto
{
  public String eventName;
  public String eventType;
  public UUID guildId;
  public Map<String, Object> eventRoster;
  public Map<String, Object> eventData;
}
