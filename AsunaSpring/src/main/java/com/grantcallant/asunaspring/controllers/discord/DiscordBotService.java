package com.grantcallant.asunaspring.controllers.discord;

import com.grantcallant.asunaspring.controllers.discord.legacy.EventListener;
import com.grantcallant.asunaspring.utility.configuration.Configuration;
import discord4j.core.DiscordClientBuilder;
import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.Event;
import discord4j.core.object.presence.ClientActivity;
import discord4j.core.object.presence.ClientPresence;
import discord4j.core.shard.GatewayBootstrap;
import discord4j.gateway.GatewayOptions;
import discord4j.gateway.intent.Intent;
import discord4j.gateway.intent.IntentSet;
import discord4j.rest.RestClient;
import discord4j.rest.service.ApplicationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;

import java.util.List;

/**
 * Receives and dispatches incoming commands and events from Discord
 *
 * @author Grant Callant
 */
@org.springframework.context.annotation.Configuration
public class DiscordBotService
{
  private final GatewayDiscordClient client;

  @Autowired
  public DiscordBotService(Configuration configuration)
  {
    client = DiscordClientBuilder.create(configuration.getDiscordToken()).build().login().block();
  }

  /**
   * Initializes a new GatewayDiscordClient for us, and maps over every available event listener without having to register each individually.
   * Now for each event listener all that needs to be done is implement EventListener and annotate with @Component.
   *
   * @param eventListenerList Spring will auto-populate this list of @Component event listeners that implement the EventListener interface.
   * @param <T>               The actual incoming event listener type (MessageEvent, ReactionEvent etc).
   * @return A new GatewayDiscordClient.
   */
  @SuppressWarnings("ReactiveStreamsUnusedPublisher")
  @Bean
  public <T extends Event> GatewayDiscordClient init(List<EventListener<T>> eventListenerList)
  {
    if (client == null)
    {
      throw new RuntimeException("Could not connect to Discord!");
    }

    eventListenerList
        .forEach(
            eventListener -> client.on(eventListener.getEventType())
                                   .flatMap(eventListener::execute)
                                   .onErrorResume(eventListener::handleError)
                                   .subscribe()
        );
    setClientIntents(client.rest().gateway());
    client.updatePresence(ClientPresence.online(ClientActivity.listening("to /commands")));
    return client;
  }

  /**
   * News to me- merely enabling privileged intents in the application is NOT enough! You have to actually claim the intents you intend to use.
   * This set of intents should cover the minimum needed intents for Asuna to function correctly.
   */
  private void setClientIntents(GatewayBootstrap<GatewayOptions> client)
  {
    client.setEnabledIntents(
        IntentSet.of(
            Intent.GUILDS,
            Intent.GUILD_MEMBERS,
            Intent.GUILD_EMOJIS,
            Intent.GUILD_INTEGRATIONS,
            Intent.GUILD_MESSAGES,
            Intent.GUILD_MESSAGE_REACTIONS,
            Intent.DIRECT_MESSAGES,
            Intent.DIRECT_MESSAGE_REACTIONS
        )
    );
  }

  public long applicationId()
  {
    return discordRestClient(client).getApplicationId().block();
  }

  @Bean
  public RestClient discordRestClient(GatewayDiscordClient client)
  {
    return client.getRestClient();
  }

  public ApplicationService applicationService()
  {
    return discordRestClient(client).getApplicationService();
  }
}
