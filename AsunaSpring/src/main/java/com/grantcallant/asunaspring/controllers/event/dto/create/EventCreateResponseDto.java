package com.grantcallant.asunaspring.controllers.event.dto.create;

import java.util.Map;

public class EventCreateResponseDto
{
  public String eventId;
  public String eventType;
  public String guildId;
  public Map<String, Object> eventRoster;
  public Map<String, Object> eventData;
}
