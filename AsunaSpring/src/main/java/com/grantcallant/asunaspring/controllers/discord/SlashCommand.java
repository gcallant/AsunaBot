package com.grantcallant.asunaspring.controllers.discord;

import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import reactor.core.publisher.Mono;

/**
 * 01 2023
 * Contract for an InputInteractionEvent (formerly called "Slash Command").
 * @author Grant Callant
 */
public interface SlashCommand extends EventListener<ChatInputInteractionEvent>
{
  default Class<ChatInputInteractionEvent> getEventType() {return ChatInputInteractionEvent.class;}
  Mono<Void> execute(ChatInputInteractionEvent event);

  /**
   * Gets the case-sensitive name of the command.
   * @return The name of the command being called.
   */
  String getName();
}
