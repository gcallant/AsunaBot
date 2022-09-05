package com.grantcallant.asunaspring.repository.event.model;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.Id;
import java.util.UUID;

/**
 * The model for events.
 */
@Entity
@Data
public class Event
{
  @Id
  private UUID id;
  private String eventName;
  private UUID eventTypeId;
  private UUID guildId;
}
