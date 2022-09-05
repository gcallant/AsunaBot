package com.grantcallant.asunaspring.utility.helpers;

import lombok.Getter;
import org.springframework.http.HttpStatus;

/**
 * Class to carry error or success messages as well as results from services to controllers.
 */
@Getter
public class ServiceResult<T>
{
  private T data;
  private String message;
  private HttpStatus status;
  private boolean success = false;
  private boolean failed = !success;

  /**
   * Force implementation to be done with builder method.
   */
  private ServiceResult() {}

  /**
   * Builder class allowing Service Result as a builder pattern.
   */
  public static class ServiceResultBuilder<T>
  {
    private T data;
    private String message;
    private HttpStatus status;
    private boolean success = false;

    public ServiceResult<T> build()
    {
      ServiceResult<T> result = new ServiceResult<>();
      result.data = this.data;
      result.message = this.message;
      result.status = this.status;
      result.success = this.success;
      return result;
    }

    public ServiceResultBuilder<T> data(T data)
    {
      this.data = data;
      return this;
    }

    public ServiceResultBuilder<T> success()
    {
      this.success = true;
      return this;
    }

    public ServiceResultBuilder<T> failed()
    {
      this.success = false;
      return this;
    }

    public ServiceResultBuilder<T> message(String message)
    {
      this.message = message;
      return this;
    }

    public ServiceResultBuilder<T> status(HttpStatus status)
    {
      this.status = status;
      return this;
    }
  }
}
