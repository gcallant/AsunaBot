package com.grantcallant.asunaspring.utility.configuration;

import org.modelmapper.ModelMapper;
import org.modelmapper.config.Configuration.AccessLevel;
import org.modelmapper.convention.MatchingStrategies;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Initializes and configures the global ModelMapper instances to be used in the controller layer.
 */
@Configuration
public class ModelMapperConfiguration
{
  @Bean
  public ModelMapper modelMapper()
  {
    ModelMapper modelMapper = new ModelMapper();
    modelMapper
        .getConfiguration()
        .setMatchingStrategy(MatchingStrategies.STANDARD)
        .setFieldAccessLevel(AccessLevel.PRIVATE)
        .setFieldMatchingEnabled(true);
    return modelMapper;
  }
}
