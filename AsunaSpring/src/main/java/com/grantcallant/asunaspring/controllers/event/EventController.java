package com.grantcallant.asunaspring.controllers.event;

import com.grantcallant.asunaspring.controllers.event.dto.EventDto;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.service.event.EventService;
import com.grantcallant.asunaspring.utility.helpers.ResponseHelper;
import com.grantcallant.asunaspring.utility.helpers.ServiceResult;
import com.grantcallant.asunaspring.utility.helpers.StreamHelper;
import com.grantcallant.asunaspring.utility.logging.Log;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Controls the endpoints responsible for creating and editing events.
 */
@RestController
@RequestMapping(value = "/api/v1/event", produces = "application/json")
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
  public ResponseEntity<Map<String, List<EventDto>>> index()
  {
    try
    {
      //TODO: Get User and guild info from context object
      UUID guildId = null;
      ServiceResult<List<Event>> serviceResult = eventService.getAllEventsForGuild(guildId);

      if (serviceResult.isSuccess())
      {
        return ResponseHelper.successfulResponse(serviceResult.getMessage(), StreamHelper.mapList(serviceResult.getData(), EventDto.class, mapper));
      }
      return ResponseHelper.failedResponse(serviceResult.getMessage(), new ArrayList<>());
    }
    catch (Exception exception)
    {
      Log.error(exception);
      throw exception;
    }
  }
}
