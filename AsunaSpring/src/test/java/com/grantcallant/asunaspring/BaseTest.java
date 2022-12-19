package com.grantcallant.asunaspring;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;

/**
 * Serves as the class to initialize and configure other test classes.
 */
@MockitoSettings(strictness = Strictness.STRICT_STUBS)
@SpringJUnitConfig
public class BaseTest
{
  @Autowired
  protected ModelMapper modelMapper;

  @BeforeAll
  public static void setup()
  {
  }

  @AfterAll
  public static void cleanup()
  {

  }
}
