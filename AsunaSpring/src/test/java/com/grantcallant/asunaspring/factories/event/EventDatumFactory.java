package com.grantcallant.asunaspring.factories.event;

import com.grantcallant.asunaspring.repository.event.model.EventDatum;

public record EventDatumFactory()
{
  public static EventDatum createEventDatum()
  {
    return new EventDatum();
  }
}
