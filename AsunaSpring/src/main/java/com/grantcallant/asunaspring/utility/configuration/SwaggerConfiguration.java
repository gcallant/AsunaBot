package com.grantcallant.asunaspring.utility.configuration;

import graphql.com.google.common.collect.Lists;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.CorsEndpointProperties;
import org.springframework.boot.actuate.autoconfigure.endpoint.web.WebEndpointProperties;
import org.springframework.boot.actuate.autoconfigure.web.server.ManagementPortType;
import org.springframework.boot.actuate.endpoint.ExposableEndpoint;
import org.springframework.boot.actuate.endpoint.web.*;
import org.springframework.boot.actuate.endpoint.web.annotation.ControllerEndpointsSupplier;
import org.springframework.boot.actuate.endpoint.web.annotation.ServletEndpointsSupplier;
import org.springframework.boot.actuate.endpoint.web.servlet.WebMvcEndpointHandlerMapping;
import org.springframework.context.annotation.Bean;
import org.springframework.core.env.Environment;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.oas.annotations.EnableOpenApi;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.ApiKey;
import springfox.documentation.service.AuthorizationScope;
import springfox.documentation.service.SecurityReference;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spi.service.contexts.SecurityContext;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger.web.*;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

/**
 * Initializes and configures Swagger.
 */
@org.springframework.context.annotation.Configuration
@EnableOpenApi
public class SwaggerConfiguration
{
  public static final String AUTHORIZATION_HEADER = "Authorization";

  private final Configuration configuration;

  @Autowired
  public SwaggerConfiguration(Configuration configuration) {this.configuration = configuration;}

  @Bean
  public Docket docketBuilder()
  {
    return new Docket(DocumentationType.OAS_30).select()
        .apis(RequestHandlerSelectors.any())
        .paths(PathSelectors.any())
        .build()
        .pathMapping("/")
        .genericModelSubstitutes(ResponseEntity.class)
        .apiInfo(apiInfoBuilder())
        .securityContexts(Lists.newArrayList(SecurityContext.builder().securityReferences(securityReference()).build()))
        .securitySchemes(Lists.newArrayList(new ApiKey("JWT", AUTHORIZATION_HEADER, "header")))
        .useDefaultResponseMessages(false);
  }

  private ApiInfo apiInfoBuilder()
  {
    return new ApiInfoBuilder()
        .title(configuration.getApplicationName())
        .description(configuration.getApplicationDescription())
        .version(configuration.getApplicationVersion())
        .build();
  }

  private List<SecurityReference> securityReference()
  {
    AuthorizationScope authorizationScope = new AuthorizationScope("global", "accessEverything");
    AuthorizationScope[] authorizationScopes = new AuthorizationScope[1];
    authorizationScopes[0] = authorizationScope;
    return Lists.newArrayList(new SecurityReference("JWT", authorizationScopes));
  }

  @Bean
  public UiConfiguration uiConfiguration()
  {
    return UiConfigurationBuilder.builder()
        .deepLinking(true)
        .displayOperationId(false)
        .defaultModelsExpandDepth(1)
        .defaultModelExpandDepth(1)
        .defaultModelRendering(ModelRendering.EXAMPLE)
        .displayRequestDuration(false)
        .docExpansion(DocExpansion.FULL)
        .filter(true)
        .operationsSorter(OperationsSorter.ALPHA)
        .showExtensions(false)
        .tagsSorter(TagsSorter.ALPHA)
        .supportedSubmitMethods(UiConfiguration.Constants.DEFAULT_SUBMIT_METHODS)
        .build();
  }

  /**
   * Required bean addition to allow SpringFox to work with Spring 2.6.0+
   */
  @Bean
  public WebMvcEndpointHandlerMapping webEndpointServletHandlerMapping(WebEndpointsSupplier webEndpointsSupplier,
                                                                       ServletEndpointsSupplier servletEndpointsSupplier, ControllerEndpointsSupplier controllerEndpointsSupplier,
                                                                       EndpointMediaTypes endpointMediaTypes, CorsEndpointProperties corsProperties,
                                                                       WebEndpointProperties webEndpointProperties, Environment environment)
  {
    List<ExposableEndpoint<?>> allEndpoints = new ArrayList<>();
    Collection<ExposableWebEndpoint> webEndpoints = webEndpointsSupplier.getEndpoints();
    allEndpoints.addAll(webEndpoints);
    allEndpoints.addAll(servletEndpointsSupplier.getEndpoints());
    allEndpoints.addAll(controllerEndpointsSupplier.getEndpoints());
    String basePath = webEndpointProperties.getBasePath();
    EndpointMapping endpointMapping = new EndpointMapping(basePath);
    boolean shouldRegisterLinksMapping = this.shouldRegisterLinksMapping(webEndpointProperties, environment,
        basePath);
    return new WebMvcEndpointHandlerMapping(endpointMapping, webEndpoints, endpointMediaTypes,
        corsProperties.toCorsConfiguration(), new EndpointLinksResolver(allEndpoints, basePath),
        shouldRegisterLinksMapping, null);
  }

  private boolean shouldRegisterLinksMapping(WebEndpointProperties webEndpointProperties, Environment environment,
                                             String basePath)
  {
    return webEndpointProperties.getDiscovery().isEnabled() && (StringUtils.hasText(basePath)
        || ManagementPortType.get(environment).equals(ManagementPortType.DIFFERENT));
  }
}
