package com.grantcallant.asunaspring.controllers.discord.commands;

import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import discord4j.core.object.entity.Message;
import reactor.core.publisher.Mono;

import java.time.Duration;

/**
 * 05 2023
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring.controllers.discord.commands
 *
 * @author Grant Callant
 */
public class EventCommand implements SlashCommand
{
  /**
   * @param event
   * @return
   */
  @Override public Mono<Void> execute(final ChatInputInteractionEvent event)
  {
    event.getInteraction().getMessage().flatMap(Message::getAuthor).get().getPrivateChannel().block(Duration.ofSeconds(5))
         .createMessage("What do you want to name the event?");
    return event.reply().withEphemeral(true).withContent(":tada: Check your messages, I just sent you something cool!");
  }

  /**
   * Gets the case-sensitive name of the command.
   *
   * @return The name of the command being called.
   */
  @Override public String getName()
  {
    return "event";
  }
}
