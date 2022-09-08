package com.grantcallant.asunaspring.repository.event.model;

import com.grantcallant.asunaspring.repository.eso.model.ESOCharacter;
import lombok.*;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "roles")
public class Role
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @Column(name = "role_name", nullable = false, length = 20)
  private String roleName;

  @OneToMany(mappedBy = "role")
  private Set<ESOCharacter> esoCharacters = new LinkedHashSet<>();

  @OneToMany(mappedBy = "role")
  private Set<EventSignup> eventSignups = new LinkedHashSet<>();

}
