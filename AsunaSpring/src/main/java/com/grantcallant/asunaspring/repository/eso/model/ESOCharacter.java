package com.grantcallant.asunaspring.repository.eso.model;

import com.grantcallant.asunaspring.repository.eso.enums.CharacterClassType;
import com.grantcallant.asunaspring.repository.event.model.Role;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "e_s_o_characters")
public class ESOCharacter
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "eso_user_id", nullable = false)
  private ESOUser esoUser;

  @Column(name = "character_name", nullable = false, length = 20)
  private String characterName;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "role_id", nullable = false)
  private Role role;

  @Enumerated(EnumType.STRING)
  @Column(name = "character_class", nullable = false)
  private CharacterClassType characterClass;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "character_race_id", nullable = false)
  private CharacterRace characterRace;

  @Column(name = "highest_dps", columnDefinition = "INT UNSIGNED")
  private Long highestDps;

  @Column(name = "is_certified", nullable = false)
  private Boolean isCertified = false;

}
