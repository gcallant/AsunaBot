package com.grantcallant.asunaspring.repository.guild.model;

import com.grantcallant.asunaspring.repository.event.model.Event;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.TimeZone;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "guilds")
public class Guild
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @Column(name = "guild_name", nullable = false, length = 500)
  private String guildName;

  @Column(name = "time_zone", nullable = false, length = 100)
  private TimeZone timeZone;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "create_event_role_id", nullable = false)
  private GuildRole createEventRole;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "admin_role_id", nullable = false)
  private GuildRole adminRole;

  @OneToMany(mappedBy = "guild")
  private Set<Event> events = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guild")
  private Set<GuildGuildMember> guildGuildMembers = new LinkedHashSet<>();
}
