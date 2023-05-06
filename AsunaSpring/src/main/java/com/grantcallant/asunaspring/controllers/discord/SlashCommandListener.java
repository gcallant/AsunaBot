package com.grantcallant.asunaspring.controllers.discord;

import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import reactor.core.publisher.Mono;

/**
 * 01 2023
 * Listens and dispatches slash commands to be processed by their appropriate handler.
 * @author Grant Callant
 */
public abstract class SlashCommandListener
{

  public Mono<Void> processCommand(ChatInputInteractionEvent event)
  {
//    return Flux.fromIterable(co)
    return null;
  }
}
