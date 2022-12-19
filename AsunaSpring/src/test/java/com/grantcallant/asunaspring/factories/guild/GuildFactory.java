package com.grantcallant.asunaspring.factories.guild;

import com.grantcallant.asunaspring.repository.guild.model.Guild;
import net.bytebuddy.utility.RandomString;

import java.util.Random;
import java.util.TimeZone;
import java.util.UUID;

/**
 * Factory for creating guilds for testing.
 *
 * @author Grant Callant
 */
public record GuildFactory()
{
  public static Guild createGuild()
  {
    Guild guild = new Guild();
    guild.setId(UUID.randomUUID());
    guild.setGuildName(RandomString.make());
    guild.setTimeZone(TimeZone.getTimeZone(randomTimeZone()));
    guild.setCreateEventRole(GuildRoleFactory.createGuildRole());
    guild.setAdminRole(GuildRoleFactory.createGuildRole());
    return guild;
  }

  private static String randomTimeZone()
  {
    int bound = TimeZoneResource.TIME_ZONE_ARRAY.length - 1;
    return TimeZoneResource.TIME_ZONE_ARRAY[new Random().nextInt(bound)];
  }
}
