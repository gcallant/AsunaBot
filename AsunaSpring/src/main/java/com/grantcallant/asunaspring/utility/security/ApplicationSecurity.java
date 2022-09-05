package com.grantcallant.asunaspring.utility.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;

/**
 * Configures the global security for the application.
 */
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class ApplicationSecurity
{
  private static final RequestMatcher requestMatcher = new AntPathRequestMatcher("/api/v1/**");
  private static final String[] AUTH_WHITELIST = {"/v2/api-docs", "/swagger-resources", "/swagger-resources/**", "/configuration/ui", "/configuration/security", "/swagger-ui.html", "/webjars/**"};
  private final AuthorizationEntryPoint authorizationEntryPoint;
  private final ForbiddenRequestHandler forbiddenRequestHandler;

  @Autowired
  public ApplicationSecurity(AuthorizationEntryPoint authorizationEntryPoint, ForbiddenRequestHandler forbiddenRequestHandler)
  {
    this.authorizationEntryPoint = authorizationEntryPoint;
    this.forbiddenRequestHandler = forbiddenRequestHandler;
  }

  @Bean
  public SecurityFilterChain filterChain(HttpSecurity http) throws Exception
  {
    http.cors().and().csrf().disable().sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
        .and().exceptionHandling().defaultAuthenticationEntryPointFor(authorizationEntryPoint, requestMatcher).defaultAccessDeniedHandlerFor(forbiddenRequestHandler, requestMatcher)
        .and().authorizeRequests().antMatchers("/api/v1/**").authenticated()
        .and().authorizeRequests().antMatchers(AUTH_WHITELIST).permitAll().and().authorizeRequests().antMatchers("/**").permitAll();

    http.headers().cacheControl().disable();
    return http.build();
  }
}
