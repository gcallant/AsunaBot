package com.grantcallant.asunaspring.utility.configuration;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Primary;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

/**
 * Gets environment specific variables and makes them available to the application.
 */
@Component("configuration")
@Order(1)
@Primary
@Getter
public class Configuration
{
  private final LocalDateTime startTime;
  @Value("${application.name}")
  private String applicationName;

  @Value("${application.description}")
  private String applicationDescription;

  @Value("${spring.profiles.active}")
  private String applicationProfile;

  @Value("${app.datasource.url}")
  private String connectString;

  @Value("${application.frontend.url}")
  private String frontendUrl;

  @Value("${app.datasource.driverClassName}")
  private String driverClassName;

  @Value("${app.datasource.url}")
  private String dataSourceUrl;

  @Value("${app.datasource.username}")
  private String dataSourceUsername;

  @Value("${app.datasource.password}")
  private String dataSourcePassword;

  @Value("${app.datasource.hikari.minimumIdle}")
  private int minIdle;

  @Value("${app.datasource.hikari.maximumPoolSize}")
  private int maxPoolSize;

  @Value("${app.datasource.hikari.idleTimeout}")
  private long idleTimeout;

  @Value("${app.datasource.hikari.poolName}")
  private String poolName;

  @Value("${app.datasource.hikari.leak-detection-threshold}")
  private long leakThreshHold;

  @Value("${app.datasource.hikari.auto-commit}")
  private boolean autoCommit;

  @Value("${app.datasource.hikari.validation-timeout}")
  private long validationTimeout;

  @Value("${app.datasource.hikari.max-lifetime}")
  private long maxLifeTime;

  @Value("${app.datasource.hikari.initialization-fail-timeout}")
  private long initFailTimeout;

  @Value("${app.datasource.hikari.connection-init-sql}")
  private String initSql;

  @Value("${app.datasource.hikari.connection-test-query}")
  private String connTestQuery;

  @Value("${app.datasource.hikari.login-timeout}")
  private long loginTimeout;

  @Value("${app.datasource.hikari.connection-timeout}")
  private long connTimeout;

  @Value("${application.version}")
  private String applicationVersion;

  private final String applicationEnvironment;

  public Configuration()
  {
    this.startTime = LocalDateTime.now();
    applicationEnvironment = System.getenv("INSTANCE_NAME") != null ? System.getenv("INSTANCE_NAME") : "unknown";
  }
}

