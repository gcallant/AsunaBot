package com.grantcallant.asunaspring.controllers.discord.legacy;

import lombok.Data;

/**
 * 05 2023
 * Created by Grant Callant for AsunaBot in com.grantcallant.asunaspring.controllers.discord.legacy
 *
 * @author Grant Callant
 */
@Data
public class CommandOption
{
  private String name;
  private String description;
  private int type;
  private boolean required;
}
