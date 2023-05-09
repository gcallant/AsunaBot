package com.grantcallant.asunaspring.controllers.discord.legacy;

import discord4j.core.event.domain.message.MessageUpdateEvent;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

/**
 * 12 2022
 * Listens for updated messages.
 *
 * @author Grant Callant
 */
@Service
public class MessageUpdateListener implements MessageListener, EventListener<MessageUpdateEvent>
{
  @Override
  public Class<MessageUpdateEvent> getEventType()
  {
    return MessageUpdateEvent.class;
  }

  @Override
  public Mono<Void> execute(MessageUpdateEvent event)
  {
    return Mono.just(event)
        .filter(MessageUpdateEvent::isContentChanged)
        .flatMap(MessageUpdateEvent::getMessage)
        .flatMap(this::processCommand);
  }
}
