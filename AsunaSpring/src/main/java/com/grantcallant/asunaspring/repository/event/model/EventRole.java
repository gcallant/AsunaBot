package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.eso.model.EsoCharacter;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "event_roles")
public class EventRole
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @Column(name = "role_name", nullable = false, length = 50)
  private String roleName;

  @OneToMany(mappedBy = "eventRole")
  private Set<EsoCharacter> esoCharacters = new LinkedHashSet<>();

  @OneToMany(mappedBy = "eventRole")
  private Set<EventSignup> eventSignups = new LinkedHashSet<>();

  @OneToMany(mappedBy = "minimumEventEventRole")
  private Set<EventDatum> eventData = new LinkedHashSet<>();
}
