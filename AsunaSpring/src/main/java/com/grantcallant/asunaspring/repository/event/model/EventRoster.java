package com.grantcallant.asunaspring.repository.event.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "eventRosters")
public class EventRoster
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private UUID id;

  private Instant createdAt;

  private Instant updatedAt;

  @OneToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "eventId", nullable = false)
  private Event event;

  @Column(columnDefinition = "TINYINT UNSIGNED")
  private Short maxTanks;

  @Column(columnDefinition = "TINYINT UNSIGNED")
  private Short maxHeals;

  @Column(columnDefinition = "TINYINT UNSIGNED")
  private Short maxRangedDps;

  @Column(columnDefinition = "TINYINT UNSIGNED")
  private Short maxMeleeDps;

  @Column(columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpTanks;

  @Column(columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpHeals;

  @Column(columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpRangedDps;

  @Column(columnDefinition = "TINYINT UNSIGNED not null")
  private Short signedUpMeleeDps;

}
