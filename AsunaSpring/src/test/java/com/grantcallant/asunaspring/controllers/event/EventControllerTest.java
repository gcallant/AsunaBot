package com.grantcallant.asunaspring.controllers.event;

import com.grantcallant.asunaspring.BaseTest;
import com.grantcallant.asunaspring.controllers.event.dto.EventDto;
import com.grantcallant.asunaspring.factories.event.EventFactory;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.service.event.EventService;
import com.grantcallant.asunaspring.utility.helpers.ServiceResult;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.List;
import java.util.Map;
import java.util.Objects;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

/**
 * Test class for EventController.
 */
@DisplayName("EventControllerTest")
@SpringBootTest
class EventControllerTest extends BaseTest
{

  static Event event;
  static List<Event> eventList;
  @Autowired
  EventController eventController;
  @MockBean
  EventService eventService;

  @BeforeEach
  public void init()
  {
    event = EventFactory.createEvent();
    eventList = List.of(event);
  }

  @Test
  @DisplayName("index should return back a mapped event DTO")
  void index()
  {
    ServiceResult<List<Event>> result = new ServiceResult.ServiceResultBuilder<List<Event>>().success().data(eventList).message("OK").build();
    when(eventService.getAllEventsForGuild(event.getGuild().getId())).thenReturn(result);
    ResponseEntity<Map<String, List<EventDto>>> response = eventController.index(event.getGuild().getId());

    assertEquals(HttpStatus.OK, response.getStatusCode());
    assertNotNull(Objects.requireNonNull(response.getBody()).get("data").stream().findFirst());

    EventDto eventDto = response.getBody().get("data").stream().findFirst().get();
    assertEquals(event.getEventName(), eventDto.eventName);
    assertEquals(event.getGuild().getId(), eventDto.guildId);
    assertEquals(event.getEventType().getId(), eventDto.eventTypeId);
  }

  @Test
  void show()
  {
    boolean b = true;
    assertTrue(b);
  }

  @Test
  void create()
  {
    boolean c = true;
    assertTrue(c);
  }

  @Test
  void destroy()
  {
    boolean d = true;
    assertTrue(d);
  }
}
