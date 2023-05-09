package com.grantcallant.asunaspring.controllers.discord.legacy;

import com.grantcallant.asunaspring.controllers.discord.legacy.commands.LegacyCommand;
import discord4j.common.JacksonResources;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * 01 2023
 * A thread-safe singleton cache of all mapped legacy commands, initialized at startup.
 *
 * @author Grant Callant
 */
@Component
public class LegacyCommandCache
{
  private static final Map<String, LegacyCommand> commands = new HashMap<>();
  private final ReentrantReadWriteLock lock;

  public LegacyCommandCache()
  {
    this.lock = new ReentrantReadWriteLock();
  }

  public static Map<String, LegacyCommand> commandMap()
  {
    return commands;
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
          commands.put("commandName", jacksonMapper.getObjectMapper().readValue(resource.getInputStream(), LegacyCommand.class));
        }
        catch (IOException ignored) {/*ignore*/}
      });

      return String.format("Added %d legacy commands", commands.size());
    }
    finally
    {
      lock.writeLock().unlock();
    }
  }
}
