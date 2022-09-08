package com.grantcallant.asunaspring.repository.guild.model;

import com.grantcallant.asunaspring.repository.event.model.Event;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "guilds")
public class Guild
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private UUID id;

  private Instant createdAt;

  private Instant updatedAt;

  @Column(nullable = false, length = 500)
  private String guildName;

  @Column(nullable = false, length = 50)
  private String timeZone;

  @Column(nullable = false)
  private Long createEventRole;

  @Column(nullable = false)
  private Long adminRole;

  @OneToMany(mappedBy = "guild")
  private Set<Event> events = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guild")
  private Set<GuildGuildMember> guildGuildMembers = new LinkedHashSet<>();

}
