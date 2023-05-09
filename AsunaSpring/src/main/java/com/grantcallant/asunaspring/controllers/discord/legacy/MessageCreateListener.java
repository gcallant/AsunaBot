package com.grantcallant.asunaspring.controllers.discord.legacy;

import discord4j.core.event.domain.message.MessageCreateEvent;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

/**
 * 12 2022
 * Listens for newly created message events.
 *
 * @author Grant Callant
 */
@Service
public class MessageCreateListener implements MessageListener, EventListener<MessageCreateEvent>
{
  @Override
  public Class<MessageCreateEvent> getEventType()
  {
    return MessageCreateEvent.class;
  }

  @Override
  public Mono<Void> execute(MessageCreateEvent event)
  {
    return processCommand(event.getMessage());
  }
}
