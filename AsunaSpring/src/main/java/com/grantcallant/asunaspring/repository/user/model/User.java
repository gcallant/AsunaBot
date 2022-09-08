package com.grantcallant.asunaspring.repository.user.model;

import com.grantcallant.asunaspring.repository.theme.model.Theme;
import com.grantcallant.asunaspring.repository.guild.model.GuildMember;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.Locale;
import java.util.TimeZone;

@Getter
@Setter
@Entity
@Table(name = "users")
public class User
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "guild_member_id", nullable = false)
  private GuildMember guildMember;

  @Column(name = "locale", nullable = false, length = 10)
  private Locale locale;

  @Column(name = "time_zone", nullable = false, length = 20)
  private TimeZone timeZone;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "theme_id", nullable = false)
  private Theme theme;

  @Column(name = "is_admin", nullable = false)
  private Boolean admin = false;

}
