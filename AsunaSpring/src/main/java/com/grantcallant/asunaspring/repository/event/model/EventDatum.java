package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.guild.model.GuildMember;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "eventData")
public class EventDatum
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

  @Column(nullable = false)
  private LocalDate eventDay;

  @Column(nullable = false)
  private LocalTime eventTime;

  @Column(nullable = false, length = 2000)
  private String eventDescription;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "eventLeader", nullable = false)
  private GuildMember eventLeader;

  @Column(nullable = false)
  private Boolean requireMinimumRole = false;

  @Column(columnDefinition = "INT UNSIGNED")
  private Long minimumRoleId;

}
