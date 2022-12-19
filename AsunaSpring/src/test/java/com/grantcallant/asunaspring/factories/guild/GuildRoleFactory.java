package com.grantcallant.asunaspring.factories.guild;

import com.grantcallant.asunaspring.repository.guild.model.GuildRole;

import java.util.Random;
import java.util.UUID;

/**
 * Factory for creating GuildRoles for testing.
 *
 * @author Grant Callant
 */
public record GuildRoleFactory()
{
  public static GuildRole createGuildRole()
  {
    GuildRole guildRole = new GuildRole();
    guildRole.setId(UUID.randomUUID());

    //Discord uses Snowflakes, a 13 digit integer
    guildRole.setDiscordRoleId((long) new Random().nextInt(Integer.MAX_VALUE));
    return guildRole;
  }
}
