package com.grantcallant.asunaspring.service.event;

import com.grantcallant.asunaspring.repository.event.EventRepository;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.utility.helpers.ServiceResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

/**
 * Manages the service layer for events.
 */
@Service
public class EventService
{
  private final EventRepository eventRepository;

  @Autowired
  public EventService(EventRepository eventRepository) {this.eventRepository = eventRepository;}

  public ServiceResult<List<Event>> getAllEventsForGuild(UUID guildId)
  {
    //TODO: Actually get data from repo
    return new ServiceResult.ServiceResultBuilder<List<Event>>().success().build();
  }
}
