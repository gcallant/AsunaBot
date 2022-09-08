package com.grantcallant.asunaspring.repository.eso.model;

import com.grantcallant.asunaspring.repository.eso.enums.RaceNameType;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "character_races")
public class CharacterRace
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @Enumerated(EnumType.STRING)
  @Column(name = "race_name", nullable = false, length = 20)
  private RaceNameType raceName;

  @OneToMany(mappedBy = "characterRace")
  private Set<ESOCharacter> eSOCharacters = new LinkedHashSet<>();

}
