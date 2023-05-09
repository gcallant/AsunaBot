package com.grantcallant.asunaspring.controllers.discord.legacy;

import com.grantcallant.asunaspring.controllers.discord.legacy.commands.LegacyCommand;
import reactor.core.publisher.Mono;

/**
 * 05 2023
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring.controllers.discord.legacy
 *
 * @author Grant Callant
 */
public class LegacyCommandAdapter implements LegacyCommand
{
  /**
   * @return
   */
  @Override public Class<LegacyMessageEvent> getEventType()
  {
    return LegacyCommand.super.getEventType();
  }

  /**
   * @param event
   * @return
   */
  @Override public Mono<Void> execute(final LegacyMessageEvent event)
  {
    return null;
  }
}
