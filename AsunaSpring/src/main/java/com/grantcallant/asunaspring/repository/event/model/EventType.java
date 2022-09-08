package com.grantcallant.asunaspring.repository.event.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "eventTypes")
public class EventType
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private UUID id;

  private Instant createdAt;

  private Instant updatedAt;

  @Column(nullable = false, length = 50)
  private String eventTypeName;

  @OneToMany(mappedBy = "eventType")
  private Set<Event> events = new LinkedHashSet<>();

}
