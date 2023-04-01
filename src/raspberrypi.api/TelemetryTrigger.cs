using System;
using System.Collections.Generic;
using System.Net;
using System.Threading.Tasks;
using Azure.Messaging.WebPubSub;
using Microsoft.AspNetCore.Http;
using Microsoft.Azure.Documents;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Azure.WebJobs.Extensions.WebPubSub;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using static Microsoft.ApplicationInsights.MetricDimensionNames.TelemetryContext;

namespace raspberrypi.changefeed
{
    public class TelemetryTrigger
    {
        private readonly IConfiguration _configuration;
        public TelemetryTrigger(IConfiguration configuration)
        {
            _configuration = configuration;
        }

        [FunctionName("TelemetryToPubSub")]
        public async Task TelemetryToPubSub([CosmosDBTrigger(
            databaseName: "airqualitymonitoringdelivery",
            collectionName: "telemetry",
            ConnectionStringSetting = "cosmosconnection",
            LeaseCollectionName = "leases",
            CreateLeaseCollectionIfNotExists = true)]IReadOnlyList<Document> input,
            ILogger log)
        {
            if (input != null && input.Count > 0)
            {
                log.LogInformation("Documents modified " + input.Count);
                log.LogInformation("First document Id " + input[0].Id);

                var serviceClient = new WebPubSubServiceClient(_configuration["WebPubSubConnectionString"], _configuration["HubName"]);
                await serviceClient.SendToAllAsync(JsonConvert.SerializeObject(input));
            }
        }
    }
}
