package com.grantcallant.asunaspring.factories.event;

import com.grantcallant.asunaspring.repository.event.model.EventRoster;

import java.util.Random;
import java.util.UUID;

/**
 * Factory for creating EventRosters for testing.
 *
 * @author Grant Callant
 */
public record EventRosterFactory()
{
  public static EventRoster createEventRoster()
  {
    EventRoster eventRoster = new EventRoster();
    eventRoster.setId(UUID.randomUUID());
    eventRoster.setEvent(EventFactory.createEvent());
    eventRoster.setMaxTanks(randomBoundShort(3));
    eventRoster.setMaxHeals(randomBoundShort(3));
    eventRoster.setMaxRangedDps(randomBoundShort(12));
    eventRoster.setMaxMeleeDps(randomBoundShort(12));
    eventRoster.setSignedUpTanks(randomBoundShort(12));
    eventRoster.setSignedUpHeals(randomBoundShort(12));
    eventRoster.setSignedUpRangedDps(randomBoundShort(12));
    eventRoster.setSignedUpMeleeDps(randomBoundShort(12));
    return eventRoster;
  }

  private static short randomBoundShort(int bound)
  {
    if (bound == Short.MAX_VALUE)
    {
      throw new IllegalArgumentException("You can't have the bound larger than a short!");
    }
    return (short) ((short) new Random().nextInt(bound) + 1);
  }
}
