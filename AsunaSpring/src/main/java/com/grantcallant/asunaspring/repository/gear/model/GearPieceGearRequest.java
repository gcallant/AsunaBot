package com.grantcallant.asunaspring.repository.gear.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "gear_piece_gear_requests")
public class GearPieceGearRequest
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
  @JoinColumn(name = "gear_request_id", nullable = false)
  private GearRequest gearRequest;

  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "gear_piece_id", nullable = false)
  private GearPiece gearPiece;

  @Column(name = "active", nullable = false)
  private Boolean active = false;
}
