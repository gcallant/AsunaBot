package com.grantcallant.asunaspring.controllers.discord.legacy.commands;

import com.grantcallant.asunaspring.controllers.discord.legacy.EventListener;
import com.grantcallant.asunaspring.controllers.discord.legacy.LegacyMessageEvent;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * 05 2023
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring.controllers.discord
 *
 * @author Grant Callant
 */
@Component
public interface LegacyCommand extends EventListener<LegacyMessageEvent>
{
  default Class<LegacyMessageEvent> getEventType() {return LegacyMessageEvent.class;}

  Mono<Void> execute(LegacyMessageEvent event);
}
