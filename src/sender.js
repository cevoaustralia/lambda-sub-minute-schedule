const AWS = require("aws-sdk");

const sqs = new AWS.SQS({
  apiVersion: "2012-11-05",
  region: process.env.AWS_REGION || "us-east-1",
});

const generateDelaySeconds = (interval) => {
  const numElem = Math.round(60 / interval);
  const array = Array.apply(0, Array(numElem + 1)).map((_, index) => {
    return index;
  });
  const min = Math.min(...array);
  const max = Math.max(...array);
  return array
    .map((a) => Math.round(((a - min) / (max - min)) * 60))
    .filter((a) => a < 60);
};

const handler = async () => {
  const interval = process.env.SCHEDULE_INTERVAL || 30;
  const delaySeconds = generateDelaySeconds(interval);
  for (const ds of delaySeconds) {
    const params = {
      MessageBody: JSON.stringify({ delaySecond: ds }),
      QueueUrl: process.env.QUEUE_URL,
      DelaySeconds: ds,
    };
    await sqs.sendMessage(params).promise();
  }
  console.log(`send messages, delay seconds - ${delaySeconds.join(", ")}`);
};

module.exports = { handler };
