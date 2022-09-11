package com.grantcallant.asunaspring.repository.eso.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "character_races")
public class CharacterRace
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "race_name", nullable = false, length = 50)
  private String raceName;

  @OneToMany(mappedBy = "characterRace")
  private Set<EsoCharacter> esoCharacters = new LinkedHashSet<>();
}
