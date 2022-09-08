package com.grantcallant.asunaspring.repository.theme.model;

import com.grantcallant.asunaspring.repository.user.model.User;
import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;
import java.util.LinkedHashSet;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "themes")
public class Theme
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @Column(name = "theme_name", nullable = false, length = 50)
  private String themeName;

  @OneToMany(mappedBy = "theme")
  private Set<User> users = new LinkedHashSet<>();

}
