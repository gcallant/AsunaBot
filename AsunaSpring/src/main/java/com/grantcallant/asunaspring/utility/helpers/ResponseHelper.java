package com.grantcallant.asunaspring.utility.helpers;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import java.util.HashMap;
import java.util.Map;

/**
 * Wraps ResponseEntity calls in a map for convenient reuse.
 */
public class ResponseHelper
{
  private ResponseHelper() {}

  public static <D> ResponseEntity<D> noContentResponse()
  {
    return ResponseEntity.status(HttpStatus.NO_CONTENT).contentType(MediaType.APPLICATION_JSON).body(null);
  }

  @SuppressWarnings("unchecked")
  public static <D> ResponseEntity<Map<String, D>> successfulDataResponse(String message, D data)
  {
    HashMap<String, D> response = new HashMap<>();
    response.put("message", (D) message);
    response.put("data", data);
    return ResponseEntity.status(HttpStatus.OK).contentType(MediaType.APPLICATION_JSON).body(response);
  }

  @SuppressWarnings("unchecked")
  public static <D> ResponseEntity<Map<String, D>> failedResponse(String message, D data)
  {
    HashMap<String, D> response = new HashMap<>();
    response.put("message", (D) message);
    response.put("data", data);
    return ResponseEntity.status(HttpStatus.BAD_REQUEST).contentType(MediaType.APPLICATION_JSON).body(response);
  }
}
