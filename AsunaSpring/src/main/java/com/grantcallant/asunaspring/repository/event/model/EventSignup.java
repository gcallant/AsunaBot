package com.grantcallant.asunaspring.repository.event.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "eventSignups")
public class EventSignup
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private UUID id;

  private Instant createdAt;

  private Instant updatedAt;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "roleId", nullable = false)
  private Role role;

  @Column(nullable = false)
  private UUID esoCharacterId;

  @Column(nullable = false)
  private Boolean noCallNoShow = false;

  @Column(length = 4000)
  private String guildMemberNotes;

  @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.REMOVE, optional = false, orphanRemoval = true)
  @JoinTable(name = "eventSignupsEvent",
      joinColumns = @JoinColumn(name = "eventSignupId"),
      inverseJoinColumns = @JoinColumn(name = "eventId"))
  private Event event;

}
