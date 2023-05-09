package com.grantcallant.asunaspring.controllers.discord.legacy;

import com.grantcallant.asunaspring.utility.logging.Log;
import discord4j.core.event.domain.Event;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * 12 2022
 * The main inlet interface for handling Discord events.
 *
 * @author Grant Callant
 */
@Component
public interface EventListener<T extends Event>
{
  Class<T> getEventType();
  Mono<Void> execute(T event);

  default Mono<Void> handleError(Throwable error)
  {
    Log.error("Unable to process event " + getEventType().getSimpleName(), error);
    return Mono.empty();
  }
}
