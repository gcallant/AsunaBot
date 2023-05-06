package com.grantcallant.asunaspring.controllers.discord;

import discord4j.core.object.component.ActionRow;
import discord4j.core.object.component.SelectMenu;
import discord4j.core.object.entity.Message;
import discord4j.core.object.entity.channel.TextChannel;
import reactor.core.publisher.Mono;

/**
 * 12 2022
 * Handles message create, and message update events.
 *
 * @author Grant Callant
 */
public abstract class MessageListener
{
  public Mono<Void> processCommand(Message eventMessage)
  {
    return Mono.just(eventMessage)
        .filter(message -> message.getAuthor().map(user -> !user.isBot()).orElse(false))
        .filter(message -> message.getContent().equalsIgnoreCase("?event"))
        .flatMap(Message::getChannel)
        .ofType(TextChannel.class)
        .flatMap(channel -> channel.createMessage("Select some string options!")
            .withComponents(ActionRow.of(
                SelectMenu.of("mySelectMenu1",
                        SelectMenu.Option.of("option 1", "foo"),
                        SelectMenu.Option.of("option 2", "bar"),
                        SelectMenu.Option.of("option 3", "baz"))
                    .withMaxValues(2)))
            .then(channel.createMessage("Select some user options!")
                .withComponents(ActionRow.of(SelectMenu.of("mySelectMenu2"))))
            .then(channel.createMessage("Select some channel options!")
                .withComponents(ActionRow.of(SelectMenu.of("mySelectMenu3",
                    SelectMenu.Option.of("option 3", "baz")))))).then();
  }
}
