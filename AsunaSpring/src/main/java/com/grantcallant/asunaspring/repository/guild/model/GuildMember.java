package com.grantcallant.asunaspring.repository.guild.model;

import com.grantcallant.asunaspring.repository.gear.model.GearRequest;
import com.grantcallant.asunaspring.repository.user.model.User;
import com.grantcallant.asunaspring.repository.event.model.EventDatum;
import com.grantcallant.asunaspring.repository.event.model.EventSignup;
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
@Table(name = "guildMembers")
public class GuildMember
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(nullable = false)
  private UUID id;

  private Instant createdAt;

  private Instant updatedAt;

  @Column(nullable = false, length = 300)
  private String name;

  @Column(nullable = false)
  private Long discordUserId;

  @Column(nullable = false, length = 1073741824)
  private Set<Long> discordRoleIds;

  @OneToMany(mappedBy = "guildMember")
  private Set<User> users = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guildMember")
  private Set<EventSignup> eventSignups = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guildMember")
  private Set<GearRequest> gearRequests = new LinkedHashSet<>();

  @OneToMany(mappedBy = "eventLeader")
  private Set<EventDatum> eventData = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guildMember")
  private Set<GuildGuildMember> guildGuildMembers = new LinkedHashSet<>();

}
