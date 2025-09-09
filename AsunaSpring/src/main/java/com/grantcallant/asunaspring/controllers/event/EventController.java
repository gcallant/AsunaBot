package com.grantcallant.asunaspring.controllers.event;

import com.grantcallant.asunaspring.controllers.event.dto.EventResponseDto;
import com.grantcallant.asunaspring.controllers.event.dto.create.EventCreateRequestDto;
import com.grantcallant.asunaspring.controllers.event.dto.create.EventCreateResponseDto;
import com.grantcallant.asunaspring.controllers.event.dto.index.EventIndexRequestDto;
import com.grantcallant.asunaspring.controllers.event.dto.index.EventIndexResponseDto;
import com.grantcallant.asunaspring.repository.event.model.Event;
import com.grantcallant.asunaspring.repository.event.model.EventDatum;
import com.grantcallant.asunaspring.repository.event.model.EventRoster;
import com.grantcallant.asunaspring.repository.guild.model.Guild;
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
import org.springframework.util.StopWatch;
import org.springframework.web.bind.annotation.*;

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

  @Autowired public EventController(ModelMapper mapper, EventService eventService)
  {
    this.mapper = mapper;
    this.eventService = eventService;
  }

  @GetMapping("") public <T> ResponseEntity<Map<String, T>> index(@PathVariable EventIndexRequestDto requestDto)
  {
    StopWatch stopWatch = new StopWatch();
    stopWatch.start();
    try
    {
      //TODO: Get User and guild info from context object
//      UUID guildId = Context.getGuildId;
      Guild guild = mapper.map(requestDto, Guild.class);

      ServiceResult<List<EventIndexResponseDto>> mappedResult = eventService.getAllEventsForGuild(guild.getId()).mapOrDefault(
          events -> StreamHelper.mapList(events, EventIndexResponseDto.class, mapper), List.<EventIndexResponseDto>of());

      if (mappedResult.isFailed())
      {
        return ResponseHelper.failedResponse(mappedResult.getMessage(), (T) mappedResult.getData());
      }
      return ResponseHelper.successfulDataResponse(mappedResult.getMessage(), (T) mappedResult.getData());
    }
    catch (Exception exception)
    {
      Log.error(exception);
      return ResponseHelper.failedResponse(LocalizedResponses.NO_EVENT.key(), (T) List.<EventIndexResponseDto>of());
    }
    finally
    {
      stopWatch.stop();
      //TODO log command execution time and info
    }
  }

  @GetMapping("/{id}") public ResponseEntity<Map<String, EventResponseDto>> show(@PathVariable UUID id)
  {
    return null;
  }

  @PostMapping("")
  public ResponseEntity<Map<String, EventCreateResponseDto>> create(@RequestBody EventCreateRequestDto eventCreateRequestDto)
  {
    StopWatch stopWatch = new StopWatch();
    stopWatch.start();

    try
    {
      //TODO Validate input newb- param validators like rails?
      EventRoster newEventRoster = mapper.map(eventCreateRequestDto.eventRoster, EventRoster.class);
      EventDatum newEventData = mapper.map(eventCreateRequestDto.eventData, EventDatum.class);

      ServiceResult<Event> serviceResult = eventService.createNewEvent(eventCreateRequestDto.eventName, eventCreateRequestDto.eventType,
          eventCreateRequestDto.guildId, newEventRoster, newEventData);

      EventCreateResponseDto responseDto = mapper.map(serviceResult.getData(), EventCreateResponseDto.class);


      if (serviceResult.isFailed())
      {
        return ResponseHelper.failedResponse(serviceResult.getMessage(), null);
      }

      return ResponseHelper.successfulDataResponse(serviceResult.getMessage(), responseDto);
    }
    catch (Exception e)
    {
      return ResponseHelper.failedResponse(LocalizedResponses.BAD_PARAMS.toString(), null);
    }
    finally
    {
      stopWatch.stop();
      //TODO log command execution time and info
    }
  }

  @DeleteMapping("/{id}") public ResponseEntity<Map<String, EventResponseDto>> destroy(@PathVariable UUID id)
  {
    return null;
  }
}
