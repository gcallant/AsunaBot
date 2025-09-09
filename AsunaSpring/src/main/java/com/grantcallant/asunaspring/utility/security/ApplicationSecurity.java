package com.grantcallant.asunaspring.utility.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.annotation.web.configurers.HeadersConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;

/**
 * Configures the global security for the application.
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity()
public class ApplicationSecurity
{
  private static final RequestMatcher requestMatcher = PathPatternRequestMatcher.pathPattern("/api/v1/**");
  private static final String[] AUTH_WHITELIST = {
    "/v2/api-docs", "/v3/api-docs", "/v3/api-docs/**",
    "/swagger-resources", "/swagger-resources/**",
    "/configuration/ui", "/configuration/security",
    "/swagger-ui.html", "/swagger-ui/**", "/webjars/**"
  };

  private final AuthorizationEntryPoint authorizationEntryPoint;
  private final ForbiddenRequestHandler forbiddenRequestHandler;

  public ApplicationSecurity(AuthorizationEntryPoint authorizationEntryPoint, ForbiddenRequestHandler forbiddenRequestHandler)
  {
    this.authorizationEntryPoint = authorizationEntryPoint;
    this.forbiddenRequestHandler = forbiddenRequestHandler;
  }

  @Bean
  public SecurityFilterChain filterChain(HttpSecurity http) throws Exception
  {
    return http
        .cors(cors -> cors.configure(http)) // Modern CORS configuration
        .csrf(AbstractHttpConfigurer::disable) // Modern CSRF disable
        .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .exceptionHandling(exceptions -> exceptions
            .defaultAuthenticationEntryPointFor(authorizationEntryPoint, requestMatcher)
            .defaultAccessDeniedHandlerFor(forbiddenRequestHandler, requestMatcher))
        .authorizeHttpRequests(authz -> authz
            .requestMatchers(AUTH_WHITELIST).permitAll() // Public endpoints first
            .requestMatchers("/api/v1/**").authenticated() // Protected API endpoints
            .anyRequest().permitAll()) // All other requests
        .headers(headers -> headers.cacheControl(HeadersConfigurer.CacheControlConfig::disable))
        .build();
  }
}
