package com.grantcallant.asunaspring.controllers.discord;

import com.grantcallant.asunaspring.utility.logging.Log;
import discord4j.common.JacksonResources;
import discord4j.discordjson.json.ApplicationCommandRequest;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashSet;
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
  private Collection commands;

  public SlashCommandCache()
  {
    commands = new HashSet();
    this.lock = new ReentrantReadWriteLock();
  }

  public void init() throws IOException
  {
    Log.info("Loading all slash commands...");
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
    }
    finally
    {
      Log.info(String.format("Added %d unique slash commands", commands.size()));
      lock.writeLock().unlock();
    }
  }
}
