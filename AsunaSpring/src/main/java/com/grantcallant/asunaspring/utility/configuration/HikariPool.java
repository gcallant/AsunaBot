package com.grantcallant.asunaspring.utility.configuration;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;

/**
 * Initializes and configures the Hikari datapool for use in the service layer.
 */
@Component
public class HikariPool
{
  private final Config config;

  @Autowired
  public HikariPool(Config config)
  {
    this.config = config;
  }

  @Bean
  @Primary
  public DataSource dataSource() {
    HikariConfig hikariConfig = new HikariConfig();
    hikariConfig.setDriverClassName(config.getDriverClassName());
    hikariConfig.setJdbcUrl(config.getDataSourceUrl());
    hikariConfig.setUsername(config.getDataSourceUsername());
    hikariConfig.setPassword(config.getDataSourcePassword());
    hikariConfig.setMaximumPoolSize(config.getMaxPoolSize());
    hikariConfig.setAllowPoolSuspension(true);
    hikariConfig.setValidationTimeout(config.getValidationTimeout());
    hikariConfig.setAutoCommit(config.isAutoCommit());
    hikariConfig.setConnectionInitSql(config.getInitSql());
    hikariConfig.setConnectionTestQuery(config.getConnTestQuery());
    hikariConfig.setIdleTimeout(config.getIdleTimeout());
    hikariConfig.setMaxLifetime(config.getMaxLifeTime());
    hikariConfig.setPoolName(config.getPoolName());
    hikariConfig.setMinimumIdle(config.getMinIdle());
    hikariConfig.setConnectionTimeout(config.getConnTimeout());

    return new HikariDataSource(hikariConfig);
  }
}
