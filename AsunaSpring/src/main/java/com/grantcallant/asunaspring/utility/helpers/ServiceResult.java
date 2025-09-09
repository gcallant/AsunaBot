package com.grantcallant.asunaspring.utility.helpers;

import lombok.Getter;
import org.springframework.http.HttpStatus;

import java.util.function.Function;

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
   * Transform the data in this ServiceResult to another type while preserving success/failure state.
   */
  public <R> ServiceResult<R> map(Function<T, R> mapper)
  {
    ServiceResultBuilder<R> builder = new ServiceResultBuilder<R>()
        .message(this.message)
        .status(this.status);
        
    if (this.success) 
    {
      return builder
          .success()
          .data(this.data != null ? mapper.apply(this.data) : null)
          .build();
    }
    
    return builder
        .failed()
        .data(null)
        .build();
  }

  /**
   * Transform successful data or provide a default value for failed results.
   */
  public <R> ServiceResult<R> mapOrDefault(Function<T, R> mapper, R defaultValue)
  {
    ServiceResultBuilder<R> builder = new ServiceResultBuilder<R>()
        .message(this.message)
        .status(this.status);
        
    if (this.success && this.data != null) 
    {
      return builder
          .success()
          .data(mapper.apply(this.data))
          .build();
    }
    
    return builder
        .failed()
        .data(defaultValue)
        .build();
  }

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
      result.failed = !this.success;
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
