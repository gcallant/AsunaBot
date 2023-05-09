package com.grantcallant.asunaspring;

import com.grantcallant.asunaspring.controllers.discord.SlashCommandCache;
import com.grantcallant.asunaspring.controllers.discord.legacy.LegacyCommandCache;
import com.grantcallant.asunaspring.utility.configuration.Configuration;
import com.grantcallant.asunaspring.utility.logging.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.DependsOn;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.TimeZone;

/**
 * Initializes the application with all the correct autowiring.
 */
@Component
@DependsOn("configuration")
public class Initialization implements ApplicationRunner
{
  private static final String BAR = "▌║█║▌│║▌│║▌║▌█║▌│║▌║▌│║║▌█║▌║█▌║█║▌│║▌│║▌║▌█║▌│║▌║▌│║║▌█║▌║█";
  private static final int BAR_LENGTH = BAR.length();
  private static final String LEFT_FRAME = "✩░▒▓▆▅▃▂▁";
  private static final String RIGHT_FRAME = "▁▂▃▅▆▓▒░✩";
  private static final int FRAME_LENGTH = LEFT_FRAME.length() + RIGHT_FRAME.length();
  private final Configuration configuration;
  private final SlashCommandCache slashCommandCache;
  private final LegacyCommandCache legacyCommandCache;

  @Autowired
  public Initialization(Configuration configuration, SlashCommandCache slashCommandCache, LegacyCommandCache legacyCommandCache)
  {
    this.configuration = configuration;
    this.slashCommandCache = slashCommandCache;
    this.legacyCommandCache = legacyCommandCache;
  }

  /**
   * Simple silly utility to pad the output, so it's centered around the frames with the length of BAR.
   */
  private String centerOutput(String output)
  {
    StringBuilder sb = new StringBuilder();
    int fullOutputLength = FRAME_LENGTH + output.length();
    double leftPadding = Math.floor((BAR_LENGTH - fullOutputLength) / 2f);
    for (int i = 0; i < leftPadding; i++)
    {
      sb.append(" ");
    }
    sb.append(output);

    double rightPadding = Math.ceil(BAR_LENGTH - (fullOutputLength + leftPadding)) - 1;
    for (int i = 0; i < rightPadding; i++)
    {
      sb.append(" ");
    }
    return sb.toString();
  }

  /**
   * Callback used to run the bean.
   *
   * @param args incoming application arguments
   */
  @Override
  public void run(ApplicationArguments args) throws IOException
  {
    Log.info(BAR);
    Log.info(LEFT_FRAME + centerOutput("STARTING") + RIGHT_FRAME);
    Log.info(BAR);
    Log.info(LEFT_FRAME + centerOutput(configuration.getApplicationName()) + RIGHT_FRAME);
    Log.info(LEFT_FRAME + centerOutput(configuration.getApplicationVersion()) + RIGHT_FRAME);
    Log.info(LEFT_FRAME + centerOutput(configuration.getApplicationEnvironment()) + RIGHT_FRAME);
    Log.info(LEFT_FRAME + centerOutput(configuration.getApplicationProfile()) + RIGHT_FRAME);
    Log.info(LEFT_FRAME + centerOutput(configuration.getFormattedStartTime()) + RIGHT_FRAME);
    Log.info(BAR);

    Log.info(LEFT_FRAME + centerOutput("Setting correct UTC timezone") + RIGHT_FRAME);
    TimeZone.setDefault(TimeZone.getTimeZone("Etc/UTC"));
    Log.info(BAR);

    Log.info(LEFT_FRAME + centerOutput(slashCommandCache.init()) + RIGHT_FRAME);
    Log.info(LEFT_FRAME + centerOutput(legacyCommandCache.init()) + RIGHT_FRAME);

    Log.info(BAR);
    Log.info(LEFT_FRAME + centerOutput("STARTUP COMPLETE") + RIGHT_FRAME);
    Log.info(BAR);
  }
}
