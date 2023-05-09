package com.grantcallant.asunaspring.controllers.discord.commands;

import com.grantcallant.asunaspring.controllers.discord.legacy.EventListener;
import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * 01 2023
 * Contract for an InputInteractionEvent (formerly called "Slash Command").
 *
 * @author Grant Callant
 */
@Component
public interface SlashCommand extends EventListener<ChatInputInteractionEvent>
{
  default Class<ChatInputInteractionEvent> getEventType() {return ChatInputInteractionEvent.class;}

  Mono<Void> execute(ChatInputInteractionEvent event);

  /**
   * Gets the case-sensitive name of the command.
   *
   * @return The name of the command being called.
   */
  String getName();
}
