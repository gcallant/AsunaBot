package com.grantcallant.asunaspring.controllers.discord;

import com.grantcallant.asunaspring.controllers.discord.commands.SlashCommand;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.interaction.ChatInputInteractionEvent;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.Collection;
import java.util.List;

/**
 * 01 2023
 * Listens and dispatches slash commands to be processed by their appropriate handler.
 * @author Grant Callant
 */
@Component
public abstract class SlashCommandListener
{
  private final Collection<SlashCommand> commands;

  protected SlashCommandListener(List<SlashCommand> commands, GatewayDiscordClient client)
  {
    this.commands = commands;
    client.on(ChatInputInteractionEvent.class, this::processCommand).subscribe();
  }
  public Mono<Void> processCommand(ChatInputInteractionEvent event)
  {
    return Flux
        .fromIterable(commands)
        .filter(slashCommand -> slashCommand.getName().equals(event.getCommandName()))
        .next()
        .flatMap(slashCommand -> slashCommand.execute(event));
  }
}
