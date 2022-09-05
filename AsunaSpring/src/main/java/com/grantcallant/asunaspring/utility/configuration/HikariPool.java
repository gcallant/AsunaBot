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
  private final Configuration configuration;

  @Autowired
  public HikariPool(Configuration configuration)
  {
    this.configuration = configuration;
  }

  @Bean
  @Primary
  public DataSource dataSource() {
    HikariConfig hikariConfig = new HikariConfig();
    hikariConfig.setDriverClassName(configuration.getDriverClassName());
    hikariConfig.setJdbcUrl(configuration.getDataSourceUrl());
    hikariConfig.setUsername(configuration.getDataSourceUsername());
    hikariConfig.setPassword(configuration.getDataSourcePassword());
    hikariConfig.setMaximumPoolSize(configuration.getMaxPoolSize());
    hikariConfig.setAllowPoolSuspension(true);
    hikariConfig.setValidationTimeout(configuration.getValidationTimeout());
    hikariConfig.setAutoCommit(configuration.isAutoCommit());
    hikariConfig.setConnectionInitSql(configuration.getInitSql());
    hikariConfig.setConnectionTestQuery(configuration.getConnTestQuery());
    hikariConfig.setIdleTimeout(configuration.getIdleTimeout());
    hikariConfig.setMaxLifetime(configuration.getMaxLifeTime());
    hikariConfig.setPoolName(configuration.getPoolName());
    hikariConfig.setMinimumIdle(configuration.getMinIdle());
    hikariConfig.setConnectionTimeout(configuration.getConnTimeout());

    return new HikariDataSource(hikariConfig);
  }
}
