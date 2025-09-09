package com.grantcallant.asunaspring.controllers.event;

import com.grantcallant.asunaspring.BaseTest;
import com.grantcallant.asunaspring.controllers.event.dto.create.EventCreateRequestDto;
import com.grantcallant.asunaspring.controllers.event.dto.create.EventCreateResponseDto;
import com.grantcallant.asunaspring.controllers.event.dto.index.EventIndexRequestDto;
import com.grantcallant.asunaspring.controllers.event.dto.index.EventIndexResponseDto;
import com.grantcallant.asunaspring.factories.event.EventDatumFactory;
import com.grantcallant.asunaspring.factories.event.EventFactory;
import com.grantcallant.asunaspring.factories.event.EventRosterFactory;
import com.grantcallant.asunaspring.factories.guild.GuildFactory;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.repository.event.model.EventDatum;
import com.grantcallant.asunaspring.repository.event.model.EventRoster;
import com.grantcallant.asunaspring.repository.guild.model.Guild;
import com.grantcallant.asunaspring.service.event.EventService;
import com.grantcallant.asunaspring.utility.helpers.LocalizedResponses;
import com.grantcallant.asunaspring.utility.helpers.ServiceResult;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

/**
 * Test class for EventController.
 */
@DisplayName("EventControllerTest")
class EventControllerTest extends BaseTest
{

  static Event eventMock;
  static List<Event> eventListMock;
  @Autowired
  EventController eventController;
  @MockitoBean
  EventService eventService;

  @BeforeEach
  public void init()
  {
    eventMock = EventFactory.createEvent();
    eventListMock = List.of(eventMock);
  }

  @Test
  @DisplayName("index should return back a mapped event DTO")
  void indexSuccess()
  {
    ServiceResult<List<Event>> result = new ServiceResult.ServiceResultBuilder<List<Event>>().success().data(eventListMock).message("OK").build();
    when(eventService.getAllEventsForGuild(eventMock.getGuild().getId())).thenReturn(result);
    EventIndexRequestDto requestDto = modelMapper.map(eventMock.getGuild().getId(), EventIndexRequestDto.class);
    ResponseEntity<Map<String, List<EventIndexResponseDto>>>response = eventController.index(requestDto);

    assertEquals(HttpStatus.OK, response.getStatusCode());
    assertNotNull(Objects.requireNonNull(response.getBody()).get("data").stream().findFirst());

    EventIndexResponseDto eventResponseDto = response.getBody().get("data").stream().findFirst().get();

    Event event = modelMapper.map(eventResponseDto, Event.class);

    assertEquals(eventMock.getId(), event.getId());
    assertEquals(eventMock.getEventName(), event.getEventName());
    assertEquals(eventMock.getGuild().getId(), event.getGuild().getId());
  }

  @Test
  @DisplayName("index should return no events found if guild has no events")
  void indexNoEventsFound()
  {
    ServiceResult<List<Event>> result = new ServiceResult.ServiceResultBuilder<List<Event>>().success().data(eventListMock).message("OK")
                                                                                             .build();
    when(eventService.getAllEventsForGuild(eventMock.getGuild().getId())).thenReturn(result);

    Guild withoutEventsGuild = GuildFactory.createGuild();

    EventIndexRequestDto requestDto = modelMapper.map(modelMapper.map(withoutEventsGuild, Guild.class), EventIndexRequestDto.class);
    ResponseEntity<Map<String, List<EventIndexResponseDto>>> response = eventController.index(requestDto);

    assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    assertNotNull(Objects.requireNonNull(response.getBody()).get("data").stream().findFirst());

    List<EventIndexResponseDto> eventResponseDto = response.getBody().get("data").stream().toList();

    assertEquals(List.of(), eventResponseDto);
  }

  @Test
  void show()
  {
    boolean b = true;
    assertTrue(b);
  }

  @Test
  void createSuccess()
  {
    String eventName = eventMock.getEventName();
    String eventType = eventMock.getEventType().getEventTypeName();
    UUID guildId = eventMock.getGuild().getId();
    EventRoster eventRoster = EventRosterFactory.createEventRoster();
    EventDatum eventDatum = EventDatumFactory.createEventDatum();
    
    eventMock.setEventRoster(eventRoster);
    eventMock.setEventDatum(eventDatum);
    
    ServiceResult<Event> result = new ServiceResult.ServiceResultBuilder<Event>().success().data(eventMock).message("OK").build();

    when(eventService.createNewEvent(eventName, eventType, guildId, eventRoster, eventDatum)).thenReturn(result);

    ResponseEntity<Map<String, EventCreateResponseDto>> response = eventController.create(
        modelMapper.map(eventMock, EventCreateRequestDto.class));
  }

  @Test
  void createFailure()
  {
    String eventName = eventMock.getEventName();
    String eventType = eventMock.getEventType().getEventTypeName();
    UUID guildId = eventMock.getGuild().getId();
    EventRoster eventRoster = EventRosterFactory.createEventRoster();
    EventDatum eventDatum = EventDatumFactory.createEventDatum();

    eventMock.setEventRoster(eventRoster);
    eventMock.setEventDatum(eventDatum);
    
    ServiceResult<Event> result = new ServiceResult.ServiceResultBuilder<Event>().failed().message("Failed to create event").build();
    
    when(eventService.createNewEvent(eventName, eventType, guildId, eventRoster, eventDatum)).thenReturn(result);

    ResponseEntity<Map<String, EventCreateResponseDto>> response = eventController.create(
        modelMapper.map(eventMock, EventCreateRequestDto.class));

    assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    assertEquals(LocalizedResponses.BAD_PARAMS.toString(), Objects.requireNonNull(response.getBody()).get("message"));
    assertNull(response.getBody().get("data"));
  }

  @Test
  void destroy()
  {
    boolean d = true;
    assertTrue(d);
  }
}
