package com.grantcallant.asunaspring.repository.guild.model;

import com.grantcallant.asunaspring.repository.eso.model.EsoUser;
import com.grantcallant.asunaspring.repository.event.model.EventSignup;
import com.grantcallant.asunaspring.repository.gear.model.GearRequest;
import com.grantcallant.asunaspring.repository.user.model.User;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "guild_members")
public class GuildMember
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @Column(name = "name", nullable = false, length = 300)
  private String name;

  @Column(name = "discord_user_id", nullable = false)
  private Long discordUserId;

  @OneToMany(mappedBy = "discordRoleId")
  private Set<GuildRole> discordRoleIds;

  @OneToOne(mappedBy = "guildMember")
  private User user;

  @OneToMany(mappedBy = "guildMember")
  private Set<EsoUser> esoUsers = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guildMember")
  private Set<EventSignup> eventSignups = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guildMember")
  private Set<GearRequest> gearRequests = new LinkedHashSet<>();

  @OneToMany(mappedBy = "guildMember")
  private Set<GuildGuildMember> guildGuildMembers = new LinkedHashSet<>();
}
