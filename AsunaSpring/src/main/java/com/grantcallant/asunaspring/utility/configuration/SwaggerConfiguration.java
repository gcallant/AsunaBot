package com.grantcallant.asunaspring.utility.configuration;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Initializes and configures OpenAPI/Swagger.
 */
@Configuration
@OpenAPIDefinition
public class SwaggerConfiguration {

    public static final String AUTHORIZATION_HEADER = "Authorization";

    private final Config config;

    @Autowired
    public SwaggerConfiguration(Config config) {
        this.config = config;
    }

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title(config.getApplicationName())
                        .description(config.getApplicationDescription())
                        .version(config.getApplicationVersion()))
                .addSecurityItem(new SecurityRequirement().addList("JWT"))
                .components(new io.swagger.v3.oas.models.Components()
                        .addSecuritySchemes("JWT", new SecurityScheme()
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")));
    }
}
