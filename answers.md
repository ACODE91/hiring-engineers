If you want to apply as a solutions engineer at [Datadog](http://datadog.com) you are in the right spot. Read on, it's fun, I promise.

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

I have used a Ubuntu v 16.04 on a vagrant VM as suggested in the README.

### Installing the Datadog Agent

1. Go to https://app.datadoghq.com/signup and fill the form

<img src="/img/SignUp.png" width="40%">

2. Informing about your stack is optional

<img src="/img/Stack.png" width="50%">

3. Inform your OS (Ubuntu) and copy the agent installation command

<img src="/img/Command.png" width="75%">

4. Paste the command in the shell and wait for the agent to inform back. We're ready to go!

<img src="/img/Running.png" width="75%">

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  1. On your server navigate to `/etc/datadog-agent`

          cd /etc/datadog-agent

  2. Edit the `datadog.yaml` file to include the following line: "tags: purpose:hiring, role:solutionsengineer, location:spain"
  
          sudo vi datadog.yaml

<img src="/img/ConfigTags.png" width="45%">   
   
  3. Restart the datadog agent
  
          sudo service datadog-agent restart
      
  4. The host is now showing the defined tags
    
<img src="/img/HostWithTags.png" width="100%">
    
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  1. I have choosen to install MongoDB. Full step by step guide on [MongoDB Installation Guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
    
  2. The MongoDB integration is installed by default with the 6.x version of the agent. The only required configuration is to create a mongo.yaml file on `/etc/datadog-agent/conf.d/mongo.d/`

          cd /etc/datadog-agent/conf.d/mongo.d
          sudo vi mongo.yaml
  
    1. I have used the simplest possible version of the MongoDB yaml file.

<img src="/img/MongoYAML.png" width="20%">
    
   3. We need to change the file owner to dd-agent and then restar the agent.
    
     sudo chown dd-agent:dd-agent mongo.yaml
     sudo service datadog-agent restart
    
   4. In the agent status we can verify that the MongoDB integration is working
    
    sudo datadog-agent status
    
<img src="/img/MongoStatus.png" width="80%">
    
  5. In Datadog we navigate to Integration and activate the MongoDB Integration. First, selecting it from the list and then clicking on the **Install Integration** button

<img src="/img/Integrations.png" width="40%">

<img src="/img/MongoIntegration.png" width="80%">

  6. And we see some interesting metrics from the MongoDB Dashboard (available from the host, clicking on the _mongodb_ tag)
  
<img src="/img/MongoDashboard.png" width="100%">
    
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

  1. Following instructions from [Datadog Documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) it's fairly straight forward to create the custom agent check.
    1. Create a file called `ruben.yaml` on the `/etc/datadog-agent/conf.d/` folder with the following code:
    
      instances: [{}]
    
    2. Create a file called `ruben.py` on the `/etc/datadog-agent/checks.d/` folder with the following code
    
            from datadog_checks.checks import AgentCheck
            from random import uniform
            __version__ = "1.0.0"
            class Ruben(AgentCheck):
              def check(self, instance):
                self.gauge('custom.ruben', uniform(0, 1000))
   3. We can verify that the check is correct using the agent's commands: `sudo datadog-agent check ruben`
    
<img src="/img/CustomCheck.png" width="100%">

   4. And see the gauge graph on Datadog
   
<img src="/img/CustomCheckGraph.png" width="100%">

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

  1. As described in [the Collection Interval section](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval), changing the collection interval is done by setting it on the `ruben.yaml`file on `/etc/datadog-agent/conf.d/`
    1. The check config file, `ruben.yaml`, needs to be updated in the following way:

<img src="/img/CheckInterval.png" width="100%">

   2. The check is now sending data every 45 seconds.
   
<img src="/img/CheckInterval.png" width="100%">
  
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

 * It seems that this question is outdated, as the obvious answer following the documentation) doesn't require to modify the custom check's python file.
 * Just for the sake of the exercise, I can try to answer the reverse question. How to report every 45 seconds without chaging the config file.
    1. Considering the default reporting inteval is 15 seconds, and the agent will report only if the previous execution of the custom check has finished, a simple answer will be to include a `time.sleep(20)`step just after the `self.gauge('custom.ruben', uniform(0, 1000))`step.
    2. This will inhibit the agent to report in the second and third slots (15 and 30 seconds), but will freed the check code long enough the third slot arrives (45 seconds).

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/agent_checks/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
