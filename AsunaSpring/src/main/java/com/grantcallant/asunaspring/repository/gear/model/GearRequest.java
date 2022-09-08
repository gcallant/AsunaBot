package com.grantcallant.asunaspring.repository.gear.model;

import com.grantcallant.asunaspring.repository.guild.model.GuildMember;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "gear_requests")
public class GearRequest
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

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "gear_set_id", nullable = false)
  private GearSet gearSet;

  @OneToMany(mappedBy = "gearRequest")
  private Set<GearPieceGearRequest> gearPieceGearRequests = new LinkedHashSet<>();

}
