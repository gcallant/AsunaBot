package com.grantcallant.asunaspring.repository.gear.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;

@Getter
@Setter
@Entity
@Table(name = "gear_piece_gear_request")
public class GearPieceGearRequest
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
  @JoinColumn(name = "gear_request_id", nullable = false)
  private GearRequest gearRequest;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "gear_piece_id", nullable = false)
  private GearPiece gearPiece;

  @Column(name = "is_active", nullable = false)
  private Boolean active = false;

}
