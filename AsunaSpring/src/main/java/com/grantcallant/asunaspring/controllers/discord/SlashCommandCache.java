package com.grantcallant.asunaspring.controllers.discord;

import com.grantcallant.asunaspring.utility.configuration.Config;
import com.grantcallant.asunaspring.utility.logging.Log;
import discord4j.common.JacksonResources;
import discord4j.discordjson.json.ApplicationCommandRequest;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * 01 2023
 * A thread-safe singleton cache of all mapped slash commands, initialized at startup.
 *
 * @author Grant Callant
 */
@Component
public class SlashCommandCache
{
  private final ReentrantReadWriteLock lock;
  private final List<ApplicationCommandRequest> commands;
  private final DiscordBotService botService;
  private final Config config;

  public SlashCommandCache(DiscordBotService botService, final Config config)
  {
    this.botService = botService;
    this.config = config;
    commands = new ArrayList<>();
    this.lock = new ReentrantReadWriteLock();
  }

  public String init() throws IOException
  {
    JacksonResources jacksonMapper = JacksonResources.create();
    PathMatchingResourcePatternResolver matcher = new PathMatchingResourcePatternResolver();

    lock.writeLock().lock();
    try
    {
      Arrays.stream(matcher.getResources("commands/*.json")).forEach(resource ->
      {
        try
        {
          commands.add(jacksonMapper.getObjectMapper().readValue(resource.getInputStream(), ApplicationCommandRequest.class));
        }
        catch (IOException ignored) {/*ignore*/}
      });

      int size = commands.size();
      if(config.getApplicationEnvironment().equalsIgnoreCase("local"))
      {
        botService.applicationService().bulkOverwriteGuildApplicationCommand(botService.applicationId(), Long.parseLong(config.getTestGuildId()), commands)
                  .doOnNext(ignore -> commands.forEach(
                      command -> Log.debug(String.format("Registered command %s, 1/%d", command.name(), size))))
                  .doOnError(e -> Log.error("Failed to register commands", e))
                  .subscribe();
      }
      else if (config.getApplicationEnvironment().equalsIgnoreCase("production"))
      {
        botService.applicationService().bulkOverwriteGlobalApplicationCommand(botService.applicationId(), commands)
                  .doOnNext(ignore -> commands.forEach(
                      command -> Log.debug(String.format("Registered command %s, 1/%d", command.name(), size))))
                  .doOnError(e -> Log.error("Failed to register commands", e))
                  .subscribe();
      }

      return String.format("Added %d unique slash commands", commands.size());
    }
    finally
    {
      lock.writeLock().unlock();
    }
  }
}
