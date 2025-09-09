package com.grantcallant.asunaspring.repository.gear.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.OffsetDateTime;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "gear_pieces")
public class GearPiece
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "created_at", nullable = false)
  private OffsetDateTime createdAt;

  @Column(name = "updated_at", nullable = false)
  private OffsetDateTime updatedAt;

  @Column(name = "gear_piece_name", nullable = false, length = 100)
  private String gearPieceName;

  @OneToMany(mappedBy = "gearPiece")
  private Set<GearPieceGearRequest> gearPieceGearRequests = new LinkedHashSet<>();
}
