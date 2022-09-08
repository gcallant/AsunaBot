package com.grantcallant.asunaspring.repository.guild.model;

import com.grantcallant.asunaspring.repository.eso.model.ESOUser;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "guild_guild_member")
public class GuildGuildMember
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
  @OnDelete(action = OnDeleteAction.CASCADE)
  @JoinColumn(name = "guild_id", nullable = false)
  private Guild guild;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @OnDelete(action = OnDeleteAction.CASCADE)
  @JoinColumn(name = "guild_member_id", nullable = false)
  private GuildMember guildMember;

  @OneToMany(mappedBy = "guildGuildMember")
  private Set<ESOUser> eSOUsers = new LinkedHashSet<>();

}
