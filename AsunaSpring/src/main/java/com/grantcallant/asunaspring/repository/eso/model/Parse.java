package com.grantcallant.asunaspring.repository.eso.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.Instant;

@Getter
@Setter
@Entity
@Table(name = "parses")
public class Parse
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private Long id;

  @Column(name = "created_at")
  private Instant createdAt;

  @Column(name = "updated_at")
  private Instant updatedAt;

  @Column(name = "dps", columnDefinition = "INT UNSIGNED not null")
  private Long dps;

  @Column(name = "parse_file_path", nullable = false, length = 100)
  private String parseFilePath;

}
