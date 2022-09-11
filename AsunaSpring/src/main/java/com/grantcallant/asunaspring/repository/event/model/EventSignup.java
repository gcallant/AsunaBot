package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.guild.model.GuildMember;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "event_signups")
public class EventSignup
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
  @JoinColumn(name = "role_id", nullable = false)
  private EventRole eventRole;

  @Column(name = "eso_character_id", nullable = false)
  private UUID esoCharacterId;

  @Column(name = "no_call_no_show", nullable = false)
  private Boolean noCallNoShow = false;

  @Column(name = "guild_member_notes", length = 4000)
  private String guildMemberNotes;

  @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.REMOVE, optional = false, orphanRemoval = true)
  @JoinTable(name = "event_signups_event",
      joinColumns = @JoinColumn(name = "event_id"),
      inverseJoinColumns = @JoinColumn(name = "event_signup_id"))
  private Event event;

  @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.REMOVE, optional = false)
  @JoinColumn(name = "guild_member_id", nullable = false)
  private GuildMember guildMember;
}
