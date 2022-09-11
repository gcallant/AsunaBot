package com.grantcallant.asunaspring.repository.user.model;

import com.grantcallant.asunaspring.repository.guild.model.GuildMember;
import com.grantcallant.asunaspring.repository.theme.model.Theme;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.Locale;
import java.util.TimeZone;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "users")
public class User
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @OneToOne(optional = false)
  @JoinColumn(name = "guild_member_id")
  private GuildMember guildMember;

  @Column(name = "locale", nullable = false, length = 50)
  private Locale locale;

  @Column(name = "time_zone", nullable = false, length = 100)
  private TimeZone timeZone;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "theme_id", nullable = false)
  private Theme theme;

  @Column(name = "admin", nullable = false)
  private Boolean admin = false;
}
