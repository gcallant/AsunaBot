package com.grantcallant.asunaspring.controllers.discord.legacy;

import lombok.Data;

import java.util.List;

/**
 * 05 2023
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring.controllers.discord.legacy
 *
 * @author Grant Callant
 */
@Data
public class LegacyCommandData
{
  private String name;
  private String description;
  private List<CommandOption> options;

}
