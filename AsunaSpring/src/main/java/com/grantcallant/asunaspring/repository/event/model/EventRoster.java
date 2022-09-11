package com.grantcallant.asunaspring.repository.event.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "event_rosters")
public class EventRoster
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @OneToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "event_id", nullable = false)
  private Event event;

  @Column(name = "max_tanks", columnDefinition = "TINYINT UNSIGNED")
  private Short maxTanks;

  @Column(name = "max_heals", columnDefinition = "TINYINT UNSIGNED")
  private Short maxHeals;

  @Column(name = "max_ranged_dps", columnDefinition = "TINYINT UNSIGNED")
  private Short maxRangedDps;

  @Column(name = "max_melee_dps", columnDefinition = "TINYINT UNSIGNED")
  private Short maxMeleeDps;

  @Column(name = "signed_up_tanks", columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpTanks;

  @Column(name = "signed_up_heals", columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpHeals;

  @Column(name = "signed_up_ranged_dps", columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpRangedDps;

  @Column(name = "signed_up_melee_dps", columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpMeleeDps;
}
