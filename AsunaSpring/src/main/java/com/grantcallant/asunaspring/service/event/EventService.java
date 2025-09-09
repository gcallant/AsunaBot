package com.grantcallant.asunaspring.service.event;

import com.grantcallant.asunaspring.repository.event.EventRepository;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.repository.event.model.EventDatum;
import com.grantcallant.asunaspring.repository.event.model.EventRoster;
import com.grantcallant.asunaspring.repository.event.model.QEvent;
import com.grantcallant.asunaspring.utility.helpers.LocalizedResponses;
import com.grantcallant.asunaspring.utility.helpers.ServiceResult;
import com.querydsl.core.types.dsl.BooleanExpression;
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
    QEvent event = QEvent.event;
    BooleanExpression thisEvent = event.guild.id.eq(guildId);
    List<Event> eventList = (List<Event>) eventRepository.findAll(thisEvent);
    
    // Empty list is still a successful result, just with no data found
    return new ServiceResult.ServiceResultBuilder<List<Event>>()
        .success()
        .data(eventList)
        .message(eventList.isEmpty() ? LocalizedResponses.NO_EVENT.toString() : null)
        .build();
  }

  public ServiceResult<Event> createNewEvent(String eventName, final String eventTypeName, final UUID guildId, final EventRoster newEventRoster,
                                             final EventDatum newEventData)
  {
    Event event = new Event();
    event.setEventName(eventName);
    return new ServiceResult.ServiceResultBuilder<Event>().success().data(eventRepository.save(event)).build();
  }
}
