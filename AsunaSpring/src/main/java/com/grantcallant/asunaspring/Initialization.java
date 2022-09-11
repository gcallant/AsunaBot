package com.grantcallant.asunaspring;

import com.grantcallant.asunaspring.utility.configuration.Configuration;
import com.grantcallant.asunaspring.utility.logging.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Component;

import java.util.TimeZone;

/**
 * Initializes the application with all the correct autowiring.
 */
@Component
@DependsOn("configuration")
public class Initialization implements ApplicationRunner
{
  private final Configuration configuration;
  private static final String BAR = "▌║█║▌│║▌│║▌║▌█║▌│║▌║▌│║║▌█║▌║█▌║█║▌│║▌│║▌║▌█║▌│║▌║▌│║║▌█║▌║█";
  private static final String LEFT_FRAME = "✩░▒▓▆▅▃▂▁";
  private static final String RIGHT_FRAME = "▁▂▃▅▆▓▒░✩";

  @Autowired
  public Initialization(Configuration configuration) {this.configuration = configuration;}

  /**
   * Callback used to run the bean.
   *
   * @param args incoming application arguments
   */
  @Override
  public void run(ApplicationArguments args)
  {
    TimeZone.setDefault(TimeZone.getTimeZone("Etc/UTC"));
    Log.info(BAR);
    Log.info(LEFT_FRAME + "STARTING" + RIGHT_FRAME);
    Log.info(BAR);
    Log.info(LEFT_FRAME + configuration.getApplicationName() + RIGHT_FRAME);
    Log.info(LEFT_FRAME + configuration.getApplicationVersion() + RIGHT_FRAME);
    Log.info(LEFT_FRAME + configuration.getApplicationEnvironment() + RIGHT_FRAME);
    Log.info(LEFT_FRAME + configuration.getApplicationProfile() + RIGHT_FRAME);
    Log.info(LEFT_FRAME + configuration.getStartTime() + RIGHT_FRAME);
    Log.info(BAR);

    Log.info(LEFT_FRAME + "STARTING COMPLETE");
    Log.info(BAR);
  }
}
