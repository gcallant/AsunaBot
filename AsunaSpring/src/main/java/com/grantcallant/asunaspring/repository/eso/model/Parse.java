package com.grantcallant.asunaspring.repository.eso.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "parses")
public class Parse
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
  @JoinColumn(name = "eso_character_id", nullable = false)
  private EsoCharacter esoCharacter;

  @Column(name = "dps", columnDefinition = "INT UNSIGNED not null")
  private Long dps;

  @Column(name = "parse_file_key", nullable = false)
  private UUID parseFileKey;
}
