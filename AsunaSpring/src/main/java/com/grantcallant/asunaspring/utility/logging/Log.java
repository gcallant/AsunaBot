package com.grantcallant.asunaspring.utility.logging;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.HashMap;
import java.util.stream.IntStream;

/**
 * A wrapper class to configure logging.
 */
public class Log {

  /**
   * Prevents instantiating the constructor
   */
  private Log(){}

  private static final HashMap<String, Logger> loggers = new HashMap<>();

  /**
   * Logs DEBUG level line to console and/or logging stream.
   */
  public static void debug(String line) {
    String className = getClassName();
    Logger logger = getLogger(className);
    logger.debug(clean(line));
  }

  /**
   * Returns calling class name from stack.
   */
  private static String getClassName() {
    StackTraceElement[] stack = Thread.currentThread().getStackTrace();
    if (stack.length <= 3) {
      return "";
    }
    StringBuilder className = new StringBuilder();
    String[] split = clean(stack[3].getClassName()).split("\\.");
    buildClassname(className, split);
    return className.toString();
  }

  /**
   * Returns instance of specified class-specific logger.
   * Creates logger if it doesn't exist.
   */
  private static Logger getLogger(String className) {
    synchronized (loggers) {
      if (loggers.containsKey(className)) {
        return loggers.get(className);
      }
      Logger logger = LoggerFactory.getLogger(className);
      loggers.put(className, logger);
      return logger;
    }
  }

  private static Logger getLogger(Class clazz)
  {
    return getLogger(clazz.toString());
  }

  /**
   * Cleans string, removes breaking characters.
   */
  private static String clean(String str) {
    return (str != null ? str : "").replace("\t", " ");
  }

  /**
   * Helper function to produce readable class names.
   */
  private static void buildClassname(StringBuilder className, String[] split) {
    IntStream.range(0, split.length).forEach(i ->
    {
      String segment = split[i];
      if ((segment.equals("com")) || (segment.equals("grantcallant")))
      {
        return;
      }
      if ((className.length() > 15) && (i < (split.length - 1)))
      {
        className.append(".");
        return;
      }
      if (className.length() > 0)
      {
        className.append(".");
      }
      className.append(segment);
    });
  }

  /**
   * Logs INFO level line to console and/or logging stream.
   */
  public static void info(String line) {
    String className = getClassName();
    Logger logger = getLogger(className);
    logger.info(clean(line));
  }

  /**
   * Logs WARN level line to console and/or logging stream.
   */
  public static void warn(String line) {
    String className = getClassName();
    Logger logger = getLogger(className);
    logger.warn(clean(line));
  }

  /**
   * Logs ERROR level exception to console and/or logging stream.
   */
  public static void error(Throwable ex) {
    String type = getType(ex);
    String className = getClassName(ex);
    logStackDetails(ex, type, className);
  }

  /**
   * Overriden error- allows for logging manual exceptions.
   */
  public static void error(String message, Throwable ex)
  {
    logStackDetails(ex, message, getClassName(ex));
  }

  /**
   * Helper function to write exception's cause.
   */
  private static void writeCause(Throwable ex) {
    String type = getType(ex);
    String className = getClassName();
    logStackDetails(ex, type, className);
  }

  /**
   * Helper function to write stack trace.
   */
  private static void logStackDetails(Throwable ex, String type, String className) {
    String method = getMethod(ex);
    int line = getLine(ex);
    String stack = getStack(ex);
    Logger logger = getLogger(className);
    logger.error(String.format("type=%s, method=%s, line=%d, message=%s", type, method, line, getMessage(ex)));
    logger.error(stack);

    if (ex.getCause() != null) {
      writeCause(ex.getCause());
    }
  }

  /**
   * Returns message from exception.
   */
  private static String getMessage(Throwable ex) {
    if (ex == null) {
      return "";
    }
    return clean(ex.getMessage());
  }

  /**
   * Returns type from exception.
   */
  private static String getType(Throwable ex) {
    if ((ex == null) || (ex.getClass() == null)) {
      return "";
    }
    return ex.getClass().getSimpleName();
  }

  /**
   * Returns calling class name from exception stack.
   */
  private static String getClassName(Throwable ex) {
    if (ex == null) {
      return "";
    }
    StackTraceElement[] stack = ex.getStackTrace();
    if ((stack == null) || (stack.length == 0)) {
      return "";
    }
    StringBuilder className = new StringBuilder();
    String[] split = clean(stack[0].getClassName()).split("\\.");
    buildClassname(className, split);
    return className.toString();
  }

  /**
   * Returns calling method name from exception stack.
   */
  private static String getMethod(Throwable ex) {
    if (ex == null) {
      return "";
    }
    StackTraceElement[] stack = ex.getStackTrace();
    if ((stack == null) || (stack.length == 0)) {
      return "";
    }
    return clean(stack[0].getMethodName());
  }

  /**
   * Returns error line from exception stack.
   */
  private static int getLine(Throwable ex) {
    if (ex == null) {
      return 0;
    }
    StackTraceElement[] stack = ex.getStackTrace();
    if ((stack == null) || (stack.length == 0)) {
      return 0;
    }
    return stack[0].getLineNumber();
  }

  /**
   * Gets exception stack as string.
   */
  private static String getStack(Throwable ex) {
    StringWriter sw = new StringWriter();
    PrintWriter pw = new PrintWriter(sw);
    ex.printStackTrace(pw);
    return sw.toString();
  }
}
