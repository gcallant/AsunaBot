package com.grantcallant.asunaspring.repository.eso.model;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.UUID;

/**
 * 09 2022
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring
 *
 * @author Grant Callant
 */
@Getter
@Setter
@Entity
@Table(name = "character_classes")
public class CharacterClass
{
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "id", nullable = false)
  private UUID id;

  @Column(name = "class_name")
  private String className;
}
