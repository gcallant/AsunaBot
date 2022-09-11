package com.grantcallant.asunaspring.repository.eso.model;

import com.grantcallant.asunaspring.repository.event.model.EventRole;
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
@Table(name = "eso_characters")
public class EsoCharacter
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "eso_user_id", nullable = false)
  private EsoUser esoUser;

  @Column(name = "character_name", nullable = false, length = 50)
  private String characterName;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "event_role_id", nullable = false)
  private EventRole eventRole;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "character_class_id", nullable = false)
  private CharacterClass characterClass;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "character_race_id", nullable = false)
  private CharacterRace characterRace;

  @OneToMany(mappedBy = "esoCharacter")
  private Set<Parse> parses = new LinkedHashSet<>();

  @Column(name = "certified")
  private Boolean certified = false;
}
