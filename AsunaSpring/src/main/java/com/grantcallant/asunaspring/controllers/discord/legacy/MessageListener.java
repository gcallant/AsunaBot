package com.grantcallant.asunaspring.controllers.discord.legacy;

import com.grantcallant.asunaspring.controllers.discord.legacy.commands.LegacyCommand;
import discord4j.core.object.entity.Message;
import discord4j.gateway.ShardInfo;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * 12 2022
 * Handles message create, and message update events.
 *
 * @author Grant Callant
 */
@Component
public interface MessageListener
{
  default Mono<Void> processCommand(Message eventMessage)
  {
    return Mono
        .just(eventMessage)
        .filter(message -> message.getAuthor().map(user -> !user.isBot()).orElse(false))
        .flatMap(message ->
        {
          String content = message.getContent();
          LegacyCommand command = LegacyCommandCache.commandMap().get(content);
          if (command != null)
          {
            LegacyMessageEvent legacyMessageEvent = new LegacyMessageEvent(message, message.getClient(), ShardInfo.create(0, 1));
            return command.execute(legacyMessageEvent);
          }
          else
          {
            return Mono.empty();
          }
        });
  }
}
