package com.grantcallant.asunaspring.controllers.discord.legacy;

import discord4j.core.GatewayDiscordClient;
import discord4j.core.event.domain.message.MessageEvent;
import discord4j.core.object.entity.Message;
import discord4j.gateway.ShardInfo;

/**
 * 05 2023
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring.controllers.discord
 *
 * @author Grant Callant
 */
public class LegacyMessageEvent extends MessageEvent
{
  private final Message message;

  public LegacyMessageEvent(Message message, GatewayDiscordClient gateway, ShardInfo shardInfo)
  {
    super(gateway, shardInfo);
    this.message = message;
  }

  public Message getMessage()
  {
    return message;
  }
}

