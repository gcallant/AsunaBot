package com.grantcallant.asunaspring.repository.gear.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "gear_pieces")
public class GearPiece
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @Column(name = "gear_piece_name", nullable = false, length = 20)
  private String gearPieceName;

  @OneToMany(mappedBy = "gearPiece")
  private Set<GearPieceGearRequest> gearPieceGearRequests = new LinkedHashSet<>();

}
