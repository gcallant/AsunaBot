package com.grantcallant.asunaspring.utility.helpers;

/**
 * An enum collection of localized messages to return.
 */
public enum LocalizedResponses
{
  NO_EVENT("noEvent", "No event found");

  private final String key;
  private final String localizedDescription;

  LocalizedResponses(final String key, final String localizedDescription)
  {
    this.key = key;
    this.localizedDescription = localizedDescription;
  }

  /**
   * The key to be returned to the front-end for localization.
   */
  public String key()
  {
    return key;
  }

  @Override
  public String toString()
  {
    return "Key: " + key + "Text: " + localizedDescription;
  }
}
