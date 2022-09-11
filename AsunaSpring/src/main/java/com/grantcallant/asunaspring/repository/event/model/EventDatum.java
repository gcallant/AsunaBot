package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.guild.model.GuildMember;
import com.grantcallant.asunaspring.repository.guild.model.GuildRole;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "event_data")
public class EventDatum
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

  @Column(name = "event_time", nullable = false)
  private OffsetDateTime eventTime;

  @Column(name = "event_description", nullable = false, length = 2000)
  private String eventDescription;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "event_leader", nullable = false)
  private GuildMember eventLeader;

  @Column(name = "required_minimum_role", nullable = false)
  private Boolean requireMinimumRole = false;

  @ManyToOne(fetch = FetchType.LAZY)
  @JoinColumn(name = "minimum_event_role_id", columnDefinition = "INT UNSIGNED")
  private GuildRole minimumEventEventRole;
}
