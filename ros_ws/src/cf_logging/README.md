# cf_logging ROS package

Additional package for the crazyswarm project for saving the specified log-variables from the crazyflies into CSV files

## Installation & Usage
   1. Load your crazyswarm project or the latest version from the [USC-ACTLab](https://github.com/USC-ACTLab/crazyswarm)
   2. Execute following command in the crazyswarm project directory to add `cf_logging` as submodule to the project into the folder `ros_ws/src/`:  
      `git submodule add https://github.com/PDfork/cf_logging ros_ws/src/cf_logging`
   3. Edit the `ros_ws/src/crazyswarm/launch/hover_swarm.launch` file and make sure, following lines are present and uncommented:  
      ```
      <node pkg="crazyswarm" type="crazyswarm_server" name="crazyswarm_server" output="screen" >
         <rosparam>
            genericLogTopics: ["log1","log2", ...] # ROS topics for publishing the log variables 
            genericLogTopicFrequencies: [10,10, ...]  # frequency of logging in ms for each topic
            # log variables from the CFs, like "stabilizer.x"
            genericLogTopic_log1_Variables: ["log_group.log_variable", ...]
            genericLogTopic_log2_Variables: ["log_group.log_variable", ...]
            enable_logging: True
         </rosparam>
      </node>
      <include file="$(find cf_logging)/launch/cf_logging.launch" />
      ```
   4. Build your project as usual with `./build.sh`
   5. Get the log data from the folder `ros_ws/src/cf_logging/data` (The data is separated into folders with its corresponding timestamp and each CF has its own CSV file)

## Troubleshoot & Notes
   - There is a limit of around 6 variables per topic, therefore multiple topics are necessary for logging more than 6 variables
   - e.g. for logging 14 variables, it may work with only 2 topics, but it would be more reliable to use 3 topics. Therefore, the `hover_swarm.launch` file needs to be edited like following:   
      ```
      <node pkg="crazyswarm" type="crazyswarm_server" name="crazyswarm_server" output="screen" >
         <rosparam>
            genericLogTopics: ["log1", "log2", "log3"]
            genericLogTopicFrequencies: [10,10,10]
            genericLogTopic_log1_Variables: ["var1", "var2", "var3", "var4", "var5"]
            genericLogTopic_log2_Variables: ["var6", "var7", "var8", "var9", "var10"]
            genericLogTopic_log3_Variables: ["var11", "var12", "var13", "var14"]
            enable_logging: True
         </rosparam>
      </node>
      <include file="$(find cf_logging)/launch/cf_logging.launch" />
      ```
   - Be advised, that logging a lot of variables with multiple CFs can slow down the communication which may lead to a crash of the CFs. Use the logging onto SD cards instead.
   - There is no error handling for misspelling a variable, the logging will fail immediately
   - It may happen, that the logging doesn't start properly, which leads to an empty csv file. This may occur due to some timing error, but still it has to be further investigated.

