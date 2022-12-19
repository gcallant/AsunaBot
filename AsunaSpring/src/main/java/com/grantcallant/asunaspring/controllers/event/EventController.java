package com.grantcallant.asunaspring.controllers.event;

import com.grantcallant.asunaspring.controllers.event.dto.EventDto;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.service.event.EventService;
import com.grantcallant.asunaspring.utility.helpers.LocalizedResponses;
import com.grantcallant.asunaspring.utility.helpers.ResponseHelper;
import com.grantcallant.asunaspring.utility.helpers.ServiceResult;
import com.grantcallant.asunaspring.utility.helpers.StreamHelper;
import com.grantcallant.asunaspring.utility.logging.Log;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Controls the endpoints responsible for creating and editing events.
 */
@RestController
@RequestMapping(value = "/api/v1/event", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
public class EventController
{
  private final ModelMapper mapper;
  private final EventService eventService;

  @Autowired
  public EventController(ModelMapper mapper, EventService eventService)
  {
    this.mapper = mapper;
    this.eventService = eventService;
  }

  @GetMapping("")
  public ResponseEntity<Map<String, List<EventDto>>> index(UUID guildId)
  {
    try
    {
      //TODO: Get User and guild info from context object
//      UUID guildId = Context.getGuildId;
      ServiceResult<List<Event>> serviceResult = eventService.getAllEventsForGuild(guildId);
      return ResponseHelper.successfulDataResponse(serviceResult.getMessage(), StreamHelper.mapList(serviceResult.getData(), EventDto.class, mapper));
    } catch (Exception exception)
    {
      Log.error(exception);
      return ResponseHelper.failedResponse(LocalizedResponses.NO_EVENT.key(), new ArrayList<>());
    }
  }

  @GetMapping("/{id}")
  public ResponseEntity<Map<String, EventDto>> show(@PathVariable UUID id)
  {
    return null;
  }

  @PostMapping("/create")
  public ResponseEntity<Map<String, EventDto>> create()
  {
    return null;
  }

  @DeleteMapping("/{id}")
  public ResponseEntity<Map<String, EventDto>> destroy(@PathVariable UUID id)
  {
    return null;
  }
}
