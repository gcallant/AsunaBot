package com.grantcallant.asunaspring.utility.security;

import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Configures the entrypoint for API authorization.
 */
@Component
public class AuthorizationEntryPoint implements AuthenticationEntryPoint
{
  /**
   * Overrides Spring's default commence method, by default sends unauthorized response back.
   */
  @Override
  public void commence(HttpServletRequest request, HttpServletResponse response,
                       AuthenticationException authException) throws IOException
  {
    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized");
  }
}
